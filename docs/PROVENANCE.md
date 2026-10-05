# Pochodzenie i granice kolekcji

Import lokalny: 2026-10-05 z `csmwrap-research/Devices`. Żadnego firmware nie wykonywano, nie flashowano ani nie modyfikowano przy imporcie. Powtórzenia o tym samym SHA256 przechowywane są raz, z aliasami źródłowymi w JSON.

Intel FSP: źródło odnotowane w wcześniejszej analizie — https://github.com/intel/FSP/tree/BayTrail/BayTrailFspBinPkg/Vbios . Importujemy istniejące bajty, bez nowego pobrania i bez uznania aktualnej gałęzi za przypiętą wersję. Wersję identyfikuje SHA256 i string build3652 w ROM. `Vga.bsf` zachowano jako sidecar.

Dla HPC7SCP4 i PIPO nie znaleziono potwierdzonego URL dostawy. `source_url: null` jest świadomą luką. Rekord zawiera nazwę, rozmiar i SHA256 źródłowego pełnego obrazu, który pozostaje w starej kolekcji. Dla HPC VBIOS pochodzi z rozpakowanego UEFI (FFS A0327FE0-1FDA-4E5B-905D-B510C45A61D0); offsety skanu odnoszą się do plików po dekompresji, a nie zawsze do offsetu w obrazie SPI.

Oryginalne raporty skanu/decode są sidecarami: ich historyczne ścieżki absolutne i nazwy nie są przenośnymi odnośnikami. Bieżące ścieżki i tożsamość plików definiuje `catalog/entries`.

PIPO X9S należy do Cherry Trail. Archiwum ZIP źródła miało nietypowe zerowe CRC w central directory; stara kolekcja zawiera raport weryfikacji wypakowanych danych. Żadne zawarte tam narzędzie flashujące nie zostało uruchomione ani uznane za sterownik.

Oryginalne obrazy ROM65 536B mają poprawne Option ROM checksum0. VBT w FSP3652 ma checksum74, HPC1024 checksum44. Zachowanie tych anomalii jest warunkiem wiernego archiwum; nie gwarantuje akceptacji przez parser VBIOS. Pochodne S165 są osobnymi wpisami i nie mają statusu firmware produkcyjnego.

## Prawa

Docelowe repozytorium: https://github.com/Baytrail-TTeam/baytrail-firmware . Nie nadano cudzym binariom nowej licencji. Zachowano notice Intela (w tym „For Evaluation Use Only”). Prawo dalszej dystrybucji binariów nie zostało ustalone i jest odnotowane w każdym rekordzie. Publikacja katalogu nie stanowi potwierdzenia licencji ani prawa do użycia lub redystrybucji jego zawartości. Niektóre pozycje mogą wymagać zastąpienia binarium przez fetch/extract recipe z hashami. Kopia istniejącego pliku nie dowodzi prawa redystrybucji.

Własne nowe skrypty i opisy także nie otrzymują domyślnie wybranej za właściciela licencji. Zasady repo nie zastępują licencji upstream i źródeł.
