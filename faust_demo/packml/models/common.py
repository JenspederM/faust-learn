import faust
from datetime import datetime
from typing import Any


class TlgHeader(faust.Record):
    validationSchema: str
    decodeToSQL: str
    dataContentDecodingSchema: str
    telegramDescription: str
    telegramTypeFriendly: str
    telegramType: int
    telegramTypeVersion: int
    timestamp: datetime
    unitID: int
    machineIDx: int
    friendlyName: str
    mode: int
    state: int
    dataContent: Any
