#!/usr/bin/env python3
"""
Test script for Tradera API Client

This script demonstrates how to use the Tradera API client to:
1. Initialize the client
2. Authenticate with a user
3. Test basic API operations
4. Handle errors and rate limiting

Run this script to test your Tradera API integration.
"""

import os
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, Any

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tradera_api_client import TraderaAPIClient, TraderaAPIError, create_sample_item_data
from config import get_config, validate_config, print_config_summary

def test_client_initialization():
    """Test client initialization"""
    print("Testing client initialization...")

    config = get_config()
    tradera_config = config['tradera']

    try:
        print(f"Debug: Using base_url: {tradera_config['base_url']}")
        client = TraderaAPIClient(
            app_id=tradera_config['app_id'],
            service_key=tradera_config['service_key'],
            public_key=tradera_config['public_key'],
            base_url=tradera_config['base_url'],
            timeout=tradera_config['timeout']
        )
        print("✅ Client initialized successfully")
        return client
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return None

def test_authentication(client: TraderaAPIClient):
    """Test user authentication"""
    print("\nTesting user authentication...")

    # Get user ID from environment variable or use the known one
    user_id = os.getenv('TRADERA_TEST_USER_ID', '5986811')  # Default to known user ID

    try:
        user_id = int(user_id)
    except ValueError:
        print(f"⚠️  Invalid user ID format: {user_id}, using default: 5986811")
        user_id = 5986811

    # For testing, we'll use a sample secret key
    # In production, you'd generate this and use it in the login URL
    secret_key = "07829484-381D-433E-B437-84BCF22FDBFC"

    try:
        token = client.fetch_token(user_id, secret_key)
        print(f"✅ Authentication successful, token: {token[:10]}...")
        return True
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

def test_get_item_field_values(client: TraderaAPIClient):
    """Test getting item field values"""
    print("\nTesting GetItemFieldValues...")

    try:
        # Use a sample category ID for testing
        category_id = 12  # Electronics category
        field_values = client.get_item_field_values(category_id)
        print(f"✅ Retrieved field values for category {category_id}: {len(field_values)} fields")

        # Print some key information
        for key, value in list(field_values.items())[:5]:  # Show first 5
            print(f"  {key}: {value}")

        if len(field_values) > 5:
            print(f"  ... and {len(field_values) - 5} more fields")

        return field_values
    except Exception as e:
        print(f"❌ Failed to get field values: {e}")
        return None

def test_login_url_generation(client: TraderaAPIClient):
    """Test login URL generation"""
    print("\nTesting Login URL Generation...")

    try:
        login_url, secret_key = client.generate_login_url()
        print(f"✅ Generated login URL successfully")
        print(f"  URL: {login_url[:80]}...")
        print(f"  Secret Key: {secret_key}")

        # Test with custom secret key
        custom_secret = "CUSTOM-SECRET-KEY-FOR-TESTING"
        login_url2, secret_key2 = client.generate_login_url(custom_secret)
        print(f"✅ Generated login URL with custom secret key")
        print(f"  Secret Key: {secret_key2}")

        return secret_key
    except Exception as e:
        print(f"❌ Failed to generate login URL: {e}")
        return None

def test_get_seller_items(client: TraderaAPIClient):
    """Test getting seller items"""
    print("\nTesting GetSellerItems...")

    try:
        items = client.get_seller_items()
        print(f"✅ Retrieved {len(items)} seller items")

        # Show sample items
        for i, item in enumerate(items[:3]):  # Show first 3
            print(f"  Item {i+1}: {item.get('Title', 'No title')} - {item.get('StartingPrice', 'No price')} kr")

        if len(items) > 3:
            print(f"  ... and {len(items) - 3} more items")

        return items
    except Exception as e:
        print(f"❌ Failed to get seller items: {e}")
        return None

def test_add_sample_item(client: TraderaAPIClient, field_values: Dict[str, Any] = None):
    """Test adding a sample item"""
    print("\nTesting AddShopItem...")

    # Create sample item data
    sample_item = create_sample_item_data(
        title="Test Item - API Test",
        description="This is a test item created via the Tradera API client for testing purposes.",
        price=50.0,
        category_id=12,  # Electronics category
        quantity=1
    )

    try:
        request_id = client.add_shop_item(sample_item)
        print(f"✅ Item addition queued successfully. Request ID: {request_id}")

        # Wait a bit and check results
        print("Waiting 5 seconds before checking results...")
        time.sleep(5)

        results = client.get_request_results(request_id)
        print(f"✅ Request results: {results}")

        return request_id
    except Exception as e:
        print(f"❌ Failed to add sample item: {e}")
        return None

def test_rate_limiting(client: TraderaAPIClient):
    """Test rate limiting information"""
    print("\nTesting rate limiting...")

    try:
        rate_info = client.get_rate_limit_info()
        print("✅ Rate limit information:")
        print(f"  Calls made: {rate_info['calls_made']}")
        print(f"  Calls remaining: {rate_info['calls_remaining']}")
        print(f"  Window start: {rate_info['window_start']}")
        print(f"  Time until reset: {rate_info['time_until_reset']:.0f} seconds")

        return rate_info
    except Exception as e:
        print(f"❌ Failed to get rate limit info: {e}")
        return None

def test_error_handling(client: TraderaAPIClient):
    """Test error handling with invalid requests"""
    print("\nTesting error handling...")

    # Test with invalid item ID
    try:
        results = client.get_request_results("invalid_request_id")
        print(f"⚠️  Unexpected success with invalid request ID: {results}")
    except TraderaAPIError as e:
        print(f"✅ Expected error caught: {e}")
    except Exception as e:
        print(f"⚠️  Unexpected error type: {type(e).__name__}: {e}")

def run_full_test():
    """Run the complete test suite"""
    print("Tradera API Client Test Suite")
    print("=" * 50)

    # Check configuration first
    print_config_summary()
    print()

    if not validate_config():
        print("❌ Configuration validation failed. Please set required environment variables.")
        return False

    # Test client initialization
    client = test_client_initialization()
    if not client:
        return False

    # Test authentication
    auth_success = test_authentication(client)

    # Test basic operations (these might fail without proper authentication)
    field_values = test_get_item_field_values(client)

    # Test login URL generation (doesn't require authentication)
    test_login_url_generation(client)

    if auth_success:
        # These tests require authentication
        test_get_seller_items(client)
        test_add_sample_item(client, field_values)

    # Test rate limiting and error handling
    test_rate_limiting(client)
    test_error_handling(client)

    print("\n" + "=" * 50)
    print("Test suite completed!")

    if auth_success:
        print("✅ All tests completed successfully")
    else:
        print("⚠️  Some tests were skipped due to authentication issues")

    return True

def main():
    """Main function"""
    try:
        success = run_full_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error during testing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
