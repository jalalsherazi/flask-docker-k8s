pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-app'
        IMAGE_TAG = 'latest'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                @FOR /f "tokens=*" %%i IN ('minikube docker-env --shell cmd') DO @%%i
                docker build -t %IMAGE_NAME%:%IMAGE_TAG% .
                '''
            }
        }

        stage('Test Docker Image') {
            steps {
                bat '''
                @FOR /f "tokens=*" %%i IN ('minikube docker-env --shell cmd') DO @%%i

                docker rm -f flask-test 2>NUL || echo No previous test container

                docker run -d --name flask-test -p 5001:5000 %IMAGE_NAME%:%IMAGE_TAG%

                timeout /t 5 /nobreak

                curl -f http://localhost:5001

                docker stop flask-test
                docker rm flask-test
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                '''
            }
        }

        stage('Restart Deployment') {
            steps {
                bat '''
                kubectl rollout restart deployment/flask-deployment
                kubectl rollout status deployment/flask-deployment --timeout=120s
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                bat '''
                kubectl get deployments
                kubectl get pods
                kubectl get services
                '''
            }
        }
    }

    post {
        always {
            bat 'docker rm -f flask-test 2>NUL || echo Test container already removed'
        }

        success {
            echo 'CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'CI/CD Pipeline failed. Check the failed stage.'
        }
    }
}