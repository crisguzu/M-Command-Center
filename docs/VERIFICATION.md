# Verification, reproduction and open gates

This is the public read-only MCC edition, not the private Work Engine. Application source baseline: b9766ea11d783c4c50261425f271991c0327e5d2. The steps 1â2 review changes documentation/presentation only; do not treat a PR or this document as an accepted deployment.

## What was observed

- Exact-source public CI completed successfully on Linux/Python 3.12: [run 42938749317](https://github.com/crisguzu/M-Command-Center/actions/runs/42938749317). The checked-in workflow runs python -m unittest discover -s tests -v, then installs the package and checks mcc --help. CI success is separate from local/browser evidence.
- On 2026-11-10, Linux arm64/Python 3.11.2: python3 -m unittest discover -s tests -p test_accounting.py -v passed 10 tests. Fresh python3 -m mcc.cli --config-dir NEW_CONFIG --data-dir NEW_DATA init --demo succeeded, produced 3 fictional projects and a 0600 auth-token file. These narrow observations do not certify full arm64/Python3.11 compatibility.
- A full local test-discovery attempt reached its 23-second subprocess deadline. It is not a passing full-suite rerun; the timeout alone does not diagnose a functional defect. Rerun the full suite on the documented Linux x86_64/Python 3.12 platform with a reviewed sufficient wall limit.
- Prior accepted platform: Linux x86_64 (WSL), Python 3.12.3 and Chromium desktop/mobile emulation. Current screenshots were captured from the actual authenticated public viewer and unchanged bundled demo() data in Chromium 134.0.6998.35 at 1440x1000 and 390x844. No page-initiated external requests or JavaScript errors were observed. Its disposable fixture and RAM scratch were removed. See [screenshot provenance](screenshots/README.md).

## Reproduce safely

From a fresh reviewed checkout, in a dedicated environment:

~~~sh
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/mcc --config-dir "$HOME/.config/mcc-review-demo" --data-dir "$HOME/.local/share/mcc-review-demo" init --demo
.venv/bin/mcc --config-dir "$HOME/.config/mcc-review-demo" --data-dir "$HOME/.local/share/mcc-review-demo" serve
~~~

The config/data paths must be NEW dedicated directories, not existing user or owner stores. Stop rather than remove/reinitialize a conflicting root. Expected outputs are a successful install, actual unittest count plus OK, successful initialization, and the loopback viewer address. Read the protected token locally and enter it in the unlock form; do not print it into reports, URLs or screenshots. Confirm 3 fictional projects; stop with Ctrl-C. No Gateway or private credentials are required. No secret should be embedded in the commands.

Critical negative-test entry points: tests/test_mcc.py covers exact Host/Origin, authentication, mutation denial, malformed framing, concurrency and deadlines; tests/test_bridge.py covers selected import/backup/digest boundaries; tests/test_owner.py covers invalidated authorizations, rejection/retry, corruption, interrupted receipts, projection isolation and recovery. tests/test_accounting.py is a synthetic file normalizer test, not live token capture.

## Public-history review

On 2026-11-10 all 10 non-HEAD refs advertised by git ls-remote were fetched into a disposable isolated bare store: 5 branch refs and 5 PR refs, including the PR merge ref. Scan coverage was 20 commits, 87 blobs, 538215 bytes. Tested credential formats, private-locator and personal-mail patterns produced zero findings. The temporary store was removed. [Machine-readable ref manifest](reviews/2026-11-10-public-history.json).

This closes the earlier unscanned-advertised-ref coverage gap only for the recorded refs/hashes and tested patterns. It is not proof that every possible secret, sensitive binary, unadvertised/dangling object or legal issue is absent. New refs require fresh review. No refs were deleted or rewritten.

## Permissions and maturity still open

Owner-authorized repository use of the concept illustration is recorded in PROVENANCE.md, but its upstream authorship/rights chain has not been independently established. This remains an OPEN permission-evidence gate. The illustration is linked separately rather than leading the README, and is excluded from MIT. Moving it does not erase existing history or resolve rights. Supply creation/source-and-license evidence or separately approve a reviewed removal/replacement; do not call this gate passed.

Same-UID processes are outside the authentication boundary. Human review in optional owner records is procedural, not cryptographic reviewer identity. Reverse-proxy/remote hosting, live Gateway/model/channel adherence, native Windows/macOS, WebKit and physical Safari remain unverified. No production-security certification or workload benchmark is claimed. The owner-record writer fsyncs file and directory; the v1 snapshot helper does not establish power-loss durability. See SECURITY.md and the architecture trust boundaries.

## Persistence failure tests (steps 3–4 review)

Five new tests in tests/test_persistence.py pass on Linux arm64/Python 3.11.2. They cover successful replacement/mode 0600, injected file-fsync and rename failures preserving the prior snapshot, refusal to clobber an existing temporary file and the current file-only fsync boundary. These are injected syscall failures, NOT physical power-loss or directory-durability certification. No production writer behavior is changed.

The supported Linux/Python 3.12 full-suite rerun must use a complete checkout, including examples/ and onboarding/. Two partial-workspace runs executed 58 tests but failed on absent harness files; they do not diagnose an application defect and are not claimed as passing. Further partial-workspace retries were stopped; the complete GitHub CI checkout is the release check.
