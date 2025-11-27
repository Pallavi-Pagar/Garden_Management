pipeline {

    agent any

    environment {
        IMAGE_NAME = "garden_app"
        IMAGE_TAG = "v1"

        // SonarQube credentials (secret text)
        SONARQUBE_TOKEN = credentials('SONARQUBE_TOKEN')

        // Nexus credentials
        NEXUS_USER = "student"
        NEXUS_PASSWORD = "Imcc@2025"

        SONAR_URL = "http://sonarqube.imcc.com"
        NEXUS_URL = "nexus.imcc.com"
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
                        -Dsonar.host.url=$SONAR_URL \
                        -Dsonar.login=$SONARQUBE_TOKEN
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                """
            }
        }

        stage('Push to Nexus') {
            steps {
                sh """
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${NEXUS_URL}/${IMAGE_NAME}:${IMAGE_TAG}
                    echo ${NEXUS_PASSWORD} | docker login ${NEXUS_URL} -u ${NEXUS_USER} --password-stdin
                    docker push ${NEXUS_URL}/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Deploy on Server') {
            steps {
                sh """
                    docker stop garden || true
                    docker rm garden || true

                    docker run -d --name garden \
                        -p 8000:8000 \
                        ${NEXUS_URL}/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }
    }
}
