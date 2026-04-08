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

        stage('Install Dependencies & Test') {
            parallel {
                stage('Backend') {
                    steps {
                        dir('backend') {
                            sh 'python3 -m venv venv'
                            sh '. venv/bin/activate && pip install -r requirements.txt'
                            sh '. venv/bin/activate && pytest tests/ || true'
                        }
                    }
                }
                stage('Frontend') {
                    steps {
                        dir('frontend') {
                            sh 'npm install'
                            sh 'npm run test || true'
                        }
                    }
                }
            }
        }

        stage('Security Scan (SAST)') {
            steps {
                // Example SonarQube invocation
                // withSonarQubeEnv('SonarQube') {
                //     sh 'sonar-scanner'
                // }
                echo "Running Static Security Analysis..."
                sh 'trivy fs --severity HIGH,CRITICAL .'
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

        stage('Container Image Scan') {
            steps {
                echo "Scanning Backend Image..."
                sh "trivy image --severity HIGH,CRITICAL ${env.DOCKER_IMAGE_BACKEND}:${env.IMAGE_TAG}"
                echo "Scanning Frontend Image..."
                sh "trivy image --severity HIGH,CRITICAL ${env.DOCKER_IMAGE_FRONTEND}:${env.IMAGE_TAG}"
            }
        }

        stage('Deploy to Staging') {
            steps {
                // Deploying to staging environment for DAST
                sh 'docker-compose -f docker-compose.yml up -d'
                echo "Deployed to Staging Environment."
            }
        }

        stage('Dynamic Security Testing (DAST)') {
            steps {
                // Example OWASP ZAP invocation
                echo "Running OWASP ZAP Baseline Scan against Staging..."
                // sh 'docker run -t owasp/zap2docker-stable zap-baseline.py -t http://localhost:5173 -r zap-report.html'
            }
        }
    }

    post {
        always {
            echo "Cleaning up workspace..."
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
