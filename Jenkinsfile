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
        dir('rossw-blog-blue-penguin') {
          git branch: 'main',
              credentialsId: 'github',
              url: 'git@github.com:rosswf/rossw-blog-blue-penguin.git'
        }
        sh "pelican-themes -i rossw-blog-blue-penguin"
      }
    }
    
    stage ('Build Content') {
      steps {
        sh "pelican content"
        sh "mv output docs"
      }
    }

    stage ('Deploy') {
      when {branch 'main'}
      steps {
        git branch: 'gh-pages',
          credentialsId: 'github',
          url: 'git@github.com:rosswf/rossw-blog.git'
        sh "git merge main"
        sh "git add docs"
        sh "git commit -m 'Update site'"
        sh "git push origin gh-pages"
      }
    }
  }
}
