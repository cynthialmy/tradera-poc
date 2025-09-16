# Tradera API Client POC

A Python client for Tradera's SOAP API services, providing full access to their marketplace for listing items, managing inventory, and handling orders.

## Features

- **Full SOAP Service Support**: Implements all six Tradera API services
- **Authentication Management**: Token-based user authentication with automatic expiry handling
- **Rate Limiting**: Built-in rate limiting (100 calls per 24 hours) with automatic tracking
- **Error Handling**: Comprehensive error handling for SOAP faults and transport issues
- **Request Queuing**: Support for Tradera's request queuing system with result tracking
- **Type Safety**: Full type hints and comprehensive documentation
- **Testing Tools**: Complete test suite with sample data and response validation

### Services Implemented

1. **PublicService** - Basic methods requiring only AppId and ServiceKey
2. **RestrictedService** - Core functionality for authenticated users
3. **OrderService** - Order management and processing
4. **SearchService** - Search functionality across Tradera
5. **ListingService** - Auction-specific methods
6. **BuyerService** - Buyer operations and actions

### Core Methods

- **Authentication**: `fetch_token()`, `generate_login_url()`
- **Item Management**: `get_seller_items()`, `add_shop_item()`, `add_item()`, `update_shop_item()`
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

#### Get Tradera Credentials
1. Register your application at Tradera's developer program
2. Get your App ID, Service Key, and Public Key
3. Set up callback URLs for authentication

#### Set Environment Variables
Create a `.env` file with your credentials:

```bash
# Required API credentials from Tradera developer program
TRADERA_APP_ID=your_application_id
TRADERA_SERVICE_KEY=your_service_key
TRADERA_PUBLIC_KEY=your_public_key

# Optional API settings
TRADERA_BASE_URL=https://api.tradera.com/v3
TRADERA_TIMEOUT=30
```

#### Authentication Flow
1. **Start auth server**: `python auth_server.py`
2. **Set callback URLs** in Tradera app settings:
   - Accept: `http://localhost:8000/auth/success`
   - Reject: `http://localhost:8000/auth/failure`
3. **Complete authorization** on Tradera website
4. **Token captured** automatically by local server

#### Detailed Authentication Steps
```python
# Step 1: Generate Login URL
login_url, secret_key = client.generate_login_url()

# Step 2: User visits URL and authorizes your application

# Step 3: Fetch Token
token = client.fetch_token(user_id, secret_key)

# Step 4: Make Authenticated Calls
items = client.get_seller_items()
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

# Add a new auction item
item_data = {
    'Title': 'Test Auction Item',
    'Description': 'This is a test auction item',
    'CategoryId': 12,  # Electronics
    'StartPrice': 1000,  # 10.00 SEK
    'Duration': 7,  # 7 days
    'AutoCommit': True
}

result = client.add_item(item_data)
print(f"Item created: {result}")
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

## 📖 Interactive Documentation

### Swagger UI
Start the interactive API documentation server:

```bash
# Start Swagger UI server
python3 swagger_server.py
```

Then visit: **http://localhost:3000**

Features:
- ✅ **Interactive API Explorer** - Browse all endpoints
- ✅ **Request/Response Examples** - See real SOAP examples
- ✅ **Try It Out** - Test endpoints directly from browser
- ✅ **Authentication Guide** - Step-by-step auth flow
- ✅ **Schema Documentation** - Complete data models

### Postman Collection
Import `postman_collections/Tradera_API_Collection.json` into Postman for:
- Pre-configured requests with proper SOAP headers
- Environment variables for easy credential management
- Complete test suite for all API methods

### Access Points
| Service          | URL                            | Description                   |
| ---------------- | ------------------------------ | ----------------------------- |
| **Swagger UI**   | http://localhost:3000          | Interactive API documentation |
| **API Examples** | http://localhost:3000/examples | Request/response examples     |
| **Health Check** | http://localhost:3000/health   | Server status                 |
| **OpenAPI Spec** | http://localhost:3000/api-docs | Raw OpenAPI JSON              |

## 📚 API Reference

### Core Client Methods

| Method                  | Description                   | Authentication Required |
| ----------------------- | ----------------------------- | ----------------------- |
| `fetch_token()`         | Get user authentication token | No                      |
| `generate_login_url()`  | Generate authorization URL    | No                      |
| `get_seller_items()`    | Get items from your shop      | Yes                     |
| `add_shop_item()`       | Add new shop item             | Yes                     |
| `add_item()`            | Add new auction item          | Yes                     |
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

## 📊 Current Status

- **Authentication**: 100% ✅ Working
- **AddItem Method**: 100% ✅ Working (with fallback to AddItemXml)
- **Response Parsing**: 100% ✅ Working
- **Error Handling**: 100% ✅ Working
- **Rate Limiting**: 100% ✅ Working
- **Core Functionality**: 95% ✅ Working

## 📖 Additional Documentation

- **Setup Guide**: [SETUP_GUIDE.md](https://github.com/cynthialmy/tradera-poc/blob/main/SETUP_GUIDE.md) - Step-by-step setup instructions
- **Postman Collection**: [`postman_collections/`](https://github.com/cynthialmy/tradera-poc/tree/main/postman_collections) - API reference collection
- **Sample Payloads**: [`sample_payloads/`](https://github.com/cynthialmy/tradera-poc/tree/main/sample_payloads) - Example API requests and responses
- **Response Logs**: [`response_logs/`](https://github.com/cynthialmy/tradera-poc/tree/main/response_logs) - Real API response examples

## Support

If you encounter issues:

1. Check the [Common Issues](#-common-issues--solutions) section
2. Review the Tradera API documentation
3. Open an issue with detailed error information
4. Include your Tradera API version and configuration details

---

**Note**: This client is designed for Tradera API v3. For older versions, please refer to the appropriate documentation.
