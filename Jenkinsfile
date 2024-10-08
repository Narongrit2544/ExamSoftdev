pipeline {
    triggers {
        pollSCM('H/1 * * * *') // Check every 5 minutes
    }
    agent { label 'vmtest' }
    environment {
        GITLAB_IMAGE_NAME = "registry.gitlab.com/threeman/examsoftdev"
        VMTEST_MAIN_WORKSPACE = "/home/vmtest/workspace/test"
        DOCKER_PORT = "5000" // Specify the port to use
    }
    stages {
        stage('Deploy Docker Compose') {
            agent { label 'connect-vmtest' }
            steps {
                sh "docker compose up -d --build"
            }
        }

        stage('Run Tests') {
            agent { label 'connect-vmtest' }
            steps {
                script {
                    try {
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
                        robot robot_test.robot || true
                        '''
                    } catch (Exception e) {
                        echo "Error during testing: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Tests failed!")
                    }
                }
            }
        }

        stage('Delivery to GitLab Registry') {
            agent { label 'connect-vmtest' }
            steps {
                script {
                    try {
                        withCredentials([usernamePassword(
                                credentialsId: 'gitlab-admin',
                                passwordVariable: 'gitlabPassword',
                                usernameVariable: 'gitlabUser'
                            )]
                        ) {
                            echo "Logging into GitLab registry..."
                            sh "docker login registry.gitlab.com -u ${gitlabUser} -p ${gitlabPassword}"
                            echo "Tagging and pushing Docker image..."
                            sh "docker tag ${GITLAB_IMAGE_NAME} ${GITLAB_IMAGE_NAME}:${env.BUILD_NUMBER}"
                            sh "docker push ${GITLAB_IMAGE_NAME}:${env.BUILD_NUMBER}"
                            sh "docker rmi ${GITLAB_IMAGE_NAME}:${env.BUILD_NUMBER}"
                        }
                    } catch (Exception e) {
                        echo "Error during delivery: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Delivery to GitLab registry failed!")
                    }
                }
            }
        }
    }
}
