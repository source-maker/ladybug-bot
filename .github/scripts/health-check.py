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
if num_lines_changed > 500 or num_commits > 5 or num_files_changed > 5:
    health_status = 'yellow'
if num_lines_changed > 1000 or num_commits > 10 or num_files_changed > 10:
    health_status = 'red'


# Create a comment body
comment_body = f"""
### PR Health Check Results
- Number of lines changed: {num_lines_changed}
- Number of commits: {num_commits}
- Number of files changed: {num_files_changed}

**Health Status: {health_status}**
"""

# Post the comment to the pull request
comment_url = f'https://api.github.com/repos/{repo}/issues/{pr_number}/comments'
comment_data = {
    'body': comment_body
}
response = requests.post(comment_url, headers=headers, data=json.dumps(comment_data))

if response.status_code != 201:
    print(f'Failed to create comment: {response.status_code}')
    print(response.json())

# Exit with an appropriate status code
if health_status == 'red':
    exit(1)
