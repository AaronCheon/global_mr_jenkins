import argparse
import subprocess
import json
import sys


def parser():
  parse = argparse.ArgumentParser("Find MR hooks")
  parse.add_argument("--project_name", "--pn" , type = str, help="Gitlab project name", required=True)
  parse.add_argument("--token"                , type = str, help="Secreate token")
  return parse

def parseData(projectname, token): # projectname : gitlab source repo
  project = projectname.split(":")[1].split(".git")[0]
  tmp_projectname = project.replace("/","%2F")
  cmd = f"curl --header PRIVATE-TOKEN:{token} http://portal:8888/api/v4/projects/{tmp_projectname}/hooks".split(" ")
  datas = subprocess.check_output(cmd).decode('utf-8')
  return json.loads(datas)

def findMRHooks(args):
  json_list = parseData( projectname =args.project_name, token = args.token)
  for data in json_list:
    if data['merge_requests_events']:
      return 1
  return 0


if __name__=="__main__":
  args = parser().parse_args()
  sys.exit(findMRHooks(args))