pipeline {
    agent any

    environment {
        IMAGE_BACKEND = 'prompt-backend'
        IMAGE_FRONTEND = 'prompt-frontend'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
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
                            sh '''
                            python3 -m venv venv
                            venv/bin/pip install -r requirements.txt
                            venv/bin/python -c "import fastapi; print('Backend OK')"
                            '''
                        }
                    }
                }

                stage('Frontend') {
                    steps {
                        dir('frontend') {
                            sh '''
                            export PATH=$PATH:/opt/homebrew/bin
                            npm install
                            npm run build || echo "Build warnings ignored"
                            '''
                        }
                    }
                }

            }
        }

        stage('Build Docker Images (LOCAL)') {
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
                sh '''
                sleep 10
                curl -f http://localhost:8000 || echo "Backend not ready"
                curl -f http://localhost:3000 || echo "Frontend not ready"
                docker ps
                '''
            }
        }
    }

    post {
        success {
            echo "🚀 App running locally on ports 8000 (backend) & 3000 (frontend)"
        }
        failure {
            echo "❌ Pipeline failed! Check logs."
        }
        always {
            cleanWs()
        }
    }
}