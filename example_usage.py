#!/usr/bin/env python3
"""
Simple example of using the Tradera API Client

This script shows basic usage patterns for the Tradera API client.
"""

import os
import sys
from datetime import datetime, timedelta

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tradera_api_client import TraderaAPIClient, create_sample_item_data
from config import get_config

def main():
    """Main example function"""
    print("Tradera API Client - Simple Example")
    print("=" * 40)

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
        print("\nExample:")
        print("  export TRADERA_APP_ID='your_app_id'")
        print("  export TRADERA_SERVICE_KEY='your_service_key'")
        print("  export TRADERA_PUBLIC_KEY='your_public_key'")
        return

    try:
        # Initialize the client
        print("Initializing Tradera API client...")
        client = TraderaAPIClient(
            app_id=tradera_config['app_id'],
            service_key=tradera_config['service_key'],
            public_key=tradera_config['public_key'],
            base_url=tradera_config['base_url']
        )
        print("✅ Client initialized successfully")

        # Show rate limit info
        rate_info = client.get_rate_limit_info()
        print(f"\nRate limit info: {rate_info['calls_remaining']} calls remaining")

                # Example: Basic client operations
        print("\nBasic client operations:")
        print("✅ Client initialized successfully")
        print("✅ Rate limiting configured")
        print("✅ SOAP client ready for API calls")

                # Example: Authenticate with user (if credentials provided)
        # Note: For now, we only have FetchToken which requires user_id and secret_key
        # You'll need to get these from Tradera's documentation or support
        print("\n⚠️  Note: FetchToken requires user_id (integer) and secret_key")
        print("   These are different from username/password")
        print("   You'll need to get these from Tradera's documentation or support")

        # Example: Show how to use FetchToken when you have the credentials
        print("\nExample FetchToken usage:")
        print("   token = client.fetch_token(user_id=12345, secret_key='your_secret_key')")

        # Example: Create sample item data (for reference)
        print("\nExample item data structure:")
        sample_item = create_sample_item_data(
            title="Example Item",
            description="This is an example item description",
            price=100.0,
            category_id=12,  # Electronics
            quantity=1
        )

        print("Sample item fields:")
        for key, value in sample_item.items():
            print(f"  {key}: {value}")

        print("\n" + "=" * 40)
        print("Example completed successfully!")
        print("\nNext steps:")
        print("1. Test the API with: python test_tradera_api.py")
        print("2. Modify the example to suit your needs")
        print("3. Check the tradera_api_client.py file for all available methods")

    except Exception as e:
        print(f"❌ Error during example execution: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    main()
