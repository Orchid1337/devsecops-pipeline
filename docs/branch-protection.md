# Branch Protection Rules

This document describes the recommended GitHub branch protection configuration for this repository.

## Main Branch (`main`)

### Required Settings

| Setting | Value | Rationale |
|---------|-------|-----------|
| Require pull request reviews | 1 approval minimum | Four-eyes principle for all changes |
| Dismiss stale reviews | Enabled | Ensures reviews reflect current code |
| Require review from code owners | Enabled | Security-sensitive paths need security team review |
| Require status checks to pass | Enabled | No merging with broken pipeline |
| Require branches to be up to date | Enabled | Prevents merge skew issues |
| Require signed commits | Enabled | Verifies commit authorship |
| Include administrators | Enabled | No bypass, even for admins |
| Restrict force pushes | Enabled | Prevents history rewriting |
| Restrict deletions | Enabled | Prevents accidental branch deletion |

### Required Status Checks

The following CI jobs must pass before merge:

- `lint` — Code quality gate
- `test` — All unit tests pass with coverage threshold
- `sast` — No HIGH/CRITICAL SAST findings
- `dependency-scan` — No dependencies with CVSS ≥ 7
- `container-scan` — No CRITICAL container vulnerabilities

### CODEOWNERS File

Create `.github/CODEOWNERS`:

```
# Security-sensitive files require security team review
SECURITY.md                    @security-team
.github/workflows/             @security-team @devops-team
Dockerfile                     @security-team @devops-team
k8s/                           @security-team @devops-team
.semgrep/                      @security-team
.trivyignore                   @security-team

# Application code
app/                           @dev-team
```

## Setup Instructions

### Via GitHub UI

1. Navigate to **Settings** → **Branches**
2. Click **Add rule** under "Branch protection rules"
3. Set **Branch name pattern** to `main`
4. Enable all settings listed above
5. Click **Create**

### Via GitHub CLI

```bash
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["lint","test","sast","dependency-scan","container-scan"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_code_owner_reviews":true}' \
  --field restrictions=null \
  --field allow_force_pushes=false \
  --field allow_deletions=false
```

## Rationale

These rules enforce:

1. **Separation of duties** — No single person can push unreviewed code to production
2. **Automated quality gates** — Security scans must pass before merge
3. **Audit trail** — Signed commits and PR history provide accountability
4. **Supply chain security** — Dependency and container scans prevent known-vulnerable code from shipping
5. **Defense in depth** — Multiple overlapping controls reduce single-point-of-failure risk
