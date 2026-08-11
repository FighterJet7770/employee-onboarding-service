# Employee Onboarding Service

FastAPI backend for managing employee onboarding lifecycle with layered architecture.

## Architecture

- Router -> Service -> Repository -> SQLAlchemy ORM Models
- Pydantic schemas for request/response contracts
- Centralized exception handling

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy environment file:
   ```bash
   cp .env.example .env
   ```
4. Run API:
   ```bash
   uvicorn app.main:app --reload
   ```

## Testing

```bash
pytest -q
```

## Database

- SQL bootstrap scripts:
  - `sql/schema.sql`
  - `sql/data.sql`
- Alembic is configured under `alembic/` for versioned migrations.

### Alembic Commands

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```
