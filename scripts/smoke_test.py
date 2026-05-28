#!/usr/bin/env python3
"""
Post-deploy smoke tests. Hits every endpoint and checks we get expected status codes.
Run this after deploying to the Kind cluster (or locally against localhost:8080).
"""
import sys
import httpx

BASE_URL = "http://localhost:8080"


def main():
    print(f"Smoke testing against {BASE_URL}\n")

    client = httpx.Client(base_url=BASE_URL, timeout=10)
    results = {"pass": 0, "fail": 0}

    checks = [
        ("GET", "/health", 200, None),
        ("GET", "/ready", 200, None),
        ("GET", "/api/v1/users/", 200, None),
        ("POST", "/api/v1/users/", 201, {"username": "smokeuser", "email": "smoke@test.io"}),
        ("GET", "/api/v1/items/", 200, None),
        ("POST", "/api/v1/items/", 201, {"name": "Smoke Widget", "price": 4.20}),
        ("GET", "/api/v1/items/1", 200, None),
    ]

    for method, path, want_status, body in checks:
        try:
            if body:
                resp = client.post(path, json=body)
            else:
                resp = client.get(path)

            ok = resp.status_code == want_status
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] {method} {path} => {resp.status_code} (want {want_status})")
            results["pass" if ok else "fail"] += 1

        except httpx.RequestError as exc:
            print(f"  [FAIL] {method} {path} => connection error: {exc}")
            results["fail"] += 1

    client.close()

    total = results["pass"] + results["fail"]
    print(f"\nDone: {results['pass']}/{total} passed")
    return results["fail"] == 0


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
