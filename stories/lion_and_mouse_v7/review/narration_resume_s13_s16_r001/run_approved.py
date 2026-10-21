"""One-shot supervisor for the exact owner-authorized operation. No retries."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[4]
FOLDER = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(name, value):
    (FOLDER / name).write_text(json.dumps(value, indent=2) + '\n')

operation = json.loads((FOLDER / 'OPERATION.json').read_text())
authorization = json.loads((FOLDER / 'AUTHORIZATION.json').read_text())
assert authorization['operation_sha256'] == sha(FOLDER / 'OPERATION.json')
for source in operation['inputs'] + [operation['exact_requests']]:
    assert sha(ROOT / source['path']) == source['sha256'], source['path']
with (FOLDER / 'STARTED.lock').open('x') as lock:
    lock.write(str(os.getpid()))
baseline = {str(p.relative_to(ROOT)): sha(p) for p in
            (ROOT / 'voice/narration/lion_and_mouse_v7/en/r001').rglob('*')
            if p.is_file() and p.suffix in ('.wav', '.json')}
write('BASELINE.json', baseline)
state = dict(status='running', supervisor_pid=os.getpid(),
             started_at=datetime.now(timezone.utc).isoformat(),
             operation_sha256=authorization['operation_sha256'],
             maximum_requests=63, automatic_retries=0)
write('EXECUTION.json', state)
env = dict(os.environ, PYTHONUNBUFFERED='1')
with (FOLDER / 'run.log').open('x') as log:
    result = subprocess.run(operation['command_argv'], cwd=ROOT, env=env,
                            stdout=log, stderr=subprocess.STDOUT)
state.update(status='completed' if result.returncode == 0 else 'stopped_on_failure',
             returncode=result.returncode,
             ended_at=datetime.now(timezone.utc).isoformat())
write('EXECUTION.json', state)
