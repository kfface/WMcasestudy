"""Output security errors from brakeman"""
import sys
import json
import csv

vulnerabilities_output = []
def read():
    """read in brakeman report.json"""
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        brakeman_report = json.load(f)
    return brakeman_report

def parse(b_r, output):
    """parse and extract vulnerability name and line number"""
    try:
        for warning in b_r['warnings']:
            warning_type = warning['warning_type']
            line_number = warning['line']
            output.append(f"{warning_type}, Line: {line_number}")
        return output
    except KeyError:
        print("output is empty")

def create_csv(output):
    """make csv of vulnerabilities to pass to next function"""
    with open('output/vulnerabilities.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        for item in output:
            writer.writerow([item])


brakeman_report = read()
parse(brakeman_report, vulnerabilities_output)
create_csv(vulnerabilities_output)
