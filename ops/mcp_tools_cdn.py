from cmdb_mcp_server import mcp
from .cmdb_client import CmdbClient

@mcp.tool()
def get_cdn_in_cmdb(cname: str) -> dict:
    """
    Get information about a given CDN.
    
    Args:
        cname (str): The name of the CDN to query.
    
    Returns:
        dict: Information about the CDN.
    """
    cmdbCli = CmdbClient()
    response = cmdbCli.get_assets(catalog='cdn', filters={'cname': cname})

    if not response['data']['list']:
        return {"cdn": cname, "info": "No information found for this CDN."}

    records = []
    for item in response['data']['list']:
        records.append({
            'cname': item['cname'],
            'cdn_origin': item['cdn_origin']
        })

    print(records)
    return {"cdn": cname, "info": records}