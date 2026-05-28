-- Create user if it doesn't exist
CREATE USER student_user WITH PASSWORD 'student_password';

-- Create database
CREATE DATABASE student_system OWNER student_user;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE student_system TO student_user;

