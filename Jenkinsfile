pipeline {
    agent any

    environment {
        // Customize these for your project
        APP_NAME = "flask-app"
        DOCKER_IMAGE = "your-dockerhub-username/${APP_NAME}"
        DOCKER_TAG = "latest"
        VENV = ".venv"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/tazerface007/blog-app-backend.git'
            }
        }

        stage('Set up Python Environment') {
            steps {
                sh '''
                    python3 -m venv ${VENV}
                    source ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    source ${VENV}/bin/activate
                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                // Example: deploy to a server via SSH
                withCredentials([sshUserPrivateKey(credentialsId: 'server-ssh', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                        ssh -i $SSH_KEY user@your-server "docker pull ${DOCKER_IMAGE}:${DOCKER_TAG} && docker stop ${APP_NAME} || true && docker rm ${APP_NAME} || true && docker run -d --name ${APP_NAME} -p 5000:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    '''
                }
            }
        }
    }

    post {
        always {
            junit 'tests/results/*.xml' // if you generate test reports
            cleanWs()
        }
    }
}
