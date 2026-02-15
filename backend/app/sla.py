from app.models import Severity

SLA_HOURS = {
    Severity.critical: 4,
    Severity.high: 8,
    Severity.medium: 24,
    Severity.low: 72,
}


def sla_for_severity(severity: Severity) -> int:
    return SLA_HOURS[severity]


def should_auto_assign(severity: Severity) -> bool:
    return severity in (Severity.high, Severity.critical)
