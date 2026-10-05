# Dodawanie firmware

1. Zidentyfikuj producenta, model, rewizję płyty, platformę i źródło. Nie przenoś właściwości dawcy na urządzenie docelowe.
2. Importuj oryginał bez zmian, np.:

```sh
python3 scripts/catalog.py add --file /path/new-vbios.rom \
  --id vendor-model-vbios-build --kind vbios --platform intel/bay-trail \
  --device vendor/model --version BUILD --source-url https://vendor.example/package \
  --description 'Opis pochodzenia i zastosowania'
```

3. Uzupełnij rekord: notice/licencja, źródłowy pakiet z SHA256, hardware evidence. Nieznane pole ma wartość null; brak testu pozostaje brakiem testu.
4. Dodaj powiązane decode/BSF jako `sidecars` z path/size/sha256. Każdy osobny VBT jest własnym wpisem. Duplikat wykrywany po SHA256: dodaj alias/provenance do istniejącego rekordu.
5. Dla modyfikacji użyj `--status derived --parent-sha256 HASH` i dołącz opis każdego patcha. `experiments` nie miesza się z oryginałami.
6. `python3 scripts/catalog.py validate`, następnie `python3 scripts/catalog.py index` oraz `sha256sum -c SHA256SUMS`; przejrzyj diff i commit. Rekordy są źródłem prawdy; polecenie index odbudowuje plik sum i tabelę z JSON.
7. W repo rozwojowym zapisz ID i SHA256 wybranego artefaktu oraz commit tego katalogu. Nie wpisuj URL lokalnego dysku do `.gitmodules`.

Sterowniki: zapisuj OS, architekturę, wersję pakietu, hardware IDs, manifest plików i podpis/publisher. Nie utożsamiaj paczki Afu/FPT z pakietem sterowników. Duże archiwa wymagają decyzji Git LFS albo recipe + hash przed dodaniem; obecne ROM-y 64KiB są normalnymi plikami Git.
