# The Reading Room — Library Tracker

A full-stack Django project for tracking books, authors, tags, and reading logs — built as a hands-on refresher covering the full lifecycle of a modern web application: data modeling, CRUD, testing, CI/CD, deployment, and a versioned public API with authentication, rate limiting, webhooks, and auto-generated documentation.

## Live Demo

- **App:** _add your Render URL here_
- **API Docs (Swagger):** `/api/v1/docs/`
- **API Docs (Redoc):** `/api/v1/redoc/`
- **OpenAPI Schema:** `/api/v1/schema/`

## Tech Stack

- **Backend:** Django 6, Django REST Framework
- **Database:** PostgreSQL (production + local), with a MongoDB modeling comparison done separately
- **Auth:** Token authentication + JWT (`djangorestframework-simplejwt`)
- **Docs:** `drf-spectacular` (OpenAPI schema, Swagger UI, Redoc)
- **Deployment:** Render (Postgres + Web Service), Gunicorn + Whitenoise
- **CI/CD:** GitHub Actions (Postgres service container, automated test runs on push/PR)
- **Config:** `python-decouple` for environment variable management
- **Design system:** "The Reading Room" — Fraunces, Inter, and JetBrains Mono, with a brass/moss/walnut palette and bookshelf-inspired layout

## Features

### Core App
- Full CRUD for `Author`, `Book`, `Tag`, and `ReadingLog` via Django `ModelForm`s
- Optimized queries using `select_related` / `prefetch_related` to avoid N+1 lookups
- Custom-designed templates and static styling (no default Django admin look)

### Public API (`/api/v1/`)
- RESTful endpoints for `Author`, `Book`, and `Tag` via DRF `ModelViewSet`s and a router
- **Dual authentication:** `TokenAuthentication` and JWT (`/api/v1/token/`, `/api/v1/token/refresh/`)
- **Rate limiting:** global throttling for both anonymous and authenticated requests
- **Webhooks:** a `Webhook` model + Django signal fires an outgoing POST to registered URLs whenever a new `Book` is created
- **Email notifications:** alongside the webhook, a notification email is sent on `Book` creation (console backend locally)
- **Self-documenting:** live OpenAPI schema with Swagger and Redoc UIs

## Local Setup

```bash
# Clone and enter the project
git clone https://github.com/ethanlutabi/librarytracker.git
cd librarytracker

# Create and activate a virtual environment
python -m venv tracker
source tracker/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env   # then fill in your local values

# Run migrations
python manage.py migrate

# Create a superuser (for Django admin + generating API tokens)
python manage.py createsuperuser

# Run the dev server
python manage.py runserver
```

Visit:
- `http://localhost:8000/` — the app
- `http://localhost:8000/admin/` — Django admin
- `http://localhost:8000/api/v1/` — API root
- `http://localhost:8000/api/v1/docs/` — interactive API docs

## Environment Variables

Managed via `python-decouple`. Example `.env`:

```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=librarytracker
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Authentication

**Token auth:**
```bash
python manage.py drf_create_token <username>
```
```
Authorization: Token <your-token>
```

**JWT:**
```bash
curl -X POST http://localhost:8000/api/v1/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "you", "password": "yourpassword"}'
```
```
Authorization: Bearer <access-token>
```

Reads (`GET`) are open to anyone; writes (`POST`/`PUT`/`PATCH`/`DELETE`) require authentication via either method.

## Webhooks

Register a URL to receive a POST notification whenever a `Book` is created:

```python
from tracker.models import Webhook
Webhook.objects.create(url="https://your-endpoint.example.com/hook", event="book.created", is_active=True)
```

Payload shape:
```json
{
  "event": "book.created",
  "book": {
    "id": 1,
    "title": "Dune",
    "author": "Frank Herbert"
  }
}
```

## Testing

```bash
python manage.py test
```

Tests mock outbound webhook calls (`tracker.signals.requests.post`) to avoid live network requests during CI runs.

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) runs the full test suite against a temporary Postgres service container on every push and pull request to `main`. Deployment to Render is triggered automatically on merge, running `collectstatic` and `migrate` as part of the build step.

## Project Structure

```
librarytracker/
├── librarytracker/        # Project settings, root URLs
├── tracker/
│   ├── models.py          # Author, Book, Tag, ReadingLog, Webhook
│   ├── views.py            # Standard CRUD views
│   ├── api_views.py         # DRF ViewSets
│   ├── serializers.py       # DRF serializers
│   ├── api_urls.py          # API router + auth/docs endpoints
│   ├── signals.py           # post_save signal: webhook + email on Book creation
│   ├── tests.py
│   └── templates/
├── .github/workflows/ci.yml
├── requirements.txt
└── manage.py
```

## Roadmap

- [ ] Build a separate client application that consumes this API
- [ ] Onboarding test with an external developer using only `/docs/`
- [ ] Explore `DATABASE_URL` + `dj-database-url` for cleaner Render config
- [ ] Study real-world API ecosystems (Stripe, VS Code extensions, Chrome extensions) for design patterns

## Why This Project Exists

This isn't just a CRUD app — it's a deliberate, hands-on study of what it takes to turn working code into a usable **developer ecosystem**: a versioned API, authentication that supports multiple client types, rate limiting to protect the service, event-driven webhooks for integrations, and documentation that lets a stranger use the API without reading the source code.