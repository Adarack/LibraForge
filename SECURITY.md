# Security Policy

## Supported versions

LibraForge is in active development. Only the latest commit on `main` is supported.

## Reporting a vulnerability

Open a [GitHub issue](https://github.com/coconautilus17/LibraForge/issues) using the
**Bug report** template and mark it as security-related in the title. Do not include
private audiobook paths, Audible credentials, or auth files in the report.

For anything sensitive, email the maintainer directly (see the GitHub profile).

## Network exposure

LibraForge can write file metadata, move files, launch conversions, and access your
Audible account. **Do not expose it to an untrusted network.** Bind it to localhost
(the default) and access it through Tailscale, a VPN, or a reverse proxy with
authentication. Anyone who can reach the port can use every feature.

## What to redact before reporting

Logs and reports can contain local paths, library structure, and Audible account
identifiers. Before pasting anything publicly:

- Replace real paths with placeholders (`/audiobooks/...`)
- Remove auth file contents and Audible user IDs
- Remove hostnames and local usernames

## What we will never ask for

We will never ask for your Audible password, auth JSON, activation bytes, or voucher
files.
