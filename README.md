# 🚀 Tradera API Client

A comprehensive Python client for Tradera's SOAP API services, providing full access to their marketplace for listing items, managing inventory, and handling orders.

## ✨ Features

- **Full SOAP Service Support**: Implements all six Tradera API services
- **Authentication Management**: Token-based user authentication with automatic expiry handling
- **Rate Limiting**: Built-in rate limiting (100 calls per 24 hours) with automatic tracking
- **Error Handling**: Comprehensive error handling for SOAP faults and transport issues
- **Request Queuing**: Support for Tradera's request queuing system with result tracking
- **Type Safety**: Full type hints and comprehensive documentation

## 🏗️ Architecture

### Services Implemented

1. **PublicService** - Basic methods requiring only AppId and ServiceKey
2. **RestrictedService** - Core functionality for authenticated users
3. **OrderService** - Order management and processing
4. **SearchService** - Search functionality across Tradera
5. **ListingService** - Auction-specific methods
6. **BuyerService** - Buyer operations and actions

### Core Methods

- **Authentication**: `fetch_token()`, `generate_login_url()`
- **Item Management**: `get_seller_items()`, `add_shop_item()`, `update_shop_item()`
- **Order Management**: `get_seller_orders()`, `set_seller_order_as_shipped()`
- **Search & Discovery**: `get_categories()`, `get_item_field_values()`
- **Rate Limiting**: `get_rate_limit_info()`

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd tradera-poc

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file with your Tradera API credentials:

```bash
# Required API credentials from Tradera developer program
TRADERA_APP_ID=your_application_id
TRADERA_SERVICE_KEY=your_service_key
TRADERA_PUBLIC_KEY=your_public_key

# Optional API settings
TRADERA_BASE_URL=https://api.tradera.com/v3
TRADERA_TIMEOUT=30
```

### 3. Basic Usage

```python
from tradera_api_client import TraderaAPIClient

# Initialize client
client = TraderaAPIClient(
    app_id="your_app_id",
    service_key="your_service_key",
    public_key="your_public_key"
)

# Generate login URL for user authorization
login_url, secret_key = client.generate_login_url()

# After user authorization, fetch token
token = client.fetch_token(user_id=12345, secret_key=secret_key)

# Get your shop items
items = client.get_seller_items()
print(f"You have {len(items)} items")

# Add a new item
item_data = {
    'Title': 'Test Item',
    'Description': 'This is a test item',
    'StartingPrice': 50.0,
    'CategoryId': 12,  # Electronics
    'Quantity': 1
}

request_id = client.add_shop_item(item_data)
print(f"Item queued with request ID: {request_id}")
```

## 🔐 Authentication Flow

### Option 1: Direct Token Retrieval
1. Generate login URL with `client.generate_login_url()`
2. User visits URL and authorizes your application
3. Call `client.fetch_token()` with user ID and secret key

### Option 2: Redirect with Token
1. Set up callback URLs in Tradera Developer Center
2. User authorizes and gets redirected with token
3. Extract token from callback URL

### Option 3: Display Token in URL
1. Enable "Display token" in Tradera Developer Center
2. User authorizes and gets redirected with token in URL
3. Extract token directly from callback

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python test_tradera_api.py

# Test specific functionality
python -c "
from tradera_api_client import TraderaAPIClient
from config import get_config

config = get_config()
client = TraderaAPIClient(**config['tradera'])

# Test authentication
token = client.fetch_token(user_id=12345, secret_key='your_secret_key')
print(f'Token: {token}')

# Test rate limiting
rate_info = client.get_rate_limit_info()
print(f'Rate limit: {rate_info}')
"
```

## 📚 API Reference

### Core Client Methods

| Method                  | Description                   | Authentication Required |
| ----------------------- | ----------------------------- | ----------------------- |
| `fetch_token()`         | Get user authentication token | No                      |
| `generate_login_url()`  | Generate authorization URL    | No                      |
| `get_seller_items()`    | Get items from your shop      | Yes                     |
| `add_shop_item()`       | Add new item to shop          | Yes                     |
| `get_rate_limit_info()` | Get current rate limit status | No                      |

### Configuration

| Environment Variable  | Description                 | Required         |
| --------------------- | --------------------------- | ---------------- |
| `TRADERA_APP_ID`      | Your Tradera application ID | Yes              |
| `TRADERA_SERVICE_KEY` | Your Tradera service key    | Yes              |
| `TRADERA_PUBLIC_KEY`  | Your Tradera public key     | Yes              |
| `TRADERA_BASE_URL`    | API base URL                | No (default: v3) |
| `TRADERA_TIMEOUT`     | Request timeout in seconds  | No (default: 30) |

## 🚨 Common Issues & Solutions

### "Invalid application id"
- Verify your App ID is properly registered in Tradera Developer Center
- Check that Service Key matches exactly what's shown in Developer Center
- Ensure your application has API access enabled

### "403 Forbidden"
- Verify your API credentials are correct
- Check that your application has the right permissions
- Ensure you're within rate limits

### "FetchTokenResult not found"
- This usually means the response format has changed
- Check the latest Tradera API documentation
- Verify SOAP headers are correctly formatted

## 📖 Documentation

- **Setup Guide**: `SETUP_GUIDE.md` - Step-by-step setup instructions
- **API Reference**: `README_tradera_api.md` - Detailed API documentation
- **Configuration**: `config.py` - Configuration management details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. Check the [Common Issues](#-common-issues--solutions) section
2. Review the Tradera API documentation
3. Open an issue with detailed error information
4. Include your Tradera API version and configuration details

---

**Note**: This client is designed for Tradera API v3. For older versions, please refer to the appropriate documentation.
