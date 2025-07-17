from collections.abc import Generator
from typing import Any
import json

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.sharepoint_client import SharePointClient


class CreateListItemTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            # Get required parameters
            list_title = tool_parameters.get("list_title", "")
            item_data_str = tool_parameters.get("item_data", "")
            
            # Validate required parameters
            if not list_title:
                yield self.create_text_message("Error: List title is required.")
                return
            if not item_data_str:
                yield self.create_text_message("Error: Item data is required.")
                return
            
            # Parse JSON data
            try:
                item_data = json.loads(item_data_str)
            except json.JSONDecodeError:
                yield self.create_text_message("Error: Item data must be valid JSON.")
                return
            
            # Get credentials from runtime
            site_url = self.runtime.credentials["site_url"]
            access_token = self.runtime.credentials["access_token"]
            
            # Create SharePoint client
            client = SharePointClient(site_url, access_token)
            
            # Create the list item
            result = client.create_list_item(list_title, item_data)
            
            # Return results
            yield self.create_json_message({
                "success": True,
                "item_info": result
            })
            yield self.create_text_message(f"Successfully created item in list '{list_title}'")
            
        except Exception as e:
            yield self.create_text_message(f"Error creating list item: {str(e)}")
            yield self.create_json_message({"success": False, "error": str(e)})
