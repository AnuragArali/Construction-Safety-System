from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from database.models import Base, SafetyRule, SystemConfig

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Seed default safety rules if empty
        if db.query(SafetyRule).count() == 0:
            default_rules = [
                SafetyRule(
                    rule_code="RULE_HELMET",
                    rule_name="Mandatory Hard Hat / Helmet",
                    category="PPE",
                    severity="HIGH",
                    is_enabled=True,
                    description="Workers inside designated construction workspace must wear safety hard hats at all times."
                ),
                SafetyRule(
                    rule_code="RULE_VEST",
                    rule_name="High-Visibility Reflective Vest",
                    category="PPE",
                    severity="MEDIUM",
                    is_enabled=True,
                    description="High-visibility safety vests must be worn to ensure visibility near heavy equipment and vehicles."
                ),
                SafetyRule(
                    rule_code="RULE_RESTRICTED_ZONE",
                    rule_name="Restricted Hazardous Exclusion Zone",
                    category="ZONE_BOUNDARY",
                    severity="CRITICAL",
                    is_enabled=True,
                    description="Personnel without authorization must not enter active excavation or heavy machinery swing zones."
                )
            ]
            db.add_all(default_rules)

        # Seed default settings
        defaults = {
            "language": settings.DEFAULT_LANGUAGE,
            "voice_enabled": str(settings.VOICE_ENABLED),
            "voice_volume": str(settings.VOICE_VOLUME),
            "alert_cooldown": str(settings.ALERT_COOLDOWN_SECONDS),
            "retention_days": str(settings.DATA_RETENTION_DAYS),
            "privacy_mode": "STRICT_LOCAL"
        }
        for k, v in defaults.items():
            if not db.query(SystemConfig).filter(SystemConfig.config_key == k).first():
                db.add(SystemConfig(config_key=k, config_value=v))
        db.commit()
    finally:
        db.close()
