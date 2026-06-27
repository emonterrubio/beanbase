"""Tests for farm name parsing."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from normalizers.farm_name import parse_importer_lot_name


def test_person_finca_colombia_microlot():
    raw = (
        "Daniel Mauricio Bolanos Zuniga - Finca El Placer - San Agustin - "
        "Huila - Caturra - Anaerobic Washed (GrainPro)"
    )
    parsed = parse_importer_lot_name(raw)
    assert parsed.farm_name == "Finca El Placer"
    assert parsed.owner_name == "Daniel Mauricio Bolanos Zuniga"
    assert parsed.department == "Huila"
    assert parsed.varietal == "Caturra"


def test_area_micro_region_finca_santa_barbara():
    raw = (
        "Area 18 - Finca Santa Barbara - Timbio - Cauca - "
        "Pink Bourbon - Oxidation Washed (GrainPro)"
    )
    parsed = parse_importer_lot_name(raw)
    assert parsed.farm_name == "Finca Santa Barbara"
    assert parsed.owner_name == "Area 18"
    assert parsed.municipality == "Timbio"
    assert parsed.department == "Cauca"
    assert parsed.varietal == "Pink Bourbon"
    assert parsed.process_hint == "Oxidation Washed"
    assert parsed.packaging_type == "(GrainPro)"


def test_process_first_fazenda():
    raw = "Natural - Fazenda Sertão - Yellow Bourbon (SC Bags)"
    parsed = parse_importer_lot_name(raw)
    assert parsed.farm_name == "Fazenda Sertão"
    assert parsed.owner_name is None
    assert parsed.varietal == "Yellow Bourbon"


def test_micromill_owner_not_farm():
    raw = "Los Madrigal Micromill - Finca El Analia - Catuai & Caturra - Natural (GrainPro)"
    parsed = parse_importer_lot_name(raw)
    assert parsed.farm_name == "Finca El Analia"
    assert parsed.owner_name == "Los Madrigal Micromill"


def test_couple_name_with_ampersand():
    raw = (
        "Paola & Carlos Trujillo - Finca Patio Bonito - Caldono - Cauca - "
        "Pink Bourbon - Washed (GrainPro)"
    )
    parsed = parse_importer_lot_name(raw)
    assert parsed.farm_name == "Finca Patio Bonito"
    assert parsed.owner_name == "Paola & Carlos Trujillo"


def test_cooperative_program():
    raw = "ARGCAFEE - Coca Substitution Program - Argelia - Cauca - Castillo & Colombia (GrainPro)"
    parsed = parse_importer_lot_name(raw)
    assert "ARGCAFEE" in parsed.farm_name
    assert parsed.owner_name is None


def test_single_cooperative_name():
    raw = 'Asociacion de productores de café de Apolo "APCA" (GrainPro)'
    parsed = parse_importer_lot_name(raw)
    assert "APCA" in parsed.farm_name or "Apolo" in parsed.farm_name
    assert parsed.owner_name is None


def test_malformed_internal_dashes():
    raw = "Las Lajas Micromill - Finca San Isidro- Caturra & Catuaí- Perla Negra- Natural (GrainPro)"
    parsed = parse_importer_lot_name(raw)
    assert parsed.farm_name == "Finca San Isidro"
    assert parsed.owner_name == "Las Lajas Micromill"


def test_finca_only_no_owner():
    raw = "Finca Juan Martin - Sotara - Cauca - Gesha - Washed (GrainPro)"
    parsed = parse_importer_lot_name(raw)
    assert parsed.farm_name == "Finca Juan Martin"
    assert parsed.owner_name is None


if __name__ == "__main__":
    for name, obj in list(globals().items()):
        if name.startswith("test_") and callable(obj):
            obj()
            print(f"ok {name}")
    print("all passed")
