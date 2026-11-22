from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from database.models import Base, SafetyRule, SystemConfig, Worker

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

        # Seed default enrolled workers if empty
        if db.query(Worker).count() == 0:
            import hashlib, json
            # Pre-generate synthetic normalized feature vectors for out-of-the-box recognition
            def make_dummy_features(seed_val: int):
                np_features = [round(((seed_val * 17 + i * 31) % 100) / 100.0, 4) for i in range(128)]
                # Normalize
                mag = sum(x*x for x in np_features) ** 0.5
                return json.dumps([round(x/mag, 4) for x in np_features])

            default_workers = [
                Worker(
                    worker_id="W-101",
                    name="Rajesh Kumar",
                    role="Site Supervisor & Framing Lead",
                    department="Structural Engineering",
                    fingerprint_id=1,
                    fingerprint_enrolled=True,
                    fingerprint_hash=hashlib.sha256(b"rajesh_kumar_fprint_1").hexdigest(),
                    face_enrolled=True,
                    face_features=make_dummy_features(101),
                    authorized_zones="General Worksite,Doorway-North,Scaffolding Zone A",
                    is_active=True
                ),
                Worker(
                    worker_id="W-102",
                    name="Amit Sharma",
                    role="Excavation Machine Operator",
                    department="Heavy Equipment",
                    fingerprint_id=2,
                    fingerprint_enrolled=True,
                    fingerprint_hash=hashlib.sha256(b"amit_sharma_fprint_2").hexdigest(),
                    face_enrolled=True,
                    face_features=make_dummy_features(102),
                    authorized_zones="General Worksite,Doorway-North,Heavy Machinery Excavation Zone",
                    is_active=True
                ),
                Worker(
                    worker_id="W-103",
                    name="Sunita Patil",
                    role="Safety Compliance Officer",
                    department="HSE & Auditing",
                    fingerprint_id=3,
                    fingerprint_enrolled=True,
                    fingerprint_hash=hashlib.sha256(b"sunita_patil_fprint_3").hexdigest(),
                    face_enrolled=True,
                    face_features=make_dummy_features(103),
                    authorized_zones="General Worksite,Doorway-North,Inspection Deck",
                    is_active=True
                ),
                Worker(
                    worker_id="W-104",
                    name="Vikram Rao",
                    role="Electrical Specialist",
                    department="HVAC & Power",
                    fingerprint_id=4,
                    fingerprint_enrolled=True,
                    fingerprint_hash=hashlib.sha256(b"vikram_rao_fprint_4").hexdigest(),
                    face_enrolled=True,
                    face_features=make_dummy_features(104),
                    authorized_zones="General Worksite,Doorway-North",
                    is_active=True
                ),
            ]
            db.add_all(default_workers)

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
