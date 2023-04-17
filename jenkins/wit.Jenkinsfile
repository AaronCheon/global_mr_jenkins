def AGENT = "sun"

pipeline {
  agent {
    label "${AGENT}"
  }

  stages{
    stage("checking_gitlab_value"){
      steps{
        script{
          print(env.gitlabActionType)
          sleep 30

          def tmp_list = []
          withCredentials([string(credentialsId: 'gitlabToken', variable: 'gitlab')]) {
            def tmp_str = sh(encodig: 'UTF-8', returnStdout:true, script: "curl --header PRIVATE-TOKEN:${gitlab} http://portal:8888/api/v4/projects/${env.gitlabMergeRequestTargetProjectId}/merge_requests/${env.gitlabMergeRequestIid}/changes").trim()
            def tmp_json = readJSON text: tmp_str
            tmp_json['changes'].each { now_item ->
              print(now_item['new_path'])
              tmp_list = tmp_list << now_item['new_path']
            }
          }
          withCredentials([string(credentialsId: 'gitlabToken', variable: 'gitlab')]) {
            def no_check_source = sh(encodig: 'UTF-8', returnStdout:true, script: "curl --header PRIVATE-TOKEN:${gitlab} http://portal:8888/api/v4/projects/${env.gitlabMergeRequestTargetProjectId}/repository/files/.wit-no-check\\?ref=${env.gitlabSourceBranch}").trim()
            def no_check_target = sh(encodig: 'UTF-8', returnStdout:true, script: "curl --header PRIVATE-TOKEN:${gitlab} http://portal:8888/api/v4/projects/${env.gitlabMergeRequestTargetProjectId}/repository/files/.wit-no-check\\?ref=${env.gitlabTargetBranch}").trim()
            def no_check_source_data = readJSON(text: no_check_source)
            def no_check_target_data = readJSON(text: no_check_target)
            if (no_check_source_data.message != "404 File Not Found" || no_check_target_data.message != "404 File Not Found") {
              print(no_check_source_data)
              print(no_check_source_data.message)
              print(no_check_source_data.message != "404 File Not Found")

              env.should_skip = "false"
            }
          }
          if('wit-manifest.json' in tmp_list){
              // env.should_skip = "false"
            }else {
              env.should_skip = "false"
            }
        }
      }
    }
    stage("when"){
      when{
        expression { env.should_skip != "false" }
      }
      steps {
        script{
          updateGitlabCommitStatus name: 'wit-manifest', state: 'running'
          withCredentials([string(credentialsId: 'gitlabToken', variable: 'gitlab')]) {
            def tmp_wit_manifest = sh(encodig: 'UTF-8', returnStdout:true, script: "curl --header PRIVATE-TOKEN:${gitlab} http://portal:8888/api/v4/projects/${env.gitlabMergeRequestTargetProjectId}/repository/files/wit-manifest.json/raw\\?ref=${env.gitlabSourceBranch}").trim()
            def wit_json = readJSON text: tmp_wit_manifest
            def buildJob = [:]
            def pattern = ".*(gitlab.semifive.com.*)"
            wit_json.each { now_item ->
              buildJob["${now_item}"] = {

                stage("${now_item}"){
                  script {
                    def result = (~pattern).matcher("${now_item['source']}").matches()
                    if (result){
                      withCredentials([string(credentialsId: 'gitlab_venus_token', variable: 'venus')]){
                        sh "python3 libs/find_protect.py --pn ${now_item['source']} --token ${venus} --commit ${now_item['commit']}"
                      }
                    } else {
                      sh "python3 libs/find_protect.py --pn ${now_item['source']} --token ${gitlab} --commit ${now_item['commit']}"
                    }
                  }
                }
              }
            }
            parallel buildJob
          }
        }
          echo "Running Kick"
      }
    }
  }
  post{
    failure {
      script {
        if(env.should_skip != "false" ) {
          print("FAILURE")
          updateGitlabCommitStatus name: 'wit-manifest', state: 'failed'
        }
      }
    }
    success {
      script {
        if(env.should_skip != "false" ){
          print("SUCCESS")
          //sleep time: 3, unit: 'MINUTES'
          updateGitlabCommitStatus name: 'wit-manifest', state: 'success'

        }
      }
    }
  }
}
