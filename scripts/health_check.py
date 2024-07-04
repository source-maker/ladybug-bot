import os
import requests
import json
import textwrap


def get_pr_details(repo, pr_number, token):
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    response = requests.get(
        f"https://api.github.com/repos/{repo}/pulls/{pr_number}", headers=headers
    )
    return response.json()


def determine_health_status(num_lines_changed, num_commits, num_files_changed):
    if num_lines_changed > 1000 or num_commits > 10 or num_files_changed > 10:
        return "red", "red"
    elif num_lines_changed > 500 or num_commits > 5 or num_files_changed > 5:
        return "yellow", "yellow"
    else:
        return "green", "brightgreen"


def create_or_update_comment(repo, pr_number, token, comment_body):
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    comments_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    response = requests.get(comments_url, headers=headers)
    comments = response.json()

    bot_comment_id = None
    for comment in comments:
        if "### PR Health Check Results" in comment["body"]:
            bot_comment_id = comment["id"]
            break

    if bot_comment_id:
        update_url = f"https://api.github.com/repos/{repo}/issues/comments/{bot_comment_id}"
        response = requests.patch(
            update_url, headers=headers, data=json.dumps({"body": comment_body})
        )
        return response.status_code == 200
    else:
        response = requests.post(
            comments_url, headers=headers, data=json.dumps({"body": comment_body})
        )
        return response.status_code == 201


def main():
    with open(os.getenv("GITHUB_EVENT_PATH")) as f:
        event = json.load(f)
        pr_number = event["pull_request"]["number"]
        repo = event["repository"]["full_name"]

    token = os.getenv("GITHUB_TOKEN")

    pr_details = get_pr_details(repo, pr_number, token)
    num_commits = pr_details["commits"]
    num_files_changed = pr_details["changed_files"]
    additions = pr_details["additions"]
    deletions = pr_details["deletions"]
    num_lines_changed = additions + deletions

    health_status, color = determine_health_status(
        num_lines_changed, num_commits, num_files_changed
    )

    comment_body = textwrap.dedent(f"""
    ### PR Health Check Results
    - Number of lines changed: {num_lines_changed}
    - Number of commits: {num_commits}
    - Number of files changed: {num_files_changed}

    **Health Status: ![{health_status}](https://img.shields.io/badge/status-{health_status}-{color})**
    """).strip()

    if (
        not create_or_update_comment(repo, pr_number, token, comment_body)
        and health_status == "red"
    ):
        exit(1)


if __name__ == "__main__":
    main()
