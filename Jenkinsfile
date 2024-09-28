pipeline {
    triggers {
        pollSCM('H/5 * * * *') // Check every 5 minutes
    }
    agent { label 'vmtest' }
    environment {
        GITLAB_IMAGE_NAME = "registry.gitlab.com/threeman/examsoftdev"
        VMTEST_MAIN_WORKSPACE = "/home/vmtest/workspace/ExamSoftdev"
    }
    stages {
        stage('Deploy Docker Compose') {
            agent { label 'vmtest-test' }
            steps {
                sh "docker-compose up -d --build"
            }
        }
        stage("Run Tests") {
            agent { label 'vmtest-test' }
            steps {
                sh '''
                . /home/vmtest/env/bin/activate
                
                cd ${VMTEST_MAIN_WORKSPACE}
                python3 -m unittest unit_test.py -v
                coverage run -m unittest unit_test.py -v
                coverage report -m

                rm -rf robot-aun
                if [ ! -d "robot-aun" ]; then
                    git clone https://github.com/Narongrit2544/exam-robottest.git
                fi
                
                pip install -r requirements.txt 
                cd exam-robottest
                robot robot_test.robot || true
                '''
            }
        }
        stage("Delivery to GitLab Registry") {
            agent { label 'vmtest-test' }
            steps {
                withCredentials(
                    [usernamePassword(
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
