# Dataclasses for environment settings
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class ScrapingConfig:
    bank_app_ids: dict
    target_reviews_per_bank: int = 500
    lang: str = 'en'
    country: str = 'us'

@dataclass(frozen=True)
class DatabaseConfig:
    db_uri: str = "postgresql://postgres:leulalmaz@localhost:5432/bank_reviews"