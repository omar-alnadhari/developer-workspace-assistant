import pytest
from fastmcp import Client
from sqlmodel import Session

from app.database import get_session
from app.main import app
from app.mcp_server import mcp


@pytest.mark.asyncio
async def test_mcp_exposes_task_tools() -> None:
    """The MCP server should expose the task-management operations."""

    async with Client(mcp) as client:
        tools = await client.list_tools()

    tool_names = {tool.name for tool in tools}

    expected_tools = {
        "create_task",
        "list_tasks",
        "get_task",
        "update_task",
        "delete_task",
    }

    assert expected_tools.issubset(tool_names)

    # Human-facing endpoints must not become AI tools.
    assert "read_root" not in tool_names
    assert "health_check" not in tool_names


@pytest.mark.asyncio
async def test_mcp_can_create_and_list_tasks(
    session: Session,
) -> None:
    """MCP tools should create and retrieve tasks successfully."""

    def get_test_session() -> Session:
        return session

    app.dependency_overrides[get_session] = get_test_session

    try:
        async with Client(mcp) as client:
            create_result = await client.call_tool(
                "create_task",
                {
                    "title": "Test MCP integration",
                    "description": "Create a task through an MCP tool",
                    "completed": False,
                },
            )

            created_task = create_result.data

            assert created_task.id is not None
            assert created_task.title == "Test MCP integration"
            assert created_task.description == (
                "Create a task through an MCP tool"
            )
            assert created_task.completed is False

            list_result = await client.call_tool(
                "list_tasks",
                {
                    "offset": 0,
                    "limit": 100,
                },
            )

            tasks = list_result.data

            assert len(tasks) == 1
            assert tasks[0].id == created_task.id
            assert tasks[0].title == "Test MCP integration"
            assert tasks[0].completed is False

    finally:
        app.dependency_overrides.clear()
