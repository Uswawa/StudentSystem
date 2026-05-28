# 🐳 Student System - Docker Implementation

## Quick Start

### Windows
```batch
start-docker.bat
```

### Linux/Mac
```bash
chmod +x start-docker.sh
./start-docker.sh
```

### Manual Command
```bash
docker-compose up --build
```

## Services Included

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| **Frontend** | 4200 | http://localhost:4200 | Angular UI |
| **Backend** | 8000 | http://localhost:8000 | FastAPI Server |
| **API Docs** | 8000 | http://localhost:8000/docs | Swagger UI |
| **Prometheus** | 9090 | http://localhost:9090 | Metrics Collection |
| **Grafana** | 3001 | http://localhost:3001 | Dashboard (admin/admin) |

## Project Structure

```
StudentSystem/
├── backend/
│   ├── Dockerfile               # Backend container setup
│   ├── .dockerignore            # Files to exclude from image
│   ├── requirements.txt         # Python dependencies
│   ├── main.py                  # FastAPI application
│   ├── database.py              # SQLAlchemy models (with roles)
│   ├── email_service.py         # Email verification
│   ├── prometheus.yml           # Prometheus config
│   └── .env                     # Environment variables
│
├── my-app/
│   ├── Dockerfile               # Frontend container setup
│   ├── .dockerignore            # Files to exclude from image
│   ├── package.json             # Node dependencies
│   ├── angular.json             # Angular config
│   └── src/
│       └── app/
│           └── services/
│               ├── auth.service.ts       # Authentication
│               ├── auth.guard.ts         # Route protection
│               └── auth.interceptor.ts   # JWT injection
│
├── docker-compose.yml           # Service orchestration
├── DOCKER_SETUP.md              # Detailed Docker guide
├── RBAC_IMPLEMENTATION.md       # Role-Based Access Control docs
├── start-docker.sh              # Linux/Mac quick start
└── start-docker.bat             # Windows quick start
```

## Key Features

### ✅ Authentication & Authorization
- JWT token-based authentication
- 3 roles: Admin, Registrar, Student
- Role-based route protection
- Automatic token injection in requests

### ✅ Backend Services
- FastAPI with auto-reload for development
- SQLAlchemy ORM with SQLite database
- Email verification system
- Prometheus metrics collection
- Health checks

### ✅ Frontend Services
- Angular 19+ with Server-Side Rendering
- Multi-role dashboard routing
- Auth guard on protected routes
- HTTP interceptor for JWT tokens
- Hot reload on code changes

### ✅ Monitoring Stack
- Prometheus metrics collection
- Grafana dashboards
- System and application monitoring
- Pre-configured health checks

## Environment Variables

### Backend (.env)
```
GMAIL_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
SECRET_KEY=your-jwt-secret-key
PYTHONUNBUFFERED=1
```

### Docker Compose (.env)
```
SECRET_KEY=your-jwt-secret-key
GMAIL_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
GRAFANA_PASSWORD=your_grafana_password
```

## Common Tasks

### Start Services
```bash
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop Services
```bash
docker-compose down
```

### Reset Database
```bash
docker-compose down -v
docker-compose up -d backend
```

### Rebuild Images
```bash
docker-compose build --no-cache
```

### Shell Access
```bash
# Backend Python shell
docker-compose exec backend /bin/bash

# Frontend Node shell
docker-compose exec frontend /bin/sh
```

## Network Communication

All services communicate via internal Docker network:
- Frontend connects to `http://backend:8000`
- Prometheus connects to `http://backend:8000/metrics`
- Grafana connects to `http://prometheus:9090`

## Development Workflow

1. **Code Changes**: Auto-detected by services (hot reload)
2. **Backend**: Python code changes auto-reload via `--reload` flag
3. **Frontend**: Angular serves changes instantly in browser
4. **Metrics**: Access http://localhost:9090 to view real-time metrics

## Database

- **Type**: SQLite
- **Location**: Volume `backend-data:/app/student_system.db`
- **Access**: 
  ```bash
  docker-compose exec backend sqlite3 student_system.db
  ```

## Testing Endpoints

### Create Admin User
```bash
curl -X POST http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@example.com",
    "password": "password123",
    "role": "admin"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123"
  }'
```

### Get Students (Requires JWT)
```bash
curl http://localhost:8000/student \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Troubleshooting

### Container won't start
```bash
docker-compose logs backend
docker-compose logs frontend
```

### Port already in use
```bash
# Find process on port
netstat -ano | findstr :4200
# Kill process
taskkill /PID <PID> /F
```

### Database locked
```bash
docker-compose down -v
docker-compose up --build
```

### Network issues
```bash
# Inspect network
docker network inspect studentsystem_studentsystem-network

# Restart services
docker-compose restart
```

## Production Checklist

- [ ] Change `SECRET_KEY` to secure random value
- [ ] Update `GMAIL_EMAIL` and `GMAIL_PASSWORD`
- [ ] Change `GRAFANA_PASSWORD`
- [ ] Implement password hashing with bcrypt
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up HTTPS/TLS with reverse proxy (nginx)
- [ ] Configure proper logging
- [ ] Set up backup strategy
- [ ] Enable container restart policies (already set)
- [ ] Use Docker secrets for sensitive data
- [ ] Implement rate limiting
- [ ] Set up monitoring alerts

## Documentation

- [DOCKER_SETUP.md](DOCKER_SETUP.md) - Detailed Docker guide
- [RBAC_IMPLEMENTATION.md](RBAC_IMPLEMENTATION.md) - Authentication & roles
- [Backend README](backend/README.md) - Backend specific info (if exists)
- [Frontend README](my-app/README.md) - Frontend specific info

## Support

For issues, check logs:
```bash
docker-compose logs <service_name>
```

For more information, see [DOCKER_SETUP.md](DOCKER_SETUP.md)

---

**Last Updated**: May 6, 2026
**Status**: ✅ Ready for Development
