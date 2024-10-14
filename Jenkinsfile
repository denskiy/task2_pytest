pipeline {
    agent any
    environment {
        VENV_PATH = 'C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\PytestPipeline\\venv'
        REPO_URL = 'https://github.com/denskiy/task2_pytest.git'
        DEVELOP_BRANCH = 'develop'
        RELEASE_BRANCH = 'release-new'
        SERVER = credentials('server-secret')
        DATABASE = credentials('database-secret')
        UID = credentials('uid-secret')
        PWD = credentials('pwd-secret')
    }
    stages {
        stage('Checkout') {
            steps {
                checkout([ 
                    $class: 'GitSCM', 
                    branches: [[name: "*/${env.DEVELOP_BRANCH}"]], 
                    doGenerateSubmoduleConfigurations: false, 
                    extensions: [], 
                    userRemoteConfigs: [[url: env.REPO_URL]]
                ])
            }
        }
        stage('Setup Python Environment') {
            steps {
                script {
                    if (!fileExists(VENV_PATH)) {
                        bat '"C:\\Users\\denis_remniakov\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m venv venv'
                    }
                }
            }
        }
        stage('Generating .env File') {
            steps {
                script {
                    bat '''
                    echo Generating .env file...
                    echo SERVER=%SERVER% > .env
                    echo DATABASE=%DATABASE% >> .env
                    echo UID=%UID% >> .env
                    echo PWD=%PWD% >> .env
                    echo Environment variables written to .env.
                    '''
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    bat '.\\run_tests.bat'
                }
            }
        }
        stage('Push Cnahges') {
            steps {
                script {
                    bat '.\\push_changes.bat'
                }
            }
        }
    }
    post {
        always {
            echo "Pipeline run is complete."
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
