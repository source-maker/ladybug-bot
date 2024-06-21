"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = require("@actions/core");
const github_1 = require("@actions/github");
async function run() {
    var _a;
    const name = (0, core_1.getInput)("name");
    const token = (0, core_1.getInput)("gh-token");
    const octokit = (0, github_1.getOctokit)(token);
    const pullRequest = github_1.context.payload.pull_request;
    try {
        if (!pullRequest) {
            throw new Error("No pull request found.");
        }
        await octokit.rest.issues.createComment({
            owner: pullRequest.base.repo.owner.login,
            repo: pullRequest.base.repo.name,
            issue_number: pullRequest.number,
            body: `hello ${name}`
        });
    }
    catch (error) {
        (0, core_1.setFailed)((_a = error === null || error === void 0 ? void 0 : error.message) !== null && _a !== void 0 ? _a : "Unknown error");
    }
}
run();
