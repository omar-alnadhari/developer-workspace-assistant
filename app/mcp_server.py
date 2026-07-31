from fastmcp import FastMCP
from fastmcp.server.providers.openapi import MCPType, RouteMap

from app.main import app


mcp = FastMCP.from_fastapi(
    app=app,
    name="Developer Workspace Assistant MCP",
    route_maps=[
        # These endpoints are useful for humans and monitoring,
        # but they should not be exposed as AI tools.
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
    mcp.run()
    