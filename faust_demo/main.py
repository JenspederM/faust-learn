from datetime import datetime
from typing import AsyncIterable, List, Optional
from faust.models.fields import StringField
from faust.types import AppT, StreamT, TableT
import faust
from faust_demo.config import Settings
import pandas as pd


app_settings = Settings()
app_settings.FAUST_CONNECT_OPTIONS["id"] = "faust-demo"

app: AppT = faust.App(**app_settings.FAUST_CONNECT_OPTIONS)


class MyModelContent(faust.Record):
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


class MyModel(faust.Record):
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
    dataContent: MyModelContent


class MyTable(faust.Record):
    timestamp: Optional[datetime] = datetime.fromtimestamp(0)
    machine_id: Optional[int] = -999
    machine_name: Optional[str] = "N/A"
    telegram_id: Optional[str] = "N/A"
    telegram_name: Optional[str] = "N/A"
    process_id: Optional[int] = -999
    unit_id: Optional[int] = -999
    process_value: Optional[float] = -999.00


reformatted: TableT[int, List[MyTable]] = app.Table("0x03015100-reformatted", default=list, partitions=3)


@app.agent(app.topic("azure-packml-fct-0x03015100-0", key_type=str, value_type=MyModel))
async def format_0x03015100(msgs: StreamT[MyModel]) -> AsyncIterable[MyModel]:
    async for msg in msgs:
        try:
            new_row = MyTable(
                timestamp=msg.timestamp,
                machine_id=msg.machineIDx,
                machine_name=msg.friendlyName,
                telegram_id=msg.telegramTypeFriendly,
                telegram_name=msg.telegramDescription,
                process_id=msg.dataContent.processID,
                unit_id=msg.dataContent.unitOfMeasure,
                process_value=msg.dataContent.processValue,
            )

            current_table = reformatted.get(new_row.machine_id)
            if current_table is None:
                current_table = [new_row]
            else:
                current_table.append(new_row)
            app.logger.debug(f"New row: {new_row}")

            reformatted[msg.machineIDx] = current_table
        except Exception as e:
            app.logger.error(f"Error: {e}\nCould not reformat message: {msg}")


@app.page("/process/{machine_id}/")
@app.table_route(table=reformatted, match_info="machine_id")
async def get_count(web, request, machine_id: str):
    try:
        machine = [v.to_representation() for v in reformatted.get(int(machine_id))]
        return web.html(pd.DataFrame(machine).to_html())
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return web.html(f"Error: {e}")


if __name__ == "__main__":
    app.main()
