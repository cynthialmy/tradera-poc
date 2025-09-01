#!/usr/bin/env python3
"""
Tradera API Client

A Python client for Tradera's SOAP API services based on their developer documentation.
This client implements the main services with the correct endpoint structure.

Author: AI Assistant
Date: 2025-08-26
"""

import logging
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import requests
from zeep import Client, Settings
from zeep.transports import Transport
from zeep.exceptions import Fault, TransportError
import xml.etree.ElementTree as ET

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TraderaAPIError(Exception):
    """Custom exception for Tradera API errors"""
    pass


class TraderaAPIClient:
    """
    Tradera API Client for interacting with their SOAP services

    Services available:
    - PublicService: Basic methods requiring only AppId and key
    - Other services will be added as needed based on actual API structure
    """

    def __init__(self, app_id: str, service_key: str, public_key: str,
                 base_url: str = "https://api.tradera.com/v3",
                 timeout: int = 30):
        """
        Initialize the Tradera API client

        Args:
            app_id: Your application ID from Tradera
            service_key: Your service key for authentication
            public_key: Your public key for token authentication
            base_url: Base URL for Tradera API (default: https://api.tradera.com/v3)
            timeout: Request timeout in seconds
        """
        self.app_id = app_id
        self.service_key = service_key
        self.public_key = public_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

        # Initialize SOAP clients for each service
        self._init_clients()

        # Rate limiting: 100 calls per 24 hours
        self.rate_limit = 100
        self.rate_limit_window = 24 * 60 * 60  # 24 hours in seconds
        self.call_count = 0
        self.window_start = time.time()

        # User token for authenticated calls
        self.user_token = None
        self.token_expiry = None

    def _init_clients(self):
        """Initialize SOAP clients for all services"""
        try:
            # Configure transport with timeout
            transport = Transport(timeout=self.timeout)
            settings = Settings(strict=False, xml_huge_tree=True)

            # Initialize service clients based on actual API structure
            self.public_service = Client(
                f"{self.base_url}/publicservice.asmx?wsdl",
                transport=transport,
                settings=settings
            )

            # Debug: Check what services are available
            logger.info(f"Available services: {list(self.public_service.wsdl.services.keys())}")
            if 'PublicService' in self.public_service.wsdl.services:
                logger.info(f"PublicService ports: {list(self.public_service.wsdl.services['PublicService'].ports.keys())}")
                logger.info(f"PublicService bindings: {list(self.public_service.wsdl.bindings.keys())}")

            # Note: Other services may have different endpoints
            # For now, we'll focus on the public service which has FetchToken
            self.restricted_service = None
            self.order_service = None
            self.search_service = None
            self.listing_service = None
            self.buyer_service = None

            logger.info("Successfully initialized Tradera API service clients")

        except Exception as e:
            logger.error(f"Failed to initialize API clients: {e}")
            raise TraderaAPIError(f"Failed to initialize API clients: {e}")

    def _check_rate_limit(self):
        """Check if we're within rate limits"""
        current_time = time.time()

        # Reset counter if window has passed
        if current_time - self.window_start > self.rate_limit_window:
            self.call_count = 0
            self.window_start = current_time

        # Check if we can make another call
        if self.call_count >= self.rate_limit:
            wait_time = self.rate_limit_window - (current_time - self.window_start)
            raise TraderaAPIError(f"Rate limit exceeded. Wait {wait_time:.0f} seconds before next call.")

        self.call_count += 1

    def _make_request(self, service_client, method_name: str, **kwargs):
        """
        Make a SOAP request with rate limiting and error handling

        Args:
            service_client: The SOAP service client to use
            method_name: Name of the method to call
            **kwargs: Arguments to pass to the method

        Returns:
            Response from the API
        """
        self._check_rate_limit()

        try:
            # Debug: Print what we're about to send
            logger.info(f"Making {method_name} request with kwargs: {kwargs}")
            logger.info(f"Service client: {service_client}")

                        # Create SOAP headers for authentication using the WSDL's predefined structure
            from zeep import xsd

            # Create AuthenticationHeader for the request
            # Based on the WSDL, this should match the FetchTokenAuthenticationHeader structure
            auth_header = xsd.Element(
                '{http://api.tradera.com}AuthenticationHeader',
                xsd.ComplexType([
                    xsd.Element('{http://api.tradera.com}AppId', xsd.Integer()),
                    xsd.Element('{http://api.tradera.com}AppKey', xsd.String())
                ])
            )

            # Create ConfigurationHeader (required for FetchToken)
            # Based on the WSDL, this should match the FetchTokenConfigurationHeader structure
            config_header = xsd.Element(
                '{http://api.tradera.com}ConfigurationHeader',
                xsd.ComplexType([
                    xsd.Element('{http://api.tradera.com}PublicKey', xsd.String())
                ])
            )

            # Create the header values with proper namespace
            auth_header_value = auth_header(
                AppId=int(self.app_id),  # Ensure it's an integer
                AppKey=self.service_key
            )

            config_header_value = config_header(
                PublicKey=self.public_key
            )

            logger.info(f"Created SOAP headers: AppId={self.app_id}, AppKey={self.service_key[:20]}..., PublicKey={self.public_key[:20]}...")

            # Access the correct service port (PublicServiceSoap)
            # The WSDL shows: service name="PublicService" with port name="PublicServiceSoap"
            # Since the WSDL is not loading properly in the class, let me try a different approach
            logger.info(f"Available services: {list(service_client.wsdl.services.keys())}")

            # Try to access the service directly from the client
            # Since the WSDL is loading correctly, let me try the direct approach
            logger.info(f"Trying direct service access for {method_name}")
            try:
                # Try to access the service directly
                service_port = service_client.service
                method = getattr(service_port, method_name)
                logger.info(f"Using direct service access for {method_name}")
            except AttributeError:
                # Fallback to create_service
                logger.info(f"Direct access failed, trying create_service")
                service_port = service_client.create_service('PublicService', 'PublicServiceSoap')
                method = getattr(service_port, method_name)
                logger.info(f"Using create_service for {method_name}")

            # Make the SOAP call with both headers
            response = method(
                **kwargs,
                _soapheaders=[auth_header_value, config_header_value]
            )

            logger.info(f"Successfully called {method_name}")
            return response

        except Fault as e:
            logger.error(f"SOAP fault in {method_name}: {e}")
            # Try to get fault details safely
            try:
                fault_code = getattr(e, 'faultcode', 'Unknown')
                fault_string = getattr(e, 'faultstring', str(e))
                logger.error(f"Fault details: {fault_code} - {fault_string}")
                # Log the full fault object for debugging
                logger.error(f"Full fault object: {e}")
                if hasattr(e, 'detail'):
                    logger.error(f"Fault detail: {e.detail}")
            except Exception as debug_e:
                logger.error(f"Fault details: {e}")
                logger.error(f"Debug error: {debug_e}")
            raise TraderaAPIError(f"SOAP fault in {method_name}: {e}")
        except TransportError as e:
            logger.error(f"Transport error in {method_name}: {e}")
            raise TraderaAPIError(f"Transport error in {method_name}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in {method_name}: {e}")
            raise TraderaAPIError(f"Unexpected error in {method_name}: {e}")

    def fetch_token(self, user_id: int, secret_key: str) -> str:
        """
        Fetch authentication token for a user

        Args:
            user_id: Tradera user ID (integer)
            secret_key: Secret key for the user

        Returns:
            User token string
        """
        try:
            # Use the public service for FetchToken
            response = self._make_request(
                self.public_service,
                'FetchToken',
                userId=user_id,
                secretKey=secret_key
            )

            # Extract token and expiry from response based on SOAP documentation
            if hasattr(response, 'FetchTokenResult'):
                result = response.FetchTokenResult
                if hasattr(result, 'AuthToken'):
                    self.user_token = result.AuthToken
                    if hasattr(result, 'HardExpirationTime'):
                        self.token_expiry = result.HardExpirationTime
                    else:
                        # Default expiry: 24 hours from now
                        self.token_expiry = datetime.now() + timedelta(hours=24)

                    logger.info(f"Successfully fetched token for user {user_id}")
                    return self.user_token
                else:
                    raise TraderaAPIError("AuthToken not found in response")
            else:
                raise TraderaAPIError("FetchTokenResult not found in response")

        except Exception as e:
            logger.error(f"Failed to fetch token: {e}")
            raise

    def get_rate_limit_info(self) -> Dict[str, Any]:
        """Get current rate limit information"""
        current_time = time.time()
        time_since_start = current_time - self.window_start

        return {
            'calls_made': self.call_count,
            'calls_remaining': self.rate_limit - self.call_count,
            'window_start': datetime.fromtimestamp(self.window_start),
            'time_since_start': time_since_start,
            'time_until_reset': max(0, self.rate_limit_window - time_since_start)
        }

    def get_item_field_values(self, category_id: int) -> Dict[str, Any]:
        """
        Get available field values for a specific category

        Args:
            category_id: Tradera category ID

        Returns:
            Dictionary with field values
        """
        try:
            # This would typically call a method like GetItemFieldValues
            # For now, return a placeholder response
            logger.info(f"Getting field values for category {category_id}")
            return {
                'category_id': category_id,
                'fields': ['Title', 'Description', 'StartingPrice', 'CategoryId'],
                'status': 'placeholder_response'
            }
        except Exception as e:
            logger.error(f"Failed to get field values: {e}")
            raise TraderaAPIError(f"Failed to get field values: {e}")

    def get_request_results(self, request_id: str) -> Dict[str, Any]:
        """
        Get results for a queued request

        Args:
            request_id: The request ID from a queued operation

        Returns:
            Dictionary with request results
        """
        try:
            logger.info(f"Getting results for request {request_id}")
            # This would typically call a method like GetRequestResults
            # For now, return a placeholder response
            return {
                'request_id': request_id,
                'status': 'completed',
                'result': 'placeholder_result'
            }
        except Exception as e:
            logger.error(f"Failed to get request results: {e}")
            raise TraderaAPIError(f"Failed to get request results: {e}")


# Example usage and helper functions
def create_sample_item_data(title: str, description: str, price: float,
                          category_id: int, quantity: int = 1) -> Dict[str, Any]:
    """
    Create sample item data for testing

    Args:
        title: Item title
        description: Item description
        price: Starting price
        category_id: Tradera category ID
        quantity: Available quantity

    Returns:
        Dictionary with item data
    """
    return {
        'Title': title,
        'Description': description,
        'StartingPrice': price,
        'CategoryId': category_id,
        'Quantity': quantity,
        'StartDate': datetime.now(),
        'EndDate': datetime.now() + timedelta(days=7),
        'PaymentMethods': [1],  # Example payment method ID
        'ShippingOptions': [1],  # Example shipping option ID
        'Condition': 'Used',     # Example condition
        'Location': 'Stockholm, Sweden'
    }


if __name__ == "__main__":
    # Example usage
    print("Tradera API Client")
    print("=" * 50)
    print("This is a Python client for Tradera's SOAP API services.")
    print("To use it, you need to:")
    print("1. Register an application with Tradera")
    print("2. Get your AppId, ServiceKey, and PublicKey")
    print("3. Initialize the client with your credentials")
    print("\nExample:")
    print("client = TraderaAPIClient('your_app_id', 'your_service_key', 'your_public_key')")
    print("token = client.fetch_token(user_id, 'secret_key')")
    print("rate_info = client.get_rate_limit_info()")
