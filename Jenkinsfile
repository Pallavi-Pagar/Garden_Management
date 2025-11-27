pipeline {
    agent {
        kubernetes {
            label 'my-jenkins-jenkins-agent'
            defaultContainer 'jnlp'
        }
    }

    environment {
        IMAGE_NAME = "garden_app"
        IMAGE_TAG = "v1"

        // SonarQube Token (Secret Text Credential)
        SONARQUBE_TOKEN = credentials('SONARQUBE_TOKEN')

        // Nexus credentials (ID must exist in Jenkins)
        NEXUS_USER = "student"
        NEXUS_PASSWORD = "Imcc@2025"

        // Replace after faculty confirms
        SONAR_URL = "http://sonarqube.imcc.com"
    }

    stages {

        /**
         * ------------------------------------------------------
         * 1. CLONE SOURCE CODE
         * ------------------------------------------------------
         */
        stage('Clone Source') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Pallavi-Pagar/Garden_Management.git'
            }
        }


        /**
         * ------------------------------------------------------
         * 2. SONARQUBE ANALYSIS
         * ------------------------------------------------------
         */
        stage('SonarQube Analysis') {
            steps {
                container('dind') {
                    withSonarQubeEnv('sonarqube') {
                        sh """
                            docker run --rm \
                            -v \$PWD:/usr/src \
                            sonarsource/sonar-scanner-cli \
                            sonar-scanner \
                                -Dsonar.projectKey=garden \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=$SONAR_URL \
                                -Dsonar.login=$SONARQUBE_TOKEN
                        """
                    }
                }
            }
        }


        /**
         * ------------------------------------------------------
         * 3. BUILD DOCKER IMAGE
         * ------------------------------------------------------
         */
        stage('Build Docker Image') {
            steps {
                container('dind') {
                    sh """
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    """
                }
            }
        }


        /**
         * ------------------------------------------------------
         * 4. PUSH DOCKER IMAGE TO NEXUS
         * ------------------------------------------------------
         */
        stage('Push to Nexus') {
            steps {
                container('dind') {
                    sh """
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} nexus.imcc.com/${IMAGE_NAME}:${IMAGE_TAG}
                        docker login nexus.imcc.com -u ${NEXUS_USER} -p ${NEXUS_PASSWORD}
                        docker push nexus.imcc.com/${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }


        /**
         * ------------------------------------------------------
         * 5. DEPLOY CONTAINER ON SERVER (Colle ge Deployment)
         * ------------------------------------------------------
         */
        stage('Deploy on Server') {
            steps {
                container('dind') {
                    sh """
                        docker stop garden || true
                        docker rm garden || true

                        docker run -d --name garden \
                            -p 8000:8000 \
                            nexus.imcc.com/${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }
    }
}
