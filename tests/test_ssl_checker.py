from datetime import timezone

from src.ssl_checker import parse_certificate_date
from src.ssl_checker import load_domains


def test_parse_certificate_date():
    value = "Dec 20 23:59:59 2026 GMT"

    result = parse_certificate_date(value)

    assert result.year == 2026
    assert result.month == 12
    assert result.day == 20
    assert result.tzinfo == timezone.utc


def test_load_domains(tmp_path):
    domain_file = tmp_path / "domains.txt"

    domain_file.write_text(
        """
# Test domains

google.com
github.com

cloudflare.com
"""
    )

    result = load_domains(domain_file)

    assert result == [
        "google.com",
        "github.com",
        "cloudflare.com"
    ]
