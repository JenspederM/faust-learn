from datetime import datetime
from typing import List, Union

import faust
from faust_demo.packml.models.common import TlgHeader


class _DamageCoordinates(faust.Record):
    x: int
    y: int


class _CoordPredictionProbability(faust.Record):
    x: int
    y: int
    confidence: float


class _Tlg0x03016250(faust.Record):
    unique_id: str
    session_id: str
    filename: str
    image_id: str
    image_datetime: datetime
    factory: str
    production_line: str
    prediction_successful: int
    prediction: int
    coordinates: List[str]
    prediction_probability: List[Union[List[int], float]]
    damage_coordinates: List[_DamageCoordinates]
    coord_prediction_probability: List[_CoordPredictionProbability]
    prediction_sent: int
    corrupt_image: int
    ratio_error: int
    valid_image: int
    file_size_mb: float
    pixel_length: int
    pixel_width: int
    corner_damage: int
    y_cut_damage: int
    x_cut_damage: int


class Tlg0x03016250(TlgHeader):
    dataContent: _Tlg0x03016250
