from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from utils.sharepoint_client import validate_sharepoint_credentials


class SharepointProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            site_url = credentials.get("site_url")
            access_token = credentials.get("access_token")
            
            if not site_url:
                raise ToolProviderCredentialValidationError("Site URL is required")
            if not access_token:
                raise ToolProviderCredentialValidationError("Access token is required")
            
            # Validate credentials by attempting to connect to SharePoint
            if not validate_sharepoint_credentials(site_url, access_token):
                raise ToolProviderCredentialValidationError("Invalid SharePoint credentials or unable to connect to site")
                
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
