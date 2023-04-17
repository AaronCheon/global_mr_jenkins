import argparse
import subprocess
import json
import sys


def parser():
  parse = argparse.ArgumentParser("Find MR hooks")
  parse.add_argument("--project_name", "--pn" , type = str, help="Gitlab project name", required=True)
  parse.add_argument("--commit"               , type = str, help="Target commit hash tag")
  parse.add_argument("--token"                , type = str, help="Secreate token")
  return parse

def parseData(projectname, token): # projectname : gitlab source repo
  project = projectname.split(":")[1].split(".git")[0]
  url = projectname.split(":")[0].split("@")[1]
  tmp_projectname = project.replace("/","%2F")
  cmd = f"curl --header PRIVATE-TOKEN:{token} http://{url}:8888/api/v4/projects/{tmp_projectname}/protected_branches".split(" ")
  datas = subprocess.check_output(cmd).decode('utf-8')
  return json.loads(datas)

def findProtectBranch(args):
  return parseData( projectname =args.project_name, token = args.token)

def findBranchTree(projectname, token, branch):
  project = projectname.split(":")[1].split(".git")[0]
  url = projectname.split(":")[0].split("@")[1]
  tmp_projectname = project.replace("/","%2F")
  cmd = f"curl --header PRIVATE-TOKEN:{token} http://{url}:8888/api/v4/projects/{tmp_projectname}/repository/commits?ref_name={branch}&per_page=9999".split(" ")
  datas = subprocess.check_output(cmd).decode('utf-8')
  return [ each_commit['id'] for each_commit in json.loads(datas) ]

def checking_branch( args, proBranch_curl ):
  proBranch_list = [ each['name'] for each in proBranch_curl ]
  for each in proBranch_list:
    tmp_list = findBranchTree( projectname =args.project_name, token = args.token, branch = each )
    if args.commit in tmp_list:
      print("PASSED")
      return 0
  return 1

if __name__=="__main__":
  args = parser().parse_args()
  sys.exit(checking_branch( args = args, proBranch_curl = findProtectBranch(args)))
