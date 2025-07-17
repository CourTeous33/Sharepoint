from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.sharepoint_client import SharePointClient


class GetContentTypesTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            # Get credentials from runtime
            site_url = self.runtime.credentials["site_url"]
            access_token = self.runtime.credentials["access_token"]
            
            # Create SharePoint client
            client = SharePointClient(site_url, access_token)
            
            # Get all content types
            content_types = client.get_content_types()
            
            # Return results
            yield self.create_json_message({"content_types": content_types})
            yield self.create_text_message(f"Found {len(content_types)} content types in SharePoint site")
            
        except Exception as e:
            yield self.create_text_message(f"Error retrieving content types: {str(e)}")
