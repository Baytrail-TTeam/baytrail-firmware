# Firmware catalog instructions

- Preserve originals byte-for-byte. Every artifact needs SHA256, provenance, platform, version (or explicit unknown) and distribution status.
- Keep modifications in experiments with a catalogued parent SHA256 and patch description. PCI ID, BDB version and build date do not establish compatibility.
- Chuwi Vi10 has no validated firmware assignment yet. PIPO X9S is Cherry Trail, not Bay Trail.
- Do not execute firmware, flash utilities or driver installers. The catalog tools only inspect and copy files.
- Before commit run `python3 scripts/catalog.py validate`, `python3 scripts/catalog.py index`, and `sha256sum -c SHA256SUMS`.
- Original nonzero VBT checksums are recorded anomalies; never repair them in place or call structural validation hardware validation.
- Keep device-specific stock dumps with private identifiers out of published history. Firmware redistribution rights are not established by a local import.
