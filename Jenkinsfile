#!groovy

pipeline {
    agent any
    stages {
        stage("Run images") {
            steps {
                sh 'docker-compose -f docker-compose.prod.yml up -d --build --remove-orphans'
            }
        }
    }
}
