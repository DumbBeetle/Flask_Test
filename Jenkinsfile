pipeline {
    agent {
        label 'agent1'
    }

    environment {
        def GIT_CHECK = ''
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

        stage('Use Git SHA Later') {
            steps {
                script {
                    echo "Previously stored GIT_CHECK: ${env.GIT_CHECK}"

                    def laterUse = env.GIT_CHECK
                    echo "Used in variable: ${laterUse}"
                }
            }
        }
    }

    post {
        always {
            script {
                def timestamp = sh(script: 'date +"%D %T"', returnStdout: true).trim()
                echo "Test was done at: ${timestamp}"
                echo "Final GIT_CHECK value: ${env.GIT_CHECK}"
            }
        }
    }
}