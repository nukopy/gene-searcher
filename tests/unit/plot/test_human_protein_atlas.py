import pytest

from app.plot.human_protein_atlas import modify_tissue_data_key


@pytest.mark.parametrize(
    "input, expected",
    [
        ("Tissue RNA - liver [nTPM]", "Liver"),
        ("Tissue RNA - endometrium 1 [nTPM]", "Endometrium"),
        ("Tissue RNA - skin 1 [nTPM]", "Skin"),
        ("Tissue RNA - stomach 1 [nTPM]", "Stomach"),
        ("Tissue RNA - brain [nTPM]", "Brain"),
    ],
)
def test_modify_tissue_data_key(input: str, expected: str):
    actual = modify_tissue_data_key(input)

    assert actual == expected
