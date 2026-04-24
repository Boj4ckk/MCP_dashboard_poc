


import anthropic
from fastmcp import Client


client_anthropic = anthropic.Anthropic()
mcp_client = Client("server.py")


async def main():
    async with mcp_client:
        mcp_tools = await mcp_client.list_tools()
    
    tools = [
        {
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        }
        for tool in mcp_tools
    ]

    messages = [{"role": "user", "content": "Montre moi les perfs du Samsung QLED pour 2024"}]
    while True:
        response = client_anthropic.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        if response.stop_reason == "tool_use":
            tool_call = next(b for b in response.content if b.type == "tool_use")

            async with mcp_client:
                result = await mcp_client.call_tool(tool_call.name, tool_call.input)
            
            messages.append({"role":"assistant", "content": response.content})
            messages.append({
                "role":"user",
                "content": [{"type": "tool_result","tool_use_id":tool_call.id,"content":str(result)}]

            })

        else:
            print(response.content[0].text)
            break

            

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
