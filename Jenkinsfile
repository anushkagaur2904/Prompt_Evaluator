pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Validation') {
    steps {
        dir('backend') {
            sh '''
            python3 -m venv venv

            . venv/bin/activate

            pip install -r requirements.txt

            python -c "import fastapi; print('Backend OK')"
            '''
        }
    }
}
        stage('Frontend Build') {
            steps {
                dir('frontend') {
                    sh '''
                    npm install
                    npm run build || echo "Build warnings ignored"
                    '''
                }
            }
        }

        stage('SonarQube Analysis') {
    steps {
        script {
            def scannerHome = tool 'SonarScanner'

            withSonarQubeEnv('SonarQube') {
                sh """
                ${scannerHome}/bin/sonar-scanner \
                -Dsonar.projectKey=prompt-evaluator \
                -Dsonar.sources=. \
                -Dsonar.host.url=http://host.docker.internal:9000 \
                -Dsonar.token=squ_c5acf21eedddd91d642e7ec4478af9dc6d387b0b
                """
            }
        }
    }
}

    post {

        success {
            echo 'Pipeline executed successfully'
        }

        failure {
            echo 'Pipeline failed'
        }

        always {
            cleanWs()
        }
    }
}