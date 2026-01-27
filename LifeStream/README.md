# LifeStream Backend

Backend infrastructure for LifeStream application.

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Make (optional, for convenience commands)

## Quick Start

1. **Clone and navigate to the project:**
   ```bash
   cd LifeStream
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env if needed (defaults work for local development)
   ```

3. **Start services (PostgreSQL and Redis):**
   ```bash
   make up
   # Or manually:
   # docker-compose -f docker/docker-compose.yml up -d
   ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize database (when ready):**
   ```bash
   cd backend
   alembic upgrade head
   ```

## Project Structure

```
LifeStream/
├── backend/
│   ├── app/
│   │   ├── db/
│   │   │   ├── base.py          # SQLAlchemy declarative base
│   │   │   └── database.py      # Database connection and session management
│   │   └── core/
│   │       ├── config.py        # Pydantic settings
│   │       └── logging.py       # Structured logging setup
│   └── migrations/
│       ├── alembic.ini          # Alembic configuration
│       └── env.py               # Alembic environment
├── docker/
│   ├── Dockerfile.backend       # Backend Docker image
│   └── docker-compose.yml       # PostgreSQL and Redis services
├── .env.example                 # Environment variables template
├── requirements.txt             # Python dependencies
├── Makefile                     # Convenience commands
└── README.md                    # This file
```

## Configuration

All configuration is managed through environment variables. See `.env.example` for available options.

### Key Settings

- **Database**: PostgreSQL connection settings (host, port, user, password, database name)
- **Redis**: Redis connection settings (host, port, database, optional password)
- **Logging**: Log level (DEBUG, INFO, WARNING, ERROR) and format (json or text)

## Makefile Commands

- `make up` - Start PostgreSQL and Redis containers
- `make down` - Stop and remove containers
- `make logs` - View logs from all services
- `make shell-db` - Open PostgreSQL shell
- `make restart` - Restart all services
- `make clean` - Stop containers and remove volumes (⚠️ deletes data)

## Database Management

### Using Alembic

Alembic is configured and ready to use. To create migrations:

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Direct Database Access

Connect to PostgreSQL:
```bash
make shell-db
```

Or using connection string:
```bash
psql postgresql://lifestream:lifestream@localhost:5432/lifestream
```

## Development

### Database Session Usage

```python
from app.db.database import get_db

# Using context manager
with get_db() as db:
    # Your database operations
    pass

# Or for dependency injection
from app.db.database import get_db_session

db = get_db_session()
try:
    # Your database operations
    pass
finally:
    db.close()
```

### Logging

```python
from app.core.logging import get_logger

logger = get_logger(__name__)
logger.info("Application started")
```

### Configuration

```python
from app.core.config import settings

database_url = settings.DATABASE_URL
redis_url = settings.REDIS_URL
```

## Docker Services

### PostgreSQL
- **Port**: 5432
- **User**: lifestream
- **Password**: lifestream
- **Database**: lifestream

### Redis
- **Port**: 6379
- **Database**: 0
- **Password**: None (by default)

## Notes

- SQLAlchemy 2.0 syntax is used throughout
- Connection pooling is configured with configurable pool size
- Structured logging supports both JSON and text formats
- Alembic is ready for migrations (no initial migrations created yet)

## Next Steps

1. Create your database models in `backend/app/models/`
2. Import models in `backend/migrations/env.py` for autogenerate support
3. Create your first migration: `alembic revision --autogenerate -m "Initial schema"`
4. Apply migrations: `alembic upgrade head`
