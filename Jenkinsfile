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
        stage('get git sha') {
            steps {
                script {
                    env.GIT_CHECK = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                }
            }
        }
        stage('install') {
            steps {
               sh ```
                apk add --no-cache python3 py3-pip
                python3 -m ensurepip --upgrade
                pip3 install -r requirements.txt
               ```
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