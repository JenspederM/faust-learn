from faust.models.fields import StringField
from datetime import datetime
from typing import Optional
import faust

from faust_demo.packml.models.common import TlgHeader


class _Tlg0x03015100(faust.Record):
    processID: int
    loggingType: int
    unitOfMeasure: int
    settingsVersion: int
    starttimestamp: str
    stoptimestamp: str
    duration: int
    processValue: int
    processValueString: str
    processValueMin: int
    processValueMax: int
    processValueSamples: int
    setpoint: int
    setpointString: str
    controlStatus: int
    controlStatus2: int
    unitPrefix: str = StringField(required=False)
    unitDescription: str = StringField(required=False)


class Tlg0x03015100(TlgHeader):
    dataContent: _Tlg0x03015100


class Tlg0x03015100Table(faust.Record):
    timestamp: Optional[datetime] = datetime.fromtimestamp(0)
    machine_id: Optional[int] = -999
    machine_name: Optional[str] = "N/A"
    telegram_id: Optional[str] = "N/A"
    telegram_name: Optional[str] = "N/A"
    process_id: Optional[int] = -999
    unit_id: Optional[int] = -999
    process_value: Optional[float] = -999.00
