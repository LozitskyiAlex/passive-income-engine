import pytest

from passive_income_engine.construction import calculate


@pytest.mark.parametrize(
    ("kind", "values", "expected"),
    [
        ("concrete_volume", [10, 4, 0.5], 20),
        ("concrete_bags", [20, 0.5], 40),
        ("gravel_volume", [10, 4, 0.25], 10),
        ("mulch_volume", [10, 4, 0.25], 10),
        ("paint_quantity", [400, 350, 2], 400 / 350 * 2),
        ("flooring_quantity", [10, 4, 10], 44),
        ("tile_quantity", [20, 10, 10, 10], 1),
        ("drywall_sheets", [5, 4, 2.5, 1.2, 2.4], 16),
        ("board_feet", [2, 8, 10, 4], 53.3333333333),
        ("material_cost", [100, 12.5, 10], 1375),
    ],
)
def test_calculators(kind, values, expected):
    assert calculate(kind, values) == pytest.approx(expected)


def test_unknown_calculator_raises():
    with pytest.raises(ValueError):
        calculate("unknown", [1])
