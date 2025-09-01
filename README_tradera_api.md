# Tradera API Client

A Python client for Tradera's SOAP API services, based on their developer documentation. This client provides a comprehensive interface to interact with Tradera's marketplace for listing items, managing inventory, and handling orders.

## Features

- **Full SOAP Service Support**: Implements all six Tradera API services
- **Authentication Management**: Token-based user authentication with automatic expiry handling
- **Rate Limiting**: Built-in rate limiting (100 calls per 24 hours) with automatic tracking
- **Error Handling**: Comprehensive error handling for SOAP faults and transport issues
- **Request Queuing**: Support for Tradera's request queuing system with result tracking
- **Type Safety**: Full type hints and comprehensive documentation

## Services Implemented

### 1. PublicService
- Basic methods requiring only AppId and ServiceKey
- No user authentication required

### 2. RestrictedService (Core)
- **AddShopItem**: Add new items to your shop
- **UpdateShopItem**: Update existing items
- **RemoveShopItem**: Remove items (sets end date to past)
- **GetSellerItems**: Retrieve your shop items
- **GetSellerOrders**: Get orders for your items
- **SetSellerOrderAsShipped**: Mark orders as shipped
- **SetQuantityOnShopItems**: Bulk quantity updates
- **SetPriceOnShopItems**: Bulk price updates
- **GetItemFieldValues**: Get field definitions and valid values
- **FetchToken**: User authentication

### 3. OrderService
- Order management and processing

### 4. SearchService
- Search functionality across Tradera

### 5. ListingService
- Auction-specific methods

### 6. BuyerService
- Buyer operations and actions

## Installation

1. **Install Dependencies**:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   ```bash
   export TRADERA_APP_ID="your_application_id"
   export TRADERA_SERVICE_KEY="your_service_key"
   export TRADERA_PUBLIC_KEY="your_public_key"
   export TRADERA_USERNAME="your_tradera_username"
   export TRADERA_PASSWORD="your_tradera_password"
   ```

## Quick Start

### Basic Usage

```python
from tradera_api_client import TraderaAPIClient

# Initialize client
client = TraderaAPIClient(
    app_id="your_app_id",
    service_key="your_service_key",
    public_key="your_public_key"
)

# Authenticate user
token = client.fetch_token("username", "password")

# Get your items
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

# Check request status
results = client.get_request_results(request_id)
print(f"Request results: {results}")
```

### Creating Items

```python
from tradera_api_client import create_sample_item_data

# Create sample item data
item = create_sample_item_data(
    title="Vintage Camera",
    description="Beautiful vintage camera in excellent condition",
    price=299.0,
    category_id=14,  # Photo, Cameras & Optics
    quantity=1
)

# Add to Tradera
request_id = client.add_shop_item(item)
```

## Configuration

The client uses environment variables for configuration. Create a `.env` file or set them in your shell:

```bash
# Required API credentials
TRADERA_APP_ID=your_application_id
TRADERA_SERVICE_KEY=your_service_key
TRADERA_PUBLIC_KEY=your_public_key

# Optional settings
TRADERA_BASE_URL=https://api.tradera.com
TRADERA_TIMEOUT=30

# User credentials for testing
TRADERA_USERNAME=your_username
TRADERA_PASSWORD=your_password
```

## Rate Limiting

Tradera enforces a rate limit of **100 API calls per 24 hours**. The client automatically:

- Tracks your call count
- Prevents exceeding the limit
- Provides information about remaining calls
- Resets the counter after 24 hours

```python
# Check rate limit status
rate_info = client.get_rate_limit_info()
print(f"Calls remaining: {rate_info['calls_remaining']}")
print(f"Time until reset: {rate_info['time_until_reset']:.0f} seconds")
```

## Error Handling

The client provides comprehensive error handling:

```python
from tradera_api_client import TraderaAPIError

try:
    items = client.get_seller_items()
except TraderaAPIError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Testing

Run the test suite to verify your setup:

```bash
python test_tradera_api.py
```

Or run the simple example:

```bash
python example_usage.py
```

## API Registration

To use this client, you need to register your application with Tradera:

1. **Go to Tradera Developer Program**: Visit their developer registration page
2. **Create Application**:
   - Name: `poc` (or your preferred name)
   - Description: `testing API for item listing`
   - Accept/Reject return URLs (if required)
3. **Get Credentials**: You'll receive:
   - Application ID (AppId)
   - Service Key
   - Public Key

## Important Notes

- **Request Queuing**: Most item operations are queued and processed asynchronously
- **Token Expiry**: User tokens expire after 24 hours and must be refreshed
- **Category IDs**: Use `GetItemFieldValues()` to get valid category IDs and other field values
- **Payment Methods**: PayPal is not supported as of September 15, 2020
- **Bulk Operations**: Use bulk methods for updating multiple items efficiently

## Troubleshooting

### Common Issues

1. **"Failed to initialize API clients"**
   - Check your internet connection
   - Verify the base URL is correct
   - Ensure all credentials are set

2. **"Rate limit exceeded"**
   - Wait for the 24-hour window to reset
   - Check your call count with `get_rate_limit_info()`

3. **"SOAP fault"**
   - Verify your credentials are correct
   - Check that the API endpoint is accessible
   - Ensure you're using the correct method parameters

4. **"Token not found in response"**
   - Check your username/password
   - Verify your public key is correct
   - Ensure the API service is responding correctly

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Examples

See the following files for complete examples:

- `example_usage.py` - Basic usage patterns
- `test_tradera_api.py` - Comprehensive test suite
- `config.py` - Configuration management

## Support

For Tradera API support:
- Contact: `apiadmin@tradera.com`
- Include your application ID when requesting help
- Request access to RestrictedService if needed
- Request higher rate limits if required

## License

This client is provided as-is for educational and development purposes. Please refer to Tradera's terms of service for commercial usage.

## Contributing

Feel free to submit issues and enhancement requests. When contributing:

1. Follow the existing code style
2. Add tests for new functionality
3. Update documentation as needed
4. Ensure all tests pass

---

**Note**: This client is based on Tradera's public API documentation. The actual API endpoints and response formats may vary. Always test thoroughly before using in production.
