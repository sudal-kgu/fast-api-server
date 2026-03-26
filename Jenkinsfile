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
                    HOST_INPUTS_DIR=${env.IMAGE_PATH_FROM_SPRING}/inputs \
                    HOST_OUTPUTS_DIR=${env.IMAGE_PATH_FROM_SPRING}/outputs \
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
