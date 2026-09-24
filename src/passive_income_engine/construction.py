from math import ceil


def calculate(kind: str, values: list[float]) -> float | int:
    if kind in {
        "concrete_volume", "gravel_volume", "mulch_volume", "sand_volume",
        "soil_volume"
    }:
        return values[0] * values[1] * values[2] if kind not in {"area", "volume"} else values[0] * values[1] if kind == "area" else values[0] * values[1] * values[2]
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
    if kind == "paver_quantity":
        return ceil(((values[0] * values[1]) * 144 / (values[2] * values[3])) * (1 + values[4] / 100))
    if kind == "fence_pickets":
        return ceil((values[0] * 12) / (values[1] + values[2]))
    if kind == "fence_posts":
        return ceil(values[0] / values[1]) + 1
    if kind == "decking_boards":
        rows = ceil((values[1] * 12) / (values[2] + values[3]))
        per_row = ceil(values[0] / values[4])
        return ceil(rows * per_row * (1 + values[5] / 100))
    if kind == "roofing_squares":
        return values[0] / 100
    if kind == "roofing_material":
        return values[0] * (1 + values[1] / 100)
    if kind in {"gravel_weight", "concrete_weight"}:
        return values[0] * values[1]
    if kind == "concrete_footing":
        return values[0] * values[1] * values[2]
    if kind == "rebar_length":
        return values[0] * values[1]
    if kind == "gravel_bags":
        return ceil(values[0] / values[1])
    if kind == "baseboard":
        return ceil(values[0] / values[1])
    if kind == "wallpaper":
        return ceil(values[0] / values[1])
    if kind == "stair_risers":
        return ceil(values[0] / values[1])
    if kind == "asphalt_volume":
        return values[0] * values[1] * values[2]
    if kind == "cubic_yards":
        return (values[0] * values[1] * values[2]) / 27
    if kind == "area":
        return values[0] * values[1]
    if kind == "volume":
        return values[0] * values[1] * values[2]
    raise ValueError(f"Unknown calculator type: {kind}")
