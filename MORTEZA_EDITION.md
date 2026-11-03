# DevSecOps Compose — Morteza Rajabi edition

A maintained learning extension of [docker/awesome-compose](https://github.com/docker/awesome-compose), with an original security policy auditor and a hardened local demo by [Morteza Rajabi](https://github.com/opswithmorteza).

The upstream samples remain credited to Docker and their contributors. This is an independent fork, not an official Docker release. The upstream CC0-1.0 LICENSE is retained; these additions are also dedicated under CC0-1.0.

## What this edition adds

- A dependency-free Python health API in a non-root container.
- Compose controls: read-only root filesystem, dropped capabilities, no privilege escalation, loopback-only port, memory and process limits, healthcheck.
- A reusable auditor for normalized Compose JSON: fails on unsafe users, host namespaces, capabilities, host mounts, exposed ports, missing limits or disabled healthchecks.
- Regression tests covering the accepted baseline and thirteen unsafe changes.

## Run locally

Requires Docker with Compose v2 and Python 3.11+ for the auditor.

```sh
python -m unittest -v test_morteza_policy.py
docker compose -f morteza-compose.yaml config --format json > compose.normalized.json
python morteza_policy.py compose.normalized.json
docker compose -f morteza-compose.yaml up --build -d --wait
curl --fail http://127.0.0.1:8080/health
docker compose -f morteza-compose.yaml down
```

Use `python3` if your environment names Python that way. On older Windows PowerShell, export JSON as UTF-8 to avoid UTF-16 redirection.

## Scope and limitations

This opinionated policy is for this local lab. It is not an ISMS certification, vulnerability scanner or production security guarantee. It deliberately rejects host bind mounts. It does not inspect image contents, kernel isolation, secrets, application authorization or supply-chain provenance. Pin and maintain verified image digests before a production deployment; add TLS, authentication, monitoring, vulnerability scanning and a documented risk assessment for the real environment.

## فارسی

این فورک، نمونه‌های اصلی Docker را با حفظ منبع نگه می‌دارد. افزوده‌های مرتضی رجبی شامل سرویس آزمایشی، تنظیمات محدودکنندهٔ کانتینر و بررسی خودکار سیاست امنیتی است. هدف، نمایش عملی DevSecOps و یادگیری است؛ برای محیط واقعی باید کنترل‌ها با نیاز و ریسک همان محیط تطبیق داده شوند.
