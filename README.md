# 🚀 Penyeza API Documentation

Penyeza is an AI-powered growth agent for small businesses that automatically plans, creates, and runs marketing campaigns. This API provides the backend services for the Penyeza mobile application.

## 📋 Table of Contents
- [Base URL](#base-url)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Models](#models)
- [Quick Start](#quick-start)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

## 🌐 Base URL

```
https://penyeza-1.onrender.com/api/
```

**Live API Documentation:** [Swagger UI](https://penyeza-1.onrender.com/swagger/?format=openapi)

## 🔐 Authentication

Penyeza API uses JWT (JSON Web Token) authentication. Most endpoints require a valid JWT token in the Authorization header.

### Getting Started with Authentication:

1. **Register a new user**
2. **Obtain JWT tokens**
3. **Use the access token in API requests**

### Authentication Flow:

```http
POST /api/auth/register/ → POST /api/auth/token/ → Use token in headers
```

## 📊 API Endpoints

### 🔑 Authentication Endpoints

#### Register User
- **POST** `/auth/register/`
- Creates a new user account
- **No authentication required**

```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "password2": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+254712345678"
}
```

#### Login (Obtain Token)
- **POST** `/auth/token/`
- Returns access and refresh tokens
- **No authentication required**

```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

#### Refresh Token
- **POST** `/auth/token/refresh/`
- Get new access token using refresh token
- **No authentication required**

```json
{
  "refresh": "your_refresh_token_here"
}
```

#### User Profile
- **GET** `/auth/profile/`
- **PUT** `/auth/profile/`
- **PATCH** `/auth/profile/`
- Manage user profile information
- **Authentication required**

### 🏢 Business Endpoints

#### Business Profile
- **GET** `/business/profile/` - Get business profile
- **PUT** `/business/profile/` - Update business profile
- **PATCH** `/business/profile/` - Partial update
- **Authentication required**

```json
{
  "business_name": "My Awesome Business",
  "business_type": "retail",
  "description": "Local retail store selling quality products",
  "target_audience": {"age": "25-45", "interests": ["shopping"]},
  "location": "Nairobi, Kenya",
  "contact_info": {"phone": "+254712345678", "email": "contact@business.com"}
}
```

#### Growth Plan
- **GET** `/business/growth-plan/`
- Get AI-generated weekly marketing growth plan
- **Authentication required**

### 📝 Content Endpoints

#### Generate Marketing Content
- **POST** `/content/generate/`
- Generate AI-powered marketing content
- **Rate limited**: 2 free generations, then requires authentication

```json
{
  "content_type": "social_post",
  "platform": "instagram",
  "theme": "weekend promotion",
  "tone": "friendly"
}
```

#### Content Management
- **GET** `/content/` - List all marketing content
- **POST** `/content/` - Create new content
- **Authentication required**

#### Approve Content
- **POST** `/content/{content_id}/approve/`
- Approve generated content for posting
- **Authentication required**

## 🏗️ Models

### UserProfile
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+254712345678",
  "business_verified": false,
  "date_joined": "2024-01-01T12:00:00Z"
}
```

### BusinessProfile
```json
{
  "id": "uuid-string",
  "business_name": "My Business",
  "business_type": "retail",
  "description": "Business description",
  "target_audience": {},
  "location": "Nairobi, Kenya",
  "contact_info": {},
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z",
  "user": 1
}
```

### MarketingContent
```json
{
  "id": "uuid-string",
  "content_type": "social_post",
  "platform": "instagram",
  "content_text": "Your marketing content here...",
  "metadata": {},
  "is_approved": false,
  "is_posted": false,
  "scheduled_time": null,
  "created_at": "2024-01-01T12:00:00Z",
  "business": "uuid-string"
}
```

## 🚀 Quick Start

### 1. Register a User
```bash
curl -X POST "https://penyeza-1.onrender.com/api/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123",
    "first_name": "Test",
    "last_name": "User",
    "phone_number": "+254700000000"
  }'
```

### 2. Get Access Token
```bash
curl -X POST "https://penyeza-1.onrender.com/api/auth/token/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### 3. Make Authenticated Request
```bash
curl -X GET "https://penyeza-1.onrender.com/api/business/profile/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

## 💡 Examples

### Generate Marketing Content (Free Tier)
```bash
curl -X POST "https://penyeza-1.onrender.com/api/content/generate/" \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "social_post",
    "platform": "instagram",
    "theme": "weekend sale",
    "tone": "exciting"
  }'
```

### Create Business Profile
```bash
curl -X POST "https://penyeza-1.onrender.com/api/business/profile/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "My Local Shop",
    "business_type": "retail",
    "description": "Best local shop in town",
    "target_audience": {"age": "18-35", "location": "local"},
    "location": "Nairobi, Kenya",
    "contact_info": {"phone": "+254712345678"}
  }'
```

## ⚠️ Error Handling

The API uses standard HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error

### Common Error Responses:

**Authentication Required:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Invalid Credentials:**
```json
{
  "detail": "No active account found with the given credentials"
}
```

**Validation Error:**
```json
{
  "email": ["This field is required."],
  "password": ["This password is too common."]
}
```

## 🚦 Rate Limiting

- **Free Tier**: 2 content generations per IP address every 24 hours
- **Registered Users**: Unlimited access to all features
- **Authentication**: Required after free tier limit

## 🛠️ Content Types

The API supports generating various types of marketing content:

- `social_post` - Social media posts
- `product_desc` - Product descriptions
- `ad_copy` - Advertising copy
- `video_script` - Video scripts
- `email` - Email campaigns
- `whatsapp` - WhatsApp messages

## 🌍 Supported Platforms

- Facebook
- Instagram
- TikTok
- Twitter
- WhatsApp
- LinkedIn

## 🔄 Business Types

- `retail` - Retail businesses
- `service` - Service providers
- `food` - Food & Beverage
- `health` - Health & Beauty
- `tech` - Technology
- `other` - Other business types

## 📞 Support

For API support and questions:
- **API Documentation**: [Swagger UI](https://penyeza-1.onrender.com/swagger/)
- **Contact**: Use the contact form in the API documentation

## 🚀 Features

- ✅ AI-powered content generation
- ✅ Business profile management
- ✅ Automated growth planning
- ✅ Multi-platform content creation
- ✅ JWT authentication
- ✅ Rate limiting
- ✅ Free tier access
- ✅ Mobile-optimized API

---

**Penyeza** - Your AI Growth Agent for Small Businesses 🚀