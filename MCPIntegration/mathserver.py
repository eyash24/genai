from mcp.server.fastmcp import FastMCP

mcp = FastMCP('math')

@mcp.tool()
def add(a:int, b:int)-> int:
    """_summary_
    Add two number
    """
    return a+b

@mcp.tool()
def multiply(a:int, b:int)-> int:
    '''Multiply two numbers'''
    return a*b

# transport='studio' tells server to use standard input / output (stdin / stdout) to receive and respond to tool funciton calls.

if __name__ =="__main__":
    mcp.run(transport='stdio')

    
