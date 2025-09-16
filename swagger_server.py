#!/usr/bin/env python3
"""
Swagger UI Server for Tradera API Documentation

This server provides an interactive Swagger UI interface for the Tradera API documentation.
It serves the OpenAPI specification and provides a web interface for developers to explore
and test the API endpoints.

Usage:
    python swagger_server.py

Then visit: http://localhost:3000
"""

import os
import yaml
from flask import Flask, render_template_string, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Swagger UI HTML template
SWAGGER_UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tradera API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css" />
    <style>
        html {
            box-sizing: border-box;
            overflow: -moz-scrollbars-vertical;
            overflow-y: scroll;
        }
        *, *:before, *:after {
            box-sizing: inherit;
        }
        body {
            margin:0;
            background: #fafafa;
        }
        .swagger-ui .topbar {
            background-color: #1f2937;
        }
        .swagger-ui .topbar .download-url-wrapper {
            display: none;
        }
        .swagger-ui .info .title {
            color: #1f2937;
        }
        .custom-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        .custom-header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .custom-header p {
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="custom-header">
        <h1>Sakla Tradera API Documentation</h1>
        <p>Interactive API documentation and testing interface</p>
    </div>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {
            const ui = SwaggerUIBundle({
                url: '/api-docs',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout",
                tryItOutEnabled: true,
                requestInterceptor: function(request) {
                    // Add custom headers or modify requests if needed
                    console.log('Making request:', request);
                    return request;
                },
                responseInterceptor: function(response) {
                    // Log responses for debugging
                    console.log('Received response:', response);
                    return response;
                }
            });
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the Swagger UI interface"""
    return render_template_string(SWAGGER_UI_TEMPLATE)

@app.route('/api-docs')
def api_docs():
    """Serve the OpenAPI specification as JSON"""
    try:
        # Load the YAML file and convert to JSON
        with open('tradera-api-openapi.yaml', 'r', encoding='utf-8') as file:
            yaml_content = yaml.safe_load(file)
        return jsonify(yaml_content)
    except FileNotFoundError:
        return jsonify({'error': 'OpenAPI specification not found'}), 404
    except yaml.YAMLError as e:
        return jsonify({'error': f'Invalid YAML: {str(e)}'}), 400

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Tradera API Documentation Server',
        'version': '1.0.0'
    })

@app.route('/examples')
def examples():
    """Provide example requests and responses"""
    examples = {
        'authentication': {
            'description': 'Authentication flow examples',
            'steps': [
                '1. Generate login URL with your credentials',
                '2. User visits URL and authorizes your app',
                '3. Use secret key to fetch user token',
                '4. Use token for authenticated API calls'
            ],
            'login_url_example': 'https://api.tradera.com/tokenlogin.aspx?appId=YOUR_APP_ID&pkey=YOUR_PUBLIC_KEY&skey=YOUR_SECRET_KEY',
            'fetch_token_request': {
                'method': 'POST',
                'url': 'https://api.tradera.com/v3/publicservice.asmx',
                'headers': {
                    'Content-Type': 'text/xml; charset=utf-8',
                    'SOAPAction': 'http://api.tradera.com/FetchToken'
                },
                'body': '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:api="http://api.tradera.com">
  <soap:Header>
    <api:AuthenticationHeader>
      <api:AppId>YOUR_APP_ID</api:AppId>
      <api:AppKey>your_service_key</api:AppKey>
    </api:AuthenticationHeader>
    <api:ConfigurationHeader>
      <api:PublicKey>your_public_key</api:PublicKey>
    </api:ConfigurationHeader>
  </soap:Header>
  <soap:Body>
    <api:FetchToken>
      <api:userId>12345</api:userId>
      <api:secretKey>your_secret_key</api:secretKey>
    </api:FetchToken>
  </soap:Body>
</soap:Envelope>'''
            }
        },
        'add_item': {
            'description': 'Add item example',
            'request': {
                'method': 'POST',
                'url': 'https://api.tradera.com/v3/restrictedservice.asmx',
                'headers': {
                    'Content-Type': 'text/xml; charset=utf-8',
                    'SOAPAction': 'http://api.tradera.com/AddItem'
                },
                'body': '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:api="http://api.tradera.com">
  <soap:Header>
    <api:AuthenticationHeader>
      <api:AppId>YOUR_APP_ID</api:AppId>
      <api:AppKey>your_service_key</api:AppKey>
    </api:AuthenticationHeader>
    <api:AuthorizationHeader>
      <api:UserId>12345</api:UserId>
      <api:Token>your_user_token</api:Token>
    </api:AuthorizationHeader>
    <api:ConfigurationHeader>
      <api:Sandbox>0</api:Sandbox>
      <api:MaxResultAge>3600</api:MaxResultAge>
    </api:ConfigurationHeader>
  </soap:Header>
  <soap:Body>
    <api:AddItem>
      <api:itemRequest>
        <api:Title>Vintage Camera</api:Title>
        <api:Description>Beautiful vintage camera in excellent condition</api:Description>
        <api:CategoryId>12</api:CategoryId>
        <api:Duration>7</api:Duration>
        <api:StartPrice>1000</api:StartPrice>
        <api:PaymentOptionIds>
          <api:int>1</api:int>
        </api:PaymentOptionIds>
        <api:ShippingOptions>
          <api:ItemShipping>
            <api:ShippingOptionId>1</api:ShippingOptionId>
            <api:Cost>0</api:Cost>
            <api:ShippingWeight>1.0</api:ShippingWeight>
            <api:ShippingProductId>1</api:ShippingProductId>
            <api:ShippingProviderId>1</api:ShippingProviderId>
          </api:ItemShipping>
        </api:ShippingOptions>
        <api:ItemType>1</api:ItemType>
        <api:AutoCommit>true</api:AutoCommit>
        <api:VAT>25</api:VAT>
      </api:itemRequest>
    </api:AddItem>
  </soap:Body>
</soap:Envelope>'''
            }
        }
    }
    return jsonify(examples)

if __name__ == '__main__':
    print("🚀 Starting Tradera API Documentation Server...")
    print("📖 OpenAPI Specification: tradera-api-openapi.yaml")
    print("🌐 Swagger UI will be available at: http://localhost:3000")
    print("📋 API Examples available at: http://localhost:3000/examples")
    print("❤️  Health check available at: http://localhost:3000/health")
    print("\n" + "="*60)

    # Check if OpenAPI file exists
    if not os.path.exists('tradera-api-openapi.yaml'):
        print("❌ Warning: tradera-api-openapi.yaml not found!")
        print("   Please ensure the OpenAPI specification file exists.")

    app.run(host='0.0.0.0', port=3000, debug=True)
