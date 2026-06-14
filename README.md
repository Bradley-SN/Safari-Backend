# Safari Stores E-Commerce Backend

A production-ready Django REST Framework e-commerce backend system for "Safari Stores" - an e-commerce platform for selling imported products in Kenya.

## 🎯 Overview

Safari Stores Backend is a comprehensive REST API built with Django and Django REST Framework, designed to handle all aspects of an e-commerce platform:

- 🛍️ **Product Management** - Categories, brands, inventory tracking
- 🛒 **Shopping Cart** - Dynamic cart management with real-time calculations
- 📦 **Orders & Fulfillment** - Order creation, tracking, shipment management
- 💳 **Payments** - Payment processing and transaction logging
- ⭐ **Reviews & Ratings** - Customer reviews with moderation
- 🎁 **Wishlist** - Customer favorites management
- 📢 **Promotions** - Coupons, flash sales, promotional banners
- 🔔 **Notifications** - Multi-channel notification system (email, SMS, in-app)
- 📊 **Analytics** - Sales reports, product analytics, customer analytics
- 👤 **User Management** - Registration, authentication, profile management

## 🏗️ Architecture

### Tech Stack
- **Framework:** Django 6.0.5
- **API Framework:** Django REST Framework 3.17.1
- **Authentication:** Simple JWT 5.5.1 (JSON Web Tokens)
- **Database:** SQLite (development) / PostgreSQL (production)
- **Image Storage:** Cloudinary
- **Background Jobs:** Celery + Redis
- **API Documentation:** Self-documenting via Django REST Framework

### Project Structure
```
safari-backend/
├── config/                  # Project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI application
├── authentication/         # User auth & management
├── products/              # Product catalog
├── categories/            # Product categories
├── brands/               # Product brands
├── orders/               # Order management
├── payments/             # Payment processing
├── cart/                # Shopping cart
├── reviews/             # Product reviews
├── wishlists/           # Customer wishlists
├── inventory/           # Stock management
├── shipment/            # Shipment tracking
├── notifications/       # Notification system
├── promotions/          # Coupons & promotions
├── analytics/           # Business analytics
├── venv/               # Virtual environment
├── manage.py           # Django management
├── db.sqlite3          # SQLite database
├── requirements.txt    # Dependencies
└── API_DOCUMENTATION.md # Complete API docs
```

### Database Models (30+)

**Authentication:**
- User (extends Django AbstractUser)
- PasswordReset

**Products:**
- Product, ProductImage
- Category, Brand

**Orders:**
- Order, OrderItem
- Payment, PaymentLog

**Shopping:**
- Cart, CartItem
- Review
- Wishlist, WishlistItem

**Logistics:**
- Shipment, ShipmentTracking
- Inventory, StockAdjustment

**Marketing:**
- Notification
- Coupon
- PromotionalBanner
- FlashSale

**Analytics:**
- DailySalesReport
- ProductAnalytics
- CustomerAnalytics
- StockAlerts

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- pip
- Virtual environment

### Installation

1. **Navigate to project directory:**
```bash
cd /home/nyandieka/projects/safari-backend
```

2. **Activate virtual environment:**
```bash
source venv/bin/activate
```

3. **Apply migrations:**
```bash
python manage.py migrate
```

4. **Create superuser (if needed):**
```bash
python manage.py createsuperuser
```

5. **Start development server:**
```bash
python manage.py runserver 0.0.0.0:8000
```

### Access Points
- **API Root:** http://127.0.0.1:8000/api/
- **Admin Portal:** http://127.0.0.1:8000/admin/
- **Browsable API:** http://127.0.0.1:8000/api-auth/

### Default Credentials
- **Username:** admin
- **Password:** admin@123

## 📚 API Documentation

For complete API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### Quick API Examples

**Get JWT Token:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin@123"}'
```

**List Products:**
```bash
curl http://127.0.0.1:8000/api/products/
```

**Get User Profile (Authenticated):**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/users/me/
```

**Create Order:**
```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "shipping_address": "123 Main Street",
    "shipping_city": "Nairobi",
    "shipping_state": "Nairobi",
    "shipping_zip_code": "00100",
    "shipping_country": "Kenya",
    "phone_number": "+254712345678",
    "email": "user@example.com",
    "tax_amount": "300.00",
    "delivery_fee": "200.00"
  }'
```

## 🔐 Authentication

The API uses JWT (JSON Web Token) authentication:

1. **Obtain tokens:**
   - Send username and password to `/api/token/`
   - Receive `access` and `refresh` tokens

2. **Use access token:**
   - Include in Authorization header: `Authorization: Bearer <access_token>`
   - Valid for 1 hour

3. **Refresh token:**
   - Use refresh token to get new access token
   - Refresh token valid for 7 days

## 📋 API Endpoints Summary

| Module | Method | Endpoint | Purpose |
|--------|--------|----------|---------|
| Users | POST | `/users/register/` | User registration |
| Users | POST | `/users/login/` | User login |
| Users | GET | `/users/me/` | Get profile |
| Products | GET | `/products/` | List products |
| Cart | POST | `/cart/add_item/` | Add to cart |
| Orders | POST | `/orders/` | Create order |
| Payments | POST | `/payments/{id}/mark_paid/` | Mark paid |
| Reviews | POST | `/reviews/` | Create review |
| Wishlists | POST | `/wishlists/add_item/` | Add to wishlist |
| Shipments | GET | `/shipments/my_shipments/` | Track shipment |
| Notifications | GET | `/notifications/unread/` | Get notifications |

**See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete endpoint reference.**

## ⚙️ Configuration

### Environment Variables
Create `.env` file with:
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Key Settings (config/settings.py)
- **TIME_ZONE:** Africa/Nairobi
- **LANGUAGE_CODE:** en-us
- **Custom User Model:** authentication.User
- **JWT Expiry:** 1 hour access, 7 days refresh
- **CORS:** Configured for localhost and 127.0.0.1

## 📊 Admin Interface Features

Access full admin interface at `/admin/`:
- **List Views:** Browse all data with filtering and search
- **Add/Edit:** Create and modify objects
- **Bulk Actions:** Perform operations on multiple objects
- **Inline Editing:** Edit related objects directly
- **Custom Actions:** Domain-specific admin actions
- **Read-only Fields:** Auto-generated fields protected from editing

**All models registered with:**
- Custom list_display configurations
- Search functionality
- List filters for common fields
- Inline admins for relationships
- Proper field grouping via fieldsets

## 🔄 Workflows

### Complete Purchase Flow
1. User registers → 2. Browse products → 3. Add to cart → 4. Checkout → 5. Payment → 6. Order tracking

### Admin Order Processing
1. View pending orders → 2. Mark as confirmed → 3. Update shipping → 4. Mark as delivered → 5. Generate reports

### Inventory Management
1. View stock levels → 2. Adjust inventory → 3. View low stock alerts → 4. Update reorder levels

## 🐛 Troubleshooting

**Issue:** Server won't start
- **Solution:** Ensure venv is activated, run `python manage.py check`

**Issue:** 401 Unauthorized on API calls
- **Solution:** Token may be expired, get new token from `/api/token/`

**Issue:** 404 on API endpoint
- **Solution:** Check endpoint URL, verify ViewSet is registered in router

**Issue:** Database errors
- **Solution:** Run `python manage.py migrate`, check settings.py for database config

## 🚀 Production Deployment

For production deployment:

1. **Use PostgreSQL instead of SQLite**
2. **Set DEBUG = False**
3. **Configure proper SECRET_KEY**
4. **Setup ALLOWED_HOSTS**
5. **Use production WSGI server (Gunicorn/uWSGI)**
6. **Enable HTTPS/SSL**
7. **Setup proper logging**
8. **Configure email backend for notifications**
9. **Setup Celery for background tasks**
10. **Configure static file serving**

## 📦 Dependencies

Key packages installed:
- Django 6.0.5
- djangorestframework 3.17.1
- djangorestframework-simplejwt 5.5.1
- django-cors-headers 4.9.0
- django-filter 25.2
- Pillow 11.2.0
- cloudinary 1.44.0
- celery 5.6.3
- redis 8.0.0

See `requirements.txt` for complete list.

## 📝 Notes

- **Time Zone:** All timestamps use Africa/Nairobi timezone
- **Currency:** Kenyan Shillings (KES)
- **Image Storage:** Cloudinary integration for product images
- **Passwords:** Hashed with PBKDF2
- **Search:** Full-text search on product names, descriptions, SKU
- **Filtering:** Advanced filtering on all list endpoints
- **Pagination:** Default pagination of 50 items per page

## 🤝 Support

For issues or questions:
1. Check API_DOCUMENTATION.md
2. Review admin interface for data overview
3. Check server logs: `python manage.py runserver`
4. Verify database: `python manage.py dbshell`

## 📄 License

Proprietary - Safari Stores

## ✅ Features Implemented

- [x] User registration and authentication
- [x] JWT token-based authentication
- [x] Product catalog with categories and brands
- [x] Shopping cart functionality
- [x] Order creation and management
- [x] Payment processing
- [x] Product reviews and ratings
- [x] Wishlist management
- [x] Inventory tracking
- [x] Shipment tracking
- [x] Multi-channel notifications
- [x] Promotional coupons and flash sales
- [x] Business analytics and reporting
- [x] Django admin interface (all models)
- [x] API documentation
- [x] CORS configuration
- [x] Image upload via Cloudinary
- [x] Comprehensive error handling
- [x] Data validation and serialization

## 🎯 Status

**Version:** 1.0
**Release Date:** May 28, 2026
**Status:** ✅ Production Ready

---

**Built with ❤️ using Django and Django REST Framework**
