# Repository transfer runbook

This runbook covers the one-time move from
`dev-ugurkontel/surface-audit` to `fillbyte/surface-audit`. It separates
changes that belong in the repository from account-level operations that
must be performed by an authorized maintainer.

Do not publish a release during the transfer. Complete the verification
checklist first, then publish a new patch version; never reuse an existing
PyPI version or immutable release tag.

## Verified pre-transfer state

As of 2026-08-30:

- the source repository is public and its default branch is `main`;
- the `fillbyte` organization has no repository named `surface-audit`;
- `dev-ugurkontel` is an organization owner and the repository owner;
- PyPI contains `surface-audit` 1.0.2, published with attestations from
  `dev-ugurkontel/surface-audit` and `.github/workflows/release.yml`;
- the current public container is
  `ghcr.io/dev-ugurkontel/surface-audit:latest`; and
- the future Pages URL, `https://fillbyte.github.io/surface-audit/`, is not
  live yet.

Recheck these facts immediately before the transfer. A stale snapshot is not
authorization to overwrite a repository or package.

## Transfer and repository verification

1. In GitHub repository settings, transfer the repository to `fillbyte`.
   Confirm the exact destination name is available before accepting.
2. Update local clones:

   ```bash
   git remote set-url origin https://github.com/fillbyte/surface-audit.git
   git remote -v
   ```

3. Verify the repository is still public and that Issues, Discussions,
   security advisories, Actions, and Pages have the intended settings.
4. Verify `dev-ugurkontel` has write access. CODEOWNERS entries only request
   reviews when the named owner has write access.
5. Inspect the `main` ruleset after transfer. Confirm the required Python
   matrix and build checks still match the current workflow check names,
   CODEOWNER review is required, and squash/linear-history policy remains in
   force.
6. Inspect the `pypi` and `github-pages` environments. Recreate any missing
   reviewer and deployment-branch policies before triggering workflows.
7. Update the repository homepage to
   `https://fillbyte.github.io/surface-audit/` after the Pages deployment
   succeeds.

GitHub redirects normal repository traffic after a transfer, but GitHub Pages
sites are not redirected. Existing users of the old Pages URL therefore need
the new URL explicitly.

## PyPI Trusted Publishing

Trusted Publisher identity is configured on PyPI, not in this repository.
Before the first post-transfer release, add this exact publisher to the
existing `surface-audit` PyPI project:

| Field | Value |
| --- | --- |
| Owner | `fillbyte` |
| Repository | `surface-audit` |
| Workflow | `release.yml` |
| Environment | `pypi` |

The release workflow grants `id-token: write` only to the PyPI publication
job and uses the protected `pypi` environment. Keep the old publisher until a
new release from `fillbyte/surface-audit` succeeds and its PyPI provenance is
verified. Remove the old publisher afterward to reduce the trusted identity
set.

Publish a new patch version such as 1.0.3 or later. PyPI versions are
immutable; 1.0.2 cannot be replaced.

## GitHub Pages

1. Confirm Pages uses GitHub Actions as its source.
2. Run the Pages workflow from the transferred repository.
3. Verify the landing page and every sample link under
   `https://fillbyte.github.io/surface-audit/`.
4. Verify the canonical and Open Graph URLs in the rendered page use the new
   organization namespace.

## GitHub Container Registry

Repository transfer does not move the existing personal GHCR package into the
organization namespace. The old image can remain available for compatibility,
but the next successful release must create and validate
`ghcr.io/fillbyte/surface-audit`.

After that release:

1. Confirm the organization permits package creation and that the image is
   public.
2. Link the package to `fillbyte/surface-audit` and verify repository access
   inheritance or explicit workflow access.
3. Pull both the exact version tag and `latest` from a logged-out client.
4. Verify the image source annotation points to the transferred repository and
   that provenance and SBOM attestations are present.

Do not delete the personal-namespace package as part of the transfer. That is
a separate, potentially breaking cleanup decision.

## First post-transfer release gate

Before tagging:

- all required checks pass from a pull request in the transferred repository;
- the PyPI Trusted Publisher tuple exactly matches the table above;
- environment approvals and branch policies are intact;
- Pages is live at the new URL; and
- GHCR organization package creation is allowed.

After tagging a new version, verify:

- the GitHub Release contains wheel, sdist, SBOM, and Sigstore bundles;
- PyPI shows the new files and provenance from `fillbyte/surface-audit`;
- GHCR exposes exact, major/minor, major, and `latest` tags under `fillbyte`;
- the moving `v1` action tag points to the new release commit; and
- `uses: fillbyte/surface-audit@v1` succeeds in a clean consumer repository.

## Primary references

- [GitHub: Transferring a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository)
- [GitHub: About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [GitHub: Package permissions and visibility](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages)
- [PyPI: Adding a Trusted Publisher](https://docs.pypi.org/trusted-publishers/adding-a-publisher/)
- [PyPI: Trusted Publisher security model](https://docs.pypi.org/trusted-publishers/security-model/)
- [PyPI: Troubleshooting Trusted Publishing](https://docs.pypi.org/trusted-publishers/troubleshooting/)
