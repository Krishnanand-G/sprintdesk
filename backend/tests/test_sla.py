import pytest
from app.models import Severity
from app.sla import sla_for_severity, should_auto_assign


@pytest.mark.parametrize(
    "severity,hours",
    [
        (Severity.critical, 4),
        (Severity.high, 8),
        (Severity.medium, 24),
        (Severity.low, 72),
    ],
)
def test_sla_hours(severity, hours):
    assert sla_for_severity(severity) == hours


@pytest.mark.parametrize(
    "severity,auto",
    [
        (Severity.critical, True),
        (Severity.high, True),
        (Severity.medium, False),
        (Severity.low, False),
    ],
)
def test_auto_assign(severity, auto):
    assert should_auto_assign(severity) is auto
