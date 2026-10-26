# Setup Guide

Step-by-step instructions for getting the AI Job Search framework running.

## 1. Prerequisites

### Claude Code

Install Claude Code (Anthropic's CLI for Claude):

```bash
npm install -g @anthropic-ai/claude-code
```

You'll need an Anthropic API key or a Claude Pro/Team subscription. See the [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code) for details.

### Python

Python 3.10+ is required for the salary lookup tool. Check with:

```bash
python3 --version
```

On Windows, `py --version` is often the most reliable check. If your system exposes Python as `python` instead of `python3`, use `python` in the commands below.

### Bun (for job search tools)

The job portal CLIs (four Danish portals plus the country-agnostic `linkedin-search` and `freehire-search` tools) are written in TypeScript and run with Bun.

- macOS/Linux:

```bash
curl -fsSL https://bun.sh/install | bash
```

- Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://bun.sh/install.ps1 | iex"
```

If you prefer a package manager, `winget install Oven-sh.Bun` also works on Windows.

### Typst (for compiling CVs and cover letters)

The stock CV and cover letter templates are [Typst](https://typst.app/) files. Typst is a single binary with no extra packages to install:

- **macOS:** `brew install typst`
- **Windows:** `winget install --id Typst.Typst`
- **Linux:** `sudo snap install typst`, or `cargo install --locked typst-cli`, or a release binary from [github.com/typst/typst/releases](https://github.com/typst/typst/releases)

Check it works from the repo root:

```bash
typst --version
typst compile --font-path cover_letters/OpenFonts/fonts cv/main_example.typ
typst compile --font-path cover_letters/OpenFonts/fonts cover_letters/cover_example.typ
```

Both commands should finish without errors and leave `main_example.pdf` and `cover_example.pdf` next to their sources. The cover letter needs `--font-path` for the bundled Lato/Raleway fonts. A snap-installed Typst can only write inside your home directory, so keep the output inside the repo.

### Optional: ATS text extraction (pypdf, then pdftotext)

`/apply` runs an ATS parseability check on the compiled CV: it extracts the PDF's text layer and verifies contact details, reading order, and keyword coverage the way an applicant-tracking system sees them.

The default extractor is **pypdf** (BSD, `pip install pypdf`). Poppler `pdftotext` remains an optional fallback:

- **macOS:** `brew install poppler`
- **Debian/Ubuntu:** `sudo apt install poppler-utils`
- **Windows:** `choco install poppler`

If a command still uses `pdftotext -layout`, it must pass `-enc UTF-8` as well. If **neither** extractor is available, `/apply` skips the mechanical check with a warning and falls back to a visual keyword review — everything else works normally.

## 2. Fork and clone

```bash
gh repo fork ai-job-search-dev/ai-job-search --clone
cd ai-job-search
gh repo set-default <your-github-username>/ai-job-search
```

Or manually: fork on GitHub, then clone your fork.

> **The `set-default` line is not optional.** `gh repo fork --clone` sets the
> **upstream** repo as gh's default repository ("The `upstream` remote will be set as
> the default remote repository" — `gh repo fork --help`), and gh uses the default for
> **creating issues and PRs**. Without it, any later `gh issue create` run from this
> clone — by you or by an agent you have asked to track your applications — silently
> files on the upstream **public** tracker, publishing whatever the issue contains
> under your GitHub identity, on a repo where you cannot delete it (#389).

> **Before you go further: forks are public.** GitHub cannot make a fork of a public
> repository private, and `/setup` (section 6) writes your personal data into **tracked**
> files — pushing those commits to a fork publishes them. If this copy is for your own
> job search rather than for contributing, prefer a **private repository** with this repo
> as `upstream`: see section 8, step 1 for the exact commands and why committing your
> personalization there is still the right move. Everything else in this guide works
> identically either way.

## 3. Install job search CLI dependencies
Run these from the repository root.

```bash
python3 tools/install_portal_clis.py   # Windows: python tools\install_portal_clis.py
```

It runs `bun install` in every portal CLI under `.agents/skills/*/cli/` - discovered, not listed, so a portal you add with `/add-portal` or copy from another fork is included on a fresh clone. A CLI whose `package.json` declares an install-time lifecycle script is skipped and reported rather than run. `--dry-run` shows what it would install.

For `linkedin-search` and `freehire-search` the install is optional: both have zero runtime dependencies and run with plain `bun`; `bun install` only pulls TypeScript dev types.

If you're outside Denmark, you can generate an equivalent search skill for your local job board with `/add-portal` — it scaffolds the same CLI structure for any public portal and test-runs a live query before registering. See the "Job search tools" section in the README.

## 4. Run the setup interview

Start Claude Code in the repository:

```bash
claude
```

Then run the onboarding:

```
/setup
```

Claude will offer three paths:

- **Path A (documents folder):** Add your CV, LinkedIn export, diplomas, references, or past applications under `documents/`. Claude reads and cross-references them before proposing profile updates. This is best when you have several source files.
- **Path B (single CV import):** Share one CV/resume by mentioning the file with `@` or pasting the text. Claude extracts it and asks follow-up questions for anything missing.
- **Path C (interview mode):** Answer structured interview questions section by section.

All three paths produce the same result: fully populated profile files.

### What gets populated

| File | Content |
|------|---------|
| `CLAUDE.md` | Your full candidate profile |
| `01-candidate-profile.md` | Structured education, experience, skills |
| `02-behavioral-profile.md` | Behavioral assessment |
| `04-job-evaluation.md` | Personalized skill match areas and career goals |
| `05-cv-templates.md` | Profile statement templates for your background |
| `07-interview-prep.md` | STAR examples from your experience |
| `cv/main_example.typ` | Your Typst CV with actual details |
| `search-queries.md` | Job search queries for `/scrape` |

### Re-running setup

You can update specific sections later:

```
/setup --section skills
/setup --section experience
/setup --section search
```

The `--section search` option is especially useful as your priorities evolve. It re-runs the search configuration interview and suggests role types you may not have considered based on your full profile.

## 5. Optional: Set up salary benchmarking

If you have salary data (from a union, salary survey, Glassdoor, or personal research):

1. **Option A:** Create `salary_data.json` manually in the repo root (see `tools/README_SALARY_TOOL.md` for the format)
2. **Option B:** Convert from Excel:
   ```bash
   pip install openpyxl
   python3 tools/convert_salary_excel.py path/to/salary-data.xlsx --source "My Salary Data 2025"
   ```

This creates `salary_data.json` which the `/apply` workflow uses for salary benchmarking. If you skip this step, salary lookup is simply omitted.

## 6. Test the workflow

Find a job posting you're interested in, then:

```
/apply https://jobindex.dk/job/1234567
```

Or paste the job description directly:

```
/apply [paste job posting text here]
```

Claude will:
1. Evaluate the fit against your profile
2. Ask if you want to proceed
3. Draft a tailored CV and cover letter
4. Have a reviewer agent critique the drafts
5. Revise and present the final output

## 7. Compile your documents

After `/apply` creates the Typst files:

```bash
typst compile --font-path cover_letters/OpenFonts/fonts cv/main_<company>_<role>.typ
typst compile --font-path cover_letters/OpenFonts/fonts cover_letters/cover_<company>_<role>.typ
```

These commands apply to the stock Typst templates. If you'd rather use your own template (Typst, LaTeX, or another toolchain), run `/add-template` — it captures the template's compile command, fonts, style rules, and page limit, test-compiles it, and wires it into `/apply`. See the "Custom templates" section in the README.

## 8. Pulling upstream updates into your fork

Upstream keeps improving the methodology files your fork has personalized, so plan for updates from day one:

**Prefer releases over raw `master`.** Tagged [releases](../../releases) are vetted checkpoints, each described in [CHANGELOG.md](CHANGELOG.md). Updating to a tag pulls a stable, documented state instead of whatever `master` happens to be mid-review. Fetch tags with `git fetch upstream --tags` and merge a release (for example `git merge v1.0.0`) when you want stability; pull `master` directly only when you specifically want the latest unreleased changes. The steps below apply either way - substitute the release tag for `upstream/master` where you see it.

1. **Commit your personalization - but know where those commits land.** `/setup` edits CLAUDE.md and the profile skill files in place; those edits are *yours*, and committing them is what lets updates merge cleanly. But a GitHub **fork of this repo is public** - forks of public repositories cannot be made private - so anything you commit *and push to a fork* is visible to anyone. If you want your profile in a remote at all, don't push it to a fork: create a **private** repository, push there, and add this repo as the `upstream` remote (`git remote add upstream https://github.com/ai-job-search-dev/ai-job-search.git`) to keep receiving updates. Committing locally without pushing is also fine. The genuinely sensitive files (tracker, salary data, `documents/`, application archives) are gitignored and never enter git either way. An uncommitted working tree is the most common reason `git pull` refuses to merge at all (`Your local changes ... would be overwritten`).
2. **Preview what changed before pulling:**
   ```bash
   git remote add upstream https://github.com/ai-job-search-dev/ai-job-search.git   # first time only, if you cloned your own fork
   git fetch upstream    # or origin, if you cloned the template directly
   python3 tools/check_upstream_updates.py
   ```
   It compares the `framework_version` markers in your framework files against upstream and lists exactly which methodology files changed, with the diff command for each.

   Two tools answer two different questions, and it's worth running both:
   - **`check_upstream_updates.py`** — *which of my personalized files changed?* It reads the `framework_version` stamp on each methodology file, so it flags exactly the customized files a release touched.
   - **`upstream_triage.py`** — *which upstream commits deserve my attention?* It walks the commits you're behind and sorts them into "worth reviewing" vs "probably skip", dropping anything you've already cherry-picked (matched by `git patch-id`, so ported work falls off with no bookkeeping), commits that only touch files your fork removed, and SHAs you've listed in `.github/upstream-wontport.txt`. It's report-only — it prints ready-to-run `git cherry-pick` lines but never merges, pushes, or opens a PR, because on a fork "applies cleanly" isn't "correct".

     ```bash
     python3 tools/upstream_triage.py --remote upstream
     ```

     Forks also inherit a `.github/workflows/upstream-watch.yml` that runs this weekly and writes the result into a single rolling issue (it no-ops on the upstream template itself, and stays disabled on a fork until you enable Actions).
3. **Merge normally.** `git merge upstream/master` (or `git pull`) three-way-merges upstream's edits around your personalization; because methodology edits rarely touch the lines `/setup` filled in, most updates land cleanly. A conflict in a personalized file is a *feature*, not a failure — it means upstream changed methodology in a section you customized, and the version marker plus its changelog commit tell you why. Resolve by keeping your data and adopting the methodology change around it.

## Troubleshooting

### "salary_data.json not found"
This is expected if you haven't set up salary benchmarking. The `/apply` workflow skips this step automatically.

### Job search CLI tools not working
Make sure Bun is installed and you ran `bun install` in each CLI directory. The tools require network access to fetch job listings.

### Typst compilation errors
- Read the error's file/line/column: Typst points at the exact character
- `label ... does not exist`: an unescaped `@` (write `\@`; see "Typst Special Characters" in `05-cv-templates.md`)
- `unclosed delimiter` or `unexpected closing bracket`: unbalanced `[` / `]` in a content block
- `error: failed to write PDF file`: a snap-installed Typst cannot write outside your home directory

### Fonts not found in cover letter
The cover letter template expects fonts in `cover_letters/OpenFonts/fonts/`. Make sure this directory exists and contains the Lato and Raleway font files.

### Stale `.claude/settings.local.json` from an older clone
Shared Claude Code permissions now live in `.claude/settings.json`: an `allow` list scoped to the exact commands the workflow runs (each portal CLI by path, the `tools/` scripts, `salary_lookup.py`, `pdftotext`), an `ask` list that always prompts before the permission-defining files are edited or `git push` runs, and a `deny` list that blocks upload-shaped shell and reads of credential files in every mode. `SECURITY.md` has the full table. Earlier versions of this repo committed a broader `.claude/settings.local.json` that pre-approved `Bash(curl:*)`, `Bash(python:*)` and `Bash(bun:*)`. If you cloned before that change, git leaves the old file behind in your working copy, and its permissions still apply on top of `settings.json`. Delete it (or trim it to your own personal overrides):

```bash
rm .claude/settings.local.json
```
