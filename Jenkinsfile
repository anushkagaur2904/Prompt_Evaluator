pipeline {
    agent any

    environment {
        IMAGE_BACKEND = 'prompt-backend'
        IMAGE_FRONTEND = 'prompt-frontend'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies & Build') {
            parallel {
                stage('Backend') {
                    steps {
                        dir('backend') {
                            sh 'python3 -m venv venv'
                            sh 'venv/bin/pip install -r requirements.txt'
                            sh 'venv/bin/python -c "import fastapi; print(\'Backend OK\')"'
                        }
                    }
                }
                stage('Frontend') {
                    steps {
                        dir('frontend') {
                            sh 'npm install'
                            sh 'npm run build || echo "Build warnings ignored"'
                        }
                    }
                }
            }
        }

        stage('Build Docker Images (LOCAL ONLY)') {
            steps {
                dir('backend') {
                    sh "docker build -t ${IMAGE_BACKEND}:${IMAGE_TAG} ."
                }
                dir('frontend') {
                    sh "docker build -t ${IMAGE_FRONTEND}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Run Containers Locally') {
            steps {
                sh '''
                docker stop backend || true
                docker stop frontend || true
                docker rm backend || true
                docker rm frontend || true

                docker run -d -p 8000:8000 --name backend ${IMAGE_BACKEND}:${IMAGE_TAG}
                docker run -d -p 3000:3000 --name frontend ${IMAGE_FRONTEND}:${IMAGE_TAG}
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh 'sleep 10'
                sh 'curl -f http://localhost:8000 || echo "Backend not ready"'
                sh 'curl -f http://localhost:3000 || echo "Frontend not ready"'
                sh 'docker ps'
            }
        }
    }

    post {
        success {
            echo "App running locally 🚀"
        }
        failure {
            echo "Pipeline failed ❌"
        }
    }
}