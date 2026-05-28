# django-captcha-auth

Secure and reusable CAPTCHA authentication package for Django applications.

`django-captcha-auth` adds CAPTCHA protection to authentication workflows such as login, registration, password reset, OTP verification, and custom sensitive endpoints to help prevent bots, brute-force attacks, and automated abuse.

---

# Features

* CAPTCHA-protected login system
* Reusable validation utilities
* Django & DRF support
* Easy integration with existing authentication flows
* Protection for sensitive endpoints
* Custom CAPTCHA providers support
* Session and token authentication compatible
* Configurable validation behavior
* Production-ready architecture
* Lightweight and extensible

---

# Supported Use Cases

* Login forms
* Registration forms
* Password reset
* OTP verification
* Public APIs
* Contact forms
* Rate-limited endpoints
* DRF authentication APIs

---

# Installation

Install package:

```bash
pip install django-captcha-auth
```

---

# Quick Start

## Add to Installed Apps

```python
INSTALLED_APPS = [
    ...
    "captcha_auth",
]
```

---

## Configure Middleware (Optional)

```python
MIDDLEWARE = [
    ...
    "captcha_auth.middleware.CaptchaMiddleware",
]
```

---

## Configure Settings

```python
CAPTCHA_AUTH = {
    "PROVIDER": "google_recaptcha",
    "SECRET_KEY": "your-secret-key",
    "SITE_KEY": "your-site-key",
    "VERIFY_LOGIN": True,
    "VERIFY_REGISTER": True,
}
```

---

# Example Django Login Integration

```python
from captcha_auth.services import verify_captcha
from django.contrib.auth import authenticate

def login_view(request):
    captcha_token = request.POST.get("captcha")

    verify_captcha(captcha_token)

    user = authenticate(
        username=request.POST["username"],
        password=request.POST["password"]
    )

    return user
```

---

# DRF Example

```python
from rest_framework.views import APIView
from captcha_auth.services import verify_captcha

class LoginAPIView(APIView):

    def post(self, request):
        captcha = request.data.get("captcha")

        verify_captcha(captcha)

        return Response({"success": True})
```

---

# Architecture

```text
Client
   │
   ▼
CAPTCHA Provider
   │
   ▼
django-captcha-auth
   │
   ▼
Authentication Flow
```

---

# Configuration Options

| Setting           | Description                   |
| ----------------- | ----------------------------- |
| `PROVIDER`        | CAPTCHA provider              |
| `SECRET_KEY`      | Provider secret key           |
| `SITE_KEY`        | Public site key               |
| `VERIFY_LOGIN`    | Protect login endpoint        |
| `VERIFY_REGISTER` | Protect registration endpoint |
| `VERIFY_RESET`    | Protect password reset        |
| `TIMEOUT`         | CAPTCHA validation timeout    |

---

# Security Features

* CAPTCHA verification
* Anti-bot protection
* Brute-force mitigation
* Secure validation flow
* Replay protection support
* DRF API protection
* Session authentication compatible
* JWT authentication compatible

---

# Supported Providers

* Google reCAPTCHA
* Cloudflare Turnstile
* hCaptcha
* Custom providers

---

# Example Use Cases

## Login Protection

Protect login endpoints from automated attacks.

## Registration Security

Prevent fake account creation and spam registrations.

## API Abuse Prevention

Protect public APIs and authentication endpoints.

## Sensitive Actions

Require CAPTCHA validation before dangerous operations.

---

# Project Structure

```text
captcha_auth/
│
├── services/
├── providers/
├── validators/
├── middleware/
├── exceptions/
├── api/
└── utils/
```

---

# Why django-captcha-auth?

Most CAPTCHA integrations are tightly coupled to forms or frontend logic.

`django-captcha-auth` is designed as:

* reusable infrastructure
* authentication-focused
* API-friendly
* DRF-compatible
* extensible
* production-ready

---

# Roadmap

* Rate limiting integration
* Redis-backed validation cache
* Async provider verification
* Built-in DRF permissions
* Admin analytics dashboard
* Adaptive CAPTCHA triggers

---

# Contributing

Pull requests, issues, and improvements are welcome.

---

# License

MIT License
