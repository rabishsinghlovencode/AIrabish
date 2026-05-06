from __future__ import annotations

from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CSV Preview")

CSV_DATA = """order_id,customer,amount,region
1001,Asha,1200,South
1002,Ravi,900,West
1003,Meena,1500,South"""

@mcp.resource("data://sales_csv")
def sales_csv() -> str:
    return CSV_DATA




import csv
from io import StringIO

@mcp.tool()
def get_csv_schema(file_text: str) -> str:
    """Return column names and row count for CSV text."""
    reader = csv.DictReader(StringIO(file_text))
    rows = list(reader)
    return f"columns={reader.fieldnames}; rows={len(rows)}"



if __name__ == "__main__":
    mcp.run()
