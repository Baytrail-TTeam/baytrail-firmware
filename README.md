# Baytrail-firmware

Katalog firmware i materiałów referencyjnych dla Bay Trail oraz pokrewnych platform, rozwijany w organizacji [Baytrail-TTeam](https://github.com/Baytrail-TTeam). Kod portów, konfiguracje urządzeń i testy znajdują się w [baytrail-device-development](https://github.com/Baytrail-TTeam/baytrail-device-development). Firmware przechowujemy wraz z SHA256 i pochodzeniem; obecność w katalogu nie oznacza zgodności z danym urządzeniem.

| Materiał | Wersja | Platforma | Uwagi |
|---|---|---|---|
| [Intel FSP Vga.dat](firmware/intel/bay-trail/vbios/3652-fsp/) | 3652 PC14.34, 2013-11-30 | Valleyview / Bay Trail | PCI8086:0f31; VBT100/BDB155; ROM64KiB |
| [HPC7SCP4 Intel VBIOS](firmware/devices/unknown/hpc7scp4/vbios/1024/) | 1024 PC14.34, 2015-02-05 | Valleyview / Bay Trail | PCI8086:0f31; VBT100/BDB189; ROM64KiB |
| [PIPO X9 VBT](firmware/devices/pipo/x9/vbt/) | BDB188 | Bay Trail | Legacy VBIOS nie wykryto w dotychczasowym skanie |
| [PIPO X9S VBT](firmware/devices/pipo/x9s/vbt/) | BDB195 | **Cherry Trail / Cherryview** | Osobna platforma; nie traktować jako dawcy Bay Trail bez analizy |
| [Eksperymenty S165](experiments/ilife/s165/hpc7scp4-transplant/) | panel0 / all-panels | Bay Trail | Modyfikacje HPC1024, z diffem i wskazaniem rodzica |

**Chuwi Vi10:** brak przypisanego i sprawdzonego VBIOS-u. Dane dawcy nie są danymi panelu Chuwi.

## Układ

- `catalog/entries/`: jeden rekord JSON na unikalny binarny artefakt; duplikaty są aliasami pochodzenia.
- `firmware/intel/`: referencyjne pakiety platformowe; `firmware/devices/`: oryginały konkretnych urządzeń.
- `experiments/`: wyłącznie pochodne, ze wskazanym SHA256 rodzica i opisem zmian.
- `devices/`: identyfikacja urządzeń; `categories/`: zasady dla VBIOS, VBT, GOP, UEFI, EC, ACPI, FSP, driver i innych Option ROM.
- `docs/`: format metadanych, import i pochodzenie; `scripts/`: narzędzia bez dostępu do sprzętu.

## Praca

```sh
git clone https://github.com/Baytrail-TTeam/baytrail-firmware.git Baytrail-firmware
cd Baytrail-firmware
python3 scripts/catalog.py list
python3 scripts/catalog.py validate
```

Dodawanie kolejnego firmware: [ADDING-FIRMWARE.md](docs/ADDING-FIRMWARE.md). Pełna lista i hashe: [CATALOG.md](CATALOG.md), [SHA256SUMS](SHA256SUMS).

Oryginalne VBT FSP3652 i HPC1024 mają sumy modulo256 odpowiednio 74 i44. Są zachowane dokładnie; walidator sprawdza zgodność z zapisanym stanem, a nie udaje, że są bezbłędne. [Pochodzenie i ograniczenia](docs/PROVENANCE.md).

Pełne obrazy OEM, drzewa UEFI i narzędzia flashujące pozostały w starej lokalnej kolekcji. Skopiowano wybrane VBIOS-y i VBT z `Devices`, nie cały dump SPI ani wcześniejsze pliki spoza `Devices`.
