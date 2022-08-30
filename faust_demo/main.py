from typing import AsyncIterable, List

import faust
from faust.types import AppT, StreamT, TableT

from faust_demo.config import Settings
from faust_demo.packml.models.processes import Tlg0x03015100, Tlg0x03015100Table
from faust_demo.utils import as_html_table

app_settings = Settings()
app_settings.FAUST_CONNECT_OPTIONS["id"] = "faust-demo"

app: AppT = faust.App(**app_settings.FAUST_CONNECT_OPTIONS)


reformatted: TableT[int, List[Tlg0x03015100Table]] = app.Table(
    "0x03015100-reformatted", default=list, partitions=3)


@app.agent(app.topic("azure-packml-fct-0x03015100-0", key_type=str, value_type=Tlg0x03015100))
async def format_0x03015100(msgs: StreamT[Tlg0x03015100]) -> AsyncIterable[Tlg0x03015100]:
    async for msg in msgs:
        try:
            new_row = Tlg0x03015100Table(
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


@app.page("/machines")
async def view_process_by_machine_table(web, request):
    return web.json({"machines": [v for v in reformatted]})


@app.page("/machines/{machine_id}/process")
@app.table_route(table=reformatted, match_info="machine_id")
async def view_process_by_machine_table(web, request, machine_id: str):
    return web.json({"process": reformatted.get(int(machine_id))})


if __name__ == "__main__":
    app.main()
