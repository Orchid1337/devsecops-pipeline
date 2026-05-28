.PHONY: help lint test scan run build deploy clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

lint: ## Run linters (ruff + hadolint)
	ruff check .
	ruff format --check .
	docker run --rm -i hadolint/hadolint < Dockerfile

test: ## Run unit tests with coverage
	pytest app/tests/ --cov=app --cov-report=term-missing --cov-report=html -v

scan: ## Run security scans (semgrep + trivy)
	semgrep scan --config p/python --config p/owasp-top-ten --config .semgrep/custom-rules.yml .
	docker build -t devsecops-api:scan .
	trivy image --severity CRITICAL,HIGH devsecops-api:scan

run: ## Run the application locally with Docker Compose
	docker compose up --build

build: ## Build the Docker image
	docker build -t devsecops-api:latest .

deploy: ## Deploy to local Kind cluster
	kind create cluster --name devsecops-local 2>/dev/null || true
	docker build -t devsecops-api:latest .
	kind load docker-image devsecops-api:latest --name devsecops-local
	kubectl apply -f k8s/

clean: ## Clean up local resources
	docker compose down -v
	kind delete cluster --name devsecops-local 2>/dev/null || true
	rm -rf htmlcov .pytest_cache __pycache__ coverage.xml test-results.xml

sonarqube: ## Start SonarQube locally
	docker compose -f docker-compose.sonarqube.yml up -d
	@echo "SonarQube starting at http://localhost:9000 (default login: admin/admin)"
	@echo "Run 'sonar-scanner' after SonarQube is ready"

pre-commit: ## Install and run pre-commit hooks
	pip install pre-commit
	pre-commit install
	pre-commit run --all-files
