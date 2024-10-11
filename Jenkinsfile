pipeline {
    agent any
    environment {
        VENV_PATH = 'venv'
        REPO_URL = 'https://github.com/denskiy/task2_pytest.git'
        DEVELOP_BRANCH = 'develop'
        RELEASE_BRANCH = 'release-candidate'
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
                        sh "python -m venv $VENV_PATH"
                    }
                    sh """
                    . $VENV_PATH/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    """
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    sh """
                    . $VENV_PATH/bin/activate
                    python TRN_DB_validation_test.py
                    """
                }
            }
        }
        stage('Push Changes') {
            steps {
                script {
                    sh ". $VENV_PATH/bin/activate"
                    dir ('release') {
                        checkout([ 
                            $class: 'GitSCM', 
                            branches: [[name: "*/${env.RELEASE_BRANCH}"]], 
                            doGenerateSubmoduleConfigurations: false, 
                            extensions: [], 
                            userRemoteConfigs: [[url: env.REPO_URL]]
                        ])
                        sh 'rsync -av --exclude=".git" ../ ./'
                        sh 'git add .'
                        sh "git commit -m 'Deploying code to release branch'"
                        sh "git push origin ${env.RELEASE_BRANCH} --set-upstream"
                    }    
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
