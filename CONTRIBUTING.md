# Contributing

## Running tests

Run tests inside the container where all dependencies are installed:

```bash
make test
```

Or directly:

```bash
docker compose exec libraforge python -m unittest discover -s app/tests -t . -p "test_*.py" -v
```

Tests must pass before opening a PR. The CI workflow runs the same command.

## Branch naming

```
feat/<short-description>
fix/<short-description>
chore/<short-description>
```

Branch from `main`. Open a PR when ready; CI must be green before merging.

## What not to commit

- Reports, caches, or metadata sidecars from real runs (`app/reports/`, `*.libraforge.json`)
- Auth files or Audible credentials (`audible-metadata.json`, `/auth/accounts/`)
- `.env` (use `.env.example` as the template)
- Private notes, local paths, or archive content
- Real audiobook files or cover art

The `.gitignore` covers most of these; double-check `git status` before committing.

## Code guidelines

- All metadata and organizer operations must default to dry-run.
- Do not apply test operations to `/audiobooks`; use `/tmp` targets.
- Preserve existing DOM IDs unless the corresponding JavaScript and tests are updated
  together.
- Add regression tests for changes to metadata matching, organizer planning, M4B
  grouping, or report parsing logic.
- Prefer small, reviewable PRs over large batches.
- Do not add a frontend framework without a concrete need.

## Adding a script version

The active scripts are selected by `default_fixer_script()` (alphabetically latest).
Do not promote experimental scripts to the maintained path until they are stable and
tested end-to-end.
