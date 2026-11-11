# Resource envelope and opt-in snapshot microprobe

**Status: MEASURED, bounded synthetic scope only (2026-11-10 local).** An owner-approved idle-worker pause provided the serial measurement window. The original process resumed after 1.0524 seconds; no unrelated job was cancelled. No production capacity,HTTP or durability result follows.

## Implemented limits, not measured capacity

mcc/model.py accepts at most 200 projects,exact schema_version 1,unique identities,text fields up to 4,000 characters,and roadmap/blocker lists up to 100 entries of 2,000 characters each. mcc/model.py::read_snapshot reads at most 2,000,000 bytes. Passing per-field validation does not mean every maximum-sized combination fits the byte cap. These are rejection bounds,not demonstrated acceptable latency or maximum memory. mcc/server.py has bounded concurrency/deadlines; the public edition remains single-host loopback,not remote/distributed serving.

## Prepared probe

After exclusive admission:

~~~sh
python3 benchmarks/snapshot_probe.py
~~~

The fixed generator creates 200 small fictional projects below the real byte cap. One warmup decode precedes 100 serial decode_snapshot samples; output includes all samples,nearest-rank p50/p95,input bytes/hash,source hashes,Python/platform. The loop measures in-memory JSON decode and contract validation only. No private tracker,token,live Gateway,network,filesystem write,owner record or HTTP request is involved. No CI performance loop runs automatically; tests only validate the generated fixture.

Proposed envelope: 45 seconds wall, 512 MiB RAM, one CPU, 32 tasks, 30 seconds per-process CPU, 16 MiB per-file, 32 MiB temp reservation, 1 MiB log. Publish actual hardware,resource peaks,input/output hashes and cleanup evidence only after a real run. A short warm-data microprobe cannot establish a stable tail,SLA,concurrent import/serve capacity or performance at maximum field lengths.

## Durability boundary

The v1 snapshot helper fsyncs its file before replacement but does not fsync the parent directory. tests/test_persistence.py proves selected injected failure behavior,not physical power-loss recovery. The optional owner-record path separately syncs file and directory. Do not conflate those paths or label v1 power-loss durable. Runtime changes to that boundary require their own reviewed tests and approval.

## Observed result, not application serving capacity

On Intel Core Ultra 9 185H/Linux x86_64 WSL/Python 3.12.3, the deterministic 200-small-project fixture was **53015 bytes**. One warmup plus 100 measured decode/validation iterations produced nearest-rank p50 **0.4607 ms** and p95 **0.6007 ms**. All decoded results retained 200 projects. This measures warm in-memory JSON validation only; it says nothing about maximum-size fields,HTTP request latency,filesystem writes,simultaneous clients or owner-record durability.

[Raw samples,source/input hashes,plan where applicable and run receipt](performance/2026-11-10-synthetic.json). Combined serial run: 512 MiB/one-CPU/32-task caps; observed peak RAM 111607808 bytes and 11 tasks. Those peaks cover both probes together,not each individually. Owned job and scratch exited; worker restoration was independently verified. Peak scratch bytes were not sampled: the reservation is not evidence of actual usage or a directory hard quota. Production and power-loss behavior remain outside scope.
