from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.sharepoint_client import SharePointClient


class GetListItemsTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            # Get required parameters
            list_title = tool_parameters.get("list_title", "")
            
            # Validate required parameters
            if not list_title:
                yield self.create_text_message("Error: List title is required.")
                return
            
            # Get optional parameters
            select_fields = tool_parameters.get("select_fields")
            filter_query = tool_parameters.get("filter_query")
            top = tool_parameters.get("top")
            
            # Get credentials from runtime
            site_url = self.runtime.credentials["site_url"]
            access_token = self.runtime.credentials["access_token"]
            
            # Create SharePoint client
            client = SharePointClient(site_url, access_token)
            
            # Get list items
            items = client.get_list_items(
                list_title=list_title,
                select_fields=select_fields,
                filter_query=filter_query,
                top=top
            )
            
            # Return results
            yield self.create_json_message({
                "items": items,
                "count": len(items)
            })
            yield self.create_text_message(f"Retrieved {len(items)} items from list '{list_title}'")
            
        except Exception as e:
            yield self.create_text_message(f"Error retrieving list items: {str(e)}")
