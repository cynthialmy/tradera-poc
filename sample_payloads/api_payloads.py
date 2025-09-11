#!/usr/bin/env python3
"""
Sample Payloads for Tradera API

This module contains essential sample payloads for Tradera API methods.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List

def get_fetch_token_payload(user_id: int = 5986811, secret_key: str = "07829484-381D-433E-B437-84BCF22FDBFC") -> Dict[str, Any]:
    """Sample payload for FetchToken method"""
    return {
        "userId": user_id,
        "secretKey": secret_key
    }

def get_add_item_payload() -> Dict[str, Any]:
    """Sample payload for AddItem method"""
    return {
        "Title": "Test Auction Item",
        "Description": "This is a test auction item created via the Tradera API",
        "CategoryId": 12,  # Electronics
        "StartPrice": 1000,  # 10.00 SEK
        "ReservePrice": 1200,  # 12.00 SEK
        "BuyItNowPrice": 2000,  # 20.00 SEK
        "Duration": 7,  # 7 days
        "AutoCommit": True,
        "ItemType": 1,  # Auction
        "VAT": 25,  # 25% VAT
        "ShippingCondition": "Standard shipping",
        "PaymentCondition": "Payment within 3 days",
        "DescriptionLanguageCodeIso2": "en"
    }

def get_add_shop_item_payload() -> Dict[str, Any]:
    """Sample payload for AddShopItem method"""
    return {
        "Title": "Test Shop Item",
        "Description": "This is a test shop item created via the Tradera API",
        "CategoryId": 12,  # Electronics
        "Price": 500,  # 5.00 SEK
        "Quantity": 1,
        "AbsoluteQuantity": 1,
        "VAT": 25,  # 25% VAT
        "ShippingCondition": "Free shipping",
        "PaymentCondition": "Payment within 3 days",
        "DescriptionLanguageCodeIso2": "en"
    }

def get_search_category_count_payload() -> Dict[str, Any]:
    """Sample payload for SearchCategoryCount method"""
    return {
        "CategoryId": 0,  # All categories
        "SearchWords": "",  # No search words
        "ItemCondition": "",  # All conditions
        "PriceMinimum": 0,
        "PriceMaximum": 0,
        "ItemType": "",  # All types
        "SellerType": "",  # All sellers
        "Mode": "",  # Default mode
        "ItemStatus": ""  # All statuses
    }

def get_get_seller_transactions_payload() -> Dict[str, Any]:
    """Sample payload for GetSellerTransactions method"""
    return {
        "MinTransactionDate": None,
        "MaxTransactionDate": None,
        "Filter": "New"  # Only new transactions
    }

def get_leave_feedback_payload() -> Dict[str, Any]:
    """Sample payload for LeaveFeedback method"""
    return {
        "TransactionId": 12345,
        "Comment": "Great transaction! Fast shipping and item as described.",
        "Type": "Positive"  # Positive, Negative, or Neutral
    }

def get_update_transaction_status_payload() -> Dict[str, Any]:
    """Sample payload for UpdateTransactionStatus method"""
    return {
        "TransactionId": 12345,
        "MarkAsPaidConfirmed": True,
        "MarkedAsShipped": True,
        "MarkShippingBooked": True
    }

def get_shop_settings_payload() -> Dict[str, Any]:
    """Sample payload for SetShopSettings method"""
    return {
        "CompanyInformation": "Your Company Name",
        "PurchaseTerms": "Standard purchase terms and conditions",
        "ShowGalleryMode": True,
        "ShowAuctionView": True,
        "LogoInformation": {
            "ImageFormat": "Jpeg",
            "ImageData": b'',  # Base64 encoded image data
            "RemoveLogo": False
        },
        "BannerColor": "#FFFFFF",
        "IsTemporaryClosed": False,
        "TemporaryClosedMessage": "",
        "ContactInformation": "contact@yourcompany.com",
        "LogoImageUrl": "",
        "MaxActiveItems": 100,
        "MaxInventoryItems": 1000
    }

def get_all_payloads() -> Dict[str, Dict[str, Any]]:
    """Get all sample payloads as a dictionary"""
    return {
        "fetch_token": get_fetch_token_payload(),
        "add_item": get_add_item_payload(),
        "add_shop_item": get_add_shop_item_payload(),
        "search_category_count": get_search_category_count_payload(),
        "get_seller_transactions": get_get_seller_transactions_payload(),
        "leave_feedback": get_leave_feedback_payload(),
        "update_transaction_status": get_update_transaction_status_payload(),
        "shop_settings": get_shop_settings_payload()
    }

# Convenience functions for common use cases
def get_auction_item_payload(title: str = "Test Auction Item",
                           description: str = "Test description",
                           category_id: int = 12,
                           start_price: int = 1000) -> Dict[str, Any]:
    """Create a custom auction item payload"""
    payload = get_add_item_payload()
    payload.update({
        "Title": title,
        "Description": description,
        "CategoryId": category_id,
        "StartPrice": start_price
    })
    return payload

def get_shop_item_payload(title: str = "Test Shop Item",
                         description: str = "Test description",
                         category_id: int = 12,
                         price: int = 500) -> Dict[str, Any]:
    """Create a custom shop item payload"""
    payload = get_add_shop_item_payload()
    payload.update({
        "Title": title,
        "Description": description,
        "CategoryId": category_id,
        "Price": price
    })
    return payload
