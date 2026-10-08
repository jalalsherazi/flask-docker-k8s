pipeline {

    agent any

    environment {

        DOCKER_IMAGE = 'jalalsherazi786/flask-app'

        IMAGE_TAG = "${BUILD_NUMBER}"

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
                docker build -t %DOCKER_IMAGE%:%IMAGE_TAG% .
                docker tag %DOCKER_IMAGE%:%IMAGE_TAG% %DOCKER_IMAGE%:latest
                '''

            }
        }


        stage('Test Docker Image') {
            steps {
                bat '''
                docker rm -f flask-test 2>NUL || echo No previous test container

                docker run -d --name flask-test -p 5001:5000 %DOCKER_IMAGE%:%IMAGE_TAG%

                powershell -Command "Start-Sleep -Seconds 8"

                docker ps

                docker logs flask-test

                curl.exe --retry 5 --retry-delay 2 --retry-connrefused -f http://127.0.0.1:5001/
                '''
            }
        }


        stage('Docker Hub Login') {

            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {

                    bat '''
                    echo %DOCKERHUB_TOKEN% | docker login -u %DOCKERHUB_USERNAME% --password-stdin
                    '''

                }
            }
        }


        stage('Push Docker Image') {

            steps {

                bat '''
                docker push %DOCKER_IMAGE%:%IMAGE_TAG%
                docker push %DOCKER_IMAGE%:latest
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


        stage('Update Kubernetes Image') {

            steps {

                bat '''
                kubectl set image deployment/flask-deployment flask-container=%DOCKER_IMAGE%:%IMAGE_TAG%
                '''

            }
        }


        stage('Wait for Deployment') {

            steps {

                bat '''
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

            bat '''
            docker rm -f flask-test 2>NUL || echo Test container already removed
            
            '''

        }


        success {

            echo 'CI/CD Pipeline completed successfully!'

        }


        failure {

            echo 'Pipeline failed. Check the failed stage.'

        }

    }

}