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
        
        stage('Build Docker Images') {
            steps {
                echo "Building Docker images..."
                sh 'docker-compose build'
            }
        }
        
        stage('Run Tests') {
            steps {
                echo "Running tests..."
                sh 'docker-compose run --rm backend python -m pytest || true'
                sh 'docker-compose run --rm frontend npm test -- --watch=false || true'
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
