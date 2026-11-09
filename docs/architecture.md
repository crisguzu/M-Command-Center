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
