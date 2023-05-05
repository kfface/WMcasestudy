"""Output security errors from brakeman"""
import json
import sys

# Load Brakeman report in JSON format
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    brakeman_report = json.load(f)

# Extract warning type and line number for each warning
for warning in brakeman_report['warnings']:
    warning_type = warning['warning_type']
    line_number = warning['line']
    print(f"{warning_type}, Line: {line_number}")
