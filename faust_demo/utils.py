import pandas as pd
from typing import Any
from faust.types import TableT, AppT
from faust.types.web import Request, Web


def as_html_table(app: AppT, web: Web, request: Request, table: TableT, table_id: Any) -> str:
    try:
        if table in table:
            records = [v.to_representation() for v in table.get(table_id)]
            return web.html(pd.DataFrame(records).to_html())
        else:
            return web.html(f"ID '{table_id}' not found in table")
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return web.html(f"Error: {e}")
