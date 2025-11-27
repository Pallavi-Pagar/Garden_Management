pipeline {
    agent any

    environment {
        IMAGE_NAME = "garden_app"
        IMAGE_TAG = "v1"
        SONARQUBE_TOKEN = credentials('SONARQUBE_TOKEN')
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
                container('dind') {
                    withSonarQubeEnv('sonarqube') {
                        sh """
                            docker run --network host --rm \
                            -v \$PWD:/usr/src \
                            sonarsource/sonar-scanner-cli \
                            sonar-scanner \
                              -Dsonar.projectKey=garden \
                              -Dsonar.sources=. \
                              -Dsonar.host.url=http://sonarqube.imcc.com/ \
                              -Dsonar.login=$SONARQUBE_TOKEN
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                container('dind') {
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push to Nexus') {
            steps {
                container('dind') {
                    sh """
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} nexus.imcc.com/${IMAGE_NAME}:${IMAGE_TAG}
                        docker login nexus.imcc.com -u student -p Imcc@2025
                        docker push nexus.imcc.com/${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Deploy on Server') {
            steps {
                container('dind') {
                    sh """
                        docker stop garden || true
                        docker rm garden || true
                        docker run -d -p 8000:8000 --name garden nexus.imcc.com/${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }
    }
}
