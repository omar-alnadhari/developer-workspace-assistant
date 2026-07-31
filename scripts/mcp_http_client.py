import asyncio

from fastmcp import Client


MCP_SERVER_URL = "http://127.0.0.1:8001/mcp"


async def main() -> None:
    """Connect to the HTTP MCP server and call its task tools."""

    async with Client(MCP_SERVER_URL) as client:
        tools = await client.list_tools()

        print("\nAvailable MCP tools:")
        for tool in tools:
            print(f"- {tool.name}")

        create_result = await client.call_tool(
            "create_task",
            {
                "title": "Test HTTP MCP",
                "description": "Create a task through the HTTP MCP server",
                "completed": False,
            },
        )

        print("\nCreated task:")
        print(create_result.data)

        list_result = await client.call_tool(
            "list_tasks",
            {
                "offset": 0,
                "limit": 100,
            },
        )

        print("\nStored tasks:")
        for task in list_result.data:
            print(task)


if __name__ == "__main__":
    asyncio.run(main())