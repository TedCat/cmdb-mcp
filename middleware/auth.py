from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.dependencies import get_http_request
from fastmcp.exceptions import ToolError
from starlette.requests import Request

class HeaderTokenAuthMiddleware(Middleware):
    """
    Very basic “Bearer token in the HTTP Authorization header” authentication.
    
    Clients must include:
      Authorization: Bearer my-secret-token
    in their HTTP request.
    """
    def __init__(self, valid_token: str):
        self.valid_token = valid_token

    async def on_request(self, context: MiddlewareContext, call_next):
        # Allow introspection without auth
        if context.method.startswith(("tools/list", "resources/list", "prompts/list")):
            return await call_next(context)

        # 2. Grab the current HTTP request via FastMCP’s dependency
        try:
            request: Request = get_http_request()        # :contentReference[oaicite:0]{index=0}
        except RuntimeError:
            # No HTTP request in context (e.g. stdio transport)
            raise ToolError("Authentication failed: HTTP transport required")

        # 3. Extract and verify Bearer token
        auth_header = request.headers.get("authorization", "")
        if not auth_header.lower().startswith("bearer "):
            raise ToolError("Authentication failed: missing Bearer token")

        token = auth_header.split(None, 1)[1].strip()
        if token != self.valid_token:
            raise ToolError("Authentication failed: invalid token")

        return await call_next(context)