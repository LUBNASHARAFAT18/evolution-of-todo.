import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp():
    server_params = StdioServerParameters(
        command="python",
        args=["d:/hackthon 2 phase 1/mcp_server.py"],
    )

    print("Connecting to MCP server...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("Listing tools...")
            tools = await session.list_tools()
            print(f"Tools found: {[t.name for t in tools.tools]}")

            print("Calling list_tasks...")
            result = await session.call_tool("list_tasks", arguments={"status": "all"})
            print(f"Result: {result.content[0].text}")

            print("Calling add_task...")
            result = await session.call_tool("add_task", arguments={"title": "Verify MCP Phase 3"})
            print(f"Result: {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(test_mcp())
