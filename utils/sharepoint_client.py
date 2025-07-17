import requests
from typing import Dict, Any, Optional, List
import json


class SharePointClient:
    """
    SharePoint REST API client for handling common operations
    """
    
    def __init__(self, site_url: str, access_token: str):
        """
        Initialize SharePoint client
        
        Args:
            site_url: SharePoint site URL (e.g., https://company.sharepoint.com/sites/sitename)
            access_token: Bearer token for authentication
        """
        self.site_url = site_url.rstrip('/')
        self.access_token = access_token
        self.base_api_url = f"{self.site_url}/_api"
        
    def _get_headers(self, content_type: str = "application/json") -> Dict[str, str]:
        """Get standard headers for API requests"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": content_type,
            "Accept": "application/json;odata=verbose"
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make HTTP request to SharePoint API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint relative to base API URL
            data: Request body data
            params: Query parameters
            
        Returns:
            JSON response data
            
        Raises:
            Exception: If API call fails
        """
        url = f"{self.base_api_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            if response.content:
                return response.json()
            else:
                return {"success": True}
                
        except requests.RequestException as e:
            raise Exception(f"SharePoint API call failed: {str(e)}")
    
    def get_site_info(self) -> Dict[str, Any]:
        """Get site information"""
        return self._make_request("GET", "web")
    
    def get_lists(self) -> List[Dict[str, Any]]:
        """Get all lists in the site"""
        response = self._make_request("GET", "web/lists")
        return response.get("d", {}).get("results", [])
    
    def get_list_by_title(self, list_title: str) -> Dict[str, Any]:
        """Get list by title"""
        endpoint = f"web/lists/getbytitle('{list_title}')"
        return self._make_request("GET", endpoint)
    
    def create_list(self, title: str, description: str = "", template_type: int = 100) -> Dict[str, Any]:
        """
        Create a new list
        
        Args:
            title: List title
            description: List description
            template_type: SharePoint list template type (default: 100 for custom list)
        """
        data = {
            "__metadata": {"type": "SP.List"},
            "Title": title,
            "Description": description,
            "BaseTemplate": template_type
        }
        return self._make_request("POST", "web/lists", data)
    
    def update_list(self, list_title: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update list properties"""
        endpoint = f"web/lists/getbytitle('{list_title}')"
        
        # Add metadata for update
        updates["__metadata"] = {"type": "SP.List"}
        
        # Need to use MERGE method for updates
        headers = self._get_headers()
        headers["X-HTTP-Method"] = "MERGE"
        headers["If-Match"] = "*"
        
        url = f"{self.base_api_url}/{endpoint}"
        
        try:
            response = requests.post(
                url=url,
                headers=headers,
                json=updates,
                timeout=30
            )
            response.raise_for_status()
            return {"success": True, "message": "List updated successfully"}
        except requests.RequestException as e:
            raise Exception(f"Failed to update list: {str(e)}")
    
    def get_list_items(self, list_title: str, select_fields: Optional[str] = None, 
                      filter_query: Optional[str] = None, top: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get items from a list
        
        Args:
            list_title: List title
            select_fields: OData $select parameter (comma-separated field names)
            filter_query: OData $filter parameter
            top: OData $top parameter (limit results)
        """
        endpoint = f"web/lists/getbytitle('{list_title}')/items"
        
        params = {}
        if select_fields:
            params["$select"] = select_fields
        if filter_query:
            params["$filter"] = filter_query
        if top:
            params["$top"] = top
            
        response = self._make_request("GET", endpoint, params=params)
        return response.get("d", {}).get("results", [])
    
    def create_list_item(self, list_title: str, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new list item"""
        endpoint = f"web/lists/getbytitle('{list_title}')/items"
        
        # Add required metadata
        item_data["__metadata"] = {"type": f"SP.Data.{list_title}ListItem"}
        
        return self._make_request("POST", endpoint, item_data)
    
    def update_list_item(self, list_title: str, item_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a list item"""
        endpoint = f"web/lists/getbytitle('{list_title}')/items({item_id})"
        
        # Add metadata for update
        updates["__metadata"] = {"type": f"SP.Data.{list_title}ListItem"}
        
        # Need to use MERGE method for updates
        headers = self._get_headers()
        headers["X-HTTP-Method"] = "MERGE"
        headers["If-Match"] = "*"
        
        url = f"{self.base_api_url}/{endpoint}"
        
        try:
            response = requests.post(
                url=url,
                headers=headers,
                json=updates,
                timeout=30
            )
            response.raise_for_status()
            return {"success": True, "message": "Item updated successfully"}
        except requests.RequestException as e:
            raise Exception(f"Failed to update item: {str(e)}")
    
    def delete_list_item(self, list_title: str, item_id: int) -> Dict[str, Any]:
        """Delete a list item"""
        endpoint = f"web/lists/getbytitle('{list_title}')/items({item_id})"
        
        headers = self._get_headers()
        headers["X-HTTP-Method"] = "DELETE"
        headers["If-Match"] = "*"
        
        url = f"{self.base_api_url}/{endpoint}"
        
        try:
            response = requests.post(
                url=url,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            return {"success": True, "message": "Item deleted successfully"}
        except requests.RequestException as e:
            raise Exception(f"Failed to delete item: {str(e)}")
    
    def upload_file(self, folder_path: str, file_name: str, file_content: bytes) -> Dict[str, Any]:
        """
        Upload file to SharePoint
        
        Args:
            folder_path: Target folder path (e.g., "Shared Documents")
            file_name: Name for the uploaded file
            file_content: File content as bytes
        """
        endpoint = f"web/GetFolderByServerRelativeUrl('{folder_path}')/Files/add(url='{file_name}',overwrite=true)"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/octet-stream"
        }
        
        url = f"{self.base_api_url}/{endpoint}"
        
        try:
            response = requests.post(
                url=url,
                headers=headers,
                data=file_content,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to upload file: {str(e)}")
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get file information"""
        endpoint = f"web/GetFileByServerRelativeUrl('{file_path}')"
        return self._make_request("GET", endpoint)
    
    def download_file(self, file_path: str) -> bytes:
        """
        Download file from SharePoint
        
        Args:
            file_path: Server relative path to the file
            
        Returns:
            File content as bytes
        """
        endpoint = f"web/GetFileByServerRelativeUrl('{file_path}')/$value"
        url = f"{self.base_api_url}/{endpoint}"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.get(
                url=url,
                headers=headers,
                timeout=60
            )
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            raise Exception(f"Failed to download file: {str(e)}")

    # ====================
    # USER MANAGEMENT
    # ====================
    
    def get_site_users(self) -> List[Dict[str, Any]]:
        """Get all users in the site"""
        response = self._make_request("GET", "web/siteusers")
        return response.get("d", {}).get("results", [])
    
    def get_site_groups(self) -> List[Dict[str, Any]]:
        """Get all site groups"""
        response = self._make_request("GET", "web/sitegroups")
        return response.get("d", {}).get("results", [])
    
    def get_current_user(self) -> Dict[str, Any]:
        """Get current user information"""
        return self._make_request("GET", "web/currentuser")
    
    def get_user_by_email(self, email: str) -> Dict[str, Any]:
        """Get user by email address"""
        endpoint = f"web/siteusers/getbyemail('{email}')"
        return self._make_request("GET", endpoint)
    
    def get_user_effective_permissions(self, user_email: str) -> Dict[str, Any]:
        """Get effective permissions for a user"""
        endpoint = f"web/getusereffectivepermissions(@user)?@user='{user_email}'"
        return self._make_request("GET", endpoint)

    # ====================
    # PERMISSIONS & ROLES
    # ====================
    
    def get_role_assignments(self) -> List[Dict[str, Any]]:
        """Get role assignments for the site"""
        response = self._make_request("GET", "web/roleassignments")
        return response.get("d", {}).get("results", [])
    
    def get_role_definitions(self) -> List[Dict[str, Any]]:
        """Get role definitions (permission levels)"""
        response = self._make_request("GET", "web/roledefinitions")
        return response.get("d", {}).get("results", [])
    
    def break_role_inheritance(self, copy_roles: bool = True) -> Dict[str, Any]:
        """Break role inheritance for the site"""
        endpoint = f"web/breakroleinheritance(copyRoleAssignments={str(copy_roles).lower()})"
        return self._make_request("POST", endpoint)

    # ====================
    # CONTENT TYPES
    # ====================
    
    def get_content_types(self) -> List[Dict[str, Any]]:
        """Get all content types"""
        response = self._make_request("GET", "web/contenttypes")
        return response.get("d", {}).get("results", [])
    
    def get_content_type_by_id(self, content_type_id: str) -> Dict[str, Any]:
        """Get content type by ID"""
        endpoint = f"web/contenttypes('{content_type_id}')"
        return self._make_request("GET", endpoint)
    
    def create_content_type(self, name: str, parent_id: str = None, description: str = "") -> Dict[str, Any]:
        """Create a new content type"""
        data = {
            "__metadata": {"type": "SP.ContentType"},
            "Name": name,
            "Description": description
        }
        if parent_id:
            data["Id"] = {"StringValue": parent_id}
        
        return self._make_request("POST", "web/contenttypes", data)

    # ====================
    # FIELDS
    # ====================
    
    def get_fields(self) -> List[Dict[str, Any]]:
        """Get all site fields"""
        response = self._make_request("GET", "web/fields")
        return response.get("d", {}).get("results", [])
    
    def get_field_by_title(self, title: str) -> Dict[str, Any]:
        """Get field by title"""
        endpoint = f"web/fields/getbytitle('{title}')"
        return self._make_request("GET", endpoint)
    
    def create_field(self, field_xml: str) -> Dict[str, Any]:
        """Create a field using XML schema"""
        data = {
            "parameters": {
                "SchemaXml": field_xml
            }
        }
        return self._make_request("POST", "web/fields/createfieldasxml", data)

    # ====================
    # VIEWS
    # ====================
    
    def get_list_views(self, list_title: str) -> List[Dict[str, Any]]:
        """Get views for a list"""
        endpoint = f"web/lists/getbytitle('{list_title}')/views"
        response = self._make_request("GET", endpoint)
        return response.get("d", {}).get("results", [])
    
    def create_list_view(self, list_title: str, view_title: str, view_query: str = "", 
                        view_fields: List[str] = None) -> Dict[str, Any]:
        """Create a view for a list"""
        data = {
            "__metadata": {"type": "SP.View"},
            "Title": view_title,
            "ViewQuery": view_query
        }
        if view_fields:
            data["ViewFields"] = {"results": view_fields}
        
        endpoint = f"web/lists/getbytitle('{list_title}')/views"
        return self._make_request("POST", endpoint, data)

    # ====================
    # SEARCH
    # ====================
    
    def search(self, query: str, select_properties: List[str] = None, 
              start_row: int = 0, row_limit: int = 10) -> Dict[str, Any]:
        """
        Search SharePoint content
        
        Args:
            query: Search query
            select_properties: Properties to return in results
            start_row: Start row for paging
            row_limit: Maximum number of results
        """
        params = {
            "querytext": f"'{query}'",
            "startrow": start_row,
            "rowlimit": row_limit
        }
        
        if select_properties:
            params["selectproperties"] = ",".join(select_properties)
        
        response = self._make_request("GET", "search/query", params=params)
        return response.get("d", {}).get("query", {})

    # ====================
    # FOLDERS
    # ====================
    
    def get_folders(self, folder_path: str = "Shared Documents") -> List[Dict[str, Any]]:
        """Get folders in a library"""
        endpoint = f"web/GetFolderByServerRelativeUrl('{folder_path}')/folders"
        response = self._make_request("GET", endpoint)
        return response.get("d", {}).get("results", [])
    
    def create_folder(self, folder_path: str, folder_name: str) -> Dict[str, Any]:
        """Create a folder"""
        data = {
            "__metadata": {"type": "SP.Folder"},
            "ServerRelativeUrl": f"{folder_path}/{folder_name}"
        }
        endpoint = f"web/folders"
        return self._make_request("POST", endpoint, data)
    
    def delete_folder(self, folder_path: str) -> Dict[str, Any]:
        """Delete a folder"""
        endpoint = f"web/GetFolderByServerRelativeUrl('{folder_path}')"
        return self._make_request("DELETE", endpoint)

    # ====================
    # SITE COLLECTION
    # ====================
    
    def get_site_collection_info(self) -> Dict[str, Any]:
        """Get site collection information"""
        return self._make_request("GET", "site")
    
    def get_regional_settings(self) -> Dict[str, Any]:
        """Get regional settings"""
        return self._make_request("GET", "web/regionalsettings")
    
    def get_features(self) -> List[Dict[str, Any]]:
        """Get activated features"""
        response = self._make_request("GET", "web/features")
        return response.get("d", {}).get("results", [])

    # ====================
    # WORKFLOW
    # ====================
    
    def get_workflows(self) -> List[Dict[str, Any]]:
        """Get workflows (if available)"""
        try:
            response = self._make_request("GET", "web/workflowtemplates")
            return response.get("d", {}).get("results", [])
        except:
            return []
    
    def get_workflow_associations(self) -> List[Dict[str, Any]]:
        """Get workflow associations"""
        try:
            response = self._make_request("GET", "web/workflowassociations")
            return response.get("d", {}).get("results", [])
        except:
            return []

    # ====================
    # NAVIGATION
    # ====================
    
    def get_navigation_nodes(self, navigation_type: str = "TopNavigationBar") -> List[Dict[str, Any]]:
        """
        Get navigation nodes
        
        Args:
            navigation_type: "TopNavigationBar" or "QuickLaunch"
        """
        endpoint = f"web/navigation/{navigation_type.lower()}"
        response = self._make_request("GET", endpoint)
        return response.get("d", {}).get("results", [])

    # ====================
    # RECYCLE BIN
    # ====================
    
    def get_recycle_bin_items(self) -> List[Dict[str, Any]]:
        """Get items in recycle bin"""
        response = self._make_request("GET", "web/recyclebin")
        return response.get("d", {}).get("results", [])
    
    def restore_recycle_bin_item(self, item_id: str) -> Dict[str, Any]:
        """Restore item from recycle bin"""
        endpoint = f"web/recyclebin('{item_id}')/restore"
        return self._make_request("POST", endpoint)

    # ====================
    # BATCH OPERATIONS
    # ====================
    
    def execute_batch(self, requests_batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute multiple requests in a batch
        
        Args:
            requests_batch: List of request dictionaries with 'method', 'url', and optional 'data'
        """
        # This is a simplified batch implementation
        # In a full implementation, you'd use $batch endpoints
        results = []
        for request in requests_batch:
            try:
                if request["method"].upper() == "GET":
                    result = self._make_request("GET", request["url"])
                elif request["method"].upper() == "POST":
                    result = self._make_request("POST", request["url"], request.get("data"))
                else:
                    result = {"error": f"Unsupported method: {request['method']}"}
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})
        
        return {"results": results}


def validate_sharepoint_credentials(site_url: str, access_token: str) -> bool:
    """
    Validate SharePoint credentials by attempting to connect
    
    Args:
        site_url: SharePoint site URL
        access_token: Bearer token
        
    Returns:
        True if credentials are valid, False otherwise
    """
    try:
        client = SharePointClient(site_url, access_token)
        client.get_site_info()
        return True
    except Exception:
        return False