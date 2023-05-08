"""takes list of vulnerabilities and creates a PR for each one"""
import json
import sys
import csv
import requests
import os

def check_for_old_vulnerabilities():
    """checking to see if known vulnerabilities file exists"""
    old_vulnerabilities = './knownVulnerabilities.csv'
    check_file = os.path.isfile(old_vulnerabilities)
    return check_file
    
def read_vulnerabilities(vulns, known_vulns, c_f):
    """if knownVulnerabilities.csv does not exist add all vulnerabilities.csv to list, else check new vulns with old and only add new vulns"""
    if not c_f:
        with open(sys.argv[1], 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                vulns.append(row[0])
    else:
        with open("knownVulnerabilities.csv", 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                known_vulns.append(row[0])
        with open("vulnerabilities.csv", 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] not in known_vulns:
                    vulns.append(row[0])
    return vulns
        
def create_pr(vuln):
    """make individual PR for every new vulnerability"""
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
    """create new or append knownVulnerabilities file with new vulnerabilities"""
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
#create_pr(vulnerabilities)
#this function is commented out because it causes the program to exit with an error since
#I did not input valid credentials as it is beyond the scope of this case study
write_known_vulnerabilities(vulnerabilities, check_file)
