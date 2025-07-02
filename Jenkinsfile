pipeline {
    agent {
        label 'agent1'
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
                    env.GIT_CHECK = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
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
                echo "Git SHA: ${env.GIT_CHECK}"
            }
        }
    }
}