pipeline {
    agent {
        label 'agent1'
    }

    environment {
        VENV = 'venv'
        PORT = '8080'
        HOST = '0.0.0.0'
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
        stage('set up venv') {
            steps {
            sh '''
                python3 -m venv env.venv
                env.venv/bin/pip install -r ./requirements.txt
            '''
            }
        }
        stage('unittest'){
           steps{
             sh '''
             env.venv/bin/python -m unittest discover
             '''
           }
        }
        stage('ls'){
            steps{
                sh 'python3 run app.py'
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