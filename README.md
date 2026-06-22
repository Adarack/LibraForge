# LibraForge — Prebuilt Docker Image

Automated GHCR build of [coconautilus17/LibraForge](https://github.com/coconautilus17/LibraForge). All credit to the original author.

A GitHub Actions workflow checks upstream daily, builds when there are new commits, and pushes to:

```
ghcr.io/adarack/libraforge:latest
ghcr.io/adarack/libraforge:sha-<short>
ghcr.io/adarack/libraforge:<YYYYMMDD>
```
