# Safari Stores E-Commerce Backend - Complete API Documentation

## 🚀 Quick Start

### Starting the Server
```bash
cd /home/nyandieka/projects/safari-backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

### Server URLs
- **API Root:** http://127.0.0.1:8000/api/
- **Admin Portal:** http://127.0.0.1:8000/admin/
- **Browsable API:** http://127.0.0.1:8000/api-auth/

### Admin Credentials
- **Username:** admin
- **Password:** admin@123

---

## 🔐 Authentication

### Getting JWT Tokens
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin@123"}'
```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Using JWT Tokens
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://127.0.0.1:8000/api/endpoint/
```

### Token Refresh
```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"YOUR_REFRESH_TOKEN"}'
```

**Token Details:**
- Access Token Lifetime: 1 hour
- Refresh Token Lifetime: 7 days

---

## 📚 API Endpoints

### 1. Users / Authentication

#### Register User
```
POST /api/users/register/
```
**Body:**
```json
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
```

#### Login
```
POST /api/users/login/
```
**Body:**
```json
{
  "username": "john_doe",
  "password": "secure_password123"
}
```

#### Get Current User Profile
```
GET /api/users/me/
```
**Requires:** Authentication

#### Change Password
```
POST /api/users/change_password/
```
**Body:**
```json
{
  "old_password": "current_password",
  "new_password": "new_password123",
  "confirm_password": "new_password123"
}
```
**Requires:** Authentication

---

### 2. Products Catalog

#### List Products
```
GET /api/products/
```

**Query Parameters:**
- `category`: Filter by category ID
- `brand`: Filter by brand ID
- `availability_status`: Filter by status (in_stock, out_of_stock, coming_soon)
- `is_featured`: Boolean (true/false)
- `search`: Search by name/description/SKU
- `ordering`: Order by (price, created_at, name)

#### Get Product Details
```
GET /api/products/{id}/
```

#### Featured Products
```
GET /api/products/featured/
```

#### Low Stock Products
```
GET /api/products/low_stock/
```

#### Upload Product Image (Admin)
```
POST /api/products/{id}/upload_image/
```
**Body:** Form-data with image file

---

### 3. Categories

#### List Categories
```
GET /api/categories/
```

#### Get Category
```
GET /api/categories/{id}/
```

---

### 4. Brands

#### List Brands
```
GET /api/brands/
```

#### Get Brand
```
GET /api/brands/{id}/
```

---

### 5. Shopping Cart

#### Get My Cart
```
GET /api/cart/my_cart/
```
**Requires:** Authentication

**Response:**
```json
{
  "id": 1,
  "customer": 1,
  "items": [
    {
      "id": 1,
      "product": 5,
      "product_name": "Product Name",
      "product_price": "1500.00",
      "quantity": 2,
      "subtotal": "3000.00"
    }
  ],
  "total_items": 2,
  "total_price": "3000.00",
  "created_at": "2026-05-28T16:20:57.340243+03:00",
  "updated_at": "2026-05-28T16:20:57.340264+03:00"
}
```

#### Add Item to Cart
```
POST /api/cart/add_item/
```
**Requires:** Authentication

**Body:**
```json
{
  "product_id": 5,
  "quantity": 2
}
```

#### Remove Item from Cart
```
POST /api/cart/remove_item/
```
**Requires:** Authentication

**Body:**
```json
{
  "product_id": 5
}
```

#### Clear Cart
```
POST /api/cart/clear_cart/
```
**Requires:** Authentication

---

### 6. Orders

#### Create Order (from Cart)
```
POST /api/orders/
```
**Requires:** Authentication

**Body:**
```json
{
  "shipping_address": "123 Main Street",
  "shipping_city": "Nairobi",
  "shipping_state": "Nairobi",
  "shipping_zip_code": "00100",
  "shipping_country": "Kenya",
  "phone_number": "+254712345678",
  "email": "john@example.com",
  "tax_amount": "300.00",
  "delivery_fee": "200.00",
  "discount_amount": "0.00",
  "notes": "Please deliver in the afternoon"
}
```

#### List My Orders
```
GET /api/orders/
```
**Requires:** Authentication

**Query Parameters:**
- `status`: Filter by status (pending, confirmed, processing, shipped, delivered, cancelled)

#### Get Order Details
```
GET /api/orders/{id}/
```
**Requires:** Authentication

#### Update Order Status (Admin)
```
POST /api/orders/{id}/update_status/
```
**Requires:** Admin authentication

**Body:**
```json
{
  "status": "processing"
}
```

---

### 7. Payments

#### Mark Payment as Paid (Admin)
```
POST /api/payments/{id}/mark_paid/
```
**Requires:** Admin authentication

#### Mark Payment as Failed (Admin)
```
POST /api/payments/{id}/mark_failed/
```
**Requires:** Admin authentication

**Body:**
```json
{
  "reason": "Payment declined by bank"
}
```

---

### 8. Reviews

#### List Product Reviews
```
GET /api/reviews/
```

**Query Parameters:**
- `product`: Filter by product ID

#### Create Review
```
POST /api/reviews/
```
**Requires:** Authentication

**Body:**
```json
{
  "product": 5,
  "rating": 5,
  "comment": "Great product, highly recommend!"
}
```

#### Mark Review as Helpful
```
POST /api/reviews/{id}/mark_helpful/
```
**Requires:** Authentication

#### Mark Review as Unhelpful
```
POST /api/reviews/{id}/mark_unhelpful/
```
**Requires:** Authentication

---

### 9. Wishlists

#### Get My Wishlist
```
GET /api/wishlists/my_wishlist/
```
**Requires:** Authentication

#### Add Item to Wishlist
```
POST /api/wishlists/add_item/
```
**Requires:** Authentication

**Body:**
```json
{
  "product_id": 5
}
```

#### Remove Item from Wishlist
```
POST /api/wishlists/remove_item/
```
**Requires:** Authentication

**Body:**
```json
{
  "product_id": 5
}
```

---

### 10. Shipments

#### Get My Shipments
```
GET /api/shipments/my_shipments/
```
**Requires:** Authentication

#### Update Shipment Tracking (Admin)
```
POST /api/shipments/{id}/update_tracking/
```
**Requires:** Admin authentication

**Body:**
```json
{
  "status": "in_transit",
  "location": "Distribution Center, Nairobi",
  "message": "Package is on the way to you"
}
```

---

### 11. Notifications

#### Get Unread Notifications
```
GET /api/notifications/unread/
```
**Requires:** Authentication

#### Mark Notification as Read
```
POST /api/notifications/{id}/mark_as_read/
```
**Requires:** Authentication

#### Mark All Notifications as Read
```
POST /api/notifications/mark_all_as_read/
```
**Requires:** Authentication

---

### 12. Inventory Management (Admin)

#### List Inventory
```
GET /api/inventory/
```

**Query Parameters:**
- `product`: Filter by product ID

#### Low Stock Items
```
GET /api/inventory/low_stock/
```

#### Adjust Stock (Admin)
```
POST /api/inventory/{id}/adjust_stock/
```
**Requires:** Admin authentication

**Body:**
```json
{
  "adjustment_type": "increase",
  "quantity": 50,
  "reason": "New stock received"
}
```

---

### 13. Promotions

#### List Coupons
```
GET /api/coupons/
```

#### List Promotional Banners
```
GET /api/banners/
```

#### List Flash Sales
```
GET /api/flash-sales/
```

---

### 14. Analytics (Admin)

#### Daily Sales Report
```
GET /api/analytics/sales/
```
**Requires:** Admin authentication

**Query Parameters:**
- `date`: Filter by date (YYYY-MM-DD)

#### Product Analytics
```
GET /api/analytics/products/
```
**Requires:** Admin authentication

#### Customer Analytics
```
GET /api/analytics/customers/
```
**Requires:** Admin authentication

#### Stock Alerts
```
GET /api/analytics/stock-alerts/
```
**Requires:** Admin authentication

---

## 📊 Django Admin Interface

Access the admin portal at: **http://127.0.0.1:8000/admin/**

All models are fully configured with:
- Comprehensive list displays
- Search functionality
- Filtering options
- Inline editing for related objects
- Custom admin actions

**Models available in admin:**
- Users & Roles
- Products, Categories, Brands
- Orders, Order Items, Payments, Payment Logs
- Cart, Cart Items
- Reviews, Wishlists
- Shipments, Shipment Tracking
- Notifications
- Inventory, Stock Adjustments
- Coupons, Promotional Banners, Flash Sales
- Analytics Reports

---

## 🔄 Common Workflows

### 1. Complete Purchase Flow
1. **User Registration:**
   ```
   POST /api/users/register/
   ```

2. **Browse Products:**
   ```
   GET /api/products/
   GET /api/products/{id}/
   ```

3. **Add to Cart:**
   ```
   POST /api/cart/add_item/
   ```

4. **Checkout:**
   ```
   POST /api/orders/
   ```

5. **Payment:**
   - Admin marks payment via admin interface
   - Or API: `POST /api/payments/{id}/mark_paid/`

6. **Track Order:**
   ```
   GET /api/orders/{id}/
   GET /api/shipments/my_shipments/
   ```

### 2. Admin Operations
1. **View Orders:**
   ```
   GET /api/orders/?status=pending
   ```

2. **Update Order Status:**
   ```
   POST /api/orders/{id}/update_status/
   ```

3. **Manage Inventory:**
   ```
   GET /api/inventory/low_stock/
   POST /api/inventory/{id}/adjust_stock/
   ```

4. **Generate Reports:**
   ```
   GET /api/analytics/sales/
   GET /api/analytics/products/
   ```

---

## ⚙️ Configuration

**Key Settings:** `config/settings.py`

**Database:** SQLite (development) - `db.sqlite3`

**Time Zone:** Africa/Nairobi

**Installed Apps:**
- Django REST Framework
- Simple JWT (Authentication)
- CORS Headers
- Django Filters
- Cloudinary (Image storage)

**CORS Settings:**
- localhost:3000
- localhost:8000
- 127.0.0.1:3000
- 127.0.0.1:8000

---

## 🐛 Troubleshooting

**Server won't start:**
- Check virtual environment: `source venv/bin/activate`
- Check database: `python manage.py migrate`
- Check for syntax errors: `python manage.py check`

**401 Unauthorized:**
- Ensure JWT token is valid and not expired
- Include `Authorization: Bearer TOKEN` header

**404 Not Found:**
- Check endpoint URL spelling
- Ensure app is registered in INSTALLED_APPS
- Check router registration in `config/urls.py`

**500 Internal Server Error:**
- Check server logs in terminal
- Verify model field names match serializer fields
- Check database migrations: `python manage.py showmigrations`

---

## 📝 Notes

- All timestamps are in **Africa/Nairobi** timezone
- All currency amounts are in **Kenyan Shillings (KES)**
- Product images are stored via Cloudinary
- Passwords are automatically hashed with PBKDF2

---

**Last Updated:** May 28, 2026
**Version:** 1.0
**Status:** ✅ Production Ready
