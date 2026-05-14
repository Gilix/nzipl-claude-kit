# How to submit feedback (step by step)

A walkthrough for getting a completed session file into the public `nzipl-claude-kit` repo, starting from zero. No prior git, GitHub, or Claude Code experience assumed.

If you already know how to open a PR, skip to **Path A** (web UI) or **Path C** (terminal) and use the file naming convention at the top: `goodenough-feedback/sessions/YYYY-MM-DD-yourtag.md`.

## What's a "PR" and why use one?

A pull request (PR) is a way of saying *"I want to add this file to the project, please accept it."* GitHub keeps a permanent record: the file, who added it, when, with a discussion thread attached. For lab feedback, that means:

- Each session lives at a stable URL the team can link to.
- Multiple testers can submit at the same time without overwriting each other.
- The full archive is searchable and survives turnover.

If you're a collaborator on `nzipl-claude-kit`, self-merge your PR. Otherwise GitHub auto-forks the repo for you and Gilberto merges your PR during weekly triage. Either way, you're not asking permission about content — the merge just lands the file in the durable trail.

## Before you start

You need two things:

1. **A GitHub account.** Sign up at https://github.com if you don't have one. Free tier is fine.
2. **A completed session file.** That is, the per-session template from [FEEDBACK.md](FEEDBACK.md) filled in with your test results. Draft it in any editor: Notes, TextEdit, VS Code, Notion, anywhere you're comfortable.

`Gilix/nzipl-claude-kit` is a public repo — no invite needed, no waiting on access. If you want self-merge (so you don't have to wait on Gilberto's weekly triage), message him and he'll add you as a collaborator.

Filename convention: `YYYY-MM-DD-yourtag.md`. Today's date plus a short tag (your initials and a topic hint). Example: `2026-05-14-og-mex-batteries.md`. Use lowercase, hyphens not spaces.

## Pick a path

Three ways to submit. Pick the one that matches your comfort level. They produce identical results.

| Path | What you need | Best for |
|---|---|---|
| **A. GitHub web UI** | A browser | First-timers, or anyone who wants zero installs. **Recommended.** |
| **B. Claude Code** | Claude Code installed and the repo cloned | You already use Claude Code. Tell it what you want, it does the git work. |
| **C. Terminal git** | git installed and the repo cloned | You're comfortable on the command line. |

If unsure, do Path A. It works on any laptop in any browser and does not require installing anything.

---

## Path A: GitHub web UI

No installs. Everything happens in your browser.

### Step 1. Open the repo

1. Go to https://github.com/Gilix/nzipl-claude-kit
2. The repo is public, so it should load without sign-in. If you see "Page not found," double-check the URL.
3. You should see the repo's file list, with entries including `README.md`, `CLAUDE.md`, and a `goodenough-feedback/` folder.

### Step 2. Navigate to the sessions folder

1. In the file list, click the folder named `goodenough-feedback`.
2. Then click the folder named `sessions`.
3. You should see `README.md` and any session files prior testers have committed.

### Step 3. Create your session file

1. Click the green `Add file` button at the top right of the file list. A small dropdown appears.
2. Choose `Create new file`.
3. **First-time only**: if you're not a collaborator, GitHub shows "You need to fork this repository to propose changes." Click **Fork this repository**. You land on the same create-file page, but on your own fork — that's normal. Subsequent visits skip this step.
4. The page that opens has a filename box at the top, just under the path breadcrumb (`nzipl-claude-kit / goodenough-feedback / sessions /`, or `<your-username> / nzipl-claude-kit / goodenough-feedback / sessions /` if you just forked). Type your filename there: `2026-05-14-og-mex-batteries.md` (use today's date and your tag).
5. The big text area below is for the file content. Paste your filled-in session template. (If you haven't filled it in yet: open [FEEDBACK.md](FEEDBACK.md), copy the template block under "Per-session template," fill it in elsewhere, then paste here.)

### Step 4. Commit your changes to a new branch

1. Scroll to the bottom of the page. You'll see a section called **Commit changes**.
2. The first text box (commit message) pre-fills with `Create 2026-05-14-og-mex-batteries.md`. You can leave it as-is or rewrite it shorter, e.g. `feedback: Mexico × Batteries SHAP test`.
3. Below the commit message you'll see two radio buttons:
   - "Commit directly to the `main` branch."
   - "Create a **new branch** for this commit and start a pull request."

   **Pick the second one.** GitHub auto-suggests a branch name like `your-username-patch-1`. You can rename it to something clearer, e.g. `feedback/2026-05-14-og-mex-batteries`. Lowercase with slashes is fine.
4. Click the green `Propose changes` button.

### Step 5. Open the pull request

1. GitHub now shows you an "Open a pull request" page.
2. The PR title is pre-filled from your commit message. Adjust if you want; something like `Feedback: Mexico × Batteries SHAP test` is enough.
3. The description box can stay empty, or one line ("rated C-Fail and E-Fail; details in file").
4. Click the green `Create pull request` button.

### Step 6. Land the file

1. You're now on the PR page. There are no automated checks on this repo, so the page will show "This branch has no conflicts with the base branch" almost immediately.
2. **If you're a collaborator**, click the green `Merge pull request` button → `Confirm merge`. Optional: click `Delete branch` to clean up.
3. **If you're not a collaborator**, leave the PR open. Gilberto merges feedback PRs during weekly triage (Mondays), so expect your file to land within a few business days. You can close the tab — the PR is preserved either way.

Done. Once merged, your feedback file lives at https://github.com/Gilix/nzipl-claude-kit/blob/main/goodenough-feedback/sessions/2026-05-14-og-mex-batteries.md and is visible to the whole team.

---

## Path B: With Claude Code

If you already use Claude Code on your laptop, this is the fastest path. Claude does the git work; you describe what you want.

### One-time setup

Skip these if you've already done them.

1. Install Claude Code. See https://docs.claude.com/en/docs/claude-code for the current install steps.
2. **If you're not a collaborator on `nzipl-claude-kit`:** fork it first. Open https://github.com/Gilix/nzipl-claude-kit, click the **Fork** button at the top-right. Then in step 4 below, clone your fork (`https://github.com/<your-username>/nzipl-claude-kit.git`) instead of the upstream URL. Skip this if you're a collaborator.
3. Open Terminal (macOS: `Cmd+Space`, type "Terminal," hit Enter).
4. Pick a folder for your repos and clone the kit into it:
   ```
   cd ~/Code            # or any folder you prefer
   git clone https://github.com/Gilix/nzipl-claude-kit.git
   cd nzipl-claude-kit
   ```
   If `git clone` asks for credentials, sign in with your GitHub account.

### Each time you submit

1. Open Terminal and go to the repo:
   ```
   cd ~/Code/nzipl-claude-kit
   ```
2. Pull the latest version:
   ```
   git pull
   ```
3. Start Claude Code by typing `claude` and hitting Enter.
4. Paste your filled-in session as a message to Claude. Phrase the request like this:

   > Please save the following feedback session as `goodenough-feedback/sessions/2026-05-14-og-mex-batteries.md` (substitute today's date and my initials), create a branch called `feedback/<same-tag>`, commit, push, and open a PR titled "Feedback: <one-line summary>." Then give me the PR URL.
   >
   > <paste your filled-in template here>

5. Claude will:
   - Create the file at the right path.
   - Create a branch.
   - Commit with a sensible message.
   - Run `git push` (it will ask permission first; say yes).
   - Run `gh pr create` to open the PR (also asks permission). If you're working from a fork, `gh` will prompt to PR against upstream — confirm.
   - Return the PR URL.
6. Open the URL Claude returned in your browser. If you're a collaborator, click `Merge pull request`, confirm. Otherwise leave it open for Gilberto's weekly triage.

### If Claude asks "should I proceed?"

Say yes. Pushing a branch and opening a PR are reversible if anything is wrong. The only risky thing would be force-pushing to `main`, which Claude won't do without explicit instruction.

---

## Path C: Terminal git

For the comfortable. Same one-time setup as Path B (clone the repo, see above; fork first if you're not a collaborator). Then each session:

```bash
cd ~/Code/nzipl-claude-kit
git checkout main
git pull
git checkout -b feedback/2026-05-14-og-mex-batteries

# Now save your filled-in session template at:
# goodenough-feedback/sessions/2026-05-14-og-mex-batteries.md
# Use any editor (nano, vim, code, TextEdit, etc.).

git add goodenough-feedback/sessions/2026-05-14-og-mex-batteries.md
git commit -m "feedback: Mexico × Batteries SHAP test"
git push -u origin feedback/2026-05-14-og-mex-batteries
```

The `git push` output prints a URL like:
```
https://github.com/Gilix/nzipl-claude-kit/pull/new/feedback/2026-05-14-og-mex-batteries
```

Open that URL in your browser, click `Create pull request`. If you're a collaborator, then `Merge pull request`, confirm. Otherwise leave it open for weekly triage.

If you have the GitHub CLI (`gh`) installed and authenticated, you can skip the browser:
```bash
gh pr create --fill
# Collaborators only:
gh pr merge --merge --delete-branch
```

---

## Common issues

**"I'm not sure what to put in the per-session template."**
See the worked example at the bottom of [FEEDBACK.md](FEEDBACK.md). Two filled rubrics (one Pass, one Flawed) show the level of detail expected. One-sentence notes per dimension are fine; over-writing is not the goal.

**"I committed to the `main` branch by mistake."**
On the GitHub web UI, this only happens if you picked the first radio button in Step 4 instead of the second, AND you're a collaborator (otherwise the option is greyed out). The file is still in the repo and the team can read it; it just bypassed the PR step. No action needed unless you want to redo it cleanly. If so, message Gilberto.

**"My PR shows merge conflicts."**
Very unlikely for separate session files, since each file is unique. If it happens: on the GitHub web UI, click `Resolve conflicts`, accept both versions, then `Mark as resolved`. If unsure, ask.

**"I want to fix something I already submitted."**
Easiest: open a new PR with the correction (a follow-up file, e.g. `2026-05-15-og-mex-batteries-correction.md`). Or edit the original file directly on GitHub: navigate to it, click the pencil icon, edit, commit to a new branch, open another PR. Don't worry about overwriting. Git records every change.

**"I don't see my filename appear in the path breadcrumb."**
You're not inside `goodenough-feedback/sessions/` when clicking `Add file`. Navigate into the folder first, then click `Add file`. The filename box should pre-fill the path `nzipl-claude-kit / goodenough-feedback / sessions /` (or `<your-username> / nzipl-claude-kit / ...` if GitHub forked the repo for you).

**"The merge button is grey."**
If you're a collaborator, refresh the page. If still grey, the PR might be targeting the wrong base branch (should be `main`). If it's targeting `main` and still grey, message Gilberto. If you're NOT a collaborator, the merge button is grey by design — leave the PR open and Gilberto will merge during weekly triage.

**"git push asks for a password."**
GitHub deprecated password authentication in 2021. You need a personal access token (PAT) or SSH key. Easiest: install the GitHub CLI (`brew install gh` on macOS), run `gh auth login`, follow the prompts, and `git push` will then work.

---

## Quick glossary

For when you hit a term and want a one-line definition.

- **Repository (repo):** A folder of files tracked by git. The kit repo lives at https://github.com/Gilix/nzipl-claude-kit. The goodenough application repo is separate and private.
- **Clone:** Downloading a repo to your laptop, with full history, so you can edit it locally.
- **Fork:** Your own copy of a public repo on GitHub. Required to propose changes if you're not a collaborator. GitHub creates it for you automatically the first time you try to commit to someone else's repo.
- **Branch:** A named copy of the repo's files where you can make changes without affecting the main version. The default branch in nzipl-claude-kit is `main`.
- **Commit:** A saved snapshot of your changes, with a short message describing what you did.
- **Push:** Sending your local commits up to GitHub so others can see them.
- **Pull:** Downloading the latest changes from GitHub into your local repo.
- **Pull request (PR):** A request to merge a branch's changes into `main`, with a discussion thread attached. The unit of "I'd like to add this; please accept."
- **Merge:** Accepting a PR. The branch's changes become part of `main`.
- **Conflict:** When two branches both edited the same lines of the same file and git can't auto-pick. Rare for separate session files.

---

## Sanity check before you submit

A 30-second checklist:

- [ ] Filename matches `YYYY-MM-DD-yourtag.md` (today's date, lowercase, hyphens).
- [ ] File is inside `goodenough-feedback/sessions/`, not somewhere else.
- [ ] You included the `#share=` URL from goodenough so the goodenough author can replay your exact session.
- [ ] Each Fail or Partial rating has a concrete one-line note. "Felt off" is not actionable; "RCA 0.31 reported as 0.42" is.
- [ ] If you flagged a hallucination, you quoted the sentence verbatim.

You're good. Submit.
