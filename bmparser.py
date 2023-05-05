"""Output security errors from brakeman"""
import json
import sys
import csv

vulnerabilities_output = []
# Read Brakeman JSON Output
def read():
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        brakeman_report = json.load(f)
    return brakeman_report

# Extract warning and line number
def parse(brakeman_report, output):

    for warning in brakeman_report['warnings']:
        warning_type = warning['warning_type']
        line_number = warning['line']
        output.append(f"{warning_type}, Line: {line_number}")
    return output

def create_csv(output):
    with open('vulnerabilities.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(output)

def main():
    brakeman_report = read()
    parse(brakeman_report, vulnerabilities_output)
    create_csv(vulnerabilities_output)
    print(vulnerabilities_output)

if __name__ == "__main__":
    main()
