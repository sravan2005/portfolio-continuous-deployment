
pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t portfolio-website:latest .'
            }
        }

        stage('Deploy Website') {
            steps {
                bat '''
                docker rm -f portfolio-website 2>NUL
                docker run -d --restart unless-stopped --name portfolio-website -p 8081:80 portfolio-website:latest
                '''
            }
        }

        stage('Verify Website') {
            steps {
                powershell '''
                $response = Invoke-WebRequest "http://localhost:8081" -TimeoutSec 15
                if ($response.StatusCode -ne 200) {
                    throw "Website verification failed"
                }
                Write-Host "Portfolio website deployed successfully"
                '''
            }
        }
    }
}
