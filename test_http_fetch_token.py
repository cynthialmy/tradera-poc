#!/usr/bin/env python3
"""
Test FetchToken using HTTP GET method

This script tests the FetchToken method using HTTP GET instead of SOAP,
as mentioned in Tradera's documentation.

Usage:
    python test_http_fetch_token.py
"""

import requests
from config import get_config

def main():
    """Main function"""
    print("🔐 Testing Tradera FetchToken via HTTP GET")
    print("=" * 50)

    # Get configuration
    config = get_config()
    tradera_config = config['tradera']

    # Check if we have the required credentials
    if not tradera_config['app_id'] or not tradera_config['service_key'] or not tradera_config['public_key']:
        print("❌ Missing required API credentials!")
        print("Please set the following environment variables:")
        print("  TRADERA_APP_ID")
        print("  TRADERA_SERVICE_KEY")
        print("  TRADERA_PUBLIC_KEY")
        return

    # User ID from the authorization flow
    user_id = 5986811

    # Secret key used in the login URL
    secret_key = "07829484-381D-433E-B437-84BCF22FDBFC"

    print(f"✅ Configuration loaded successfully!")
    print(f"App ID: {tradera_config['app_id']}")
    print(f"Service Key: {tradera_config['service_key'][:20]}...")
    print(f"Public Key: {tradera_config['public_key'][:20]}...")
    print(f"User ID: {user_id}")
    print(f"Secret Key: {secret_key}")
    print()

    # Try HTTP GET method as mentioned in Tradera docs
    base_url = "https://api.tradera.com/v3/publicservice.asmx"

    # Method 1: HTTP GET with query parameters
    print("🔍 Testing HTTP GET method...")
    get_url = f"{base_url}/FetchToken"

    params = {
        'userId': user_id,
        'secretKey': secret_key
    }

    headers = {
        'User-Agent': 'Tradera-POC-Client/1.0'
    }

    try:
        print(f"GET URL: {get_url}")
        print(f"Parameters: {params}")
        print()

        response = requests.get(get_url, params=params, headers=headers, timeout=30)

        print(f"HTTP Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print()

        if response.status_code == 200:
            print("✅ HTTP GET successful!")
            print(f"Response length: {len(response.text)} characters")
            print()
            print("Response content:")
            print(response.text[:1000])  # First 1000 characters

            # Check if response contains token
            if 'AuthToken' in response.text:
                print("✅ AuthToken found in response!")
            else:
                print("❌ AuthToken NOT found in response")

        else:
            print(f"❌ HTTP GET failed with status: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ Error with HTTP GET: {e}")

    print("\n" + "="*50)

    # Method 2: HTTP POST with form data
    print("🔍 Testing HTTP POST method...")
    post_url = f"{base_url}/FetchToken"

    post_data = {
        'userId': str(user_id),
        'secretKey': secret_key
    }

    try:
        print(f"POST URL: {post_url}")
        print(f"Form data: {post_data}")
        print()

        response = requests.post(post_url, data=post_data, headers=headers, timeout=30)

        print(f"HTTP Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print()

        if response.status_code == 200:
            print("✅ HTTP POST successful!")
            print(f"Response length: {len(response.text)} characters")
            print()
            print("Response content:")
            print(response.text[:1000])  # First 1000 characters

            # Check if response contains token
            if 'AuthToken' in response.text:
                print("✅ AuthToken found in response!")
            else:
                print("❌ AuthToken NOT found in response")

        else:
            print(f"❌ HTTP POST failed with status: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ Error with HTTP POST: {e}")

if __name__ == "__main__":
    main()
