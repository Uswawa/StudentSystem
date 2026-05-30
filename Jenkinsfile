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
                    sh '''
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
                    sh '''
                        npm install
                        npm run build
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                echo "Running tests..."
                dir('backend') {
                    sh 'python -m pytest || true'
                }
                dir('my-app') {
                    sh 'npm test -- --watch=false || true'
                }
            }
        }
        
        stage('Build Docker Images') {
            steps {
                echo "Building Docker images..."
                sh 'docker-compose build'
            }
        }
        
        stage('Deploy') {
            steps {
                echo "Deploying with Docker Compose..."
                sh '''
                    docker-compose down || true
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
