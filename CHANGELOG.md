# Changelog

All notable changes. No tagged releases yet - tracking by PR.

---

## Unreleased

### 2026-06-22 (PR #21-22)
- Organizer: trusted-first title pipeline, folder-level sidecar discovery, consistent
  directory display, fix false duplicate-source warning, re-caching phase announcement
- Docs: replace all em dashes in README

### 2026-06-21 (PR #14-20)
- Forge: scan button beside browse field, persistent skip patterns (survive restarts),
  flag cluster cleanup, clearer force controls, action guide, auto-backup toggle
- Fixer: smart-skip count surfaced in summary and UI; smart-skip labelled explicitly
  in dry-run and apply output
- Sidecar: unified `.libraforge.json` per book (replaces separate fixer/organizer sidecars)
- Progress: fix progress counters, fixer PermissionError on read-only metadata.json,
  scan already-processed detection
- Install: zero-config first boot, `make up` one-command setup, `Makefile` with
  `up/down/logs/restart/rebuild/test` targets

### 2026-06-21 (PR #12-13)
- Fixer: scoring overhaul, always-on `metadata.json` export, report categories
  (exact/fill/smart-skip/manual-review), publisher policy (`publishers.default.json`,
  local override)
- Forge: browse and scan loose folders, compare-panel duration row, fill-category labels

### 2026-06-20 (PR #9-11)
- Library Downloader: browse Audible library, download AAX/AAXC purchases to M4B with
  chapters, embedded cover, and ASIN; optional post-download organize
- Accounts: multi-account Audible auth, account switcher, rename, switch, disconnect/
  deregister, retry/delete-anyway on deregister failure
- Providers: Audiobookshelf and abs-agg as metadata providers for batch runs and
  Manual Review; provider setup on Accounts page

### 2026-06-18-19 (PR #3-8)
- Smart scan cache (1hr TTL + fingerprint), larger covers, book list with organized
  category
- Smart write diff, write modes (`smart`/`fill-missing`/`overwrite`), ASIN embedding
  and extraction (fixer v5)
- Horizontal site nav, page descriptors, Start Here landing page with folder scan and
  NAS path support
- Studio exclusions, genre subtitle preservation, false-positive book-number review fix

### 2026-06-17 (PR #2)
- Fix CI test failures: env vars, import errors, stale script refs
- Organizer metadata review improvements

### 2026-06-16 (initial release)
- Initial public release: Metadata Forge, M4B Tool, Folder Forge, Docker setup,
  MIT license, CI, health endpoint, dry-run-first defaults
