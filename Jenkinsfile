pipeline {
    agent any

    environment {
        IMAGE_NAME = "garden_app"
        IMAGE_TAG = "v1"
    }

    stages {

        stage('Clone Source') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Pallavi-Pagar/Garden_Management.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh """
                        sonar-scanner \
                        -Dsonar.projectKey=garden \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://sonarqube.imcc.com/
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push to Nexus') {
            steps {
                sh """
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} nexus.imcc.com/${IMAGE_NAME}:${IMAGE_TAG}
                    docker login nexus.imcc.com -u student -p Imcc@2025
                    docker push nexus.imcc.com/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Deploy on Server') {
            steps {
                sh """
                    docker stop garden || true
                    docker rm garden || true
                    docker run -d -p 8000:8000 --name garden nexus.imcc.com/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }
    }
}
