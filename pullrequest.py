"""takes list of vulnerabilities and creates a PR for each one"""
import json
import sys
import csv
import requests
import os

def check_for_old_vulnerabilities():
    old_vulnerabilities = './knownVulnerabilities.csv'
    check_file = os.path.isfile(old_vulnerabilities)
    return check_file
    
def read_vulnerabilities(vulnerabilities, known_vulnerabilities, check_file):
    if not check_file:
        with open("vulnerabilities.csv", 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                vulnerabilities.append(row[0])
    else:
        with open("knownVulnerabilities.csv", 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                known_vulnerabilities.append(row[0])
        with open("vulnerabilities.csv", 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] not in known_vulnerabilities:
                    vulnerabilities.append(row[0])
    return vulnerabilities
        
def create_pr(vuln):
    for prtitle in vuln:
        branch_name = prtitle.split()[:2]
        branch_name = branch_name[0] + branch_name[1]
        branch_name = ''.join(char for char in branch_name if char.isalnum())
        url = "https://api.github.com/repos/kfface/WMcasestudy/pulls"
        title = prtitle
        body = "Please fix this vulnerabilitiy"
        head = branch_name
        base = "main"
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

def write_known_vulnerabilities(vuln, c_f):
    if not c_f:
        with open('knownVulnerabilities.csv', 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            for item in vuln:
                writer.writerow([item])
    else:
        with open('knownVulnerabilities.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            for item in vuln:
                writer.writerow([item])

vulnerabilities = []
known_vulnerabilities = []
check_file = check_for_old_vulnerabilities()
read_vulnerabilities(vulnerabilities, known_vulnerabilities, check_file)
create_pr(vulnerabilities)
write_known_vulnerabilities(vulnerabilities, check_file)
