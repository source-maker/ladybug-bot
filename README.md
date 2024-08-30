# Ladybug Lineter
github actionでプルリクエストのヘルスチェックを行います。
CI/CDに組み込むことで、エンジニアのPullRequestへフィードバックをコメントします。

# Installation
以下 .github/YouNameThis.yml に保存してください。

```yml
on:
    pull_request:
    workflow_dispatch:

jobs:
    github_actions_sample:
        runs-on: ubuntu-latest
        permissions:
          issues: write
          pull-requests: write
          contents: write
        name: Run health check on every pull request
        steps:
        - name: Checkout
          uses: actions/checkout@v2

        - name: Run github action using docker
          id: pr_health_check
          uses: source-maker/ladybug-bot@main
          env:
            GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```