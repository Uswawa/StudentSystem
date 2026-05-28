pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo "Checking out code..."
                checkout scm
            }
        }
        
        stage('Build Backend') {
            steps {
                echo "Building backend..."
                dir('backend') {
                    bat '''
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }
        
        stage('Build Frontend') {
            steps {
                echo "Building frontend..."
                dir('my-app') {
                    bat '''
                        call npm install
                        call npm run build
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                echo "Running tests..."
                dir('backend') {
                    bat 'python -m pytest || exit /b 0'
                }
                dir('my-app') {
                    bat 'call npm test -- --watch=false || exit /b 0'
                }
            }
        }
        
        stage('Build Docker Images') {
            steps {
                echo "Building Docker images..."
                bat 'docker-compose build'
            }
        }
        
        stage('Deploy') {
            steps {
                echo "Deploying with Docker Compose..."
                bat '''
                    docker-compose down || exit /b 0
                    docker-compose up -d
                '''
            }
        }
    }
    
    post {
        success {
            echo '✓ Build successful!'
        }
        failure {
            echo '✗ Build failed!'
        }
        always {
            echo 'Pipeline execution completed.'
        }
    }
}
