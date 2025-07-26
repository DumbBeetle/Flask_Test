pipeline {
  agent {
    kubernetes {
      inheritFrom 'docker-python-agent'
      defaultContainer 'agent'
    }
  }
  environment {
    VENV = 'venv'

    // Flask configuration
    PORT = '5000'
    HOST = '0.0.0.0'
    TAG = 'v0.3'

    // Build configuration
    PYTHON_VERSION = '3.9'
    BUILD_TIMEOUT = '300'
    TEST_RESULTS_DIR = 'test-results'

    // Docker configuration
    DOCKER_REGISTRY = 'docker.io'
    IMAGE_NAME = 'flask_app'

    // Logging configuration
    LOG_LEVEL = 'INFO'
    BUILD_LOG_FILE = 'build.log'
  }

  stages {
    stage('Setup') {
      steps {
        script {
          try {
            env.DATE = sh(script: 'date +"%D"', returnStdout: true).trim()
            echo "Starting pipeline for ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}"
            echo "Build started at: ${env.DATA}"
            echo "Environment: ${env.NODE_NAME}"

            // Create directories
            sh '''
              mkdir -p ${TEST_RESULTS_DIR}
              mkdir -p logs
              echo "Pipeline started" > logs/${BUILD_LOG_FILE}
            '''
          } catch (Exception e) {
            echo "Setup failed: ${e.getMessage()}"
            currentBuild.result = 'FAILURE'
            throw e
          }
        }
      }
    }

    stage('Checkout') {
      steps {
        script {
          try {
            echo "Checking out source code..."
            git branch: 'master', url: 'https://github.com/DumbBeetle/Flask_Test'
            echo "Source code checked out successfully"
            sh 'echo "Source code checked out" >> logs/${BUILD_LOG_FILE}'
          } catch (Exception e) {
            echo "Checkout failed: ${e.getMessage()}"
            sh 'echo "ERROR - Checkout failed: ${e.getMessage()}" >> logs/${BUILD_LOG_FILE}'
            throw e
          }
        }
      }
    }

    stage('Get Git SHA') {
      steps {
        script {
          try {
            echo "Getting git commit information..."
            env.GIT_CHECK = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
            env.GIT_BRANCH = sh(script: 'git rev-parse --abbrev-ref HEAD', returnStdout: true).trim()
            env.GIT_AUTHOR = sh(script: 'git log -1 --pretty=format:"%an"', returnStdout: true).trim()

            echo "Git SHA: ${env.GIT_CHECK}"
            echo "Git Branch: ${env.GIT_BRANCH}"
            echo "Git Author: ${env.GIT_AUTHOR}"

            sh '''
              echo "Git SHA: ${GIT_CHECK}" >> logs/${BUILD_LOG_FILE}
              echo "Git Branch: ${GIT_BRANCH}" >> logs/${BUILD_LOG_FILE}
            '''
          } catch (Exception e) {
            echo "Failed to get git information: ${e.getMessage()}"
            sh 'echo "ERROR - Git info failed: ${e.getMessage()}" >> logs/${BUILD_LOG_FILE}'
            throw e
          }
        }
      }
    }

    stage('Setup Virtual Environment') {
      steps {
        script {
          try {
            echo "Setting up Python virtual environment..."
            sh '''
              echo "$Creating virtual environment" >> logs/${BUILD_LOG_FILE}
              python3 -m venv env.venv

              echo "Installing dependencies" >> logs/${BUILD_LOG_FILE}
              env.venv/bin/pip install --upgrade pip
              env.venv/bin/pip install -r ./requirements.txt

              echo "Virtual environment setup completed" >> logs/${BUILD_LOG_FILE}
            '''
            echo "Virtual environment setup completed"
          } catch (Exception e) {
            echo "Virtual environment setup failed: ${e.getMessage()}"
            sh 'echo "ERROR - Venv setup failed: ${e.getMessage()}" >> logs/${BUILD_LOG_FILE}'
            throw e
          }
        }
      }
    }

    stage('Run Tests') {
      steps {
        script {
          try {
            echo "Running unit tests..."
            sh '''
              echo "Starting unit tests" >> logs/${BUILD_LOG_FILE}
              env.venv/bin/python -m unittest discover -v 2>&1 | tee ${TEST_RESULTS_DIR}/unittest.log
              echo "Unit tests completed" >> logs/${BUILD_LOG_FILE}
            '''
            echo "Unit tests completed"
          } catch (Exception e) {
            echo "Unit tests failed: ${e.getMessage()}"
            sh 'echo "$ERROR - Unit tests failed: ${e.getMessage()}" >> logs/${BUILD_LOG_FILE}'
            throw e
          }
        }
      }
      post {
        always {
          script {
            if (fileExists("${env.TEST_RESULTS_DIR}/results.xml")) {
              publishTestResults testResultsPattern: "${env.TEST_RESULTS_DIR}/results.xml"
            }
          }
        }
      }
    }

    stage('Build and Push Docker Image') {
      steps {
        withCredentials([
          string(credentialsId: 'DOCKER_USERNAME', variable: 'DOCKER_USER'),
          string(credentialsId: 'DOCKER_TOKEN', variable: 'DOCKER_PASS'),
        ]) {
          script {
            try {
              echo "Building and pushing Docker image..."

              def time = sh(script: 'date +"%T"', returnStdout: true).trim()
              def gitSha = env.GIT_CHECK
              def buildNumber = env.BUILD_NUMBER

              sh '''
                echo "Starting Docker build" >> logs/${BUILD_LOG_FILE}

                # Build the Docker image
                docker build \
                  --build-arg DEPLOY_DATE="${env.DATE}" \
                  --build-arg DEPLOY_TIME="${time}" \
                  --build-arg GIT_SHA="${gitSha}" \
                  --build-arg BUILD_NUMBER="${buildNumber}" \
                  --build-arg HOST="${HOST}" \
                  --build-arg PORT="${PORT}" \
                  -t ${DOCKER_USER}/${IMAGE_NAME}:${TAG} .

                echo "ocker build completed" >> logs/${BUILD_LOG_FILE}

                # Login to Docker registry
                echo "Logging into Docker registry" >> logs/${BUILD_LOG_FILE}
                echo "${DOCKER_PASS}" | docker login ${DOCKER_REGISTRY} -u "${DOCKER_USER}" --password-stdin

                # Push all tags
                echo "Pushing Docker images" >> logs/${BUILD_LOG_FILE}
                docker push ${DOCKER_USER}/${IMAGE_NAME}:${TAG}

                echo "Docker images pushed successfully" >> logs/${BUILD_LOG_FILE}

                # Cleanup
                docker logout
                rm -rf ~/.docker

                echo "Docker operations completed" >> logs/${BUILD_LOG_FILE}
              '''

              echo "Docker image built and pushed successfully"

            } catch (Exception e) {
              echo "Docker build/push failed: ${e.getMessage()}"
              sh 'echo "ERROR - Docker operations failed: ${e.getMessage()}" >> logs/${BUILD_LOG_FILE}'
              throw e
            }
          }
        }
      }
    }
  }

  post {
    always {
      script {
        echo "🔍 Build completed - collecting artifacts and logs..."

        // Archive logs and test results
        archiveArtifacts artifacts: 'logs/**/*', allowEmptyArchive: true
        archiveArtifacts artifacts: "${env.TEST_RESULTS_DIR}/**/*", allowEmptyArchive: true

        // Print build summary
        def buildDuration = currentBuild.duration ?: 0
        echo """
        BUILD SUMMARY:
        ==================
        Job: ${env.JOB_NAME}
        Build: ${env.BUILD_NUMBER}
        Duration: ${buildDuration}ms
        Date: ${new Date()}
        Status: ${currentBuild.currentResult}
        Git SHA: ${env.GIT_CHECK}
        Tag: ${env.TAG}
        """

        // Final log entry
        sh 'echo "Pipeline completed with status: ${currentBuild.currentResult}" >> logs/${BUILD_LOG_FILE}'
      }
    }

    success {
      script {
        echo "Pipeline completed successfully!"
        sh '''
          echo "SUCCESS - All stages completed successfully" >> logs/${BUILD_LOG_FILE}
          echo "Docker image ${DOCKER_USER}/${IMAGE_NAME}:${TAG} is ready for deployment"
        '''
      }
    }

    failure {
      script {
        echo "Pipeline failed!"
        sh '''
          echo "FAILURE - Pipeline failed at stage" >> logs/${BUILD_LOG_FILE}
          echo "Build failed - check logs for details"
        '''
      }
    }
  }
}
