# Shrestha Roy — Portfolio

Static portfolio site (`index.html`, `style.css`, `assets/`) deployed by Netlify from `main` to https://shrestha-roy.netlify.app. CV scripts and full workflow notes live in `resume/CLAUDE.md`.

## Rule: preview before merging

Every change goes through a PR. **Never merge to `main` (the live site) without the user's explicit approval.**

1. Branch → commit → push → open the PR via REST (`gh api repos/isagiyo1ch1/shrestha-portfolio/pulls --method POST ...`; `gh pr create`/GraphQL are blocked).
2. Wait for the Netlify deploy preview, then share its link (`https://deploy-preview-<PR number>--shrestha-roy.netlify.app`). Find it with:
   `gh api repos/isagiyo1ch1/shrestha-portfolio/commits/<branch>/statuses --jq '.[] | select(.context|test("deploy-preview")) | "\(.state) \(.target_url)"'`
3. Ask the user if it's okay to merge to the live site, and stop.
4. Merge (`gh api .../pulls/<n>/merge --method PUT -f merge_method=squash`) only after they say yes. For requested changes, push to the same branch and ask again.
