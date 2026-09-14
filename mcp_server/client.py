import asyncio
import sys
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


server_params = StdioServerParameters(
    command=sys.executable,
    args=["-m", "mcp_server.server"],
    env=os.environ.copy(),
)


async def main():

    async with stdio_client(
        server_params
    ) as (read, write):

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            tools = await session.list_tools()

            print(
                "\n===== AVAILABLE TOOLS =====\n"
            )

            for tool in tools.tools:

                print(
                    f"- {tool.name}"
                )

            print(
                "\n===== CALLING run_tests =====\n"
            )

            result = await session.call_tool(
                "run_tests",
                {}
            )

            print(
                "\n===== TOOL RESULT =====\n"
            )

            for content in result.content:

                if hasattr(content, "text"):

                    print(content.text)

            print(
                "\n===== CALLING read_test_report =====\n"
            )

            report_result = await session.call_tool(
                "read_test_report",
                {}
            )

            print(
                "\n===== TEST EXECUTION REPORT =====\n"
            )

            for content in report_result.content:

                if hasattr(content, "text"):

                    print(content.text)


if __name__ == "__main__":

    asyncio.run(main())
