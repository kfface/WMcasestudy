"""takes list of vulnerabilities and creates a PR for each one"""
import json
import sys
import csv
import requests
import os

def read_vulnerabilities(v_list):
    with open("vulnerabilities.csv", 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            v_list.append(row[0])
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

vulnerabilities = []
read_vulnerabilities(vulnerabilities)
if not vulnerabilities:
    sys.exit(1)
print(vulnerabilities)
create_pr(vulnerabilities)
