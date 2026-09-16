# Presenter script

Run all commands from this repository. Nothing in this script creates the repository or configures a remote; replace `<remote>` with the already-approved remote name if one is added later. The preparation branches are local staging aids and do not need PRs.

## Publish the baseline and demo branches

```bash
git switch main
pytest
git push -u <remote> main

git push -u <remote> demo/single-fix
git push -u <remote> demo/all-categories
git push -u <remote> demo/fix-all
git push -u <remote> demo/lifecycle
git push -u <remote> demo/manual-actions
```

Create each PR against `main` (these commands are examples only; do not run them while preparing this repository):

```bash
gh pr create \
  --base main \
  --head demo/single-fix \
  --title "Demo: targeted AI fix" \
  --body "Demonstrates one isolated AI-generated fix."

gh pr create \
  --base main \
  --head demo/all-categories \
  --title "Demo: findings across all categories" \
  --body "Demonstrates security, bug, performance, readability, and edge-case review findings."

gh pr create \
  --base main \
  --head demo/fix-all \
  --title "Demo: bulk AI fixing" \
  --body "Demonstrates five isolated findings fixed in one batch."

gh pr create \
  --base main \
  --head demo/lifecycle \
  --title "Demo: incremental review lifecycle" \
  --body "Demonstrates manual resolution, incremental review, and matching after code moves."

gh pr create \
  --base main \
  --head demo/manual-actions \
  --title "Demo: manual review actions" \
  --body "Demonstrates ignored, manually resolved, and coordinated-review findings."
```

Wait for the AI review to reach its completed state after each PR creation or push before taking the next action.

## Targeted and bulk fixes

On `demo/single-fix`, find SF-1 in the Files changed view. Post **`/ai-fix` as a reply to that specific inline AI review comment**. Inspect the generated commit, wait for post-fix verification, and show that SF-1 is fixed.

On `demo/fix-all`, post **`/ai-fix all` as a top-level PR Conversation comment** (not an inline reply). Show the five non-overlapping patches arriving in one commit, then wait for successful post-fix verification.

## Triage and manual resolution

On `demo/all-categories`, mark AC-7 ignored in the dashboard and explain that a team may deliberately accept low-value style debt. Mark AC-2 for manual review because callback destination policy is security-sensitive.

On `demo/manual-actions`, mark MA-1 `IGNORED`. For MA-2, manually change the rejected result status to `rejected`, add a regression assertion, commit and push, wait for review, then resolve the GitHub review thread. Leave MA-3 as `NEEDS_REVIEW`: its write and lookup paths require a coordinated two-file change.

## Lifecycle advancement

`demo/lifecycle` remains at Commit 1. The two preparation branches contain exactly one sequential commit each. After the initial review completes, advance the PR branch locally with these commands (the concrete SHAs are recorded after repository generation):

```bash
git switch demo/lifecycle
git cherry-pick LIFECYCLE_STEP_2_SHA
git push <remote> demo/lifecycle
# Wait for incremental review; show LC-2 resolved while LC-1 and LC-3 remain.

git cherry-pick LIFECYCLE_STEP_3_SHA
git push <remote> demo/lifecycle
# Wait again; show LC-3 matched after its code moved and LC-1 remains open.
```

Do not move the local preparation branches or rebase after recording these SHAs. In the product, show all review runs grouped under the same pull request to demonstrate incremental history rather than separate reviews.

## Capture sanitized `/demo` fixtures

After the reviews stabilize, use browser developer tools or the application's documented API inspector to capture only the minimum JSON responses needed by `/demo`. Remove authorization headers, cookies, installation/account identifiers, repository owner names, user names, emails, URLs, and free-form text that could contain private data. Replace IDs consistently with synthetic values, retain only fields rendered by `/demo`, validate the fixture offline, and review the final diff before committing it to the separate AI code-review application repository. Never copy credentials or raw webhook payloads.

