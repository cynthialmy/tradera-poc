#!/usr/bin/env python3
"""
Test FetchToken Call

This script tests the FetchToken method using the User ID obtained from the authorization flow
and the secret key used in the login URL.

Usage:
    python test_fetch_token.py
"""

from tradera_api_client import TraderaAPIClient
from config import get_config

def main():
    """Main function"""
    print("🔐 Testing Tradera FetchToken")
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

    # Secret key used in the login URL (you need to replace this with the actual one you used)
    secret_key = "07829484-381D-433E-B437-84BCF22FDBFC"  # Replace with your actual secret key

    print(f"✅ Configuration loaded successfully!")
    print(f"App ID: {tradera_config['app_id']}")
    print(f"Service Key: {tradera_config['service_key'][:20]}...")
    print(f"Public Key: {tradera_config['public_key'][:20]}...")
    print(f"User ID: {user_id}")
    print(f"Secret Key: {secret_key}")
    print()

    try:
        # Initialize the API client
        print("🚀 Initializing Tradera API client...")
        client = TraderaAPIClient(
            app_id=tradera_config['app_id'],
            service_key=tradera_config['service_key'],
            public_key=tradera_config['public_key']
        )
        print("✅ API client initialized successfully!")
        print()

        # Test the connection first
        print("🔍 Testing API connection...")
        rate_info = client.get_rate_limit_info()
        print(f"✅ API connection successful!")
        print(f"Rate limit info: {rate_info}")
        print()

        # Call FetchToken
        print("🔐 Calling FetchToken...")
        print(f"User ID: {user_id}")
        print(f"Secret Key: {secret_key}")
        print()

        token = client.fetch_token(user_id=user_id, secret_key=secret_key)

        print("🎉 SUCCESS! FetchToken returned:")
        print("=" * 50)
        print(f"Token: {token}")
        print("=" * 50)
        print()

        print("📋 What you can do now:")
        print("1. Use this token for authenticated API calls")
        print("2. Test item listing operations")
        print("3. The token is automatically stored in the client")
        print()

        print("🚀 Ready to test item listing APIs!")

    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("🔍 Troubleshooting:")
        print("1. Make sure you're using the correct secret key from your login URL")
        print("2. Check that your Tradera application is properly registered")
        print("3. Verify your API credentials are correct")
        print("4. Ensure you're within the rate limits")

if __name__ == "__main__":
    main()

