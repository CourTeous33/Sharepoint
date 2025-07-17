from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.sharepoint_client import SharePointClient


class GetUserPermissionsTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            # Get required parameters
            user_email = tool_parameters.get("user_email", "")
            
            # Validate required parameters
            if not user_email:
                yield self.create_text_message("Error: User email is required.")
                return
            
            # Get credentials from runtime
            site_url = self.runtime.credentials["site_url"]
            access_token = self.runtime.credentials["access_token"]
            
            # Create SharePoint client
            client = SharePointClient(site_url, access_token)
            
            # Get user information first
            try:
                user_info = client.get_user_by_email(user_email)
            except Exception as e:
                yield self.create_text_message(f"Error: Could not find user with email '{user_email}': {str(e)}")
                return
            
            # Get user permissions
            permissions = client.get_user_effective_permissions(user_email)
            
            # Return results
            yield self.create_json_message({
                "permissions": permissions,
                "user_info": user_info
            })
            yield self.create_text_message(f"Retrieved permissions for user '{user_email}'")
            
        except Exception as e:
            yield self.create_text_message(f"Error retrieving user permissions: {str(e)}")
