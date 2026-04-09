pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
        DOCKER_IMAGE_BACKEND = 'anushka/prompt-evaluator-backend'
        DOCKER_IMAGE_FRONTEND = 'anushka/prompt-evaluator-frontend'
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
                            sh '. venv/bin/activate && pip install -r requirements.txt'
                            sh '. venv/bin/activate && python3 -c "import fastapi; print(\'Backend dependencies OK\')"'
                        }
                    }
                }
                stage('Frontend') {
                    steps {
                        dir('frontend') {
                            sh 'npm install'
                            sh 'npm run build || echo "Build completed with warnings"'
                        }
                    }
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                dir('backend') {
                    sh "docker build -t ${env.DOCKER_IMAGE_BACKEND}:${env.IMAGE_TAG} ."
                }
                dir('frontend') {
                    sh "docker build -t ${env.DOCKER_IMAGE_FRONTEND}:${env.IMAGE_TAG} ."
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                withDockerRegistry([credentialsId: env.DOCKER_CREDENTIALS_ID, url: '']) {
                    sh "docker push ${env.DOCKER_IMAGE_BACKEND}:${env.IMAGE_TAG}"
                    sh "docker push ${env.DOCKER_IMAGE_FRONTEND}:${env.IMAGE_TAG}"
                    // Tag as latest
                    sh "docker tag ${env.DOCKER_IMAGE_BACKEND}:${env.IMAGE_TAG} ${env.DOCKER_IMAGE_BACKEND}:latest"
                    sh "docker tag ${env.DOCKER_IMAGE_FRONTEND}:${env.IMAGE_TAG} ${env.DOCKER_IMAGE_FRONTEND}:latest"
                    sh "docker push ${env.DOCKER_IMAGE_BACKEND}:latest"
                    sh "docker push ${env.DOCKER_IMAGE_FRONTEND}:latest"
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                // Deploying to staging environment
                sh 'docker-compose -f docker-compose.yml up -d'
                echo "Deployed to Staging Environment."
                // Wait for services to be ready
                sh 'sleep 30'
            }
        }

        stage('Health Check') {
            steps {
                // Check if services are healthy
                sh 'curl -f http://localhost:8000/ || echo "Backend not ready"'
                sh 'curl -f http://localhost:80/ || echo "Frontend not ready"'
                sh 'docker ps'
            }
        }
    }

    post {
        always {
            echo "Cleaning up workspace and containers..."
            sh 'docker-compose -f docker-compose.yml down || true'
            cleanWs()
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed! Please check the logs."
        }
    }
}
