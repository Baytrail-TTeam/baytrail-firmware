#!/usr/bin/env python3
"""Local, read-only validation of catalogued firmware; import only copies files."""
import argparse
import hashlib
import json
import pathlib
import re
import shutil
import sys
from validate_rom import inspect

ROOT = pathlib.Path(__file__).resolve().parents[1]
KINDS = ('vbios', 'vbt', 'gop', 'uefi', 'ec', 'acpi', 'driver', 'optionrom', 'fsp', 'other')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def confined(value):
    path = (ROOT / value).resolve()
    if not path.is_relative_to(ROOT) or path == ROOT:
        raise ValueError(f'Path outside repository: {value}')
    return path


def records():
    return [(p, json.loads(p.read_text())) for p in sorted((ROOT / 'catalog/entries').glob('*.json'))]


def observed(path, kind):
    if kind in ('vbios', 'vbt'):
        result = inspect(path)
        result.pop('file', None)
        return result
    return None


def validate():
    errors, ids, used = [], set(), set()
    for meta, item in records():
        try:
            if item['schema_version'] != 1 or item['kind'] not in KINDS:
                raise ValueError('Unsupported schema/kind')
            if item['id'] in ids or meta.stem != item['id']:
                raise ValueError('Duplicate id or filename/id mismatch')
            ids.add(item['id'])
            if item['status'] not in ('original', 'derived'):
                raise ValueError('Unsupported status')
            if not item['provenance'] or not item['license']['redistribution']:
                raise ValueError('Missing provenance/redistribution status')
            path = confined(item['path'])
            if (ROOT / item['path']).is_symlink() or not path.is_file():
                raise ValueError('Missing/nonregular payload')
            if sha(path) != item['sha256'] or path.stat().st_size != item['size']:
                raise ValueError('SHA256/size mismatch')
            used.add(item['path'])
            if observed(path, item['kind']) != item.get('structure'):
                raise ValueError('Structural observations changed; do not silently normalize original firmware')
            if item['status'] == 'derived' and not item.get('parent_sha256'):
                raise ValueError('Derived artifact has no parent SHA256')
            for sidecar in item.get('sidecars', []):
                path = confined(sidecar['path'])
                if sha(path) != sidecar['sha256'] or path.stat().st_size != sidecar['size']:
                    raise ValueError(f'Sidecar SHA256/size mismatch: {path}')
                used.add(sidecar['path'])
        except (KeyError, ValueError, OSError, TypeError) as exc:
            errors.append(f'{meta.relative_to(ROOT)}: {exc}')
    for _, item in records():
        if item.get('status') == 'derived' and item.get('parent_sha256') not in {r['sha256'] for _, r in records()}:
            errors.append(f'{item["id"]}: parent is not catalogued')
    for base in ('firmware', 'experiments'):
        for path in (ROOT / base).rglob('*'):
            if path.is_file() and path.name != 'README.md':
                if path.relative_to(ROOT).as_posix() not in used:
                    errors.append(f'Uncatalogued payload/sidecar: {path.relative_to(ROOT)}')
    print(f'{len(ids)} catalog entries checked; {len(errors)} errors')
    for error in errors:
        print(error, file=sys.stderr)
    anomalies = sum(bool(r.get('structure', {}).get('errors')) or any(v['checksum_mod256'] for v in r.get('structure', {}).get('vbts', [])) for _, r in records() if r.get('structure'))
    print(f'{anomalies} entries have recorded original structural/checksum anomalies (preserved, not repaired)')
    return bool(errors)


def index():
    rows = ['# Katalog artefaktów\n', '| ID | Typ | Status | Rozmiar | Wersja | SHA256 |',
            '|---|---|---|---:|---|---|']
    sums = {}
    for _, item in records():
        rows.append(f'| [{item["id"]}]({item["path"]}) | {item["kind"]} | {item["status"]} | {item["size"]} | {item["version"] or "—"} | `{item["sha256"]}` |')
        for asset in [item] + item['sidecars']:
            sums[asset['path']] = asset['sha256']
    (ROOT / 'CATALOG.md').write_text('\n'.join(rows) + '\n')
    (ROOT / 'SHA256SUMS').write_text(''.join(f'{digest}  {path}\n' for path, digest in sorted(sums.items())))
    print('Regenerated CATALOG.md and SHA256SUMS from catalog metadata')


def add(args):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.id):
        raise ValueError('Use a lowercase slug for --id')
    source = pathlib.Path(args.file).resolve()
    digest = sha(source)
    for _, item in records():
        if item['sha256'] == digest:
            raise ValueError(f'Already catalogued as {item["id"]}; add provenance to that entry instead')
    meta = ROOT / 'catalog/entries' / (args.id + '.json')
    dest = ROOT / ('experiments' if args.status == 'derived' else 'firmware') / args.platform / args.kind / args.id / source.name
    if meta.exists() or dest.exists():
        raise ValueError('Destination already exists')
    confined(dest.relative_to(ROOT))
    if args.status == 'derived' and args.parent_sha256 not in {r['sha256'] for _, r in records()}:
        raise ValueError('--parent-sha256 must identify an existing catalogue parent')
    item = dict(schema_version=1, id=args.id, kind=args.kind, platform=args.platform,
                device=args.device, status=args.status, version=args.version,
                description=args.description, path=dest.relative_to(ROOT).as_posix(),
                size=source.stat().st_size, sha256=digest,
                provenance=[dict(source_url=args.source_url, local_filename=source.name,
                                 method='byte-for-byte copy; source not executed')],
                license=dict(owner='unknown', redistribution='not established'),
                compatibility=dict(verified_devices=[], notes='No hardware compatibility inferred from PCI ID/version'),
                structure=observed(source, args.kind), sidecars=[])
    if args.status == 'derived':
        item['parent_sha256'] = args.parent_sha256
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation keeps imports from overwriting another artifact.
    with dest.open('xb') as output:
        with source.open('rb') as inp:
            shutil.copyfileobj(inp, output)
    with meta.open('x') as output:
        json.dump(item, output, ensure_ascii=False, indent=2)
        output.write('\n')
    print(f'Added {args.id}; review metadata, run validate, then commit')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='cmd', required=True)
    sub.add_parser('validate')
    sub.add_parser('list')
    sub.add_parser('index')
    imp = sub.add_parser('add')
    for field in ('file', 'id', 'platform', 'description'):
        imp.add_argument('--' + field, required=True)
    imp.add_argument('--kind', choices=KINDS, required=True)
    imp.add_argument('--status', choices=('original', 'derived'), default='original')
    for field in ('device', 'version', 'source-url', 'parent-sha256'):
        imp.add_argument('--' + field)
    args = parser.parse_args()
    try:
        if args.cmd == 'validate':
            return validate()
        if args.cmd == 'list':
            for _, r in records():
                print(f'{r["id"]:44} {r["kind"]:10} {r["status"]:8} {r["version"] or "unknown":12} {r["sha256"][:12]}')
        elif args.cmd == 'index':
            index()
        else:
            add(args)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == '__main__':
    sys.exit(main())
