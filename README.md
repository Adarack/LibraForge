# LibraForge

> **Note:** This tool is in active development. Features and interfaces may change.

Self-hosted Audible metadata matching, M4B conversion, Audiobookshelf-style library
organisation, and direct Audible downloading — four tools in one Docker container, with
a vanilla-JS web UI. Every write operation defaults to a dry run.

---

## Features

### Start Here (`/`)
Pick a folder and get a one-glance scan summary: how many books need metadata, need
conversion, and are ready to organise. Links through to the right tool for each stage.

### Metadata Forge (`/forge`)
Searches Audible (or another provider) and writes matched metadata to your files.

- **Dry-run first**, then enable **Apply** to write. **Backup and cache** on the first
  apply preserves originals and speeds up later runs.
- **Concurrent workers** (v5): parallel Audible search with a per-thread client pool,
  per-query de-duplication, and a persistent chapter-count cache that makes repeat
  discovery near-instant.
- **Write modes:** `smart` (skip the write when embedded tags already match),
  `fill-missing` (only write currently-empty fields), `overwrite` (always write).
- **ASIN aware:** the matched ASIN is embedded in every file; if a file already carries
  an ASIN (tags or `[B0XXXXXXXX]` in the name) it is looked up directly first, and an
  ASIN mismatch flags the book for manual review.
- **Manual Review:** load any book or folder, search Audible manually, and apply per
  book with an explicit `Full metadata` or `Series only` mode.
- **Providers:** Audible (direct), **Audiobookshelf** (via its own search API), and
  **abs-agg** (LibriVox, Storytel, BookBeat, Big Finish, and others).

### M4B Tool (`/m4b-tool`)
Converts or merges audio into a single M4B. Loads existing fixer sidecars automatically,
scans for multipart / non-M4B conversion candidates, and exposes codec, bitrate, and job
count. `No conversion` is safe only when all source streams are AAC with matching sample
rate and channel layout.

### Folder Forge (`/organizer`)
Plans and applies `Author/Series/Book N - Title` destination moves with a dry-run
preview and structured review reasons. **Index library and exit** rebuilds the
destination-structure cache on its own.

### Library Downloader (`/library`)
Browse your Audible library and download purchases straight into a mounted folder,
decrypted to standard **M4B** with chapters, metadata, embedded cover, and ASIN intact —
no external tooling. Supports AAX (`activation_bytes`) and AAXC (per-file voucher).
Books already in your library are flagged as **Owned**; a per-run or per-book rule
controls duplicate handling (Keep both / Replace), and an optional pass auto-organises
the downloads when finished.

### Accounts (`/auth-setup`)
Guided Audible OAuth sign-in — no CLI tools. Connect **multiple accounts**, each with a
recognisable name, and **switch between them in one click**, rename them, or **disconnect**
cleanly (deregisters the device with Audible, then removes the login; offers retry or
local-only delete if Audible is unreachable). The active account is shared by every tool.
This page also configures the Audiobookshelf and abs-agg providers.

### Planned
- Local agent advisory review (read-only LLM suggestions, no automatic writes).
- Chapter detection via speech recognition before M4B conversion.
- Unraid Community Apps package.

---

## Install

```bash
cp .env.example .env
```

Edit `.env`:

```dotenv
UID=1000
GID=1000
AUDIOBOOKS_PATH=/path/to/audiobooks
AUDIBLE_AUTH_PATH=/path/to/audible-auth
```

```bash
docker compose up -d --build
```

LibraForge listens on `127.0.0.1:5056`. For HTTPS, attach to your reverse proxy network
via `docker-compose.override.yml` (git-ignored). Connect an Audible account from the
**Accounts** page, or skip Audible and use Audiobookshelf / abs-agg as providers.

### Optional companion services

| Service | Purpose | Required? |
|---|---|---|
| [Audiobookshelf](https://www.audiobookshelf.org/) | Metadata provider via ABS's built-in search API. Create a dedicated API key in ABS Settings → Users → API Keys and add it on the Accounts page. | No |
| [abs-agg](https://github.com/Vito0912/abs-agg) | Aggregates metadata from LibriVox, Storytel, BookBeat, Big Finish, and others. Deploy on the same Docker network; set the URL in provider settings. | No |

---

## Container paths

| Purpose | Path |
|---|---|
| Audiobook library | `/audiobooks` |
| Audible auth directory | `/auth` — active account `/auth/audible-metadata.json`; saved accounts `/auth/accounts/` |
| Scripts | `/app/scripts` |
| Reports and caches | `/app/reports` |

## Safety

- All operations default to dry-run. Review before applying, and back up media before
  the first write.
- A dedicated, empty Audible account is recommended for metadata lookups; use a
  real-library account for the downloader.
- The `/auth` directory is mounted **read-write** so the app can add, switch, and
  disconnect accounts. Point `AUDIBLE_AUTH_PATH` at a dedicated directory — not your
  primary audible-cli config — and keep it off untrusted networks.
- Do not expose LibraForge to an untrusted network. Access control is host-level only;
  anyone who can reach the port can use it.

## Development

```bash
# Run tests
python3 -m unittest discover -s app/tests -v

# Restart after backend (app/main.py) changes
docker compose restart libraforge

# Rebuild after Dockerfile or dependency changes
docker compose up -d --build
```

Static files (`app/static`, `scripts/`) are bind-mounted — HTML, CSS, and JS edits are
live without a restart.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for dependency licence information.
