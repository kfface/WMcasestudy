"""takes list of vulnerabilities and creates a PR for each one"""
import json
import sys
import csv
import requests
    
def read_vulnerabilities():
    with open(sys.argv[1], 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        vulnerabilities = []
        for row in reader:
            vulnerabilities.append(row)
    return vulnerabilities

def create_pr(v):
    for prtitle in v:
        url = "https://api.github.com/repos/kfface/WMcasestudy/pulls"
        title = prtitle
        body = "Please pull these awesome changes in!"
        head = "octocat:new-feature"
        base = "master"
        token = "<YOUR-TOKEN>"

        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        payload = {
            "title": title,
            "body": body,
            "head": head,
            "base": base
        }

        response = requests.post(url.format(owner="kfface", repo="WMcasestudy"), headers=headers, data=json.dumps(payload))
        if response.status_code == 201:
            print("Pull request created successfully!")
        else:
            print(f"Error creating pull request: {response.status_code} - {response.text}")

vulnerabilities = read_vulnerabilities()
create_pr(vulnerabilities)
