# Format metadanych — schema_version 1

Każdy `catalog/entries/<id>.json` opisuje jeden unikalny plik. Wymagane: id, kind, platform, device (może null), status, version (może null), description, path, size, sha256, provenance, license, compatibility, structure, sidecars.

`kind`: vbios/vbt/gop/uefi/ec/acpi/driver/optionrom/fsp/other. `status`: original/derived. Pochodny wymaga `parent_sha256` katalogowanego oryginału. `provenance` zawiera source_url (null jeśli nieustalone), local_path lub local_filename oraz metodę pozyskania; może wskazać niezałączony source_image z SHA256.

`structure` to pomiar offline Option ROM/PCIR/VBT/BDB, a nie certyfikat działania. `errors` i niezerowe sumy VBT są zachowywane. Walidacja musi odtworzyć dokładnie zapisane obserwacje. `compatibility.verified_devices` jest puste, dopóki nie dołączono wyników testów powiązanych z modelem/revision, konfiguracją i SHA256. MIPI support nie wynika z samej obecności bloku; nie przypisano go donorom bez analizy kodu.

Każdy sidecar ma path/size/sha256. Wersja BDB znajduje się w structure.vbts[].bdb_version. Identyfikatory PCI znajdują się w structure.rom.vendor/device. Nowe pola sterowników/EC mogą być dodane bez zmiany znaczenia pól v1; zmiana znaczenia wymaga nowej wersji schematu.
