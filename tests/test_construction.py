import json
from pathlib import Path
import pytest
from passive_income_engine.construction import calculate
ROOT=Path(__file__).resolve().parents[1]
@pytest.mark.parametrize(("kind","values","expected"),[
("concrete_volume",[10,4,.5],20),("concrete_bags",[20,.5],40),("gravel_volume",[10,4,.25],10),("mulch_volume",[10,4,.25],10),("paint_quantity",[400,350,2],400/350*2),("flooring_quantity",[10,4,10],44),("tile_quantity",[100,12,12,10],110),("drywall_sheets",[20,15,8,4,8],18),("board_feet",[2,8,10,4],53.3333333333),("material_cost",[100,4,10],440),("paver_quantity",[20,12,12,6,5],504),("sand_volume",[20,10,.1],20),("soil_volume",[10,10,.5],50),("fence_pickets",[100,5.5,1.5],172),("fence_posts",[100,8],14),("decking_boards",[20,12,6,.125,12,0],48),("roofing_squares",[2400],24),("roofing_material",[2400,10],2640),("gravel_weight",[10,1.6],16),("concrete_weight",[10,150],1500),("concrete_footing",[20,1,.5],10),("rebar_length",[20,4],80),("gravel_bags",[10,.5],20),("baseboard",[100,8],13),("wallpaper",[120,25],5),("stair_risers",[96,8],12),("asphalt_volume",[20,10,.2],40),("cubic_yards",[27,1,1],1),("area",[20,15],300),("volume",[20,15,2],600)])
def test_all_calculators(kind,values,expected): assert calculate(kind,values)==pytest.approx(expected)
def test_catalog_types_are_all_covered():
 items=json.loads((ROOT/"data/construction_calculators.json").read_text()); assert len(items)==30; assert len({x["type"] for x in items})==30

def test_unknown_calculator_raises():
 with pytest.raises(ValueError): calculate("unknown",[1])
