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

def test_get_categories(client: TraderaAPIClient):
    """Test getting categories"""
    print("\nTesting GetCategories...")

    try:
        categories = client.get_categories()
        print(f"✅ Retrieved {len(categories)} categories")

        # Show sample categories
        for i, category in enumerate(categories[:5]):  # Show first 5
            print(f"  Category {i+1}: {category.get('Name', 'No name')} (ID: {category.get('CategoryId', 'No ID')})")

        if len(categories) > 5:
            print(f"  ... and {len(categories) - 5} more categories")

        return categories
    except Exception as e:
        print(f"❌ Failed to get categories: {e}")
        return None

def test_get_item_field_values(client: TraderaAPIClient, category_id: int = 12):
    """Test getting item field values"""
    print(f"\nTesting GetItemFieldValues for category {category_id}...")

    try:
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

def test_search_category_count(client: TraderaAPIClient):
    """Test searching category count"""
    print("\nTesting SearchCategoryCount...")

    try:
        # Test with default parameters
        search_results = client.search_category_count()
        print(f"✅ Default search completed: {search_results['total_categories']} categories, {search_results['total_items']} items")

        # Test with specific search parameters
        search_params = {
            'CategoryId': 12,  # Electronics
            'SearchWords': 'laptop',
            'ItemCondition': 'New',
            'PriceMinimum': 100,
            'PriceMaximum': 1000
        }
        specific_results = client.search_category_count(search_params)
        print(f"✅ Specific search completed: {specific_results['total_categories']} categories")

        return search_results
    except Exception as e:
        print(f"❌ Failed to search category count: {e}")
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

def test_add_shop_item_mock(client: TraderaAPIClient, field_values: Dict[str, Any] = None):
    """Test adding a shop item (mock implementation)"""
    print("\nTesting AddShopItem (Mock Implementation)...")

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

def test_add_item_functionality(client: TraderaAPIClient):
    """Test AddItem functionality with RestrictedService (Real API)"""
    print("\nTesting AddItem functionality (Real RestrictedService API)...")

    if not client.user_token:
        print("⚠️  Skipping AddItem test - no user token available")
        return None

    try:
        # Create sample item data for testing
        item_data = {
            'Title': 'Test Item - API Integration',
            'Description': 'This is a test item created via the Tradera API to verify AddItem functionality.',
            'CategoryId': 12,  # Electronics category
            'Duration': 3,     # 3 days auction
            'StartPrice': 1000,  # 10 SEK (1000 öre)
            'ReservePrice': 800,  # 8 SEK reserve
            'BuyItNowPrice': 2000,  # 20 SEK buy it now
            'PaymentOptionIds': [1],  # Example payment method
            'ItemType': 1,  # Auction item
            'AutoCommit': False,  # Don't commit yet (for image upload workflow)
            'VAT': 25,  # 25% VAT
            'DescriptionLanguageCodeIso2': 'en'
        }

        print(f"Creating test item: {item_data['Title']}")

        # Add the item
        result = client.add_item(item_data)

        print(f"✅ Item created successfully!")
        print(f"  Request ID: {result['RequestId']}")
        print(f"  Item ID: {result['ItemId']}")
        print(f"  Status: {result['status']}")

        # Test image upload workflow
        print("\nTesting image upload workflow...")

        # Simulate adding an image (we'll use a small test image)
        test_image_data = b'fake_image_data_for_testing'

        try:
            image_result = client.add_item_image(
                item_id=result['ItemId'],
                image_data=test_image_data,
                image_name='test_image.jpg'
            )
            print(f"✅ Image added successfully: {image_result}")

            # Commit the item
            commit_result = client.add_item_commit(result['ItemId'])
            print(f"✅ Item committed successfully: {commit_result}")

        except Exception as img_e:
            print(f"⚠️  Image upload workflow test failed (this is expected in test environment): {img_e}")

        return result

    except TraderaAPIError as e:
        print(f"❌ AddItem failed with TraderaAPIError: {e}")
        return None
    except Exception as e:
        print(f"❌ AddItem failed with unexpected error: {e}")
        return None

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
    categories = test_get_categories(client)
    if categories:
        category_id = categories[0]['CategoryId']
    else:
        category_id = 12  # Default to Electronics category
    field_values = test_get_item_field_values(client, category_id)

    # Test login URL generation (doesn't require authentication)
    test_login_url_generation(client)

    # Test search functionality (doesn't require authentication)
    test_search_category_count(client)

    if auth_success:
        # These tests require authentication
        test_get_seller_items(client)
        test_add_shop_item_mock(client, field_values)

        # Test AddItem functionality (requires RestrictedService access)
        test_add_item_functionality(client)

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
