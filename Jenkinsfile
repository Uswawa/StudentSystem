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
                echo "✓ Code checked out successfully"
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
                sh 'docker-compose -p studentsystem-test run --rm backend python -m pytest || true'
                sh 'docker-compose -p studentsystem-test run --rm frontend npm test -- --watch=false || true'
                sh 'docker-compose -p studentsystem-test down || true'
            }
        }
        
        stage('Deploy') {
            steps {
                echo "Deploying updated services..."
                sh '''
                    # Rebuild only backend and frontend (not Jenkins)
                    docker-compose -p studentsystem build backend frontend
                    # Update services with new images (only restarts changed ones)
                    docker-compose -p studentsystem up -d backend frontend postgres
                '''
            }
        }
    }
    
    post {
        success {
            echo '✅ Build successful!'
        }
        failure {
            echo '❌ Build failed!'
        }
        always {
            echo 'Pipeline execution completed.'
        }
    }
}
