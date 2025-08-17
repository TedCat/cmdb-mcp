from cmdb_mcp_server import mcp
from .cmdb_client import CmdbClient

@mcp.tool()
def get_instance_in_cmdb(instance_id: str, public_ip: str, private_ip: str) -> dict:
    """
    Get information about a given instance. provide one of the following parameters: instance_id, public_ip, private_ip.
    
    Args:
        instance_id (str): The instance-id to query.
        public_ip (str): The public IP address of the instance.
        private_ip (str): The private IP address of the instance.
    
    Returns:
        dict: Information about the domain.
    """
    cmdbCli = CmdbClient()
    filters = {}

    if instance_id:
        filters['instance_id'] = instance_id
    if public_ip:
        filters['public_ip'] = public_ip
    if private_ip:
        filters['private_ip'] = private_ip

    response = cmdbCli.get_assets(catalog='vm', filters=filters)

    if not response['data']['list']:
        return {"provided": filters, "info": "No information found."}

    print(response['data']['list'])

    return {"provided": filters, "match_list": response['data']['list']} 