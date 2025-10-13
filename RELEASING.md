# Release Process

This document describes the release process for the Invoice Manager application.

## Version Management

This project uses a **monorepo versioning strategy** where all services (UI, Server, ML Server) share the same version number. The version is tracked in multiple places:

- `VERSION` - Single source of truth for the version number
- `ui/package.json` - UI package version
- `server/pyproject.toml` - Server package version
- `ml-server/pyproject.toml` - ML Server package version

## Semantic Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version (X.0.0): Incompatible API changes
- **MINOR** version (0.X.0): New functionality in a backwards-compatible manner
- **PATCH** version (0.0.X): Backwards-compatible bug fixes

## Release Workflow

### 1. Prepare for Release

Ensure all changes for the release are merged to the `main` branch:

```bash
git checkout main
git pull origin main
```

### 2. Update Changelog

Edit `CHANGELOG.md` to move items from `[Unreleased]` to a new version section:

```markdown
## [Unreleased]

## [1.1.0] - 2025-10-13

### Added
- New feature description

### Changed
- Changed feature description

### Fixed
- Bug fix description
```

### 3. Bump Version

Use the Makefile targets to bump the version. This will:
- Update the VERSION file
- Update all package.json and pyproject.toml files
- Update CHANGELOG.md
- Create a git commit

#### For a patch release (bug fixes):
```bash
make version-bump-patch
```

#### For a minor release (new features):
```bash
make version-bump-minor
```

#### For a major release (breaking changes):
```bash
make version-bump-major
```

Alternatively, you can use commitizen directly:
```bash
uvx --with commitizen cz bump
```

### 4. Push Changes

Push the version bump commit:
```bash
git push origin main
```

### 5. Create and Push Git Tag

Create and push the git tag to trigger the release:

```bash
# Create the tag
make version-tag

# Or manually:
git tag -a "v1.1.0" -m "Release version 1.1.0"

# Push the tag
git push origin v1.1.0
```

### 6. Automated Release Process

Once the tag is pushed, the following happens automatically:

1. **GitHub Release Workflow** (`.github/workflows/release.yml`):
   - Creates a GitHub Release with changelog notes
   - Marks the release as published

2. **CD Workflow** (`.github/workflows/cd.yml`):
   - Builds Docker images for all services (UI, Server, ML Server)
   - Tags images with:
     - Version tag (e.g., `v1.1.0`)
     - Major.minor tag (e.g., `1.1`)
     - Semantic version (e.g., `1.1.0`)
     - Git SHA
     - `latest` (for main branch)
   - Pushes images to GitHub Container Registry (ghcr.io)

3. **Deployment**:
   - Pull the new tagged images on your server
   - Update docker-compose.yml to use the new version
   - Restart services

### 7. Deploy to Production

SSH into your production server and update the deployment:

```bash
# Pull latest images
docker compose -f docker-compose.yml -f docker-compose.prod.yml pull

# Restart services with new version
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Or use make target
make prod-up
```

### 8. Verify Deployment

Check that the new version is running:

```bash
# Check server version
curl https://api.myinvoicemanager.pro/health

# Check ML server version
curl https://api.myinvoicemanager.pro/ml/health

# Check UI version (if you add version display)
curl https://app.myinvoicemanager.pro
```

## Version Checking

You can check the current version at any time:

```bash
# Check VERSION file
make version-current

# Or directly
cat VERSION
```

## Rollback Procedure

If a release has issues:

### 1. Quick Rollback (Recommended)

Deploy the previous version by updating docker-compose.prod.yml:

```yaml
services:
  server:
    image: ghcr.io/jeremyarancio/invoice-reader-app-server:v1.0.0  # Previous version

  ml-server:
    image: ghcr.io/jeremyarancio/invoice-reader-app-ml-server:v1.0.0

  ui:
    image: ghcr.io/jeremyarancio/invoice-reader-app-ui:v1.0.0
```

Then restart:
```bash
make prod-up
```

### 2. Revert Git Changes

If needed, revert the version bump commit:

```bash
git revert <commit-hash>
git push origin main
```

## Hotfix Process

For urgent production fixes:

1. Create a hotfix branch from the tag:
   ```bash
   git checkout -b hotfix/v1.0.1 v1.0.0
   ```

2. Make the fix and commit

3. Bump patch version:
   ```bash
   make version-bump-patch
   ```

4. Merge to main:
   ```bash
   git checkout main
   git merge hotfix/v1.0.1
   git push origin main
   ```

5. Create and push the tag:
   ```bash
   make version-tag
   git push origin v1.0.1
   ```

## Release Checklist

- [ ] All tests passing in CI
- [ ] CHANGELOG.md updated with release notes
- [ ] Version bumped using make targets or commitizen
- [ ] Changes pushed to main branch
- [ ] Git tag created and pushed
- [ ] GitHub release created automatically
- [ ] Docker images built and pushed to registry
- [ ] Production deployment updated
- [ ] Health endpoints verified
- [ ] Monitoring dashboards checked for errors

## Monitoring Releases

After deployment, monitor:

- **Grafana Dashboard**: https://monitor.myinvoicemanager.pro
- **Server logs**: `docker compose logs -f server`
- **ML Server logs**: `docker compose logs -f ml-server`
- **Error rates** in Prometheus metrics
- **User reports** via GitHub Issues

## Questions?

For questions about the release process, contact the maintainer or open an issue in the GitHub repository.
