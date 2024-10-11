pipeline {
    agent any
    environment {
        VENV_PATH = 'C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\PytestPipeline\\venv'
        REPO_URL = 'https://github.com/denskiy/task2_pytest.git'
        DEVELOP_BRANCH = 'develop'
        RELEASE_BRANCH = 'release-candidate'
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
        stage('Prepare Environment') {
            steps {
                script {
                    // Generate .env file
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
        // stage('Activate and Install Dependencies') {
        //     steps {
        //         bat "call C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\PytestPipeline\\venv\\Scripts\\activate.bat"
        //     }
        // }
        // stage('Upgrade pip and Install Dependencies') {
        //     steps 
        //         bat '"C:\\Users\\denis_remniakov\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pip install --upgrade pip && pip install -r requirements.txt'
        // }
        // stage('Run Tests') {
        //     steps {
        //         script {
        //             bat """
        //             "C:\\Users\\denis_remniakov\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" pytest
        //             """
        //         }
        //     }
        // }
        stage('Run Tests') {
            steps {
                script {
                    // Run the batch file
                    bat '.\\run_tests.bat'
                }
            }
        }
        stage('Push Changes') {
            steps {
                script {
                    bat ". $VENV_PATH/bin/activate"
                    dir ('release') {
                        checkout([ 
                            $class: 'GitSCM', 
                            branches: [[name: "*/${env.RELEASE_BRANCH}"]], 
                            doGenerateSubmoduleConfigurations: false, 
                            extensions: [], 
                            userRemoteConfigs: [[url: env.REPO_URL]]
                        ])
                        bat 'rsync -av --exclude=".git" ../ ./'
                        bat 'git add .'
                        bat "git commit -m 'Deploying code to release branch'"
                        bat "git push origin ${env.RELEASE_BRANCH} --set-upstream"
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
