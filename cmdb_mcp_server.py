# from mcp.server.fastmcp import FastMCP
from fastmcp import FastMCP
import os

from fastapi import HTTPException, Header
from middleware.auth import HeaderTokenAuthMiddleware

mcp = FastMCP("Get information from self managed CMDB by provided info. can check whether the asset belong to our own and get much more detail info for an asset")
# mcp.add_middleware(HeaderTokenAuthMiddleware(valid_token="whatever"))