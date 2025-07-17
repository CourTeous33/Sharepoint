from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.sharepoint_client import SharePointClient


class CreateListTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            # Get required parameters
            title = tool_parameters.get("title", "")
            description = tool_parameters.get("description", "")
            
            # Validate required parameters
            if not title:
                yield self.create_text_message("Error: List title is required.")
                return
            
            # Get credentials from runtime
            site_url = self.runtime.credentials["site_url"]
            access_token = self.runtime.credentials["access_token"]
            
            # Create SharePoint client
            client = SharePointClient(site_url, access_token)
            
            # Create the list
            result = client.create_list(title, description)
            
            # Return results
            yield self.create_json_message({
                "success": True,
                "list_info": result
            })
            yield self.create_text_message(f"Successfully created list '{title}'")
            
        except Exception as e:
            yield self.create_text_message(f"Error creating list: {str(e)}")
            yield self.create_json_message({"success": False, "error": str(e)})
