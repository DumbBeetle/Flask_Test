pipeline {
    agent {
        label 'agent1'
    }

    // Initialize a global variable at the top
    def gitCheck = ''

    stages {
        stage('checkout') {
            steps {
                checkout scm
            }
        }

        stage('Get Git SHA') {
            steps {
                script {
                    gitCheck = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    echo "Git SHA stored in gitCheck: ${gitCheck}"
                }
            }
        }

        stage('Use Git SHA Later') {
            steps {
                script {
                    echo "Using gitCheck: ${gitCheck}"  // This will work
                }
            }
        }
    }
}