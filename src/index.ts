import { getInput, setFailed } from "@actions/core"
import { context, getOctokit } from "@actions/github"

export async function run() {
    const name = getInput("name")
    const token = getInput("gh-token")
    const label = getInput("label")

    const octokit = getOctokit(token)
    const pullRequest = context.payload.pull_request

    try {
        if (!pullRequest) {
            throw new Error("No pull request found.")
        }

        await octokit.rest.issues.createComment({
            owner: pullRequest.base.repo.owner.login,
            repo: pullRequest.base.repo.name,
            issue_number: pullRequest.number,
            body: `hello ${name}`
        });
    } catch (error) {
        setFailed((error as Error)?.message ?? "Unknown error")
    }
}

if (!process.env.JEST_WORKER_ID){
    run();
}