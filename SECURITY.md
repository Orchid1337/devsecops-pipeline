# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please report it responsibly.

### How to Report

1. **Do NOT** open a public GitHub issue for security vulnerabilities.
2. Email your findings to: `security@example.com`
3. Include the following in your report:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: Within 48 hours of your report
- **Initial Assessment**: Within 5 business days
- **Resolution Timeline**: Critical vulnerabilities within 7 days, High within 30 days
- **Disclosure**: Coordinated disclosure after patch is available

### Scope

The following are in scope for security reports:

- Authentication and authorization bypasses
- SQL injection, XSS, CSRF, and other injection attacks
- Sensitive data exposure
- Container escape vulnerabilities
- CI/CD pipeline security issues (secret leakage, supply chain attacks)
- Kubernetes misconfigurations that could lead to privilege escalation

### Out of Scope

- Denial of service attacks
- Social engineering
- Physical security
- Issues in dependencies (report these upstream)

### Safe Harbor

We will not take legal action against researchers who:

- Make a good faith effort to avoid privacy violations and data destruction
- Only interact with accounts they own or with explicit permission
- Do not exploit a vulnerability beyond what is necessary to confirm it
- Report findings promptly and do not publicly disclose before a fix is available

## Security Controls

This project implements the following security measures:

- **SAST**: Semgrep with OWASP Top 10 rules
- **SCA**: OWASP Dependency-Check for known vulnerabilities
- **Container Scanning**: Trivy for image vulnerabilities
- **Secret Detection**: detect-secrets pre-commit hook
- **Input Validation**: Pydantic models with strict validation
- **Least Privilege**: Non-root containers, dropped capabilities, read-only filesystem
- **Network Policies**: Default-deny with explicit allow rules
