# Conventional Commits for Software Citation
### Flash Talk — Software Citation Workshop, UCSD 2026

This repository is the live demo companion for a 10-minute talk given during the Software Citation Workshop at UCSD, 2026.
---

## Part 1: Concepts

### 1. Atomic Commits

An atomic commit captures exactly one logical change. It should consist in an irreducible change that works on its own, and can be described in one line. This has the adde benefit of producing a clear, readable log, and easily reversible commits.

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