# SQLite Database for Backend

## Implemented

- SQLite + SQLAlchemy + Alembic migration solution
- `access_tokens` table: `token` (string, PK), `created` (datetime)
- Testability API: `POST /testability/reset-db` to reset database
- E2E Before hook: reset db before every scenario
- Backend startup: `Base.metadata.create_all()` ensures schema exists

## Commands

```bash
# Run migrations (when schema changes)
nix develop -c bash -c "cd backend && alembic upgrade head"
```

## Files

- `backend/database.py` - engine, session, base
- `backend/models/access_tokens.py` - AccessToken model
- `backend/migrations/` - Alembic migrations
- `backend/main.py` - reset-db endpoint, startup
