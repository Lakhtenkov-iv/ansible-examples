//node("${env.SLAVE}") {
node("EPBYMINW2033") {
  stage("Build"){

    sh "echo build artefact"
    step([$class: 'WsCleanup'])
    checkout scm
    sh 'echo "Build time: $(date)" > src/main/resources/build-info.txt'
    sh 'echo "Build Machine: $(hostname)" >> src/main/resources/build-info.txt'
    sh 'echo "Build User Name: $(whoami)" >> src/main/resources/build-info.txt'
    sh 'echo "GIT URL: $(git config --get remote.origin.url)" >> src/main/resources/build-info.txt'
    sh 'echo "GIT Commit: $(git log --reverse | tail -1)" >> src/main/resources/build-info.txt'
    sh 'echo "GIT Branch: $(git branch | grep -Po \'(?<=\\*\\s).+\')" >> src/main/resources/build-info.txt'

    sh "mvn clean package -DbuildNumber=$BUILD_NUMBER"

  }

  stage("Package"){

    sh "echo package artefact"
    sh "tar -C ./target -czf mnt-exam.tar.gz ./mnt-exam.war"
    archiveArtifacts "mnt-exam.tar.gz"

  }

  stage("Roll out Dev VM"){

    sh "ansible-playbook createvm.yml -i inventory.py"
  }

  stage("Provision VM"){
      withCredentials([usernamePassword(credentialsId: 'ansible', passwordVariable: 'vaultpass']) {            
          sh '''
          vaultpasswordfile="vault_pass.txt"
          echo $vaultpass >> $vaultpasswordfile
          ansible-playbook provisionvm.yml -i inventory.py --vault-password-file $vaultpasswordfile
          '''
      }
    

  }

  stage("Deploy Artefact"){

    sh "ansible-playbook deploy.yml -e artifact=mnt-exam.tar.gz -i inventory.py"

  }

  stage("Test Artefact is deployed successfully"){

    sh "ansible-playbook application_tests.yml -i inventory.py"
    //sleep 600
    input message: 'Do you want to finish job?', ok: 'Yes'
    sh "ansible-playbook destroyvm.yml -i inventory.py"
  }

}

