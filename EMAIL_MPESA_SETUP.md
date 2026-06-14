# Safari Stores - Email & M-Pesa Integration Setup Guide

## 🚀 Email Configuration

### Development Setup (Console Backend)

By default, emails are sent to the console (terminal output). This is perfect for development and testing.

```python
# config/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@safaristores.com'
```

When an order is created, you'll see email content printed to the console/terminal.

### Production Setup (Gmail SMTP)

For production, use Gmail or your preferred SMTP provider:

1. **Enable 2-Step Verification on your Gmail account**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer" (or your device)
   - Google will generate a 16-character password

3. **Configure Django Settings**

Option A: Update `config/settings.py` directly:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'xxxx xxxx xxxx xxxx'  # 16-char app password
DEFAULT_FROM_EMAIL = 'noreply@safaristores.com'
```

Option B: Use Environment Variables (Recommended):
```bash
# .env or environment variables
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
DEFAULT_FROM_EMAIL=noreply@safaristores.com
```

Then in settings.py:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@safaristores.com')
```

### Email Templates

Email templates are stored in `/templates/`:
- `order_confirmation.html` - HTML version of order confirmation
- `order_confirmation.txt` - Plain text version of order confirmation

Customize these templates to match your brand and requirements.

### Email Events

**Automatic Emails Sent:**

1. **Order Confirmation Email**
   - Triggered: When order is created (POST /api/orders/)
   - Recipients: Customer, Admin
   - Contains: Full order details, items, pricing, shipping address

2. **Payment Confirmation Email**
   - Triggered: When payment status changes to 'paid'
   - Recipients: Customer
   - Contains: Transaction ID, receipt number, payment method

3. **Shipment Notification Email**
   - Triggered: When shipment status is updated
   - Recipients: Customer
   - Contains: Tracking number, courier, estimated delivery

---

## 💳 M-Pesa Integration (Daraja API)

### Prerequisites

- Safaricom Business Account
- Access to Daraja API Portal

### Step 1: Get Daraja API Credentials

1. Visit: https://developer.safaricom.co.ke/
2. Create/Login to your account
3. Create a new application:
   - Name: "Safari Stores"
   - Description: "E-commerce platform M-Pesa integration"
4. Copy your credentials:
   - Consumer Key
   - Consumer Secret
   - Business Shortcode

### Step 2: Get Your Passkey

For **Sandbox Environment:**
```
Passkey: bfb279f9ba9b9d1ddb224758a0c55afe02c4541ae4fdd7f963a20065dc2ced5e
Business Shortcode: 174379
```

For **Production Environment:**
- Get from Daraja Portal under "Your Apps"
- Each app has a unique passkey

### Step 3: Configure Django Settings

Option A: Direct Configuration (Development):
```python
# config/settings.py
DARAJA_CONSUMER_KEY = 'your_consumer_key'
DARAJA_CONSUMER_SECRET = 'your_consumer_secret'
DARAJA_BUSINESS_SHORTCODE = '174379'
DARAJA_PASSKEY = 'bfb279f9ba9b9d1ddb224758a0c55afe02c4541ae4fdd7f963a20065dc2ced5e'
DARAJA_ENVIRONMENT = 'sandbox'  # or 'production'
MPESA_CALLBACK_URL = 'http://127.0.0.1:8000/api/payments/mpesa-callback/'
```

Option B: Environment Variables (Recommended):
```bash
# .env file or system environment variables
DARAJA_CONSUMER_KEY=your_consumer_key
DARAJA_CONSUMER_SECRET=your_consumer_secret
DARAJA_BUSINESS_SHORTCODE=174379
DARAJA_PASSKEY=bfb279f9ba9b9d1ddb224758a0c55afe02c4541ae4fdd7f963a20065dc2ced5e
DARAJA_ENVIRONMENT=sandbox
MPESA_CALLBACK_URL=http://127.0.0.1:8000/api/payments/mpesa-callback/
```

Then in settings.py:
```python
DARAJA_CONSUMER_KEY = os.getenv('DARAJA_CONSUMER_KEY', '')
DARAJA_CONSUMER_SECRET = os.getenv('DARAJA_CONSUMER_SECRET', '')
DARAJA_BUSINESS_SHORTCODE = os.getenv('DARAJA_BUSINESS_SHORTCODE', '')
DARAJA_PASSKEY = os.getenv('DARAJA_PASSKEY', '')
DARAJA_ENVIRONMENT = os.getenv('DARAJA_ENVIRONMENT', 'sandbox')
MPESA_CALLBACK_URL = os.getenv('MPESA_CALLBACK_URL', 'http://127.0.0.1:8000/api/payments/mpesa-callback/')
```

### Step 4: Test M-Pesa Integration

#### Sandbox Testing

1. **Create an order:**
```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "shipping_address": "123 Main St",
    "shipping_city": "Nairobi",
    "shipping_zip_code": "00100",
    "shipping_country": "Kenya",
    "phone_number": "+254712345678",
    "email": "customer@example.com"
  }'
```

Response will contain order ID.

2. **Initiate M-Pesa Payment:**
```bash
curl -X POST http://127.0.0.1:8000/api/payments/initiate_mpesa/ \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "phone_number": "254712345678"
  }'
```

Response:
```json
{
  "success": true,
  "message": "Enter M-Pesa PIN to complete this transaction",
  "checkout_request_id": "ws_CO_28062226234656878",
  "payment_id": 1
}
```

3. **Sandbox Test Credentials:**

For testing, use these sandbox M-Pesa credentials:
- Phone Number: 254712345678
- Test PIN: Any 4-5 digits (e.g., 1234)

4. **Query Payment Status:**
```bash
curl -X POST http://127.0.0.1:8000/api/payments/query_mpesa_status/ \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "checkout_request_id": "ws_CO_28062226234656878"
  }'
```

### Step 5: Production Deployment

When moving to production:

1. **Update Environment Variables:**
```bash
DARAJA_ENVIRONMENT=production
DARAJA_BUSINESS_SHORTCODE=your_prod_shortcode
DARAJA_PASSKEY=your_prod_passkey
MPESA_CALLBACK_URL=https://yourdomain.com/api/payments/mpesa-callback/
```

2. **Update Your Domain:**
   - Go to Daraja Portal
   - Set Callback URL to your production domain:
   ```
   https://yourdomain.com/api/payments/mpesa-callback/
   ```

3. **Test with Real Transactions:**
   - Use real M-Pesa enabled phone numbers
   - Process a small test transaction
   - Verify payment confirmation emails are sent

### Daraja API Details

#### STK Push Request
- **Endpoint:** `/mpesa/stkpush/v1/processrequest`
- **Amount:** In KES (whole numbers only)
- **Phone Number:** Format 254XXXXXXXXX (starts with 254, no +)
- **Account Reference:** Order number (alpha-numeric, no spaces)
- **Transaction Desc:** Payment description (max 13 chars recommended)

#### STK Push Response
- **CheckoutRequestID:** Unique ID for tracking the transaction
- **ResponseCode:** "0" = success, other codes = failure

#### Query Transaction Status
- **Endpoint:** `/mpesa/stkpushquery/v1/query`
- **ResultCode:** "0" = transaction completed, "1" = pending
- **MpesaReceiptNumber:** M-Pesa receipt (only if completed)

### Callback Handling

When payment is completed on customer's phone, M-Pesa sends a callback with:
- CheckoutRequestID
- ResultCode (0 = success)
- MpesaReceiptNumber
- Amount
- PhoneNumber
- Timestamp

The system automatically:
1. Updates payment status to 'paid'
2. Updates order status to 'confirmed'
3. Sends confirmation emails
4. Creates payment logs

### Troubleshooting

**Common Issues:**

1. **"Invalid Consumer Key/Secret"**
   - Verify credentials match your Daraja app
   - Check DARAJA_ENVIRONMENT matches (sandbox/production)

2. **"Invalid Phone Number Format"**
   - Phone must be 254XXXXXXXXX (12 digits)
   - Must start with 254
   - No + or leading 0

3. **"Invalid Amount"**
   - Amount must be integer (no decimals)
   - Amount must be > 1 KES
   - Match order's final_amount

4. **"Timeout"**
   - Check internet connectivity
   - Verify MPESA_CALLBACK_URL is reachable
   - For production, ensure domain is HTTPS

5. **"STK Timeout"**
   - Customer didn't enter PIN within 120 seconds
   - Query status to check if eventually paid
   - Allow customer to retry payment initiation

### Monitoring

Check payment logs for debugging:
```python
from payments.models import Payment, PaymentLog

# Get payment
payment = Payment.objects.get(id=1)

# View all logs
for log in payment.logs.all():
    print(f"{log.status}: {log.message}")

# Check latest status
latest_log = payment.logs.latest('created_at')
print(f"Latest: {latest_log.status}")
```

---

## 📊 Integration Workflow

### Complete M-Pesa Payment Flow

```
1. Customer creates account
   ↓
2. Customer adds products to cart
   ↓
3. Customer creates order (POST /api/orders/)
   → Order Confirmation Email sent
   ↓
4. Customer initiates payment (POST /api/payments/initiate_mpesa/)
   → STK Push sent to customer's phone
   ↓
5. Customer enters M-Pesa PIN
   ↓
6. M-Pesa processes payment
   ↓
7. System receives callback OR customer queries status
   → Payment marked as 'paid'
   → Order status changed to 'confirmed'
   → Payment Confirmation Email sent
   ↓
8. Admin processes and ships order
   → Shipment created
   → Shipment Notification Email sent
   ↓
9. Customer receives order
   → Can leave reviews and ratings
```

### Customer-Facing Payment Process

1. **After Order Creation:**
   - "Thank you for your order! Proceed to payment to confirm."

2. **Click "Pay Now":**
   - System initiates M-Pesa payment
   - Customer receives STK prompt on phone

3. **Complete M-Pesa Transaction:**
   - Enter M-Pesa PIN
   - Wait for confirmation

4. **Payment Confirmed:**
   - "Payment successful! Order confirmed."
   - Confirmation email received
   - Can track order status

---

## 📝 Testing Checklist

- [ ] Email sending (console output shows emails)
- [ ] Order confirmation email includes all details
- [ ] M-Pesa sandbox credentials configured
- [ ] STK Push initiated successfully
- [ ] Payment status query works
- [ ] Payment confirmation email sent on successful payment
- [ ] Admin receives order notification
- [ ] Payment logs recorded properly
- [ ] Order status auto-updates to 'confirmed'
- [ ] Test with production credentials (if deploying)

---

## 🔐 Security Notes

1. **Keep Credentials Secure:**
   - Never commit credentials to git
   - Use environment variables only
   - Rotate credentials periodically

2. **Validate Phone Numbers:**
   - Always validate 254XXXXXXXXX format
   - Implement rate limiting on payment initiation

3. **Secure Callbacks:**
   - HTTPS only in production
   - Validate callback signatures if implementing
   - Log all payment transactions

4. **PCI Compliance:**
   - Never store M-Pesa PINs
   - Don't log sensitive data
   - Use HTTPS for all transactions

---

**Last Updated:** May 28, 2026  
**Version:** 1.0
