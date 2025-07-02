pipeline {
    agent {
        label 'agent1'
    }
    environment  {
        GIT_SHA = ''
    }

    stages {
        stage('checkout') {
            steps {
                checkout scm
            }
        }
        stage('Get Git SHA') {
            steps {
                script {
                    def GIT_SHA = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    env.GIT_SHA = GIT_SHA
                    echo "Git SHA is: ${GIT_SHA}"

                    def time = sh(script: 'date +"%T"', returnStdout: true).trim()
                    def date = sh(script: 'date +"%D"', returnStdout: true).trim()
                    echo "Current Date: ${date}"
                    echo "Current Time: ${time}"
                }
            }
        }
    }
}