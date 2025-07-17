from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.sharepoint_client import SharePointClient


class GetListsTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            # Get credentials from runtime
            site_url = self.runtime.credentials["site_url"]
            access_token = self.runtime.credentials["access_token"]
            
            # Create SharePoint client
            client = SharePointClient(site_url, access_token)
            
            # Get all lists
            lists = client.get_lists()
            
            # Return results
            yield self.create_json_message({"lists": lists})
            yield self.create_text_message(f"Found {len(lists)} lists in SharePoint site")
            
        except Exception as e:
            yield self.create_text_message(f"Error retrieving lists: {str(e)}")
