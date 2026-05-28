# Role-Based Access Control (RBAC) Implementation

## Overview
This document describes the role-based access control (RBAC) system implemented in the Student Management System. The system supports three user roles: **Admin**, **Registrar**, and **Student**.

## Roles and Permissions

### Admin
- **Access**: Full access to all system features
- **Permissions**:
  - Manage all students (create, read, update, delete)
  - Manage users and their roles
  - Access admin dashboard
  - Manage courses
  - View all reports and analytics

### Registrar/Admission
- **Access**: Administrative functions for admissions
- **Permissions**:
  - View and manage students
  - Create and update student records
  - Access admin dashboard
  - Manage courses
  - Cannot delete students or manage user roles

### Student
- **Access**: Limited to personal information
- **Permissions**:
  - View personal details
  - View enrolled courses and semester information
  - View grades and study load
  - Cannot create or modify other students' records

---

## Backend Implementation

### Database Schema Updates

#### UserDB Model
```python
class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_verified = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)  # NEW
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### UserRole Enum
```python
class UserRole(PyEnum):
    ADMIN = "admin"
    REGISTRAR = "registrar"
    STUDENT = "student"
```

### JWT Authentication

#### Token Creation
- **Algorithm**: HS256
- **Secret Key**: Configured via environment variable `SECRET_KEY`
- **Expiration**: 30 minutes (configurable)
- **Payload**: Contains user email, role, user_id, first_name, and last_name

#### Endpoints

##### `/login` (POST)
**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user_id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "admin",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

##### `/signup` (POST)
**Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "student"
}
```

**Response:**
```json
{
  "message": "User created successfully. Verification code sent to email.",
  "user_id": 1,
  "role": "student"
}
```

### Role-Based Endpoint Protection

#### Student Endpoints

| Endpoint | Method | Required Roles | Description |
|----------|--------|-----------------|-------------|
| `/student` | GET | admin, registrar | Get all students |
| `/student` | POST | admin, registrar | Create new student |
| `/student/{id}` | GET | any authenticated | Get specific student |
| `/student/{id}` | PUT | admin, registrar | Update student |
| `/student/{id}` | DELETE | admin | Delete student |

#### Implementation Example
```python
@app.get("/student")
def get_students(current_user: dict = Depends(require_role("admin", "registrar")), 
                 db: Session = Depends(get_db)):
    """Get all students - Only admin and registrar"""
    students = db.query(StudentDB).all()
    return {"students": students, "accessed_by": current_user["email"]}
```

### Helper Functions

#### `create_access_token(data, expires_delta)`
Creates a JWT token with the provided data and expiration time.

#### `verify_token(token)`
Verifies the JWT token and returns the payload containing user information.

#### `get_current_user(credentials)`
Dependency function to extract and verify the current user from the JWT token.

#### `require_role(*allowed_roles)`
Dependency factory that creates a role checker function to restrict endpoints to specific roles.

---

## Frontend Implementation

### Authentication Service

[File: `src/app/services/auth.service.ts`]

The `AuthService` manages user authentication state and provides methods for:
- Storing/retrieving authentication tokens
- Managing current user information
- Checking user roles
- Logging out users

**Key Methods:**
- `setAuthData(authToken)`: Store authentication data after login
- `getCurrentUser()`: Get current user information
- `getToken()`: Get JWT token
- `isAuthenticated()`: Check if user is authenticated
- `hasRole(role)`: Check if user has specific role
- `hasAnyRole(roles)`: Check if user has any of specified roles
- `logout()`: Clear authentication data

### Route Guard

[File: `src/app/services/auth.guard.ts`]

The `AuthGuard` protects routes and enforces role-based access:
- Redirects unauthenticated users to login
- Checks route-level role requirements
- Redirects to appropriate dashboard based on user role

**Usage in Routes:**
```typescript
{
  path: 'admin',
  component: AdminLayout,
  canActivate: [AuthGuard],
  data: { roles: ['admin', 'registrar'] },
  children: [...]
}
```

### HTTP Interceptor

[File: `src/app/services/auth.interceptor.ts`]

The `AuthInterceptor` automatically adds the JWT token to all HTTP requests:
```typescript
Authorization: Bearer <access_token>
```

### Updated Components

#### Login Component
- Calls API with email and password
- Stores authentication data on successful login
- Redirects to appropriate dashboard based on role
- Displays error messages on failure

#### Signup Component
- Includes role selection (student, registrar, admin)
- Sends role to backend during registration
- Routes to email verification after successful signup

### API Service Updates

[File: `src/app/services/api.service.ts`]

Enhanced with:
- Automatic token storage on successful login
- Logout method to clear authentication
- All requests automatically include JWT token via interceptor

---

## Environment Configuration

### Backend
Add to `.env` file:
```
SECRET_KEY=your-secret-key-change-in-production
```

### Frontend CORS
Frontend runs on `http://localhost:4200`
Backend CORS is configured to allow requests from this origin.

---

## Security Considerations

1. **Token Storage**: JWT tokens are stored in localStorage (production should consider more secure options)
2. **Token Expiration**: Tokens expire after 30 minutes
3. **HTTPS**: Always use HTTPS in production
4. **Password Hashing**: Currently passwords are stored as plain text (TODO: implement bcrypt hashing)
5. **Token Refresh**: Implement refresh token mechanism for better security

---

## Database Migration

To apply the schema changes:

1. Delete or backup existing `student_system.db` file
2. Run backend application - it will recreate tables with new schema
3. Create new users with appropriate roles

---

## Testing the RBAC

### Test Users to Create

```python
# Admin user
POST /signup
{
  "first_name": "Admin",
  "last_name": "User",
  "email": "admin@example.com",
  "password": "admin123",
  "role": "admin"
}

# Registrar user
POST /signup
{
  "first_name": "Registrar",
  "last_name": "User",
  "email": "registrar@example.com",
  "password": "registrar123",
  "role": "registrar"
}

# Student user
POST /signup
{
  "first_name": "Student",
  "last_name": "User",
  "email": "student@example.com",
  "password": "student123",
  "role": "student"
}
```

### Test Cases

1. **Login with different roles**: Verify correct dashboard is shown
2. **Access protected endpoints**: Test with invalid tokens or missing authorization
3. **Role-based restrictions**: Try accessing admin endpoints as student
4. **Token expiration**: Wait for token to expire and retry request

---

## Dependencies Added

- `PyJWT==2.8.1`: JWT token creation and verification
- `passlib==1.7.4`: Password hashing utilities
- `bcrypt==4.1.1`: Secure password hashing (TODO: implement)

---

## Next Steps

1. **Implement password hashing** using bcrypt
2. **Add refresh tokens** for better security
3. **Implement token blacklisting** for logout
4. **Add role-specific API endpoints** (e.g., `/me` for current user info)
5. **Add audit logging** for role-based actions
6. **Implement permission-based access** (more granular than role-based)

---

## Support

For issues or questions about the RBAC implementation, refer to the code comments in:
- Backend: `backend/main.py`, `backend/database.py`
- Frontend: `src/app/services/auth.service.ts`, `src/app/services/auth.guard.ts`
