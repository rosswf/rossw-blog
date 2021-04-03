def serverip
def username = "ubuntu"

pipeline {
  agent any
  triggers { pollSCM('H/15 * * * * ')}

  stages {
    stage ('Get AWS ip') {
      steps {
        script {
                serverip = sh (
                script: 'aws ec2 describe-instances --filter "Name=tag:Name,Values=Blog Web Server" --query "Reservations[*].Instances[*].PublicIpAddress" --output=text',
                returnStdout: true
              ).trim()
        echo "The server IP is ${serverip}"
        }
      }
    }
    stage ('Install Template') {
      steps {
        git branch: 'main',
            credentialsId: 'github',
            url: 'git@github.com:rosswf/rossw-blog-blue-penguin.git'
        sh "pelican-themes -i rossw-blog-blue-penguin"
      }
    }
    
    stage ('Build Content') {
      steps {
        sh "pelican content"
      }
    }

    stage ('Deploy') {
      when {branch 'main'}
      steps {
        sh "scp -rv -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null output/* ${username}@${serverip}:/var/www/blog/"
      }
    }
  }
}