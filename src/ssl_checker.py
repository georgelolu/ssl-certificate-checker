#!/usr/bin/env python3

import argparse
import json
import socket
import ssl
from datetime import datetime, timezone


DEFAULT_PORT = 443
DEFAULT_WARNING_DAYS = 30


def get_certificate(domain, port=DEFAULT_PORT, timeout=10):
    context = ssl.create_default_context()

    with socket.create_connection((domain, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            certificate = ssock.getpeercert()

    return certificate


def parse_certificate_date(date_string):
    return datetime.strptime(
        date_string,
        "%b %d %H:%M:%S %Y %Z"
    ).replace(tzinfo=timezone.utc)


def check_certificate(domain, port=DEFAULT_PORT, warning_days=DEFAULT_WARNING_DAYS):
    try:
        certificate = get_certificate(domain, port)

        expiry_date = parse_certificate_date(
            certificate["notAfter"]
        )

        issued_date = parse_certificate_date(
            certificate["notBefore"]
        )

        now = datetime.now(timezone.utc)

        remaining = expiry_date - now
        remaining_days = remaining.total_seconds() / 86400

        issuer = dict(
            item[0]
            for item in certificate.get("issuer", [])
        )

        subject = dict(
            item[0]
            for item in certificate.get("subject", [])
        )

        if remaining_days <= 0:
            status = "EXPIRED"
        elif remaining_days <= warning_days:
            status = "EXPIRING_SOON"
        else:
            status = "VALID"

        return {
            "domain": domain,
            "port": port,
            "status": status,
            "issuer": issuer.get("organizationName", "Unknown"),
            "subject": subject.get("commonName", "Unknown"),
            "issued_at": issued_date.isoformat(),
            "expires_at": expiry_date.isoformat(),
            "remaining_days": round(remaining_days, 2),
        }

    except ssl.SSLCertVerificationError as error:
        return {
            "domain": domain,
            "port": port,
            "status": "INVALID",
            "error": f"Certificate verification failed: {error}",
        }

    except (socket.timeout, socket.gaierror, ConnectionRefusedError) as error:
        return {
            "domain": domain,
            "port": port,
            "status": "ERROR",
            "error": str(error),
        }

    except Exception as error:
        return {
            "domain": domain,
            "port": port,
            "status": "ERROR",
            "error": str(error),
        }


def load_domains(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return [
            line.strip()
            for line in file
            if line.strip() and not line.startswith("#")
        ]


def print_result(result):
    print("=" * 60)
    print(f"Domain:          {result['domain']}")
    print(f"Status:          {result['status']}")

    if "issuer" in result:
        print(f"Issuer:          {result['issuer']}")
        print(f"Subject:         {result['subject']}")
        print(f"Issued:          {result['issued_at']}")
        print(f"Expires:         {result['expires_at']}")
        print(f"Remaining days:  {result['remaining_days']}")

    if "error" in result:
        print(f"Error:           {result['error']}")


def main():
    parser = argparse.ArgumentParser(
        description="Check SSL/TLS certificate validity and expiration."
    )

    parser.add_argument(
        "domain",
        nargs="?",
        help="Domain to check"
    )

    parser.add_argument(
        "--file",
        help="File containing domains to check"
    )

    parser.add_argument(
        "--warning-days",
        type=int,
        default=30,
        help="Number of days before expiry to report EXPIRING_SOON"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    if args.domain:
        domains = [args.domain]
    elif args.file:
        domains = load_domains(args.file)
    else:
        parser.error("Provide a domain or use --file")

    results = []

    for domain in domains:
        result = check_certificate(
            domain,
            warning_days=args.warning_days
        )

        results.append(result)

        if not args.json:
            print_result(result)

    if args.json:
        print(json.dumps(results, indent=2))

    # Exit with non-zero status if any certificate is invalid,
    # expired, or could not be checked.
    problem_statuses = {"INVALID", "EXPIRED", "ERROR"}

    if any(
        result["status"] in problem_statuses
        for result in results
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
