#!/usr/bin/env python3
"""
Tradera API Authentication Flow Script

This script provides a comprehensive authentication flow for the Tradera API,
including token generation, user authorization, and token management.

Usage:
    python auth_flow.py [--user-id USER_ID] [--secret-key SECRET_KEY] [--quick]
"""

import argparse
import sys
import os
from datetime import datetime, timedelta
from typing import Optional, Tuple

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tradera_api_client import TraderaAPIClient, TraderaAPIError
from config import get_config, validate_config

def generate_login_url(client: TraderaAPIClient, secret_key: Optional[str] = None) -> Tuple[str, str]:
    """Generate a login URL for user authorization"""
    print("🔐 Generating Tradera login URL...")

    try:
        login_url, secret_key = client.generate_login_url(secret_key)

        print(f"✅ Login URL generated successfully!")
        print(f"📋 Secret Key: {secret_key}")
        print(f"🌐 Login URL: {login_url}")
        print()
        print("📝 Instructions:")
        print("1. Copy the login URL above")
        print("2. Open it in your web browser")
        print("3. Log in to your Tradera account")
        print("4. Authorize the application")
        print("5. Note the user ID from the authorization page")
        print("6. Use the secret key and user ID for token generation")

        return login_url, secret_key

    except Exception as e:
        print(f"❌ Failed to generate login URL: {e}")
        return None, None

def fetch_token(client: TraderaAPIClient, user_id: int, secret_key: str) -> Optional[str]:
    """Fetch authentication token for a user"""
    print(f"🔑 Fetching token for user {user_id}...")

    try:
        token = client.fetch_token(user_id, secret_key)
        print(f"✅ Token fetched successfully!")
        print(f"🎫 Token: {token}")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return token

    except Exception as e:
        print(f"❌ Failed to fetch token: {e}")
        return None

def quick_authenticate() -> Optional[str]:
    """Quick authentication using known test credentials"""
    print("🚀 Quick Authentication (Test Mode)")
    print("=" * 40)

    # Validate configuration
    if not validate_config():
        print("❌ Configuration validation failed. Please set required environment variables.")
        return None

    # Initialize client
    try:
        config = get_config()
        client = TraderaAPIClient(
            app_id=config['tradera']['app_id'],
            service_key=config['tradera']['service_key'],
            public_key=config['tradera']['public_key'],
            base_url=config['tradera']['base_url'],
            timeout=config['tradera']['timeout']
        )
        print("✅ Client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return None

    # Use known test credentials
    user_id = "YOUR_USER_ID"
    secret_key = "YOUR_SECRET_KEY"

    print(f"👤 Using test user ID: {user_id}")
    print(f"🔐 Using test secret key: {secret_key[:8]}...")

    # Fetch token
    token = fetch_token(client, user_id, secret_key)

    if token:
        print("\n🎉 Quick authentication completed successfully!")
        print("You can now use this token for API calls.")

    return token

def interactive_authenticate() -> Optional[str]:
    """Interactive authentication flow"""
    print("🔐 Interactive Authentication Flow")
    print("=" * 40)

    # Validate configuration
    if not validate_config():
        print("❌ Configuration validation failed. Please set required environment variables.")
        return None

    # Initialize client
    try:
        config = get_config()
        client = TraderaAPIClient(
            app_id=config['tradera']['app_id'],
            service_key=config['tradera']['service_key'],
            public_key=config['tradera']['public_key'],
            base_url=config['tradera']['base_url'],
            timeout=config['tradera']['timeout']
        )
        print("✅ Client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return None

    # Generate login URL
    login_url, secret_key = generate_login_url(client)
    if not login_url:
        return None

    print("\n⏳ Waiting for user authorization...")
    print("Press Enter after you have completed the authorization process...")
    input()

    # Get user ID from user
    try:
        user_id = int(input("Enter your Tradera user ID: "))
    except ValueError:
        print("❌ Invalid user ID format")
        return None

    # Fetch token
    token = fetch_token(client, user_id, secret_key)

    if token:
        print("\n🎉 Authentication completed successfully!")
        print("You can now use this token for API calls.")

    return token

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Tradera API Authentication Flow")
    parser.add_argument("--user-id", type=int, help="Tradera user ID")
    parser.add_argument("--secret-key", type=str, help="Secret key from login URL")
    parser.add_argument("--quick", action="store_true", help="Use quick authentication with test credentials")

    args = parser.parse_args()

    if args.quick:
        token = quick_authenticate()
    elif args.user_id and args.secret_key:
        # Direct authentication with provided credentials
        print("🔐 Direct Authentication")
        print("=" * 30)

        if not validate_config():
            print("❌ Configuration validation failed. Please set required environment variables.")
            return

        try:
            config = get_config()
            client = TraderaAPIClient(
                app_id=config['tradera']['app_id'],
                service_key=config['tradera']['service_key'],
                public_key=config['tradera']['public_key'],
                base_url=config['tradera']['base_url'],
                timeout=config['tradera']['timeout']
            )
            token = fetch_token(client, args.user_id, args.secret_key)
        except Exception as e:
            print(f"❌ Failed to initialize client: {e}")
            return
    else:
        # Interactive mode
        token = interactive_authenticate()

    if token:
        print(f"\n✅ Authentication successful!")
        print(f"Token: {token}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("\n❌ Authentication failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
