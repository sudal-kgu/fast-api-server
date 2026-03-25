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
                    docker compose down || true
                    RABBITMQ_USERNAME=${env.RABBITMQ_PROD_USERNAME} \
                    RABBITMQ_PASSWORD=${env.RABBITMQ_PROD_PASSWORD} \
                    HOST_INPUTS_DIR=/home/github/trash/images/spring/inputs \
                    HOST_OUTPUTS_DIR=/home/github/trash/images/spring/outputs \
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
