from math import ceil


def calculate(kind: str, values: list[float]) -> float | int:
    if kind in {"concrete_volume", "gravel_volume", "mulch_volume"}:
        return values[0] * values[1] * values[2]
    if kind == "concrete_bags":
        return ceil(values[0] / values[1])
    if kind == "paint_quantity":
        return (values[0] / values[1]) * values[2]
    if kind == "flooring_quantity":
        return values[0] * values[1] * (1 + values[2] / 100)
    if kind == "tile_quantity":
        return ceil((values[0] / (values[1] * values[2])) * (1 + values[3] / 100))
    if kind == "drywall_sheets":
        return ceil((2 * (values[0] + values[1]) * values[2]) / (values[3] * values[4]))
    if kind == "board_feet":
        return (values[0] * values[1] * values[2] / 12) * values[3]
    if kind == "material_cost":
        return values[0] * values[1] * (1 + values[2] / 100)
    raise ValueError(f"Unknown calculator type: {kind}")
