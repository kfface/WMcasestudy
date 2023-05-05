this is a source for brakeman and rubocop parsing
https://github.com/rjkaes/ci-parse-and-report-bitbucket

# Required and typically comes from Jenkins when it runs as job
#   GIT_COMMIT

# Adjust to match your setup
export BITBUCKET_WORKSPACE='the-bitbucket-workspace'
export BITBUCKET_USER='username'
export BITBUCKET_PASSWORD='password'
export REPO_SLUG='the-repository'

# Submit Rubocop Report to Bitbucket (for a typical Rails application)
rubocop -c /opt/rubocop.yml --fail-level E --format json --out report.rubocop.json $(find app lib spec -name '*.rb' -print)
report.parse.rubocop.rb report.rubocop.json > parsed.report.rubocop.json
report.submit.rb $REPO_SLUG rubocop parsed.report.rubocop.json || true

# Submit Brakeman Report to Bitbucket
brakeman -A -f json -o report.brakeman.json --no-exit-on-warn --no-exit-on-error --force-scan
report.parse.brakeman.rb report.brakeman.json > parsed.report.brakeman.json
report.submit.rb $REPO_SLUG brakeman parsed.report.brakeman.json || true