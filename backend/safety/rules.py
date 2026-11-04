from dataclasses import dataclass

@dataclass
class RuleDefinition:
    code: str
    name: str
    category: str
    severity: str
    description: str

SAFETY_RULES_REGISTRY = {
    "RULE_HELMET": RuleDefinition(
        code="RULE_HELMET",
        name="Mandatory Hard Hat / Helmet",
        category="PPE",
        severity="HIGH",
        description="Workers inside designated construction workspace must wear safety hard hats at all times."
    ),
    "RULE_VEST": RuleDefinition(
        code="RULE_VEST",
        name="High-Visibility Reflective Vest",
        category="PPE",
        severity="MEDIUM",
        description="High-visibility safety vests must be worn to ensure visibility near machinery."
    ),
    "RULE_RESTRICTED_ZONE": RuleDefinition(
        code="RULE_RESTRICTED_ZONE",
        name="Restricted Hazardous Exclusion Zone",
        category="ZONE_BOUNDARY",
        severity="CRITICAL",
        description="Unauthorized personnel must not enter heavy machinery or fall hazard exclusion zones."
    )
}
