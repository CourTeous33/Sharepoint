from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.sharepoint_client import SharePointClient


class SearchContentTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            # Get required parameters
            query = tool_parameters.get("query", "")
            
            # Validate required parameters
            if not query:
                yield self.create_text_message("Error: Search query is required.")
                return
            
            # Get optional parameters
            select_properties = tool_parameters.get("select_properties")
            row_limit = tool_parameters.get("row_limit", 10)
            
            # Parse select_properties if provided
            select_props_list = None
            if select_properties:
                select_props_list = [prop.strip() for prop in select_properties.split(',')]
            
            # Get credentials from runtime
            site_url = self.runtime.credentials["site_url"]
            access_token = self.runtime.credentials["access_token"]
            
            # Create SharePoint client
            client = SharePointClient(site_url, access_token)
            
            # Perform search
            search_results = client.search(
                query=query,
                select_properties=select_props_list,
                row_limit=row_limit
            )
            
            # Extract results
            results = search_results.get("PrimaryQueryResult", {}).get("RelevantResults", {})
            rows = results.get("Table", {}).get("Rows", [])
            total_rows = results.get("TotalRows", 0)
            
            # Return results
            yield self.create_json_message({
                "results": rows,
                "total_rows": total_rows
            })
            yield self.create_text_message(f"Found {len(rows)} results for query '{query}' (total: {total_rows})")
            
        except Exception as e:
            yield self.create_text_message(f"Error searching content: {str(e)}")
