# Architecture and implementation boundaries

The diagram describes implemented public code, not a private installation.

- **Explicit intake CLI** — `mcc/cli.py`, `mcc/model.py`, `mcc/fs.py`: validate a selected neutral snapshot; write only dedicated owner-controlled roots.
- **Optional OpenClaw file bridge** — `mcc/bridge.py`, `docs/openclaw.md`: explicitly refresh selected records; no automatic agent dispatch.
- **Optional owner records** — `mcc/owner.py`, `contracts/v2/README.md`: versioned project/task records, attempts, evidence and procedural review decisions.
- **Snapshot projection** — `mcc/owner.py`, `mcc/model.py`: derived viewer data, not a replacement for canonical owner history.
- **Local server** — `mcc/server.py`: loopback IPv4, token login, in-memory sessions and browser-origin checks.
- **Browser UI** — `mcc/static/`: read-only project and task-history presentation.

## Trust boundaries

Selected records may contain sensitive text; validation is not redaction. Same-UID local processes are outside the authentication boundary. Human review is procedural, not cryptographic identity. The viewer does not run shell commands, models, workers or hardware. Remote hosting/reverse proxies are unsupported. V2 owner history and v1 snapshot-only roots have different backup requirements; see the README.

The original architecture diagram follows the repository MIT code/documentation license. The separately supplied concept artwork retains its existing exclusion.

## Decisions and tradeoffs

- **Loopback and read-only UI over remote convenience:** mcc/server.py binds IPv4 loopback, checks exact Host/Origin, and exposes no task execution. This reduces authority and ingress scope; reverse proxies and same-UID adversaries are not supported security boundaries.
- **Strict selected contracts over automatic tracker discovery:** mcc/model.py rejects unknown fields, duplicate identities and unsupported versions; mcc/fs.py uses bounded descriptor-relative reads. This deliberately sacrifices arbitrary import compatibility and does not redact sensitive text.
- **Canonical owner history separate from derived UI snapshots:** mcc/owner.py owns locked records and projections. Snapshot-only and owner-record backup/restore procedures are not interchangeable; a stale projection must not erase canonical history.
- **Bounded replacement, not blanket durability:** the owner writer fsyncs file and parent directory. The v1 snapshot replacement helper fsyncs the file but does not establish parent-directory power-loss durability. Verification and interrupted-write coverage must remain path-specific.

See [observed results, commands and open gates](VERIFICATION.md). These choices do not imply a private engine, scheduler, cryptographic reviewer identity or production certification.
