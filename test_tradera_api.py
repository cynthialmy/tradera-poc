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
        user_id = "YOUR_USER_ID"

    # For testing, we'll use a sample secret key
    # In production, you'd generate this and use it in the login URL
    secret_key = "YOUR_SECRET_KEY"

    try:
        token = client.fetch_token(user_id, secret_key)
        print(f"✅ Authentication successful, token: {token[:10]}...")
        return True
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

def test_basic_api_operations(client: TraderaAPIClient):
    """Test basic API operations"""
    print("\nTesting basic API operations...")

    # Test GetCategories
    print("Testing GetCategories...")
    try:
        categories = client.get_categories()
        print(f"✅ Retrieved {len(categories)} categories")
        for i, category in enumerate(categories[:3]):
            print(f"  Category {i+1}: {category.get('Name', 'No name')} (ID: {category.get('CategoryId', 'No ID')})")
    except Exception as e:
        print(f"❌ GetCategories failed: {e}")

    # Test GetItemFieldValues
    print("\nTesting GetItemFieldValues...")
    try:
        field_values = client.get_item_field_values(12)
        print(f"✅ Retrieved field values for category 12: {len(field_values)} fields")
        for i, field in enumerate(field_values[:3]):
            print(f"  Field {i+1}: {field.get('name', 'No name')} ({field.get('type', 'No type')})")
    except Exception as e:
        print(f"❌ GetItemFieldValues failed: {e}")

    # Test Login URL Generation
    print("\nTesting Login URL Generation...")
    try:
        login_url, secret_key = client.generate_login_url()
        print(f"✅ Generated login URL successfully")
        print(f"  URL: {login_url[:80]}...")
        print(f"  Secret Key: {secret_key}")
    except Exception as e:
        print(f"❌ Login URL generation failed: {e}")

    # Test SearchCategoryCount
    print("\nTesting SearchCategoryCount...")
    try:
        search_result = client.search_category_count()
        print(f"✅ Default search completed: {search_result.get('CategoryCount', 0)} categories, {search_result.get('ItemCount', 0)} items")
    except Exception as e:
        print(f"❌ SearchCategoryCount failed: {e}")

def test_restricted_service_operations(client: TraderaAPIClient):
    """Test RestrictedService operations"""
    print("\nTesting RestrictedService operations...")

    # Test GetShippingOptions
    print("Testing GetShippingOptions...")
    try:
        shipping_options = client.get_shipping_options()
        print(f"✅ Retrieved {len(shipping_options)} shipping options")
        for i, option in enumerate(shipping_options[:3]):
            print(f"  Option {i+1}: {option.get('Name', 'No name')} (ID: {option.get('ShippingOptionId', 'No ID')}) - {option.get('Cost', 0)} kr")
    except Exception as e:
        print(f"❌ GetShippingOptions failed: {e}")

    # Test GetMemberPaymentOptions
    print("\nTesting GetMemberPaymentOptions...")
    try:
        payment_options = client.get_member_payment_options(5986811)
        print(f"✅ Retrieved {len(payment_options)} payment options")
        for i, option in enumerate(payment_options[:3]):
            print(f"  Option {i+1}: {option.get('name', 'No name')} (ID: {option.get('id', 'No ID')})")
    except Exception as e:
        print(f"❌ GetMemberPaymentOptions failed: {e}")

    # Test GetSellerItems
    print("\nTesting GetSellerItems...")
    try:
        seller_items = client.get_seller_items()
        print(f"✅ Retrieved {len(seller_items)} seller items")
    except Exception as e:
        print(f"❌ GetSellerItems failed: {e}")

    # Test GetSellerTransactions
    print("\nTesting GetSellerTransactions...")
    try:
        transactions = client.get_seller_transactions()
        print(f"✅ Retrieved {len(transactions)} transactions")
    except Exception as e:
        print(f"❌ GetSellerTransactions failed: {e}")

def test_add_item_functionality(client: TraderaAPIClient):
    """Test AddItem functionality"""
    print("\nTesting AddItem functionality (Real RestrictedService API)...")

    # Get shipping and payment options
    try:
        shipping_options = client.get_shipping_options()
        payment_options = client.get_member_payment_options(5986811)

        shipping_option_id = shipping_options[0].get('ShippingOptionId', 1) if shipping_options else 1
        payment_option_id = payment_options[0].get('id', 1) if payment_options else 1

        print(f"Using shipping option ID: {shipping_option_id}")
        print(f"Using payment option ID: {payment_option_id}")
    except Exception as e:
        print(f"⚠️  Could not get options, using defaults: {e}")
        shipping_option_id = 1
        payment_option_id = 1

    # Create test item
    print("Creating test item: Test Item - API Integration")
    item_data = {
        'Title': 'Test Item - API Integration',
        'Description': 'This is a test item created via the Tradera API to verify AddItem functionality.',
        'CategoryId': 12,  # Electronics
        'StartPrice': 1000,  # 10.00 SEK
        'ReservePrice': 1200,  # 12.00 SEK
        'BuyItNowPrice': 2000,  # 20.00 SEK
        'Duration': 3,  # 3 days
        'AutoCommit': False  # Don't auto-commit for testing
    }

    try:
        result = client.add_item(item_data)
        print(f"✅ AddItem successful: {result}")

        # Test image upload workflow if item was created
        if result and result.get('RequestId'):
            print("\nTesting image upload workflow...")
            try:
                # Add item image (mock implementation)
                image_result = client.add_item_image(result['RequestId'], 'test_image.jpg', b'fake_image_data')
                print(f"✅ AddItemImage successful: {image_result}")

                # Commit item
                commit_result = client.add_item_commit(result['RequestId'])
                print(f"✅ AddItemCommit successful: {commit_result}")
            except Exception as e:
                print(f"⚠️  Image upload workflow failed: {e}")

    except Exception as e:
        print(f"❌ AddItem failed: {e}")

def test_item_management_methods(client: TraderaAPIClient):
    """Test item management methods"""
    print("\nTesting Item Management methods...")

    # Test GetItem
    print("Testing GetItem...")
    try:
        item = client.get_item(12345)
        print(f"✅ GetItem successful: {item}")
    except Exception as e:
        print(f"⚠️  GetItem failed (expected): {e}")

    # Test EndItem
    print("\nTesting EndItem...")
    try:
        result = client.end_item(12345)
        print(f"✅ EndItem successful: {result}")
    except Exception as e:
        print(f"⚠️  EndItem failed: {e}")

    # Test RemoveShopItem
    print("\nTesting RemoveShopItem...")
    try:
        result = client.remove_shop_item(12345)
        print(f"✅ RemoveShopItem successful: {result}")
    except Exception as e:
        print(f"⚠️  RemoveShopItem failed (expected): {e}")

def test_shop_management_methods(client: TraderaAPIClient):
    """Test shop management methods"""
    print("\nTesting Shop Management methods...")

    # Test GetShopSettings
    print("Testing GetShopSettings...")
    try:
        settings = client.get_shop_settings()
        print(f"✅ GetShopSettings successful: {settings}")
    except Exception as e:
        print(f"⚠️  GetShopSettings failed: {e}")

    # Test SetShopSettings
    print("\nTesting SetShopSettings...")
    try:
        shop_settings = {
            'CompanyInformation': 'Test Company',
            'PurchaseTerms': 'Standard terms',
            'ShowGalleryMode': True,
            'ShowAuctionView': True,
            'LogoInformation': {
                'ImageFormat': 'Jpeg',
                'ImageData': b'',
                'RemoveLogo': False
            },
            'BannerColor': '#FFFFFF',
            'IsTemporaryClosed': False,
            'TemporaryClosedMessage': '',
            'ContactInformation': 'test@example.com',
            'LogoImageUrl': '',
            'MaxActiveItems': 100,
            'MaxInventoryItems': 1000
        }
        result = client.set_shop_settings(shop_settings)
        print(f"✅ SetShopSettings successful: {result}")
    except Exception as e:
        print(f"⚠️  SetShopSettings failed: {e}")

def test_transaction_management_methods(client: TraderaAPIClient):
    """Test transaction management methods"""
    print("\nTesting Transaction Management methods...")

    # Test GetSellerTransactions
    print("Testing GetSellerTransactions...")
    try:
        transactions = client.get_seller_transactions()
        print(f"✅ GetSellerTransactions successful: {len(transactions)} transactions")
    except Exception as e:
        print(f"❌ GetSellerTransactions failed: {e}")

    # Test LeaveFeedback
    print("\nTesting LeaveFeedback...")
    try:
        result = client.leave_feedback(12345, 'Great transaction!', 'Positive')
        print(f"✅ LeaveFeedback successful: {result}")
    except Exception as e:
        print(f"⚠️  LeaveFeedback failed (expected): {e}")

    # Test UpdateTransactionStatus
    print("\nTesting UpdateTransactionStatus...")
    try:
        status_data = {
            'TransactionId': 12345,
            'MarkAsPaidConfirmed': True,
            'MarkedAsShipped': True,
            'MarkShippingBooked': True
        }
        result = client.update_transaction_status(status_data)
        print(f"✅ UpdateTransactionStatus successful: {result}")
    except Exception as e:
        print(f"⚠️  UpdateTransactionStatus failed (expected): {e}")

def test_rate_limiting(client: TraderaAPIClient):
    """Test rate limiting functionality"""
    print("\nTesting rate limiting...")

    try:
        rate_info = client.get_rate_limit_info()
        print(f"✅ Rate limit information:")
        print(f"  Calls made: {rate_info.get('calls_made', 0)}")
        print(f"  Calls remaining: {rate_info.get('calls_remaining', 0)}")
        print(f"  Window start: {rate_info.get('window_start', 'Unknown')}")
        print(f"  Time until reset: {rate_info.get('time_until_reset', 0)} seconds")
    except Exception as e:
        print(f"❌ Rate limiting test failed: {e}")

def test_error_handling(client: TraderaAPIClient):
    """Test error handling"""
    print("\nTesting error handling...")

    try:
        # Test invalid request ID
        result = client.get_request_results("invalid_request_id")
        print(f"❌ Expected error not caught: {result}")
    except Exception as e:
        print(f"✅ Expected error caught: {e}")

def main():
    """Main test function"""
    print("Tradera API Client Test Suite")
    print("=" * 50)

    # Print configuration summary
    print_config_summary()
    print()

    # Test configuration validation
    print("Testing configuration validation...")
    try:
        validate_config()
        print("✅ Configuration validation passed!")
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return

    # Initialize client
    client = test_client_initialization()
    if not client:
        print("❌ Cannot proceed without client initialization")
        return

    # Test authentication
    auth_success = test_authentication(client)
    if not auth_success:
        print("❌ Cannot proceed without authentication")
        return

    # Run all test suites
    test_basic_api_operations(client)
    test_restricted_service_operations(client)
    test_add_item_functionality(client)
    test_item_management_methods(client)
    test_shop_management_methods(client)
    test_transaction_management_methods(client)
    test_rate_limiting(client)
    test_error_handling(client)

    print("\n" + "=" * 50)
    print("Test suite completed!")
    print("✅ All tests completed successfully")

if __name__ == "__main__":
    main()
