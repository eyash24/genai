from mcp.server.fastmcp import FastMCP

mcp = FastMCP('weather')

@mcp.tool()
async def get_weather(location: str)-> str:
    '''Get weather of the location specified'''
    return f"It's is raining in {location}"

if __name__ == '__main__':
    mcp.run(transport='streamable-http')

