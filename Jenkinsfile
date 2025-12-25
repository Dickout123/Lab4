pipeline {
    agent {
        docker {
            image 'alpine:3.21'
			args '-u root:root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

	triggers {
		cron('H/30 * * * *')      
        pollSCM('H * * * *')
    }


	environment {
        DOCKER_IMAGE = 'lebedenkoo/lab4'
		DOCKER_CREDS_ID = 'docker-credentials'
    }
	
    options {
        timestamps()
    }

    stages {
        
        stage('Check SCM') {
            steps {
                checkout scm
            }
        }
		
		stage('Update alpine repository') {
            steps {
                sh '''
                    apk update && apk upgrade
                '''
            }
        }

        stage('Install deps') {
            steps {
                sh '''
                    apk add --no-cache bash python3 py-pip
                    pip install xmlrunner
                '''
            }
        }

		
        stage('Test') {
            steps {
				sh 'python3 test_school_service.py'
            }
			post {
				always {
					junit 'test-reports/*.xml'
				}
				success {
					echo 'application testing successfully completed'
				}
				failure {
					echo 'Oh nooooo!!! Tests failed!'
				}
			}
		}

    
        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'school_service.py', fingerprint: true
            }
        }

		stage('Install docker') {
            steps {
                sh '''
                    apk add --no-cache docker
                '''
            }
        }
		
		stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} .'
                    sh 'docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest'
				}
            }
        }
		
		stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDS_ID, passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                        sh 'docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}'
                        sh 'docker push ${DOCKER_IMAGE}:latest'
                    }
                }
            }
        }
		
		stage('Cleanup') {
             steps {
                 sh 'docker rmi ${DOCKER_IMAGE}:${BUILD_NUMBER} || true'
                 sh 'docker rmi ${DOCKER_IMAGE}:latest || true'
             }
        }
    }
}
