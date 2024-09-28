pipeline {
    triggers {
        pollSCM('H/5 * * * *') // Check every 5 minutes
    }
    agent { label 'vmtest' }
    environment {
        GITLAB_IMAGE_NAME = "registry.gitlab.com/threeman/examsoftdev"
        VMTEST_MAIN_WORKSPACE = "/home/vmtest/workspace/ExamSoftdev"
        DOCKER_PORT = "5000" // Specify the port to use
    }
    stages {
        stage('Deploy Docker Compose') {
            agent { label 'vmtest-test' }
            steps {
                script {
                    // Check if any process is using port 5000 and kill it
                    def usedPort = sh(script: "lsof -i :${DOCKER_PORT} -t || true", returnStdout: true).trim()
                    if (usedPort) {
                        echo "Port ${DOCKER_PORT} is in use by process ${usedPort}, killing it..."
                        sh "kill -9 ${usedPort} || true"
                    } else {
                        echo "Port ${DOCKER_PORT} is free."
                    }

                    // Check if any running container is using port 5000 and stop it
                    def containerUsingPort = sh(script: "docker ps --filter 'publish=${DOCKER_PORT}' -q || true", returnStdout: true).trim()
                    if (containerUsingPort) {
                        echo "Docker container ${containerUsingPort} is using port ${DOCKER_PORT}, stopping it..."
                        sh "docker stop ${containerUsingPort} || true"
                        sh "docker rm ${containerUsingPort} || true"
                    }

                    // Stop and remove existing containers with docker-compose down
                    sh "docker-compose down || true"

                    // Deploy using docker-compose
                    sh "docker-compose up -d --build"
                }
            }
        }

        stage('Run Tests') {
            agent { label 'vmtest-test' }
            steps {
                sh '''
                . /home/vmtest/env/bin/activate
                
                # Clone and set up the test repository if not already cloned
                rm -rf exam-robottest
                git clone https://github.com/Narongrit2544/exam-robottest.git || true
                
                # Install dependencies
                cd ${VMTEST_MAIN_WORKSPACE}
                pip install -r requirements.txt
                
                # Run unit tests with coverage
                python3 -m unittest unit_test.py -v
                coverage run -m unittest unit_test.py -v
                coverage report -m
                
                # Run robot tests
                cd exam-robottest
                pip install -r requirements.txt
                robot robot_test.robot || true
                '''
            }
        }

        stage('Delivery to GitLab Registry') {
            agent { label 'vmtest-test' }
            steps {
                withCredentials([usernamePassword(
                        credentialsId: 'gitlab-admin',
                        passwordVariable: 'gitlabPassword',
                        usernameVariable: 'gitlabUser'
                    )]
                ) {
                    sh "docker login registry.gitlab.com -u ${gitlabUser} -p ${gitlabPassword}"
                    sh "docker tag ${GITLAB_IMAGE_NAME} ${GITLAB_IMAGE_NAME}:${env.BUILD_NUMBER}"
                    sh "docker push ${GITLAB_IMAGE_NAME}:${env.BUILD_NUMBER}"
                    sh "docker rmi ${GITLAB_IMAGE_NAME}:${env.BUILD_NUMBER}"
                }
            }
        }
    }
}
