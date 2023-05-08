Write-up:
Assumptions:
1. This pipeline is a mature one, and scanners and linters have been optimized to minimize false positives.
2. A script has been written to remove remediated vulnerabilities from knownVulnerabilities.csv. (this could be done quickly by making a few tweaks to my current algorithms but did not think it necessary to repeat myself for this case study)

Development Workflow:
The development workflow begins with Rubocop linting, using the -a argument for automatic remediation of formatting issues. Once the code is formatted, the pipeline moves on to the Brakeman security scan, which generates a report.json output in JSON format for automated processes.

The pipeline then calls two Python files. The first one, bmparser.py, takes report.json as an argument and performs three steps: (1) reading the Brakeman report, (2) parsing the report to create a list of vulnerabilities with their names and line numbers, and (3) creating a CSV file with the title and line number for use in the next Python script.

The second Python script, pullrequest.py, takes vulnerabilities.csv as an argument and performs the bulk of the remediation in four steps:
1. Checking for the existence of knownVulnerabilities.csv, which will be created at the end of this function to maintain consistency in the CI/CD pipeline.
2a. If knownVulnerabilities.csv does not exist, vulnerabilities.csv is read in its entirety, and each vulnerability and line number are added to a list.
2b. If knownVulnerabilities.csv exists, vulnerabilities.csv is cross-referenced against the list of known vulnerabilities, and only new vulnerabilities are added to the list.
3. Creating an individual pull request (PR) for each new error found, with the PR title as the name and location of the error and the branch name as the first two words of the PR title (special characters and spaces are removed). Each issue is handled as an individual PR to ensure prompt remediation and separation of concerns.
4. Once the PRs are sent, the list of new vulnerabilities is either appended (if knownVulnerabilities.csv exists) or a new file is created labeled as knownVulnerabilities.csv. This step is crucial because PRs are sent for individual vulnerabilities, and we want to make sure that known vulnerabilities are taken into account. When a vulnerability is patched, it must be removed from knownVulnerabilities.csv (automatically via a Python script), and new PRs should not be created for vulnerabilities that were previously sent through the pipeline.

An essential aspect of DevSecOps is automatically gathering useful data, analyzing it, and using it to create a better pipeline. For the next step, SMTP is used to send the CSV file to a security analyst, who can monitor which vulnerabilities are recurring. We can then teach our developers to be more cautious with these vulnerabilities and/or implement tools in their IDEs to catch these vulnerabilities and require their remediation before PR creation.

It's important to continuously monitor and manage risk throughout the SDLC for this reason I have chosen to use a blue/green environment which allows for great agilitiy and more frequent deployments while reducing risk as much as possible.
We can implement this by monitoring the number (and idealy severity) of known vulnerabilities, I have set this value to an environment variable which can be used to automatically deploy to blue/green environments based on the agility of the pipeline and the risk acceptance of the security team.

