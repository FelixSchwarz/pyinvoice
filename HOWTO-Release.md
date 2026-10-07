# Releases

Releases are built by the `Create Release Artifacts` workflow, not locally. It
runs the test suite against `uv.lock`, builds wheel and sdist with the
hash-pinned build backend from `build-constraints.txt`, builds the PyInstaller
executable from that wheel, attests the build provenance and attaches all
artifacts to a GitHub release. pyinvoice is not published on PyPI (the name
"pyinvoice" belongs to a different project there).

The `release` environment (repository settings → Environments) must require a
reviewer, otherwise GitHub creates it on the first run without any protection.

1. Optionally refresh pinned dependencies and tooling:

   ```console
   $ just update-dependencies
   $ just update-prek-hooks
   $ just update-workflow-actions
   ```

   `just update-dependencies` also regenerates `build-constraints.txt`.

2. Set the release version in `VERSION.txt` and commit it.

3. Push the tag to trigger the release workflow:

   ```console
   $ git tag "v$(cat VERSION.txt)"
   $ git push origin main "v$(cat VERSION.txt)"
   ```

4. Approve the deployment to the `release` environment in the workflow run.
   This publishes the GitHub release.

5. Set the next development version in `VERSION.txt` and commit it.

`just build` and `just build-executable` produce the same artifacts locally, for
example to test the packaging.

The provenance of a downloaded artifact can be verified with:

```console
$ gh attestation verify pyinvoice-*-linux-x86_64 --repo FelixSchwarz/pyinvoice
```
