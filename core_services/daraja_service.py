"""
Daraja API Service Module
Handles M-Pesa payment integration using Safaricom's Daraja API
"""

import requests
import json
import base64
from datetime import datetime
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class DarajaAPIClient:
    """
    Daraja API Client for M-Pesa integration
    
    Credentials needed in settings:
    - DARAJA_CONSUMER_KEY
    - DARAJA_CONSUMER_SECRET
    - DARAJA_BUSINESS_SHORTCODE
    - DARAJA_PASSKEY
    - DARAJA_ENVIRONMENT: 'sandbox' or 'production'
    """
    
    def __init__(self):
        """Initialize Daraja API client"""
        self.consumer_key = getattr(settings, 'DARAJA_CONSUMER_KEY', '')
        self.consumer_secret = getattr(settings, 'DARAJA_CONSUMER_SECRET', '')
        self.business_shortcode = getattr(settings, 'DARAJA_BUSINESS_SHORTCODE', '')
        self.passkey = getattr(settings, 'DARAJA_PASSKEY', '')
        self.environment = getattr(settings, 'DARAJA_ENVIRONMENT', 'sandbox')
        
        if self.environment == 'sandbox':
            self.base_url = 'https://sandbox.safaricom.co.ke'
        else:
            self.base_url = 'https://api.safaricom.co.ke'
        
        self.access_token = None
        self.token_expiry = None
    
    def _get_access_token(self):
        """
        Get OAuth access token from Daraja API
        
        Returns:
            str: Access token
        """
        try:
            url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
            
            auth = (self.consumer_key, self.consumer_secret)
            
            response = requests.get(url, auth=auth, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data.get('access_token')
            
            logger.info("Successfully obtained Daraja access token")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting Daraja access token: {str(e)}")
            return None
    
    def _get_timestamp(self):
        """Get current timestamp in format YYYYMMDDHHmmss"""
        return datetime.now().strftime('%Y%m%d%H%M%S')
    
    def _generate_password(self, timestamp):
        """
        Generate password for STK Push
        
        Args:
            timestamp: Current timestamp
            
        Returns:
            str: Encoded password
        """
        password_str = f"{self.business_shortcode}{self.passkey}{timestamp}"
        encoded_password = base64.b64encode(password_str.encode()).decode()
        return encoded_password
    
    def stk_push(self, phone_number, amount, account_reference, description, callback_url):
        """
        Initiate STK Push for M-Pesa payment
        
        Args:
            phone_number: Customer's phone number (254XXXXXXXXX format)
            amount: Amount in KES
            account_reference: Order reference/number
            description: Payment description
            callback_url: URL for payment callback
            
        Returns:
            dict: API response with CheckoutRequestID
        """
        try:
            # Get access token
            token = self._get_access_token()
            if not token:
                return {
                    'success': False,
                    'error': 'Failed to get access token'
                }
            
            # Prepare request data
            timestamp = self._get_timestamp()
            password = self._generate_password(timestamp)
            
            url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'BusinessShortCode': self.business_shortcode,
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': int(amount),
                'PartyA': phone_number,
                'PartyB': self.business_shortcode,
                'PhoneNumber': phone_number,
                'CallBackURL': callback_url,
                'AccountReference': account_reference,
                'TransactionDesc': description,
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('ResponseCode') == '0':
                logger.info(f"STK Push initiated for phone {phone_number}: {data.get('CheckoutRequestID')}")
                return {
                    'success': True,
                    'checkout_request_id': data.get('CheckoutRequestID'),
                    'response_code': data.get('ResponseCode'),
                    'response_description': data.get('ResponseDescription'),
                    'customer_message': data.get('CustomerMessage'),
                }
            else:
                logger.warning(f"STK Push failed: {data.get('ResponseDescription')}")
                return {
                    'success': False,
                    'error': data.get('ResponseDescription', 'STK Push failed'),
                    'response_code': data.get('ResponseCode'),
                }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error during STK Push: {str(e)}")
            return {
                'success': False,
                'error': f"Request error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error during STK Push: {str(e)}")
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}"
            }
    
    def query_transaction_status(self, checkout_request_id):
        """
        Query the status of a payment transaction
        
        Args:
            checkout_request_id: CheckoutRequestID from STK Push
            
        Returns:
            dict: Transaction status response
        """
        try:
            token = self._get_access_token()
            if not token:
                return {'success': False, 'error': 'Failed to get access token'}
            
            timestamp = self._get_timestamp()
            password = self._generate_password(timestamp)
            
            url = f"{self.base_url}/mpesa/stkpushquery/v1/query"
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'BusinessShortCode': self.business_shortcode,
                'Password': password,
                'Timestamp': timestamp,
                'CheckoutRequestID': checkout_request_id,
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('ResponseCode') == '0':
                result_code = data.get('ResultCode')
                if result_code == '0':
                    return {
                        'success': True,
                        'status': 'completed',
                        'response_code': result_code,
                        'response_description': data.get('ResponseDescription'),
                        'result_desc': data.get('ResultDesc'),
                        'mpesa_receipt_number': data.get('MpesaReceiptNumber'),
                    }
                else:
                    return {
                        'success': False,
                        'status': 'pending',
                        'response_code': result_code,
                        'response_description': data.get('ResponseDescription'),
                    }
            else:
                return {
                    'success': False,
                    'error': data.get('ResponseDescription'),
                    'response_code': data.get('ResponseCode'),
                }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error querying transaction: {str(e)}")
            return {'success': False, 'error': f"Request error: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error querying transaction: {str(e)}")
            return {'success': False, 'error': f"Unexpected error: {str(e)}"}
    
    def validate_callback(self, callback_data):
        """
        Validate and parse M-Pesa callback data
        
        Args:
            callback_data: Raw callback data from M-Pesa
            
        Returns:
            dict: Parsed callback data
        """
        try:
            # Parse the callback data
            body = json.loads(callback_data) if isinstance(callback_data, str) else callback_data
            
            result = body.get('Body', {}).get('stkCallback', {})
            
            return {
                'success': True,
                'merchant_request_id': result.get('MerchantRequestID'),
                'checkout_request_id': result.get('CheckoutRequestID'),
                'result_code': result.get('ResultCode'),
                'result_description': result.get('ResultDesc'),
                'amount': result.get('CallbackMetadata', {}).get('Item', [{}])[-3].get('Value') if result.get('CallbackMetadata') else None,
                'mpesa_receipt_number': result.get('CallbackMetadata', {}).get('Item', [{}])[-1].get('Value') if result.get('CallbackMetadata') else None,
                'phone_number': result.get('CallbackMetadata', {}).get('Item', [{}])[-2].get('Value') if result.get('CallbackMetadata') else None,
            }
            
        except Exception as e:
            logger.error(f"Error validating callback: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


def get_daraja_client():
    """Factory function to get Daraja API client"""
    return DarajaAPIClient()
