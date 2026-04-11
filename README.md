# Conventional Commits for Software Citation
### Flash Talk — Software Citation Workshop, UCSD 2026

This repository is the live demo companion for a 10-minute flash talk arguing that
Conventional Commits, combined with Semantic Versioning and automated release tooling,
give research software a lightweight but rigorous versioning discipline — one that makes
software directly citable, with human-readable changelogs that describe exactly what
differs between versions.

---

## Part 1: Concepts

### 1. Atomic Commits

An atomic commit captures exactly one logical change. Not one file, not one session —
one *idea*. The test is: can you describe what this commit does in a single sentence
without using "and"? If not, it should be two commits.

Atomic commits matter for citation because they make the history auditable. A reader
can check out any point in the history and understand what the software was doing at
that moment, with no ambiguity about whether an unrelated change snuck in.

**In practice:** during a work session you commit freely and messily. Before pushing,
you clean up with an interactive rebase (`git rebase -i HEAD~N`) — squashing half-steps,
splitting mixed commits, rewriting messages. The public history looks intentional because
you made it so after the fact.

### 2. Conventional Commits

Conventional Commits is a lightweight specification for commit message structure:

```
<type>[optional scope]: <short description>

[optional body]

[optional footer(s)]
```

**Types and their meaning:**

| Type | What it means | Semver impact |
|---|---|---|
| `fix` | A bug fix visible to users | Patch bump |
| `feat` | A new user-facing feature | Minor bump |
| `feat!` or `BREAKING CHANGE:` footer | Incompatible API change | Major bump |
| `docs` | Documentation only | No bump |
| `refactor` | Internal restructure, no behavior change | No bump |
| `test` | Adding or fixing tests | No bump |
| `chore` | Build process, tooling, config | No bump |
| `perf` | Performance improvement | No bump |
| `ci` | CI/CD pipeline changes | No bump |

A breaking change can be signaled either by appending `!` to the type
(`feat!: rename API keys`) or by including a `BREAKING CHANGE:` line in the commit
footer. Both trigger a major version bump in automated tooling.

**Full example:**
```
feat!: restructure author fields to support multiple authors

Replace the flat 'author_last'/'author_first' keys with an 'authors'
list of {'last', 'first'} dicts. All three formatters updated accordingly.

BREAKING CHANGE: 'author_last' and 'author_first' keys are removed.
Callers must migrate to authors=[{"last": ..., "first": ...}].
```

### 3. Semantic Versioning (SemVer)

Semantic Versioning encodes meaning directly into version numbers using the
format `MAJOR.MINOR.PATCH`:

- **PATCH** (`0.0.x`): backwards-compatible bug fixes
- **MINOR** (`0.x.0`): backwards-compatible new functionality; resets PATCH to 0
- **MAJOR** (`x.0.0`): incompatible API changes; resets MINOR and PATCH to 0

Versions below `1.0.0` (i.e. `0.x.y`) are considered unstable — anything may change
at any time. The `1.0.0` release signals a stable public API.

Conventional Commits map directly onto SemVer decisions. This is not coincidental —
the two specifications were designed together. The key insight is that the person
writing the commit message is making a versioning decision in real time, at the moment
they understand the change best.

**This commit chain in this repo resolves to v1.0.0:**

```
fix: strip whitespace from BibTeX citation keys          → would be 0.0.1
feat: add format_mla formatter for MLA 9th edition       → would be 0.1.0
feat: add volume, number, and pages fields to BibTeX     → would be 0.2.0
chore: add .gitignore for Python build artifacts         → no bump
feat!: restructure author fields to support multiple...  → 1.0.0  ← MAJOR
```

### 4. The Recommended Workflow

```
Work session
    │
    ▼
Commit freely (messy, incremental)
    │
    ▼
git rebase -i HEAD~N   ← clean up: squash, split, reword
    │
    ▼
Conventional Commit messages on each atomic commit
    │
    ▼
git push to main
    │
    ▼
GitHub Action (release-please) fires automatically
    │
    ▼
Release PR opened with CHANGELOG.md + version bump in pyproject.toml
    │
    ▼
Maintainer reviews and merges
    │
    ▼
GitHub Release created at the new tag → citable version
```

### 5. release-please

[release-please](https://github.com/googleapis/release-please) is a Google-maintained
tool that automates the release lifecycle by parsing Conventional Commits. It runs as
a GitHub Action and:

1. Watches every push to `main`
2. Opens a "Release PR" proposing the next version and a fully generated `CHANGELOG.md`
3. Keeps the PR updated as new commits land (without creating noise)
4. When the PR is merged: creates a git tag and a GitHub Release

The changelog it generates is grouped by type (Breaking Changes, Features, Bug Fixes)
and links each entry back to its commit. This is the artifact that makes a version
citable with a clear, human-readable description of what changed.

**Other tools in this space:**
- `git-cliff` — Rust-based, highly configurable, runs as CLI or Action; good for offline demos
- `semantic-release` — fully automated (no PR step), more common in JavaScript ecosystems
- `conventional-changelog` — the original Node.js CLI tool, useful for scripted pipelines

---

## Part 2: Slide-by-Slide Talk Plan

**Total time: 10 minutes | Format: flash talk with live demo**

---

### Slide 1 — Title (0:00–0:30)

**Title:** "Version numbers that mean something: Conventional Commits for research software"

**Speaker note:** One sentence setup: "I want to show you a Git workflow that takes 10
minutes to set up and gives you software citations with meaningful, auto-generated changelogs."

---

### Slide 2 — The citation problem (0:30–1:30)

**Content:**
- "Please cite this software" → which version?
- Two versions of the same tool, different results — which commit introduced the change?
- DOIs exist, but they don't tell you *what changed*

**Visual:** Two version tags (`v0.2.0` vs `v1.0.0`) with a question mark between them.

**Speaker note:** Frame the gap: we have DOIs for versions, but the story between versions
lives in commit messages that are usually noise ("fix", "wip", "asdf"). The changelog is
the missing piece.

---

### Slide 3 — Atomic commits (1:30–2:30)

**Content:**
- One commit = one logical change
- The test: describe it in one sentence, no "and"
- Messy during work sessions → clean before pushing with `git rebase -i`

**Visual:** Before/after of a messy local history rebased into three clean commits.

**Speaker note:** Emphasize that this is a discipline about *publishing* history, not
about how you work. You can still commit freely during a session.

---

### Slide 4 — Conventional Commits format (2:30–4:00)

**Content:**
```
<type>[scope]: <description>

[body]

[footer]
```
Types: `fix`, `feat`, `feat!` / `BREAKING CHANGE:`, `docs`, `chore`, `refactor`...

**Visual:** Annotated commit message with each part labeled.

**Speaker note:** Show a real example from the demo repo. Point out that the type is a
*decision*, not a description — you are declaring the intent and impact of the change.

---

### Slide 5 — SemVer in one slide (4:00–4:45)

**Content:**
```
MAJOR . MINOR . PATCH
  │       │       └─ fix:   backwards-compatible bug fix
  │       └───────── feat:  backwards-compatible new feature
  └───────────────── feat!: breaking API change
```

**Visual:** The version number with arrows pointing to the commit types that drive each digit.

**Speaker note:** The key insight: Conventional Commits and SemVer were co-designed.
Writing the commit type IS making the versioning decision, at the moment you best understand the change.

---

### Slide 6 — The full workflow (4:45–5:30)

**Content:** The pipeline diagram:
`commit → rebase → push → Action fires → Release PR → merge → GitHub Release`

**Visual:** Linear flowchart, highlight the automated section in a different color.

**Speaker note:** Everything after `push` is automated. The human decision is in the
commit message. That's the only place where judgment is required.

---

### Slide 7 — LIVE DEMO: the commit history (5:30–6:30)

**Action:** In terminal, run:
```bash
git log --oneline
```

**What to show:** The five-commit chain in this repo. Walk through each one:
- `fix:` → patch
- two `feat:` → minor, minor
- `chore:` → no bump ("notice this one doesn't affect the version")
- `feat!:` + `BREAKING CHANGE:` footer → major

**Speaker note:** "The machine can read this log and make all the version decisions
automatically — because we wrote the messages with that in mind."

---

### Slide 8 — LIVE DEMO: the Release PR (6:30–8:00)

**Action:** Open GitHub in browser → show the Release PR opened by release-please.

**What to point out:**
1. The PR title: "chore(main): release 1.0.0"
2. The `CHANGELOG.md` diff in the PR — grouped by Breaking Changes / Features / Bug Fixes
3. The `pyproject.toml` version bump from `0.0.0` to `1.0.0`
4. Every changelog entry links back to its commit SHA

**Speaker note:** "This PR was opened automatically, seconds after I pushed. I didn't
write a word of this changelog." If the release is already merged, show the GitHub
Release page instead — same content, now tagged and citable.

---

### Slide 9 — LIVE DEMO: the GitHub Release (8:00–8:45)

**Action:** Navigate to `github.com/LucasMDeSa/conv_commits_ucsd2026/releases`

**What to show:** The v1.0.0 release with the generated changelog, git tag, and the
option to attach build artifacts (wheel, tarball) for archiving.

**Speaker note:** "This is your citable unit. Tag it with Zenodo, get a DOI, and the
changelog tells anyone exactly what v1.0.0 is and how it differs from whatever came before."

---

### Slide 10 — Why this matters for citation (8:45–9:30)

**Content:**
- Version = DOI-able, archivable snapshot
- Changelog = human-readable diff between versions (generated, not written)
- Commit history = machine-readable audit trail
- `BREAKING CHANGE:` = a flag that results may not reproduce across versions

**Visual:** The CITATION.cff or Zenodo badge alongside the CHANGELOG excerpt.

**Speaker note:** "If a paper cites v0.2.0 and a reader tries to reproduce with v1.0.0,
the breaking change entry in the changelog tells them exactly why their results differ
and what they need to change."

---

### Slide 11 — Takeaways + resources (9:30–10:00)

**Content:**
- Conventional Commits spec: `conventionalcommits.org`
- SemVer spec: `semver.org`
- release-please: `github.com/googleapis/release-please`
- This demo repo: `github.com/LucasMDeSa/conv_commits_ucsd2026`
- Setup cost: ~15 minutes for an existing repo

**Speaker note:** "The workflow asks for one extra thought per commit. In exchange you
get a changelog, a version history, and citable releases — for free."

---

## Demo Repository Commit History

```
5207cda chore: initial project scaffold
a196614 fix: strip whitespace from BibTeX citation keys
aac8319 feat: add format_mla formatter for MLA 9th edition
7438a85 feat: add volume, number, and pages fields to BibTeX output
f043d9c chore: add .gitignore for Python build artifacts
d8c0364 feat!: restructure author fields to support multiple authors
b95efe4 chore: add release-please GitHub Action
```

The commit chain above produces a v1.0.0 release with a three-section changelog
(Breaking Changes, Features, Bug Fixes), demonstrating the full SemVer range from
a single short development sequence.
