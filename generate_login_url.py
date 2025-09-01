#!/usr/bin/env python3
"""
Generate Tradera Login URL

This script helps you generate the correct login URL for Tradera's tokenlogin.aspx page
based on the Option 2 authentication flow (recommended by Tradera).

Usage:
    python generate_login_url.py
"""

import uuid
from config import get_config

def generate_secret_key():
    """Generate a UUID-based secret key as recommended by Tradera"""
    return str(uuid.uuid4()).upper()

def generate_login_url(app_id, public_key, secret_key):
    """Generate the Tradera login URL"""
    base_url = "https://api.tradera.com/tokenlogin.aspx"
    return f"{base_url}?appId={app_id}&pkey={public_key}&skey={secret_key}"

def main():
    """Main function"""
    print("🔐 Tradera Login URL Generator")
    print("=" * 50)

    # Get configuration
    config = get_config()
    tradera_config = config['tradera']

    # Check if we have the required credentials
    if not tradera_config['app_id'] or not tradera_config['public_key']:
        print("❌ Missing required API credentials!")
        print("Please set the following environment variables:")
        print("  TRADERA_APP_ID")
        print("  TRADERA_PUBLIC_KEY")
        print("\nExample:")
        print("  export TRADERA_APP_ID='your_app_id'")
        print("  export TRADERA_PUBLIC_KEY='your_public_key'")
        return

    # Generate a secret key
    secret_key = generate_secret_key()

    # Generate the login URL
    login_url = generate_login_url(
        tradera_config['app_id'],
        tradera_config['public_key'],
        secret_key
    )

    print("✅ Configuration loaded successfully!")
    print(f"App ID: {tradera_config['app_id']}")
    print(f"Public Key: {tradera_config['public_key'][:20]}...")
    print(f"Secret Key: {secret_key}")
    print()

    print("🔗 Generated Login URL:")
    print("=" * 50)
    print(login_url)
    print("=" * 50)
    print()

    print("📋 Next Steps:")
    print("1. Copy the login URL above")
    print("2. Open it in a web browser")
    print("3. Log in with your Tradera credentials")
    print("4. You'll be redirected to your auth server")
    print("5. Use the userId and secret key to call FetchToken")
    print()

    print("💾 Save this secret key - you'll need it for FetchToken:")
    print(f"Secret Key: {secret_key}")
    print()

    print("🔧 Tradera Application Settings:")
    print("- Accept Return URL: http://localhost:8000/auth/success")
    print("- Reject Return URL: http://localhost:8000/auth/failure")
    print("- Show token: Disabled (Option 2)")
    print()

    print("🚀 Ready to test! Start your auth server and visit the login URL.")

if __name__ == "__main__":
    main()
