"""Opt-in in-memory JSON decode/validation microprobe; not HTTP or fsync performance."""
from pathlib import Path
import copy
import hashlib
import json
import math
import platform
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mcc.model import decode_snapshot, demo

PROJECTS, SAMPLES = 200, 100

def fixture():
    row = demo()['projects'][0]
    rows = []
    for i in range(PROJECTS):
        item = copy.deepcopy(row)
        item['id'] = 'synthetic-' + str(i)
        item['name'] = 'Fictional project ' + str(i)
        rows.append(item)
    return json.dumps({'schema_version': 1, 'projects': rows}, sort_keys=True).encode()

def main():
    payload = fixture()
    assert len(payload) <= 2_000_000
    assert len(decode_snapshot(payload)['projects']) == PROJECTS
    samples = []
    for _ in range(SAMPLES):
        started = time.perf_counter()
        assert len(decode_snapshot(payload)['projects']) == PROJECTS
        samples.append((time.perf_counter() - started) * 1000)
    ordered = sorted(samples)
    print(json.dumps({'synthetic': True, 'scope': 'in-memory decode_snapshot only; NOT HTTP/import/owner-record/fsync throughput',
        'projects': PROJECTS, 'samples': SAMPLES, 'warmup_decodes': 1,
        'input_bytes': len(payload), 'input_sha256': hashlib.sha256(payload).hexdigest(),
        'python': platform.python_version(), 'platform': platform.system()+' '+platform.machine(),
        'decode_ms': samples, 'p50_ms': ordered[math.ceil(SAMPLES*.5)-1], 'p95_ms': ordered[math.ceil(SAMPLES*.95)-1],
        'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [Path(__file__), ROOT/'mcc/model.py']},
        'limitations': ['single host, one process, warm data', 'short microprobe: no stable tail-latency or scaling claim',
            '200 small projects, not maximum field/list/text payload', 'no filesystem, power-loss, HTTP or concurrency measurement',
            'run resource caps and hardware belong to separate job receipt']}, sort_keys=True))

if __name__ == '__main__':
    main()
