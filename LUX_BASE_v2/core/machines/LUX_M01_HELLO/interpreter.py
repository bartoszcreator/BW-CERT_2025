#!/usr/bin/env python3
"""
LUX_M01_HELLO – prosty interpreter prototypowego języka LUX-Lang.

Założenie:
- czytamy manifest.json, żeby znać podstawowe metadane modułu,
- czytamy module.lux i wykonujemy najprostsze polecenia,
  np. linie zaczynające się od `SAY`.

To jest **prototyp** – ma pokazać zasadę: jeden klocek (module.lux)
+ mały interpreter = działająca maszyna LUX.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


# Ścieżki do plików modułu
MODULE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = MODULE_DIR / "manifest.json"
LUX_SOURCE_PATH = MODULE_DIR / "module.lux"


def load_manifest() -> dict:
    """Wczytaj manifest modułu LUX z pliku JSON."""
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Brak pliku manifestu: {MANIFEST_PATH}")

    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Minimalna walidacja – w prototypie tylko ID i wersja
    required_keys = ["id", "version", "type"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Brak wymaganej właściwości '{key}' w manifest.json")

    return data


def load_lux_source() -> str:
    """Wczytaj kod źródłowy w języku LUX-Lang."""
    if not LUX_SOURCE_PATH.exists():
        raise FileNotFoundError(f"Brak pliku źródłowego: {LUX_SOURCE_PATH}")

    return LUX_SOURCE_PATH.read_text(encoding="utf-8")


def parse_say_instructions(source: str) -> Iterable[str]:
    """
    Bardzo prosty parser:

    - przechodzimy po liniach,
    - wybieramy linie zaczynające się od `SAY`,
    - wyciągamy tekst w cudzysłowie.

    Przykład w module.lux:
        SAY "Witaj! To jest pierwszy moduł demonstracyjny systemu LUX."
    """
    for line in source.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            # komentarze i puste linie ignorujemy
            continue

        if stripped.startswith("SAY "):
            # Odcinamy prefiks `SAY` i bierzemy resztę
            payload = stripped[4:].strip()

            # Jeśli tekst jest w cudzysłowie, zdejmujemy je
            if payload.startswith('"') and payload.endswith('"'):
                payload = payload[1:-1]

            yield payload


def run_module() -> None:
    """Uruchom moduł LUX_M01_HELLO w trybie tekstowym (stdout)."""
    manifest = load_manifest()
    source = load_lux_source()

    module_id = manifest.get("id", "UNKNOWN")
    version = manifest.get("version", "0.0.0")

    print(f"[LUX] Uruchamiam moduł: {module_id} (wersja {version})")
    print(f"[LUX] Plik źródłowy: {LUX_SOURCE_PATH.name}")
    print("-" * 60)

    messages = list(parse_say_instructions(source))
    if not messages:
        print("[LUX] Brak instrukcji SAY w module.lux – nic do wyświetlenia.")
        return

    for msg in messages:
        print(f"[LUX] {msg}")

    print("-" * 60)
    print("[LUX] Zakończono działanie modułu.")


if __name__ == "__main__":
    run_module()
