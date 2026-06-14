# Safari Stores - Quick Testing Guide

## ✅ Verify Installation

### 1. Check Server Status
```bash
# Server should be running on:
http://127.0.0.1:8000/api/
```

Expected response: JSON with all available endpoints

### 2. Check Email Configuration
Emails are currently configured to use **Console Backend** (development).
When emails are sent, they appear in the server terminal.

---

## 📧 Test Email Functionality

### Create Test Order (This Will Send Emails)

1. **Get Authentication Token:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin@123"
  }'
```

Save the `access` token from response.

2. **Create an Order:**
```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "shipping_address": "123 Main Street, Nairobi",
    "shipping_city": "Nairobi",
    "shipping_state": "Nairobi",
    "shipping_zip_code": "00100",
    "shipping_country": "Kenya",
    "phone_number": "+254712345678",
    "email": "customer@example.com",
    "tax_amount": "500.00",
    "delivery_fee": "300.00",
    "discount_amount": "0.00"
  }'
```

**Expected Behavior:**
- Order is created with status 'pending'
- **Check Server Terminal:** You should see email content printed with:
  - Order Confirmation Email (to customer)
  - Admin Notification Email (to admin@safaristores.com)
  - Emails include complete order details

### 3. Check Email Output in Terminal

Look for email headers and content like:
```
From: noreply@safaristores.com
To: admin@safaristores.com
Subject: [ADMIN] New Order Received - ORD-xxxxx

[HTML/Plain text email content...]
```

---

## 💳 Test M-Pesa Integration (Sandbox)

### 1. Configure Daraja Sandbox Credentials

Already configured in `config/settings.py`:
```python
DARAJA_CONSUMER_KEY = 'test_consumer_key'
DARAJA_CONSUMER_SECRET = 'test_consumer_secret'
DARAJA_BUSINESS_SHORTCODE = '174379'
DARAJA_PASSKEY = 'bfb279f9ba9b9d1ddb224758a0c55afe02c4541ae4fdd7f963a20065dc2ced5e'
DARAJA_ENVIRONMENT = 'sandbox'
```

These are **Safaricom sandbox credentials** for testing.

### 2. Initiate M-Pesa Payment

After creating an order (get `order_id` from response):

```bash
curl -X POST http://127.0.0.1:8000/api/payments/initiate_mpesa/ \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "phone_number": "254712345678"
  }'
```

Expected response:
```json
{
  "success": true,
  "message": "Enter M-Pesa PIN to complete this transaction",
  "checkout_request_id": "ws_CO_28062226234656878",
  "payment_id": 1
}
```

**What happens:**
- STK Push is sent to customer's phone (in sandbox, this is simulated)
- Payment record is created with checkout_request_id
- Payment status is 'pending'

### 3. Query Payment Status

```bash
curl -X POST http://127.0.0.1:8000/api/payments/query_mpesa_status/ \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "checkout_request_id": "ws_CO_28062226234656878"
  }'
```

**In Sandbox:**
Response will show status as 'pending' (simulation doesn't auto-confirm).

**To Mark as Paid (Admin):**
Use this endpoint to manually mark payment as paid (simulating successful M-Pesa transaction):

```bash
curl -X POST http://127.0.0.1:8000/api/payments/{payment_id}/mark_paid/ \
  -H "Authorization: Bearer {ADMIN_TOKEN}"
```

**Expected Behavior:**
- Payment status changes to 'paid'
- Order status changes to 'confirmed'
- **Check Terminal:** Payment confirmation email should appear
- Payment logs are created

---

## 🔄 Complete Workflow Test

### Step-by-Step Process

1. **Login/Get Token:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin@123"}'
```

2. **Add Product to Cart:**
```bash
curl -X POST http://127.0.0.1:8000/api/cart/add_item/ \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

3. **Create Order:**
```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "shipping_address": "123 Main Street",
    "shipping_city": "Nairobi",
    "shipping_state": "Nairobi",
    "shipping_zip_code": "00100",
    "shipping_country": "Kenya",
    "phone_number": "+254712345678"
  }'
```

4. **Initiate M-Pesa Payment:**
```bash
curl -X POST http://127.0.0.1:8000/api/payments/initiate_mpesa/ \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1, "phone_number": "254712345678"}'
```

5. **Mark Payment as Paid (Simulating M-Pesa Success):**
```bash
curl -X POST http://127.0.0.1:8000/api/payments/1/mark_paid/ \
  -H "Authorization: Bearer {TOKEN}"
```

**Verification:**
- ✅ Order created email received
- ✅ Payment confirmation email received
- ✅ Order status is 'confirmed'
- ✅ Payment status is 'paid'
- ✅ All details logged

---

## 🧪 Test Email Content

### Check Email Templates

Email templates are at:
- `templates/order_confirmation.html` (HTML version)
- `templates/order_confirmation.txt` (Plain text version)

Customize these files to match your brand.

### Modify Default Email Recipients

**Admin Email:** Currently set to `admin@safaristores.com`

To change, modify in `orders/signals.py`:
```python
admin_emails=['your-admin-email@company.com']
```

---

## 🔧 Development Tips

### Enable Email in Production Mode

Update `config/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'app-specific-password'
```

### Monitor Payment Logs

View all payment logs:
```bash
curl -X GET http://127.0.0.1:8000/api/payments/1/ \
  -H "Authorization: Bearer {TOKEN}"
```

Check the `logs` array for transaction history.

### View Payment Data in Admin

1. Go to http://127.0.0.1:8000/admin/
2. Login with admin/admin@123
3. Navigate to:
   - Orders → View orders and their details
   - Payments → View payment records with M-Pesa data
   - Payment Logs → View transaction history

---

## 📊 Database Inspection

### Check Orders and Payments (Python Shell)

```bash
cd /home/nyandieka/projects/safari-backend
source venv/bin/activate
python manage.py shell
```

```python
from orders.models import Order
from payments.models import Payment, PaymentLog

# View all orders
orders = Order.objects.all()
for order in orders:
    print(f"Order {order.order_number}: {order.status}")

# View all payments
payments = Payment.objects.all()
for payment in payments:
    print(f"Payment {payment.id}: {payment.status} ({payment.payment_method})")
    # View logs
    for log in payment.logs.all():
        print(f"  → {log.status}: {log.message}")

# Exit shell
exit()
```

---

## ⚠️ Common Issues & Solutions

### Issue: Emails not appearing in terminal
**Solution:** 
- Ensure `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`
- Check server terminal (not a separate window)
- Email content appears after order creation

### Issue: M-Pesa API returns "Invalid Consumer Key"
**Solution:**
- Verify credentials in settings.py
- Ensure DARAJA_ENVIRONMENT matches (sandbox/production)
- Use sandbox credentials for testing

### Issue: "Phone number must be in format 254XXXXXXXXX"
**Solution:**
- Phone must start with 254 (no +, no 0)
- Must be exactly 12 digits
- Example: 254712345678 ✅, +254712345678 ❌

### Issue: STK Push returns error but no specific message
**Solution:**
- Check payment logs: `payment.logs.all()`
- Verify amount is > 0 and matches order.final_amount
- Check callback URL is configured correctly
- Test with real phone number if production

---

## 📚 Documentation Files

- **COMPLETE_API_ENDPOINTS.md** - Full API reference with all endpoints
- **EMAIL_MPESA_SETUP.md** - Detailed setup and production guide
- **README.md** - Project overview
- **API_DOCUMENTATION.md** - Original API documentation

---

## 🚀 Next Steps

1. ✅ Test all endpoints with provided curl examples
2. ✅ Verify emails appear in terminal
3. ✅ Test M-Pesa payment flow
4. ✅ Review payment logs
5. ✅ Customize email templates
6. ✅ Configure for production (update credentials, domain, SMTP)
7. ✅ Deploy to production server

---

**All Features Implemented and Ready!** ✨

Questions? Check the detailed documentation files or review the service implementations in:
- `core_services/email_service.py`
- `core_services/daraja_service.py`
- `payments/views.py`
- `orders/signals.py`
