import os

from fastmcp import FastMCP
from fastmcp.server.providers.openapi import MCPType, RouteMap

from app.database import create_db_and_tables
from app.main import app


mcp = FastMCP.from_fastapi(
    app=app,
    name="Developer Workspace Assistant MCP",
    route_maps=[
        RouteMap(
            pattern=r"^/$",
            mcp_type=MCPType.EXCLUDE,
        ),
        RouteMap(
            pattern=r"^/health$",
            mcp_type=MCPType.EXCLUDE,
        ),
    ],
)


if __name__ == "__main__":
    create_db_and_tables()

    mcp.run(
        transport="http",
        host=os.getenv("MCP_HOST", "127.0.0.1"),
        port=int(os.getenv("MCP_PORT", "8001")),
    )