import os
import requests
import json

# Get the pull request number from the GitHub context
with open(os.getenv('GITHUB_EVENT_PATH')) as f:
    event = json.load(f)
    pr_number = event['pull_request']['number']
    repo = event['repository']['full_name']

# Fetch the pull request details using the GitHub API
headers = {
    'Authorization': f'token {os.getenv("GITHUB_TOKEN")}',
    'Accept': 'application/vnd.github.v3+json'
}
response = requests.get(f'https://api.github.com/repos/{repo}/pulls/{pr_number}', headers=headers)
pr_details = response.json()

# Extract required details
num_commits = pr_details['commits']
num_files_changed = pr_details['changed_files']
additions = pr_details['additions']
deletions = pr_details['deletions']
num_lines_changed = additions + deletions

# Determine health status
health_status = 'green'
if num_lines_changed > 1000 or num_commits > 10 or num_files_changed > 10:
    health_status = 'yellow'
if num_lines_changed > 2000 or num_commits > 20 or num_files_changed > 20:
    health_status = 'red'

# Output the result
print(f'Number of lines changed: {num_lines_changed}')
print(f'Number of commits: {num_commits}')
print(f'Number of files changed: {num_files_changed}')
print(f'Health Status: {health_status}')

# Set the health status as an output for use in other steps
print(f'::set-output name=health-status::{health_status}')

# Exit with an appropriate status code
if health_status == 'red':
    exit(1)
