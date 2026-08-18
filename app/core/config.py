from pydantic_settings import BaseSettings
from typing import List
import os
import re
from dotenv import load_dotenv

load_dotenv()

# Render's EXTERNAL hostname (resolves from any region). The Internal
# hostname (dpg-xxxx without a domain) only works inside Render's network,
# in the same region as the database — that's why the app default uses the
# external host and requires the real password via the DATABASE_URL env var.
DEFAULT_DATABASE_URL = (
    "postgresql://bookstore_q5pc_user:PASSWORD_HERE@"
    "dpg-d9u8r9740ujc73fq4pt0-a.singapore-postgres.render.com/bookstore_q5pc"
)


def _resolve_database_url(raw: str) -> str:
    """Safety net: if DATABASE_URL points at Render's *internal* Postgres
    hostname (e.g. dpg-xxxx-a with no domain — which only resolves inside
    Render's network, in the same region), rewrite it to the external
    hostname so it works from any region.
    Region suffix comes from RENDER_POSTGRES_REGION (default: singapore)."""
    if not raw:
        return raw
    match = re.match(
        r"^(postgres(?:ql)?://[^@/]+@)(dpg-[A-Za-z0-9]+-a)(:\d+)?(/.*)?$",
        raw,
    )
    if match and "." not in match.group(2):
        region = os.getenv("RENDER_POSTGRES_REGION", "singapore")
        port = match.group(3) or ""
        path = match.group(4) or ""
        return (
            f"{match.group(1)}{match.group(2)}."
            f"{region}-postgres.render.com{port}{path}"
        )
    return raw


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-me-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    @property
    def CORS_ORIGINS(self) -> List[str]:
        origins = os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:3001,http://localhost:5173,http://localhost:8000,"
            "https://marvelous-conkies-eaa8ca.netlify.app,https://magenta-dieffenbachia-043f38.netlify.app",
        )
        return [origin.strip() for origin in origins.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra env vars not declared as fields (e.g. CORS_ORIGINS)


settings = Settings()

# Safety net: if the configured URL uses Render's *internal* hostname,
# rewrite it to the external hostname so it resolves from any region.
_resolved = _resolve_database_url(settings.DATABASE_URL)
if _resolved != settings.DATABASE_URL:
    print("INFO: DATABASE_URL used a Render internal host — rewrote to the external hostname.")
    settings.DATABASE_URL = _resolved

# Fail fast with a clear message instead of a cryptic DNS/auth error at deploy time.
if not settings.DATABASE_URL or "PASSWORD_HERE" in settings.DATABASE_URL:
    raise RuntimeError(
        "\n"
        "=============================================================\n"
        " DATABASE_URL is not configured!\n"
        "-------------------------------------------------------------\n"
        " Set the DATABASE_URL environment variable on Render to the\n"
        " EXTERNAL Database URL from your Postgres dashboard:\n"
        "   Render -> PostgreSQL (bookstore) -> Connect ->\n"
        "   \"External Database URL\"\n"
        " It looks like:\n"
        "   postgresql://USER:PASSWORD@dpg-xxxx.singapore-postgres.render.com/DBNAME\n"
        " Add it under: Service -> Environment -> Add Environment Variable,\n"
        " then Deploy again.\n"
        "=============================================================\n"
    )
