pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Deploy') {
            when {
                branch 'develop'
            }

            steps {
                sh """
                    RABBITMQ_USERNAME=${env.RABBITMQ_PROD_USERNAME} \
                    RABBITMQ_PASSWORD=${env.RABBITMQ_PROD_PASSWORD} \
                    docker compose up -d --build
                """
            }
        }
    }

    post {
        success {
            sh 'docker image prune -f'
        }
    }
}
