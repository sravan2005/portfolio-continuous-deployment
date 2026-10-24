
pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *')
    }

    options {
        timestamps()
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

        stage('Start Test Website') {
            steps {
                bat '''
                docker rm -f portfolio-test 2>NUL
                docker run -d --name portfolio-test -p 8082:80 portfolio-website:latest
                '''

                powershell '''
                $ready = $false

                for ($i = 0; $i -lt 20; $i++) {
                    try {
                        $r = Invoke-WebRequest `
                            -Uri "http://localhost:8082" `
                            -UseBasicParsing `
                            -TimeoutSec 3

                        if ($r.StatusCode -eq 200) {
                            $ready = $true
                            break
                        }
                    } catch {}

                    Start-Sleep -Seconds 2
                }

                if (-not $ready) {
                    throw "Test website did not start"
                }
                '''
            }
        }

        stage('Selenium Tests') {
            steps {
                bat '''
                python -m pip install -r requirements.txt
                set "SELENIUM_REMOTE_URL=http://localhost:4444" && set "BASE_URL=http://host.docker.internal:8082" && python -m unittest discover -s tests -v
                '''
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

        stage('Verify Deployment') {
            steps {
                powershell '''
                $r = Invoke-WebRequest `
                    -Uri "http://localhost:8081" `
                    -UseBasicParsing `
                    -TimeoutSec 15

                if ($r.StatusCode -ne 200) {
                    throw "Production website verification failed"
                }

                Write-Host "Deployment successful: HTTP $($r.StatusCode)"
                '''
            }
        }
    }

    post {
        always {
            bat 'docker rm -f portfolio-test 2>NUL & exit /b 0'
        }
    }
}
