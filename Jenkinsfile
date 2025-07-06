pipeline {
    agent {
        label 'agent1'
    }

    environment {
        VENV = 'venv'
        PORT = '5000'
        HOST = '0.0.0.0'
    }

    stages {
        stage('checkout') {
            steps {
                 git branch: 'master', url: 'https://github.com/DumbBeetle/Flask_Test'
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
        stage('dockerize'){
            steps{
                 withCredentials([
                    string(credentialsId: 'DOCKER_USERNAME', variable: 'DOCKER_USER'),
                    string(credentialsId: 'DOCKER_TOKEN', variable: 'DOCKER_PASS')
                ]) {
                    sh '''
                        docker build -t $DOCKER_USER/flask_app .
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $DOCKER_USER/flask_app
                        rm -rf ~/.docker
                    '''
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