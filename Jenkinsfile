pipeline {
    agent {
        label 'agent1'
    }
    environment  {
        GIT_CHECK = ''
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
                    env.GIT_CHECK = GIT_SHA
                    echo "Git SHA is: ${GIT_SHA}"
                    echo "Git Check is: ${env.GIT_CHECK}"
                }
            }
        }
    }
    post{
        always{
            script{
                def time = sh(script: 'date +"%T"', returnStdout: true).trim()
                def date = sh(script: 'date +"%D"', returnStdout: true).trim()
                echo "Test was done on Date: ${date}, Time: ${time}"
            }
        }
    }
}