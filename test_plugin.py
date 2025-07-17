#!/usr/bin/env python3
"""
Test script for SharePoint Dify Plugin

This script demonstrates how to test the SharePoint plugin locally
"""

import requests
import json
import os
from typing import Dict, Any

# Plugin server configuration
PLUGIN_URL = "http://localhost:5000"

def test_credential_validation():
    """Test credential validation"""
    print("=== Testing Credential Validation ===")
    
    # Replace with your actual SharePoint credentials
    test_credentials = {
        "site_url": "https://company.sharepoint.com/sites/testsite",
        "access_token": "your_access_token_here"
    }
    
    payload = {
        "provider": "sharepoint",
        "credentials": test_credentials
    }
    
    try:
        response = requests.post(
            f"{PLUGIN_URL}/validate-credentials",
            json=payload,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_get_lists():
    """Test getting SharePoint lists"""
    print("\n=== Testing Get Lists Tool ===")
    
    # Replace with your actual credentials
    credentials = {
        "site_url": "https://company.sharepoint.com/sites/testsite",
        "access_token": "your_access_token_here"
    }
    
    payload = {
        "provider": "sharepoint",
        "tool": "get_lists",
        "credentials": credentials,
        "parameters": {}
    }
    
    try:
        response = requests.post(
            f"{PLUGIN_URL}/invoke-tool",
            json=payload,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_create_list():
    """Test creating a SharePoint list"""
    print("\n=== Testing Create List Tool ===")
    
    credentials = {
        "site_url": "https://company.sharepoint.com/sites/testsite", 
        "access_token": "your_access_token_here"
    }
    
    payload = {
        "provider": "sharepoint",
        "tool": "create_list",
        "credentials": credentials,
        "parameters": {
            "title": "Test List from Dify Plugin",
            "description": "This list was created using the SharePoint Dify plugin"
        }
    }
    
    try:
        response = requests.post(
            f"{PLUGIN_URL}/invoke-tool",
            json=payload,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_get_list_items():
    """Test getting list items"""
    print("\n=== Testing Get List Items Tool ===")
    
    credentials = {
        "site_url": "https://company.sharepoint.com/sites/testsite",
        "access_token": "your_access_token_here"
    }
    
    payload = {
        "provider": "sharepoint",
        "tool": "get_list_items", 
        "credentials": credentials,
        "parameters": {
            "list_title": "Test List",
            "top": 10
        }
    }
    
    try:
        response = requests.post(
            f"{PLUGIN_URL}/invoke-tool",
            json=payload,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_create_list_item():
    """Test creating a list item"""
    print("\n=== Testing Create List Item Tool ===")
    
    credentials = {
        "site_url": "https://company.sharepoint.com/sites/testsite",
        "access_token": "your_access_token_here"
    }
    
    item_data = {
        "Title": "Test Item from Plugin",
        "Description": "This item was created using the SharePoint Dify plugin"
    }
    
    payload = {
        "provider": "sharepoint",
        "tool": "create_list_item",
        "credentials": credentials,
        "parameters": {
            "list_title": "Test List",
            "item_data": json.dumps(item_data)
        }
    }
    
    try:
        response = requests.post(
            f"{PLUGIN_URL}/invoke-tool",
            json=payload,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_search_content():
    """Test SharePoint search functionality"""
    print("\n=== Testing Search Content Tool ===")
    
    credentials = {
        "site_url": "https://company.sharepoint.com/sites/testsite",
        "access_token": "your_access_token_here"
    }
    
    payload = {
        "provider": "sharepoint",
        "tool": "search_content",
        "credentials": credentials,
        "parameters": {
            "query": "test",
            "row_limit": 5
        }
    }
    
    try:
        response = requests.post(
            f"{PLUGIN_URL}/invoke-tool",
            json=payload,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_get_site_users():
    """Test getting site users"""
    print("\n=== Testing Get Site Users Tool ===")
    
    credentials = {
        "site_url": "https://company.sharepoint.com/sites/testsite",
        "access_token": "your_access_token_here"
    }
    
    payload = {
        "provider": "sharepoint",
        "tool": "get_site_users",
        "credentials": credentials,
        "parameters": {}
    }
    
    try:
        response = requests.post(
            f"{PLUGIN_URL}/invoke-tool",
            json=payload,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_get_user_permissions():
    """Test getting user permissions"""
    print("\n=== Testing Get User Permissions Tool ===")
    
    credentials = {
        "site_url": "https://company.sharepoint.com/sites/testsite",
        "access_token": "your_access_token_here"
    }
    
    payload = {
        "provider": "sharepoint",
        "tool": "get_user_permissions",
        "credentials": credentials,
        "parameters": {
            "user_email": "user@company.com"
        }
    }
    
    try:
        response = requests.post(
            f"{PLUGIN_URL}/invoke-tool",
            json=payload,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_get_content_types():
    """Test getting content types"""
    print("\n=== Testing Get Content Types Tool ===")
    
    credentials = {
        "site_url": "https://company.sharepoint.com/sites/testsite",
        "access_token": "your_access_token_here"
    }
    
    payload = {
        "provider": "sharepoint",
        "tool": "get_content_types",
        "credentials": credentials,
        "parameters": {}
    }
    
    try:
        response = requests.post(
            f"{PLUGIN_URL}/invoke-tool",
            json=payload,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run all tests"""
    print("SharePoint Plugin Test Suite - Advanced Edition")
    print("=" * 50)
    print("Available Tools:")
    print("1. Basic Operations:")
    print("   - get_lists, create_list")
    print("   - get_list_items, create_list_item")
    print("   - update_list_item, delete_list_item")
    print("   - upload_file, download_file")
    print("2. Advanced Operations:")
    print("   - get_site_users")
    print("   - search_content")
    print("   - get_user_permissions")
    print("   - get_content_types")
    print("=" * 50)
    print("Make sure to:")
    print("1. Update credentials in this script")
    print("2. Start the plugin server with: python -m main")
    print("3. Run this test script in another terminal")
    print("=" * 50)
    
    # Uncomment the tests you want to run
    # Note: You need to provide valid SharePoint credentials
    
    # Basic Operations
    # test_credential_validation()
    # test_get_lists()
    # test_create_list() 
    # test_get_list_items()
    # test_create_list_item()
    
    # Advanced Operations
    # test_search_content()
    # test_get_site_users()
    # test_get_user_permissions()
    # test_get_content_types()
    
    print("\nUpdate the credentials in this script and uncomment the tests to run them!")
    print("The plugin now supports 12 different SharePoint operations!")

if __name__ == "__main__":
    main()