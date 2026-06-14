# Safari Stores Backend - Complete API Endpoints Reference

**Last Updated:** May 28, 2026  
**Version:** 1.0  
**Status:** Production Ready ✅

---

## 📋 Table of Contents

1. [Authentication Endpoints](#authentication-endpoints)
2. [User Management](#user-management)
3. [Products & Catalog](#products--catalog)
4. [Shopping Cart](#shopping-cart)
5. [Orders & Checkout](#orders--checkout)
6. [Payments & M-Pesa Integration](#-payments)
7. [Email Notifications](#-email-notifications)
8. [Reviews & Ratings](#-reviews--ratings)
9. [Wishlists](#wishlists)
10. [Shipments & Tracking](#shipments--tracking)
11. [Inventory Management](#inventory-management)
12. [Notifications](#notifications)
13. [Promotions & Coupons](#promotions--coupons)
14. [Analytics & Reports](#analytics--reports)


---

## 🔐 Authentication Endpoints

### Get JWT Access Token
```
POST /api/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin@123"
}

Response (200 OK):
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Refresh Access Token
```
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

Response (200 OK):
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Token Details:**
- Access Token Lifetime: 1 hour
- Refresh Token Lifetime: 7 days
- Algorithm: HS256

---

## 👤 User Management

### Register New User
```
POST /api/users/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password123",
  "confirm_password": "secure_password123",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+254712345678",
  "role": "customer"
}

Response (201 Created):
{
  "id": 2,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+254712345678",
  "role": "customer",
  "is_active": true,
  "created_at": "2026-05-28T16:35:00+03:00"
}
```

### User Login
```
POST /api/users/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password123"
}

Response (200 OK):
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Get Current User Profile
```
GET /api/users/me/
Authorization: Bearer {ACCESS_TOKEN}

Response (200 OK):
{
  "id": 1,
  "username": "admin",
  "email": "admin@safaristores.com",
  "first_name": "",
  "last_name": "",
  "phone_number": null,
  "date_of_birth": null,
  "profile_picture": null,
  "address": null,
  "city": null,
  "state": null,
  "zip_code": null,
  "country": null,
  "role": "customer",
  "is_verified": false,
  "is_active": true,
  "created_at": "2026-05-28T16:08:58+03:00"
}
```

### Change Password
```
POST /api/users/change_password/
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "old_password": "current_password",
  "new_password": "new_password123",
  "confirm_password": "new_password123"
}

Response (200 OK):
{
  "detail": "Password changed successfully"
}
```

### Update User Profile
```
PATCH /api/users/{user_id}/
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+254712345678",
  "address": "123 Main Street",
  "city": "Nairobi",
  "state": "Nairobi",
  "zip_code": "00100",
  "country": "Kenya",
  "date_of_birth": "1990-01-15"
}

Response (200 OK):
[Full user object with updated fields]
```

---

## 🛍️ Products & Catalog

### List All Products
```
GET /api/products/

Query Parameters:
- page: Page number (default: 1)
- category: Category ID (filter)
- brand: Brand ID (filter)
- availability_status: in_stock, out_of_stock, coming_soon
- is_featured: true/false
- search: Search term
- ordering: price, created_at, name

Response (200 OK):
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Premium Coffee Beans",
      "slug": "premium-coffee-beans",
      "category": 1,
      "category_name": "Beverages",
      "brand": 1,
      "brand_name": "Elite Coffee",
      "sku": "COFFEE-001",
      "price": "2500.00",
      "discount_price": "2000.00",
      "current_price": "2000.00",
      "discount_percentage": 20,
      "stock_quantity": 150,
      "availability_status": "in_stock",
      "is_featured": true,
      "created_at": "2026-05-28T16:00:00+03:00"
    }
  ]
}
```

### Get Product Details
```
GET /api/products/{product_id}/

Response (200 OK):
{
  "id": 1,
  "name": "Premium Coffee Beans",
  "slug": "premium-coffee-beans",
  "description": "High quality imported coffee beans",
  "category": 1,
  "category_name": "Beverages",
  "brand": 1,
  "brand_name": "Elite Coffee",
  "sku": "COFFEE-001",
  "price": "2500.00",
  "discount_price": "2000.00",
  "current_price": "2000.00",
  "discount_percentage": 20,
  "stock_quantity": 150,
  "availability_status": "in_stock",
  "is_featured": true,
  "images": [
    {
      "id": 1,
      "image": "https://cdn.example.com/coffee.jpg",
      "alt_text": "Coffee Package",
      "is_primary": true
    }
  ],
  "created_at": "2026-05-28T16:00:00+03:00",
  "updated_at": "2026-05-28T16:00:00+03:00"
}
```

### Get Featured Products
```
GET /api/products/featured/

Response (200 OK):
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [Featured products list]
}
```

### Get Low Stock Products (Admin)
```
GET /api/products/low_stock/
Authorization: Bearer {ADMIN_TOKEN}

Response (200 OK):
{
  "count": 5,
  "results": [Products with low stock]
}
```

### Upload Product Image (Admin)
```
POST /api/products/{product_id}/upload_image/
Authorization: Bearer {ADMIN_TOKEN}
Content-Type: multipart/form-data

Parameters:
- image: (file) Image file
- alt_text: (optional) Alternative text
- is_primary: (optional) true/false

Response (201 Created):
{
  "id": 2,
  "image": "https://cdn.example.com/image.jpg",
  "alt_text": "Product image",
  "is_primary": false
}
```

### List Categories
```
GET /api/categories/

Response (200 OK):
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "name": "Beverages",
      "slug": "beverages",
      "description": "Coffee, tea, and drinks",
      "is_active": true,
      "created_at": "2026-05-28T16:00:00+03:00"
    }
  ]
}
```

### Get Category Details
```
GET /api/categories/{category_id}/
```

### List Brands
```
GET /api/brands/

Response (200 OK):
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "name": "Elite Coffee",
      "slug": "elite-coffee",
      "logo": "https://cdn.example.com/logo.jpg",
      "description": "Premium coffee brand",
      "is_active": true,
      "created_at": "2026-05-28T16:00:00+03:00"
    }
  ]
}
```

### Get Brand Details
```
GET /api/brands/{brand_id}/
```

---

## 🛒 Shopping Cart

### Get My Cart
```
GET /api/cart/my_cart/
Authorization: Bearer {ACCESS_TOKEN}

Response (200 OK):
{
  "id": 1,
  "customer": 1,
  "items": [
    {
      "id": 1,
      "product": 5,
      "product_name": "Premium Coffee Beans",
      "product_price": "2000.00",
      "quantity": 2,
      "subtotal": "4000.00"
    }
  ],
  "total_items": 2,
  "total_price": "4000.00",
  "created_at": "2026-05-28T16:20:57+03:00",
  "updated_at": "2026-05-28T16:20:57+03:00"
}
```

### Add Item to Cart
```
POST /api/cart/add_item/
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "product_id": 5,
  "quantity": 2
}

Response (201 Created):
{
  "id": 1,
  "product": 5,
  "product_name": "Premium Coffee Beans",
  "product_price": "2000.00",
  "quantity": 2,
  "subtotal": "4000.00"
}
```

### Remove Item from Cart
```
POST /api/cart/remove_item/
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "product_id": 5
}

Response (200 OK):
{
  "detail": "Item removed from cart"
}
```

### Clear Cart
```
POST /api/cart/clear_cart/
Authorization: Bearer {ACCESS_TOKEN}

Response (200 OK):
{
  "detail": "Cart cleared successfully"
}
```

---

## 📦 Orders & Checkout

### List My Orders
```
GET /api/orders/
Authorization: Bearer {ACCESS_TOKEN}

Query Parameters:
- status: pending, confirmed, processing, shipped, delivered, cancelled
- page: Page number

Response (200 OK):
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "order_number": "ORD-550e8400-e29b-41d4-a716-446655440000",
      "customer": 1,
      "customer_email": "user@example.com",
      "status": "pending",
      "total_items": 3,
      "final_amount": "8500.00",
      "created_at": "2026-05-28T16:30:00+03:00",
      "updated_at": "2026-05-28T16:30:00+03:00"
    }
  ]
}
```

### Create Order from Cart
```
POST /api/orders/
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "shipping_address": "123 Main Street",
  "shipping_city": "Nairobi",
  "shipping_state": "Nairobi",
  "shipping_zip_code": "00100",
  "shipping_country": "Kenya",
  "phone_number": "+254712345678",
  "email": "user@example.com",
  "tax_amount": "500.00",
  "delivery_fee": "300.00",
  "discount_amount": "0.00",
  "notes": "Please deliver in the afternoon"
}

Response (201 Created):
{
  "id": 1,
  "order_number": "ORD-550e8400-e29b-41d4-a716-446655440000",
  "customer": 1,
  "status": "pending",
  "items": [
    {
      "id": 1,
      "product": 5,
      "product_name": "Premium Coffee Beans",
      "quantity": 2,
      "price_at_purchase": "2000.00",
      "subtotal": "4000.00"
    }
  ],
  "shipping_address": "123 Main Street",
  "shipping_city": "Nairobi",
  "shipping_state": "Nairobi",
  "shipping_zip_code": "00100",
  "shipping_country": "Kenya",
  "phone_number": "+254712345678",
  "email": "user@example.com",
  "tax_amount": "500.00",
  "delivery_fee": "300.00",
  "discount_amount": "0.00",
  "final_amount": "8300.00",
  "notes": "Please deliver in the afternoon",
  "created_at": "2026-05-28T16:30:00+03:00",
  "updated_at": "2026-05-28T16:30:00+03:00"
}
```

### Get Order Details
```
GET /api/orders/{order_id}/
Authorization: Bearer {ACCESS_TOKEN}

Response (200 OK):
[Full order object with all details and items]
```

### Update Order Status (Admin)
```
POST /api/orders/{order_id}/update_status/
Authorization: Bearer {ADMIN_TOKEN}
Content-Type: application/json

{
  "status": "processing"
}

Response (200 OK):
{
  "detail": "Order status updated to processing"
}
```

**Valid Status Transitions:**
- pending → confirmed
- confirmed → processing
- processing → shipped
- shipped → delivered
- Any status → cancelled

---

## 💳 Payments

### List Payments
```
GET /api/payments/
Authorization: Bearer {ACCESS_TOKEN}

Response (200 OK):
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "order": 1,
      "order_number": "ORD-550e8400-e29b-41d4-a716-446655440000",
      "amount": "8300.00",
      "payment_method": "mpesa",
      "status": "pending",
      "transaction_id": null,
      "description": null,
      "checkout_request_id": "ws_CO_28062226234656878",
      "mpesa_receipt_number": null,
      "phone_number": "254712345678",
      "logs": [],
      "created_at": "2026-05-28T16:30:00+03:00",
      "updated_at": "2026-05-28T16:30:00+03:00"
    }
  ]
}
```

### Get Payment Details
```
GET /api/payments/{payment_id}/
Authorization: Bearer {ACCESS_TOKEN}

Response (200 OK):
{
  "id": 1,
  "order": 1,
  "order_number": "ORD-550e8400-e29b-41d4-a716-446655440000",
  "amount": "8300.00",
  "payment_method": "mpesa",
  "status": "paid",
  "transaction_id": "LHD1H2L425",
  "description": null,
  "checkout_request_id": "ws_CO_28062226234656878",
  "mpesa_receipt_number": "LHD1H2L425",
  "phone_number": "254712345678",
  "logs": [
    {
      "id": 1,
      "status": "pending",
      "message": "STK Push initiated: Enter M-Pesa PIN to complete this transaction",
      "created_at": "2026-05-28T16:30:00+03:00"
    },
    {
      "id": 2,
      "status": "paid",
      "message": "Payment confirmed: The transaction was successful.",
      "created_at": "2026-05-28T16:35:00+03:00"
    }
  ],
  "created_at": "2026-05-28T16:30:00+03:00",
  "updated_at": "2026-05-28T16:35:00+03:00"
}
```

### Initiate M-Pesa Payment (STK Push)
```
POST /api/payments/initiate_mpesa/
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "order_id": 1,
  "phone_number": "254712345678"
}

Response (201 Created):
{
  "success": true,
  "message": "Enter M-Pesa PIN to complete this transaction",
  "checkout_request_id": "ws_CO_28062226234656878",
  "payment_id": 1
}
```

**Request Parameters:**
- order_id (integer, required): ID of the order to pay for
- phone_number (string, required): Customer's M-Pesa registered phone number in format 254XXXXXXXXX

**Response:**
- success (boolean): Whether STK Push was initiated successfully
- message (string): Customer-facing message from M-Pesa
- checkout_request_id (string): Unique request ID for tracking the payment
- payment_id (integer): ID of the created Payment record

### Query M-Pesa Payment Status
```
POST /api/payments/query_mpesa_status/
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "checkout_request_id": "ws_CO_28062226234656878"
}

Response (200 OK):
{
  "success": true,
  "status": "paid",
  "message": "Payment confirmed",
  "receipt_number": "LHD1H2L425"
}
```

**Response on Pending:**
```json
{
  "success": false,
  "status": "pending",
  "message": "Payment still pending"
}
```

**Daraja API Configuration:**
Configure these in your environment variables or settings.py:
```
DARAJA_CONSUMER_KEY=your_consumer_key
DARAJA_CONSUMER_SECRET=your_consumer_secret
DARAJA_BUSINESS_SHORTCODE=174379
DARAJA_PASSKEY=bfb279f9ba9b9d1ddb224758a0c55afe02c4541ae4fdd7f963a20065dc2ced5e
DARAJA_ENVIRONMENT=sandbox  # or 'production'
MPESA_CALLBACK_URL=http://127.0.0.1:8000/api/payments/mpesa-callback/
```

Get your credentials from: https://developer.safaricom.co.ke/

### Mark Payment as Paid (Admin)
```
POST /api/payments/{payment_id}/mark_paid/
Authorization: Bearer {ADMIN_TOKEN}

Response (200 OK):
{
  "id": 1,
  "order": 1,
  "order_number": "ORD-550e8400-e29b-41d4-a716-446655440000",
  "amount": "8300.00",
  "payment_method": "card",
  "status": "paid",
  "transaction_id": "TXN-123456789",
  "logs": [...]
}
```

### Mark Payment as Failed (Admin)
```
POST /api/payments/{payment_id}/mark_failed/
Authorization: Bearer {ADMIN_TOKEN}
Content-Type: application/json

{
  "reason": "Payment declined by bank"
}

Response (200 OK):
{
  "id": 1,
  "order": 1,
  "amount": "8300.00",
  "status": "failed",
  "logs": [...]
}
```

**Payment Methods:**
- mpesa (M-Pesa - STK Push Integration)
- card (Credit/Debit Card)
- bank_transfer (Bank Transfer)

**Payment Status:**
- pending (Payment initiated, awaiting confirmation)
- paid (Payment confirmed)
- failed (Payment failed)

**M-Pesa Payment Flow:**
1. Create order via POST /api/orders/
2. Initiate payment via POST /api/payments/initiate_mpesa/
3. Customer receives STK prompt on M-Pesa registered phone
4. Customer enters M-Pesa PIN
5. System receives callback or customer queries status via POST /api/payments/query_mpesa_status/
6. Order status automatically updates to 'confirmed' when payment is received
7. Confirmation emails sent to customer and admin

---

## 📧 Email Notifications

### Order Confirmation Email
**Automatically sent when:**
- New order is created (POST /api/orders/)

**Recipients:**
- Customer email address
- Admin email (admin@safaristores.com)

**Email Contains:**
- Order number and date
- Customer information (name, email, phone)
- Shipping address
- Complete order items with quantities and prices
- Order summary (subtotal, tax, delivery fee, discount, total)
- Order notes (if any)
- Payment instructions

**Example Email Subject:**
```
Order Confirmation - ORD-550e8400-e29b-41d4-a716-446655440000
```

### Payment Confirmation Email
**Automatically sent when:**
- Payment is marked as paid (via M-Pesa callback or manual admin action)

**Recipients:**
- Customer email address
- Admin email

**Email Contains:**
- Order number
- Transaction ID / Receipt number
- Amount paid
- Payment method
- Payment date/time

### Shipment Notification Email
**Automatically sent when:**
- Shipment is created (when order status = shipped)

**Recipients:**
- Customer email address

**Email Contains:**
- Order number
- Tracking number
- Courier name
- Estimated delivery date
- Link to track shipment

### Email Configuration
To enable email notifications, configure in settings.py or environment variables:

**Console Backend (Development):**
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**SMTP Backend (Production - Gmail):**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-specific-password'
DEFAULT_FROM_EMAIL = 'noreply@safaristores.com'
```

**Environment Variables:**
```bash
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=noreply@safaristores.com
```


---

## ⭐ Reviews & Ratings

### List Product Reviews
```
GET /api/reviews/

Query Parameters:
- product: Product ID (filter)
- search: Search in comments
- ordering: rating, created_at

Response (200 OK):
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "product": 5,
      "product_name": "Premium Coffee Beans",
      "customer": 1,
      "customer_name": "John",
      "rating": 5,
      "comment": "Excellent product, highly recommended!",
      "is_verified_purchase": true,
      "is_approved": true,
      "helpful_count": 15,
      "unhelpful_count": 2,
      "created_at": "2026-05-28T16:00:00+03:00",
      "updated_at": "2026-05-28T16:00:00+03:00"
    }
  ]
}
```

### Create Review
```
POST /api/reviews/
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "product": 5,
  "rating": 5,
  "comment": "Excellent product, highly recommended!"
}

Response (201 Created):
{
  "id": 1,
  "product": 5,
  "product_name": "Premium Coffee Beans",
  "customer": 1,
  "customer_name": "John",
  "rating": 5,
  "comment": "Excellent product, highly recommended!",
  "is_verified_purchase": true,
  "is_approved": true,
  "helpful_count": 0,
  "unhelpful_count": 0,
  "created_at": "2026-05-28T16:35:00+03:00",
  "updated_at": "2026-05-28T16:35:00+03:00"
}
```

### Mark Review as Helpful
```
POST /api/reviews/{review_id}/mark_helpful/
Authorization: Bearer {ACCESS_TOKEN}

Response (200 OK):
{
  "helpful_count": 16
}
```

### Mark Review as Unhelpful
```
POST /api/reviews/{review_id}/mark_unhelpful/
Authorization: Bearer {ACCESS_TOKEN}

Response (200 OK):
{
  "unhelpful_count": 3
}
```

**Rating Scale:** 1-5 stars

---

## ❤️ Wishlists

### Get My Wishlist
```
GET /api/wishlists/my_wishlist/
Authorization: Bearer {ACCESS_TOKEN}

Response (200 OK):
{
  "id": 1,
  "customer": 1,
  "items": [
    {
      "id": 1,
      "product": 5,
      "product_details": {
        "id": 5,
        "name": "Premium Coffee Beans",
        "price": "2000.00",
        "current_price": "2000.00",
        "availability_status": "in_stock"
      },
      "added_at": "2026-05-28T16:00:00+03:00"
    }
  ],
  "created_at": "2026-05-28T16:23:01+03:00",
  "updated_at": "2026-05-28T16:23:01+03:00"
}
```

### Add Item to Wishlist
```
POST /api/wishlists/add_item/
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "product_id": 5
}

Response (201 Created):
{
  "id": 1,
  "product": 5,
  "product_details": {...},
  "added_at": "2026-05-28T16:35:00+03:00"
}
```

### Remove Item from Wishlist
```
POST /api/wishlists/remove_item/
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "product_id": 5
}

Response (200 OK):
{
  "detail": "Item removed from wishlist"
}
```

---

## 📦 Shipments & Tracking

### Get My Shipments
```
GET /api/shipments/my_shipments/
Authorization: Bearer {ACCESS_TOKEN}

Query Parameters:
- status: pending, picked_up, in_transit, out_for_delivery, delivered, failed, returned

Response (200 OK):
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "order": 1,
      "order_number": "ORD-550e8400-e29b-41d4-a716-446655440000",
      "tracking_number": "TRK-123456789",
      "status": "in_transit",
      "courier": "Fast Courier",
      "estimated_delivery_date": "2026-05-30",
      "actual_delivery_date": null,
      "rider_name": "James Mwangi",
      "rider_phone": "+254712345678",
      "tracking_updates": [
        {
          "id": 1,
          "status": "picked_up",
          "location": "Nairobi Distribution Center",
          "message": "Package picked up",
          "created_at": "2026-05-28T17:00:00+03:00"
        }
      ],
      "created_at": "2026-05-28T16:30:00+03:00",
      "updated_at": "2026-05-28T17:00:00+03:00"
    }
  ]
}
```

### Get Shipment Details
```
GET /api/shipments/{shipment_id}/
Authorization: Bearer {ACCESS_TOKEN}
```

### Update Shipment Tracking (Admin)
```
POST /api/shipments/{shipment_id}/update_tracking/
Authorization: Bearer {ADMIN_TOKEN}
Content-Type: application/json

{
  "status": "in_transit",
  "location": "Distribution Center, Nairobi",
  "message": "Package is on the way to you"
}

Response (201 Created):
{
  "id": 2,
  "status": "in_transit",
  "location": "Distribution Center, Nairobi",
  "message": "Package is on the way to you",
  "created_at": "2026-05-28T17:15:00+03:00"
}
```

**Shipment Status:**
- pending
- picked_up
- in_transit
- out_for_delivery
- delivered
- failed
- returned

---

## 📦 Inventory Management

### List Inventory
```
GET /api/inventory/
Authorization: Bearer {ACCESS_TOKEN}

Query Parameters:
- product: Product ID (filter)

Response (200 OK):
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "product": 5,
      "product_name": "Premium Coffee Beans",
      "current_stock": 150,
      "reserved_stock": 20,
      "reorder_level": 50,
      "available_stock": 130,
      "adjustments": [],
      "created_at": "2026-05-28T16:00:00+03:00",
      "updated_at": "2026-05-28T16:00:00+03:00"
    }
  ]
}
```

### Get Low Stock Items (Admin)
```
GET /api/inventory/low_stock/
Authorization: Bearer {ADMIN_TOKEN}

Response (200 OK):
{
  "count": 5,
  "results": [Inventory items below reorder level]
}
```

### Adjust Stock (Admin)
```
POST /api/inventory/{inventory_id}/adjust_stock/
Authorization: Bearer {ADMIN_TOKEN}
Content-Type: application/json

{
  "adjustment_type": "increase",
  "quantity": 50,
  "reason": "New stock received from supplier"
}

Response (201 Created):
{
  "id": 1,
  "inventory": 1,
  "adjustment_type": "increase",
  "quantity": 50,
  "reason": "New stock received from supplier",
  "created_by": 1,
  "created_by_name": "Admin",
  "created_at": "2026-05-28T17:30:00+03:00"
}
```

### List Stock Adjustments
```
GET /api/stock-adjustments/
Authorization: Bearer {ACCESS_TOKEN}

Response (200 OK):
{
  "count": 100,
  "results": [All stock adjustment records]
}
```

**Adjustment Types:**
- increase
- decrease

---

## 🔔 Notifications

### Get Unread Notifications
```
GET /api/notifications/unread/
Authorization: Bearer {ACCESS_TOKEN}

Response (200 OK):
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "recipient": 1,
      "recipient_name": "John",
      "notification_type": "order_confirmation",
      "title": "Order Confirmed",
      "message": "Your order ORD-123 has been confirmed",
      "channel": "email",
      "order": 1,
      "order_number": "ORD-550e8400-e29b-41d4-a716-446655440000",
      "is_read": false,
      "is_sent": true,
      "sent_at": "2026-05-28T16:30:00+03:00",
      "created_at": "2026-05-28T16:30:00+03:00",
      "updated_at": "2026-05-28T16:30:00+03:00"
    }
  ]
}
```

### List All Notifications
```
GET /api/notifications/
Authorization: Bearer {ACCESS_TOKEN}

Query Parameters:
- notification_type: order_confirmation, order_status, delivery_update, payment_confirmation, low_stock, promotional, system
- channel: email, sms, in_app
- is_read: true/false

Response (200 OK):
[All notifications for current user]
```

### Mark Notification as Read
```
POST /api/notifications/{notification_id}/mark_as_read/
Authorization: Bearer {ACCESS_TOKEN}

Response (200 OK):
{
  "detail": "Notification marked as read"
}
```

### Mark All Notifications as Read
```
POST /api/notifications/mark_all_as_read/
Authorization: Bearer {ACCESS_TOKEN}

Response (200 OK):
{
  "detail": "All notifications marked as read"
}
```

**Notification Types:**
- order_confirmation
- order_status
- delivery_update
- payment_confirmation
- low_stock
- promotional
- system

**Notification Channels:**
- email
- sms
- in_app

---

## 🎁 Promotions & Coupons

### List Coupons
```
GET /api/coupons/

Query Parameters:
- search: Search by coupon code
- is_active: true/false

Response (200 OK):
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "code": "WELCOME10",
      "discount_type": "percentage",
      "discount_value": "10.00",
      "max_discount": "1000.00",
      "min_purchase_amount": "500.00",
      "usage_limit": 100,
      "usage_count": 15,
      "valid_from": "2026-05-01T00:00:00+03:00",
      "valid_to": "2026-06-30T23:59:59+03:00",
      "is_valid": true,
      "created_at": "2026-05-01T16:00:00+03:00"
    }
  ]
}
```

### Get Coupon Details
```
GET /api/coupons/{coupon_id}/
```

### List Promotional Banners
```
GET /api/banners/

Query Parameters:
- is_active: true/false

Response (200 OK):
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "title": "Summer Sale",
      "description": "Get 50% off on selected items",
      "image": "https://cdn.example.com/banner.jpg",
      "link": "https://example.com/sale",
      "is_active": true,
      "start_date": "2026-05-01T00:00:00+03:00",
      "end_date": "2026-06-30T23:59:59+03:00",
      "created_at": "2026-05-01T16:00:00+03:00",
      "updated_at": "2026-05-01T16:00:00+03:00"
    }
  ]
}
```

### List Flash Sales
```
GET /api/flash-sales/

Query Parameters:
- is_active: true/false

Response (200 OK):
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "name": "Weekend Flash Sale",
      "description": "Limited time offers",
      "discount_percentage": 30,
      "start_date": "2026-05-27T00:00:00+03:00",
      "end_date": "2026-05-28T23:59:59+03:00",
      "is_active": true,
      "products": [
        {
          "id": 5,
          "name": "Premium Coffee Beans",
          "price": "2000.00"
        }
      ],
      "created_at": "2026-05-25T16:00:00+03:00",
      "updated_at": "2026-05-25T16:00:00+03:00"
    }
  ]
}
```

**Discount Types:**
- percentage (%)
- fixed (Fixed amount in KES)

---

## 📊 Analytics & Reports

### Daily Sales Report (Admin)
```
GET /api/analytics/sales/
Authorization: Bearer {ADMIN_TOKEN}

Query Parameters:
- date: YYYY-MM-DD (filter)
- ordering: date

Response (200 OK):
{
  "count": 30,
  "results": [
    {
      "id": 1,
      "date": "2026-05-28",
      "total_orders": 25,
      "total_revenue": "250000.00",
      "total_items_sold": 85,
      "average_order_value": "10000.00",
      "created_at": "2026-05-28T23:59:59+03:00"
    }
  ]
}
```

### Product Analytics (Admin)
```
GET /api/analytics/products/
Authorization: Bearer {ADMIN_TOKEN}

Query Parameters:
- product: Product ID (filter)
- date: YYYY-MM-DD (filter)
- ordering: revenue, units_sold

Response (200 OK):
{
  "count": 100,
  "results": [
    {
      "id": 1,
      "product": 5,
      "product_name": "Premium Coffee Beans",
      "date": "2026-05-28",
      "units_sold": 25,
      "revenue": "50000.00",
      "views": 500,
      "created_at": "2026-05-28T23:59:59+03:00"
    }
  ]
}
```

### Customer Analytics (Admin)
```
GET /api/analytics/customers/
Authorization: Bearer {ADMIN_TOKEN}

Query Parameters:
- customer: Customer ID (filter)
- date: YYYY-MM-DD (filter)

Response (200 OK):
{
  "count": 150,
  "results": [
    {
      "id": 1,
      "customer": 1,
      "customer_email": "user@example.com",
      "date": "2026-05-28",
      "total_spent": "25000.00",
      "orders_count": 3,
      "average_order_value": "8333.33",
      "created_at": "2026-05-28T23:59:59+03:00"
    }
  ]
}
```

### Stock Alerts (Admin)
```
GET /api/analytics/stock-alerts/
Authorization: Bearer {ADMIN_TOKEN}

Query Parameters:
- is_resolved: true/false (filter)

Response (200 OK):
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "product": 5,
      "product_name": "Premium Coffee Beans",
      "current_stock": 45,
      "reorder_level": 50,
      "is_resolved": false,
      "created_at": "2026-05-28T16:00:00+03:00",
      "updated_at": "2026-05-28T16:00:00+03:00"
    }
  ]
}
```

---

## 📋 HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Successful but no content to return |
| 400 | Bad Request - Invalid request parameters |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 500 | Server Error - Internal server error |

---

## 🔒 Authentication & Permissions

**Public Endpoints:** No authentication required
- GET /api/products/
- GET /api/categories/
- GET /api/brands/
- GET /api/reviews/
- GET /api/banners/
- GET /api/coupons/
- GET /api/flash-sales/

**Authenticated User Endpoints:** Requires valid JWT token
- POST /api/users/register/
- POST /api/users/login/
- GET /api/users/me/
- POST /api/users/change_password/
- GET /api/cart/my_cart/
- POST /api/cart/add_item/
- GET /api/orders/
- POST /api/orders/
- POST /api/reviews/
- GET /api/wishlists/
- POST /api/wishlists/add_item/
- GET /api/notifications/
- All customer-specific operations

**Admin Only Endpoints:** Requires admin JWT token
- POST /api/products/{id}/upload_image/
- POST /api/orders/{id}/update_status/
- POST /api/payments/{id}/mark_paid/
- POST /api/payments/{id}/mark_failed/
- GET /api/products/low_stock/
- POST /api/inventory/{id}/adjust_stock/
- POST /api/shipments/{id}/update_tracking/
- GET /api/analytics/sales/
- GET /api/analytics/products/
- GET /api/analytics/customers/
- GET /api/analytics/stock-alerts/

---

## 🌐 Base URL

```
http://127.0.0.1:8000
```

All API endpoints are prefixed with `/api/`

Example: 
```
http://127.0.0.1:8000/api/products/
```

---

## 📝 Request/Response Format

**All requests and responses use JSON format**

### Standard Error Response
```json
{
  "detail": "Error message"
}
```

### Validation Error Response
```json
{
  "field_name": ["Error message"]
}
```

---

## 🔄 Common Workflows

### Complete Purchase Workflow
1. Register or login: `POST /api/users/register/` or `POST /api/users/login/`
2. Browse products: `GET /api/products/`
3. View product details: `GET /api/products/{id}/`
4. Add to cart: `POST /api/cart/add_item/`
5. Review cart: `GET /api/cart/my_cart/`
6. Create order: `POST /api/orders/`
7. Process payment: Admin marks payment as paid
8. Track shipment: `GET /api/shipments/my_shipments/`
9. Leave review: `POST /api/reviews/`

### Admin Order Processing
1. View pending orders: `GET /api/orders/?status=pending`
2. Confirm order: `POST /api/orders/{id}/update_status/` (status: confirmed)
3. Process order: `POST /api/orders/{id}/update_status/` (status: processing)
4. Create shipment: Shipment auto-created with order
5. Update tracking: `POST /api/shipments/{id}/update_tracking/`
6. Mark as delivered: Update shipment status to "delivered"

---

**Built with Django REST Framework**  
**Version 1.0 - Production Ready ✅**
