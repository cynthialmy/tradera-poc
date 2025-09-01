#!/usr/bin/env python3
"""
Configuration file for Tradera API Client

This file contains configuration settings and credentials for the Tradera API.
Copy this file to config_local.py and fill in your actual credentials.
"""

import os
from typing import Optional, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Tradera API Configuration
TRADERA_CONFIG = {
    # Your application credentials from Tradera developer program
    'app_id': os.getenv('TRADERA_APP_ID', ''),
    'service_key': os.getenv('TRADERA_SERVICE_KEY', ''),
    'public_key': os.getenv('TRADERA_PUBLIC_KEY', ''),

    # API base URL (default from documentation)
    'base_url': os.getenv('TRADERA_BASE_URL', 'https://api.tradera.com/v3'),

    # Request timeout in seconds
    'timeout': int(os.getenv('TRADERA_TIMEOUT', '30')),

    # User credentials for testing
    'username': os.getenv('TRADERA_USERNAME', ''),
    'password': os.getenv('TRADERA_PASSWORD', ''),
}

# Test item configuration
TEST_ITEM_CONFIG = {
    # Sample category IDs (you'll need to get actual ones from GetItemFieldValues)
    'categories': {
        'electronics': 12,      # Datorer & Tillbehör
        'books': 11,           # Böcker & Tidningar
        'clothing': 16,        # Kläder
        'home': 31,            # Hem & Hushåll
        'sports': 25,          # Sport & Fritid
    },

    # Sample payment methods (get actual IDs from GetItemFieldValues)
    'payment_methods': {
        'tradera_payment': 1,  # Tradera's integrated payment
        'bank_transfer': 2,    # Bank transfer
        'cash': 3,             # Cash on pickup
    },

    # Sample shipping options (get actual IDs from GetItemFieldValues)
    'shipping_options': {
        'postnord': 1,         # PostNord
        'schenker': 2,         # DB Schenker
        'dhl': 3,              # DHL
        'pickup': 4,           # Pickup
    },

    # Sample item conditions
    'conditions': [
        'New',
        'Used - Like New',
        'Used - Very Good',
        'Used - Good',
        'Used - Acceptable',
        'For parts or not working'
    ]
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'tradera_api.log'
}

# Rate limiting configuration
RATE_LIMIT_CONFIG = {
    'calls_per_day': 100,
    'window_hours': 24,
    'retry_delay': 60,  # seconds to wait when rate limited
}

def get_authorization_token() -> Optional[str]:
    """
    Get the authorization token from the token file created by the auth server

    Returns:
        The authorization token string, or None if not found
    """
    token_file = 'tradera_token.txt'

    if not os.path.exists(token_file):
        return None

    try:
        with open(token_file, 'r') as f:
            lines = f.readlines()

        # Find the token line (skip comments and empty lines)
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                return line

        return None
    except Exception as e:
        print(f"Warning: Could not read token file: {e}")
        return None

def get_authorization_info() -> Optional[Dict[str, str]]:
    """
    Get the authorization info from the auth info file created by the auth server

    Returns:
        Dictionary with authorization info, or None if not found
    """
    auth_file = 'tradera_auth_info.txt'

    if not os.path.exists(auth_file):
        return None

    try:
        auth_info = {}
        with open(auth_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    auth_info[key.strip()] = value.strip()

        return auth_info if auth_info else None
    except Exception as e:
        print(f"Warning: Could not read auth info file: {e}")
        return None

def get_config() -> dict:
    """Get the complete configuration"""
    return {
        'tradera': TRADERA_CONFIG,
        'test_items': TEST_ITEM_CONFIG,
        'logging': LOGGING_CONFIG,
        'rate_limit': RATE_LIMIT_CONFIG
    }

def validate_config() -> bool:
    """Validate that required configuration is present"""
    required_fields = ['app_id', 'service_key', 'public_key']

    for field in required_fields:
        if not TRADERA_CONFIG.get(field):
            print(f"ERROR: Missing required configuration field: {field}")
            print("Please set the TRADERA_{field.upper()} environment variable")
            return False

    return True

def print_config_summary():
    """Print a summary of the current configuration"""
    print("Tradera API Configuration Summary")
    print("=" * 40)

    config = get_config()

    print(f"App ID: {'*' * len(config['tradera']['app_id']) if config['tradera']['app_id'] else 'NOT SET'}")
    print(f"Service Key: {'*' * len(config['tradera']['service_key']) if config['tradera']['service_key'] else 'NOT SET'}")
    print(f"Public Key: {'*' * len(config['tradera']['public_key']) if config['tradera']['public_key'] else 'NOT SET'}")
    print(f"Base URL: {config['tradera']['base_url']}")
    print(f"Timeout: {config['tradera']['timeout']}s")
    print(f"Username: {config['tradera']['username'] if config['tradera']['username'] else 'NOT SET'}")
    print(f"Password: {'*' * len(config['tradera']['password']) if config['tradera']['password'] else 'NOT SET'}")

    # Check for authorization info
    auth_info = get_authorization_info()
    if auth_info:
        print(f"Authorization Info: Available (User ID: {auth_info.get('User ID', 'Unknown')})")
        print(f"  Expiration: {auth_info.get('Expiration', 'Unknown')}")
    else:
        print("Authorization Info: NOT SET (run auth_server.py and complete login flow)")

    # Check for authorization token (legacy)
    auth_token = get_authorization_token()
    if auth_token:
        print(f"Legacy Token: {'*' * min(20, len(auth_token))}... (from file)")
    else:
        print("Legacy Token: NOT SET")

    print(f"\nRate Limit: {config['rate_limit']['calls_per_day']} calls per {config['rate_limit']['window_hours']} hours")
    print(f"Logging Level: {config['logging']['level']}")

    if not validate_config():
        print("\n⚠️  Configuration validation failed!")
        print("Please set the required environment variables before using the API client.")
    else:
        print("\n✅ Configuration validation passed!")

if __name__ == "__main__":
    print_config_summary()
