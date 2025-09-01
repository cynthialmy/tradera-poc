# 🚀 Tradera API POC Setup Guide

This guide will walk you through setting up and testing the Tradera API client for your POC.

## 📋 Prerequisites

- Python 3.7+ with virtual environment
- Tradera developer account
- Basic understanding of API authentication flows

## 🔧 Step-by-Step Setup

### 1. **Install Dependencies**
```bash
# Activate your virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. **Register Your Tradera Application**

Go to Tradera's developer program registration page and fill out the form:

**Application Details:**
- **Name**: `poc` (or your preferred name)
- **Description**: `testing API for item listing`

**Callback URLs:**
- **Accept Return URL**: `http://localhost:8000/auth/success`
- **Reject Return URL**: `http://localhost:8000/auth/failure`

**Important Settings:**
- ✅ **Check "Display token"** - This will append the token to your success URL

### 3. **Set Environment Variables**

Create a `.env` file or set environment variables:

```bash
# Required API credentials from Tradera
export TRADERA_APP_ID="your_application_id_here"
export TRADERA_SERVICE_KEY="your_service_key_here"
export TRADERA_PUBLIC_KEY="your_public_key_here"

# Optional: User credentials for testing
export TRADERA_USERNAME="your_tradera_username"
export TRADERA_PASSWORD="your_tradera_password"

# Optional: API settings
export TRADERA_BASE_URL="https://api.tradera.com"
export TRADERA_TIMEOUT="30"
```

### 4. **Start the Authentication Server**

```bash
# Start the local auth server
python auth_server.py
```

You should see:
```
🚀 Tradera API POC - Authentication Server
==================================================
Server running on: http://localhost:8000
Callback URLs:
  Accept: http://localhost:8000/auth/success
  Reject: http://localhost:8000/auth/failure
==================================================
Keep this server running while testing the authorization flow.
Press Ctrl+C to stop the server.
```

### 5. **Test the Authorization Flow**

1. **Keep the auth server running** in one terminal
2. **In another terminal**, test your configuration:
   ```bash
   python config.py
   ```
3. **Go to Tradera** and start the authorization process for your application
4. **You'll be redirected** to `http://localhost:8000/auth/success?token=YOUR_TOKEN`
5. **The server will capture the token** and save it to `tradera_token.txt`

### 6. **Test the API Client**

Once you have the token, test the API client:

```bash
# Test basic functionality
python example_usage.py

# Run comprehensive tests
python test_tradera_api.py
```

## 🔐 Understanding the Authentication Flow

```
User → Tradera → Your App → Local Server → Token Captured
  ↓         ↓         ↓           ↓           ↓
Login → Authorize → Redirect → Local URL → Save Token
```

1. **User logs into Tradera**
2. **Tradera asks for authorization** of your application
3. **User approves** and Tradera redirects to your Accept Return URL
4. **Local server captures the token** from the URL query string
5. **Token is saved** to `tradera_token.txt` for the API client to use

## 📁 File Structure

```
tradera-poc/
├── tradera_api_client.py    # Main API client
├── config.py                # Configuration management
├── auth_server.py           # Local OAuth callback server
├── test_tradera_api.py      # Comprehensive test suite
├── example_usage.py         # Basic usage examples
├── env_template.txt         # Environment variables template
├── requirements.txt         # Python dependencies
└── README_tradera_api.md    # Complete documentation
```

## 🧪 Testing Your Setup

### **Configuration Test**
```bash
python config.py
```
Expected output:
```
✅ Configuration validation passed!
Authorization Token: ********************... (from file)
```

### **Basic API Test**
```bash
python example_usage.py
```
This will test:
- Client initialization
- Rate limiting info
- Basic API operations

### **Full Test Suite**
```bash
python test_tradera_api.py
```
This will test:
- All API methods
- Error handling
- Rate limiting
- Authentication flow

## 🚨 Common Issues & Solutions

### **"Port 8000 already in use"**
```bash
# Kill existing processes
pkill -f "python auth_server.py"

# Or use a different port
python auth_server.py  # It will auto-detect available ports
```

### **"Configuration validation failed"**
- Check that all environment variables are set
- Verify the variable names match exactly
- Restart your terminal after setting environment variables

### **"Authorization failed"**
- Verify your Tradera credentials
- Check that callback URLs match exactly
- Ensure "Display token" is checked in Tradera

### **"Token not found in response"**
- Make sure the auth server is running
- Check that Tradera is redirecting to the correct URL
- Verify the token is being appended to the query string

## 🔄 Complete Workflow Example

```bash
# Terminal 1: Start auth server
python auth_server.py

# Terminal 2: Set credentials and test
export TRADERA_APP_ID="your_app_id"
export TRADERA_SERVICE_KEY="your_service_key"
export TRADERA_PUBLIC_KEY="your_public_key"

# Test configuration
python config.py

# Test API client
python example_usage.py

# Run full test suite
python test_tradera_api.py
```

## 📚 Next Steps

1. **Test basic operations** like getting item field values
2. **Try listing a test item** using the API
3. **Explore bulk operations** for managing multiple items
4. **Implement error handling** for production use
5. **Add logging and monitoring** for API usage

## 🆘 Getting Help

- **Check the logs** in your terminal for detailed error messages
- **Verify Tradera's documentation** for API endpoint details
- **Test with simple operations** first before complex workflows
- **Use the test suite** to isolate specific issues

## 🎯 Success Indicators

You'll know everything is working when:
- ✅ Auth server starts without errors
- ✅ Configuration validation passes
- ✅ Authorization token is captured and saved
- ✅ API client can make basic calls
- ✅ Test suite runs successfully

---

**Happy coding! 🚀** Your Tradera API POC is now ready to test item listing functionality.
