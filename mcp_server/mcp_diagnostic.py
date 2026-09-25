import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    print("1. Starting MCP server...")

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server.server"],
        env=os.environ.copy(),
    )

    async with stdio_client(server_params) as (read, write):
        print("2. Server process started.")

        async with ClientSession(read, write) as session:
            print("3. Initializing MCP session...")

            await session.initialize()

            print("4. MCP initialization SUCCESS.")

            tools = await session.list_tools()

            print("5. MCP tools:")
            for tool in tools.tools:
                print(f"   - {tool.name}")

            print("6. Calling run_tests...")

            result = await session.call_tool(
                "run_tests",
                {}
            )

            print("7. run_tests response received.")

            for content in result.content:
                if hasattr(content, "text"):
                    print(content.text)


if __name__ == "__main__":
    asyncio.run(main())