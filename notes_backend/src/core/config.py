from functools import lru_cache
import os

# PUBLIC_INTERFACE
def get_env(key: str, default: str | None = None) -> str | None:
    """Get environment variable with optional default."""
    return os.getenv(key, default)


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self) -> None:
        # Default to a local SQLite database file if not provided
        self.DATABASE_URL: str = get_env("DATABASE_URL", "sqlite:///./notes.db")  # noqa: N815


# PUBLIC_INTERFACE
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached Settings instance."""
    return Settings()
