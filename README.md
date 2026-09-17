# SSL Certificate Checker

A Python automation tool for checking SSL/TLS certificates, validating certificate status, monitoring expiration dates, and reporting certificate details.

## Features

- Check SSL/TLS certificates for individual domains
- Check multiple domains from a file
- Detect certificate validity
- Display certificate issuer and subject
- Display certificate issue and expiration dates
- Calculate remaining certificate lifetime
- Configure expiration warning thresholds
- Generate JSON output for automation
- Handle invalid and unreachable certificates
- Automated unit tests with pytest
- Manual verification with OpenSSL
- GitHub Actions CI
- Scheduled daily SSL monitoring

## Technologies

- Python 3
- Python `ssl` module
- OpenSSL
- pytest
- Git
- GitHub Actions

## Project Structure

```text
ssl-certificate-checker/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── __init__.py
│   └── ssl_checker.py
├── tests/
│   ├── data/
│   │   └── test-domains.txt
│   └── test_ssl_checker.py
├── reports/
├── domains.txt
├── pytest.ini
├── requirements.txt
├── README.md
└── .gitignore
Installation

Clone the repository:

git clone https://github.com/georgelolu/ssl-certificate-checker.git
cd ssl-certificate-checker

Create a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt
Usage
Check a Single Domain
python src/ssl_checker.py google.com
Check Multiple Domains
python src/ssl_checker.py --file domains.txt
Configure Expiration Warning
python src/ssl_checker.py google.com --warning-days 30

Certificates with remaining lifetime at or below the configured threshold are reported as:

EXPIRING_SOON
JSON Output
python src/ssl_checker.py --file domains.txt --json

Example:

[
  {
    "domain": "example.com",
    "port": 443,
    "status": "VALID",
    "issuer": "Certificate Authority",
    "subject": "example.com",
    "issued_at": "2026-01-01T00:00:00+00:00",
    "expires_at": "2026-12-31T23:59:59+00:00",
    "remaining_days": 105.4
  }
]
Testing

Run the automated test suite:

pytest -v

Current tests cover:

Certificate date parsing
Domain file loading
OpenSSL Verification

Certificate information can be independently verified using OpenSSL:

openssl s_client -connect google.com:443 -servername google.com </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates

The OpenSSL output can be compared with the information reported by the Python SSL checker.

GitHub Actions

The project uses GitHub Actions to automatically:

Check out the repository
Set up Python
Install dependencies
Run pytest
Check monitored SSL certificates

The workflow runs on:

Push
Pull requests
Manual workflow dispatch
Daily scheduled execution

Scheduled monitoring is configured for:

08:00 UTC
09:00 Nigeria time
Exit Codes

The script exits successfully when monitored certificates are valid or within the configured warning state.

It returns a non-zero exit status when a certificate is:

Invalid
Expired
Unreachable
Unable to be checked

This allows GitHub Actions and other automation systems to detect certificate problems.

Example
============================================================
Domain:          google.com
Status:          VALID
Issuer:          Google Trust Services
Subject:         *.google.com
Issued:          2026-08-10T08:37:35+00:00
Expires:         2026-11-02T08:37:34+00:00
Remaining days:  45.91
DevOps Skills Demonstrated

This project demonstrates practical experience with:

Python automation
SSL/TLS
Linux command-line tools
OpenSSL
Automated testing
Git and GitHub
GitHub Actions
CI automation
Scheduled monitoring
Error handling
JSON-based reporting
Service reliability monitoring
Future Improvements

Potential future enhancements include:

Email or Slack notifications
Prometheus metrics
Grafana dashboards
Certificate chain analysis
Custom ports
HTML reports
Docker support
AWS deployment
Alerting when certificates approach expiration
License

This project is available for educational and portfolio purposes.
