# Docker Setup Guide

## Prerequisites

- **Docker**: [Install Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Docker Compose**: Usually included with Docker Desktop

## Quick Start

### 1. Build and Start All Services

```bash
# Build images and start all containers
docker-compose up --build
```

This will start:
- **Frontend**: Angular app on http://localhost:4200
- **Backend**: FastAPI on http://localhost:8000
- **Prometheus**: Metrics on http://localhost:9090
- **Grafana**: Dashboard on http://localhost:3001

### 2. Access the Application

| Service | URL |
|---------|-----|
| Frontend (Angular) | http://localhost:4200 |
| Backend (FastAPI) | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Metrics (Prometheus) | http://localhost:9090 |
| Dashboard (Grafana) | http://localhost:3001 |

**Grafana Login:**
- Username: `admin`
- Password: `admin` (or set via `GRAFANA_PASSWORD` env var)

## Service Configuration

### Backend Service

The backend service runs FastAPI with auto-reload for development.

**Environment Variables:**
```
PYTHONUNBUFFERED=1         # Python output buffering
GMAIL_EMAIL                # Gmail account for email verification
GMAIL_PASSWORD             # Gmail app-specific password
SECRET_KEY                 # JWT secret key (change in production)
DATABASE_URL               # SQLite database path
```

**Database:**
- SQLite database stored in volume `backend-data:/app`
- Database file: `student_system.db`

### Frontend Service

The frontend runs Angular development server with hot reload.

**Features:**
- Auto-reload on code changes
- Configured to work with backend on http://backend:8000
- Polling interval: 2000ms

### Monitoring Stack

**Prometheus** collects metrics from the backend at http://backend:8000/metrics

**Grafana** visualizes the metrics from Prometheus

## Common Commands

### Start Services
```bash
# Start all services in background
docker-compose up -d

# Start specific service
docker-compose up -d backend
docker-compose up -d frontend
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clear data)
docker-compose down -v
```

### View Logs
```bash
# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Rebuild Images
```bash
# Rebuild all images
docker-compose build

# Rebuild specific service
docker-compose build backend
docker-compose build frontend
```

### Shell Access
```bash
# Access backend container shell
docker-compose exec backend /bin/bash

# Access frontend container shell
docker-compose exec frontend /bin/sh
```

### Health Check
```bash
# Check service status
docker-compose ps
```

## Environment Configuration

### Backend .env File

Create or update `backend/.env`:

```env
# Gmail Configuration
GMAIL_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=your_app_password

# JWT Secret (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
SECRET_KEY=your-generated-secret-key

# Database
DATABASE_URL=sqlite:///./student_system.db

# Python
PYTHONUNBUFFERED=1
```

### Docker Compose .env Overrides

Create `.env` in project root to override docker-compose variables:

```env
# Backend
GMAIL_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
SECRET_KEY=your-secret-key

# Grafana
GRAFANA_PASSWORD=your_grafana_password
```

## Network

All services communicate on the `studentsystem-network` bridge network:

```
Frontend (4200) <---> Backend (8000) <---> Prometheus (9090)
                           ↓
                       Grafana (3001)
```

### Service Discovery

Within the network, services can be reached by name:
- Backend from Frontend: `http://backend:8000`
- Prometheus from Grafana: `http://prometheus:9090`

## Database Management

### View SQLite Database

```bash
# From backend container
docker-compose exec backend sqlite3 student_system.db

# List tables
.tables

# Query
SELECT * FROM users;
```

### Reset Database

```bash
# Remove volume and restart
docker-compose down -v
docker-compose up -d backend
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :4200    # Frontend
lsof -i :8000    # Backend
lsof -i :9090    # Prometheus
lsof -i :3001    # Grafana

# Kill process (Linux/Mac)
kill -9 <PID>
```

### Container Won't Start

```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild and start fresh
docker-compose down -v
docker-compose up --build
```

### Database Lock Issues

```bash
# Remove database volume
docker volume rm studentsystem_backend-data

# Restart backend
docker-compose up -d backend
```

### Network Issues

```bash
# Test connectivity from container
docker-compose exec backend curl http://backend:8000/
docker-compose exec frontend curl http://backend:8000/

# Inspect network
docker network inspect studentsystem_studentsystem-network
```

## Production Deployment

### Pre-Deployment Checklist

- [ ] Change `SECRET_KEY` to a secure value
- [ ] Update `GMAIL_EMAIL` and `GMAIL_PASSWORD`
- [ ] Change `GRAFANA_PASSWORD`
- [ ] Use HTTPS (implement nginx reverse proxy)
- [ ] Implement password hashing in backend
- [ ] Set up proper database (PostgreSQL recommended)
- [ ] Configure backup strategy
- [ ] Set up monitoring and logging
- [ ] Use environment-specific configurations

### Production docker-compose.yml

```yaml
# Add production overrides
services:
  backend:
    restart: always
    environment:
      - SECRET_KEY=${SECRET_KEY}  # Must be set in environment
    # Remove --reload flag
    command: uvicorn main:app --host 0.0.0.0 --port 8000
```

## Development Tips

### Hot Reload

- **Frontend**: Changes to code auto-refresh in browser (ng serve)
- **Backend**: Changes auto-reload via `--reload` flag

### API Testing

```bash
# Test login endpoint
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Test with JWT token
curl http://localhost:8000/student \
  -H "Authorization: Bearer <token>"
```

### Metrics Testing

```bash
# View Prometheus metrics
curl http://localhost:8000/metrics
```

## Useful Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Angular Docker Guide](https://angular.io/guide/ivy)
- [FastAPI Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

## Support

For issues or questions, check the service logs:

```bash
docker-compose logs -f <service_name>
```

