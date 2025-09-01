#!/usr/bin/env python3
"""
Simple Authentication Server for Tradera API POC

This server handles the OAuth callback URLs that Tradera will redirect to
after user authorization. It captures the token and displays it for testing.

Usage:
    python auth_server.py

Then set these URLs in your Tradera application registration:
- Accept Return URL: http://localhost:8000/auth/success
- Reject Return URL: http://localhost:8000/auth/failure
"""

import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from datetime import datetime

class TraderaAuthHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Tradera authentication callbacks"""

    def do_GET(self):
        """Handle GET requests for authentication callbacks"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == '/auth/success':
            self.handle_success(parsed_url)
        elif path == '/auth/failure':
            self.handle_failure(parsed_url)
        elif path == '/':
            self.handle_home()
        else:
            self.handle_not_found()

    def handle_success(self, parsed_url):
        """Handle successful authorization"""
        query_params = parse_qs(parsed_url.query)
        token = query_params.get('token', ['No token found'])[0]
        user_id = query_params.get('userId', ['Unknown'])[0]
        exp = query_params.get('exp', ['Unknown'])[0]

        # Store authorization info in a file for the API client to use
        self.store_authorization_info(token, user_id, exp)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tradera Authorization Success</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .success {{ color: green; font-size: 24px; }}
                .token {{ background: #f0f0f0; padding: 10px; margin: 20px 0; font-family: monospace; }}
                .info {{ background: #e7f3ff; padding: 15px; border-left: 4px solid #2196F3; }}
            </style>
        </head>
        <body>
            <h1 class="success">✅ Authorization Successful!</h1>

            <div class="info">
                <h3>What happened:</h3>
                <p>Tradera has successfully authorized your application and redirected you here.</p>
                <p><strong>Note:</strong> Since you're using Option 2 (recommended by Tradera), the token is not included in the URL.</p>
                <p>You need to call FetchToken to retrieve the actual token.</p>
            </div>

            <h3>Authorization Details:</h3>
            <ul>
                <li><strong>User ID:</strong> {user_id}</li>
                <li><strong>Expiration:</strong> {exp}</li>
                <li><strong>Received at:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
            </ul>

            <div class="info">
                <h3>Next Steps:</h3>
                <ol>
                    <li>Use the secret key (skey) you used in the login URL</li>
                    <li>Call FetchToken with userId={user_id} and your secret key</li>
                    <li>Use the returned token for API calls</li>
                </ol>
            </div>

            <h3>Example FetchToken Call:</h3>
            <div class="token">
                client.fetch_token(user_id={user_id}, secret_key='your_secret_key_here')
            </div>

            <hr>
            <p><em>This is a local POC server. Close this window when done testing.</em></p>
        </body>
        </html>
        """

        self.wfile.write(html_content.encode('utf-8'))

        print(f"✅ Authorization successful! User ID: {user_id}")
        print(f"   Expiration: {exp}")
        print(f"   Authorization info saved to: tradera_auth_info.txt")

    def handle_failure(self, parsed_url):
        """Handle failed authorization"""
        query_params = parse_qs(parsed_url.query)
        error = query_params.get('error', ['Unknown error'])[0]
        error_description = query_params.get('error_description', ['No description'])[0]

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tradera Authorization Failed</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .error {{ color: red; font-size: 24px; }}
                .error-details {{ background: #ffe6e6; padding: 15px; border-left: 4px solid #f44336; }}
            </style>
        </head>
        <body>
            <h1 class="error">❌ Authorization Failed</h1>

            <div class="error-details">
                <h3>Error Details:</h3>
                <p><strong>Error:</strong> {error}</p>
                <p><strong>Description:</strong> {error_description}</p>
            </div>

            <h3>What to do:</h3>
            <ol>
                <li>Check your Tradera application settings</li>
                <li>Verify your credentials</li>
                <li>Try the authorization process again</li>
                <li>Check Tradera's developer documentation</li>
            </ol>

            <hr>
            <p><em>This is a local POC server. Close this window when done testing.</em></p>
        </body>
        </html>
        """

        self.wfile.write(html_content.encode('utf-8'))

        print(f"❌ Authorization failed! Error: {error}")
        print(f"   Description: {error_description}")

    def handle_home(self):
        """Handle the home page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tradera API POC - Auth Server</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .info { background: #e7f3ff; padding: 20px; border-radius: 5px; }
                .urls { background: #f0f0f0; padding: 15px; border-radius: 5px; font-family: monospace; }
                .steps { background: #fff3cd; padding: 20px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Tradera API POC - Authentication Server</h1>

                <div class="info">
                    <h2>What is this?</h2>
                    <p>This is a local authentication server that handles Tradera's OAuth callbacks during the authorization process.</p>
                </div>

                <div class="urls">
                    <h3>Callback URLs to use in Tradera:</h3>
                    <p><strong>Accept Return URL:</strong> http://localhost:8000/auth/success</p>
                    <p><strong>Reject Return URL:</strong> http://localhost:8000/auth/failure</p>
                    <p><strong>Show token:</strong> Disabled (Option 2 - recommended by Tradera)</p>
                </div>

                <div class="steps">
                    <h3>Setup Steps:</h3>
                    <ol>
                        <li>Register your application with Tradera using the URLs above</li>
                        <li><strong>Disable "Show token"</strong> (Option 2)</li>
                        <li>Generate a secret key (skey) - use a UUID like: 77FA15BA-E13C-4D83-B6DC-E7F9FFB6601F</li>
                        <li>Redirect users to: <code>https://api.tradera.com/tokenlogin.aspx?appId=YOUR_APP_ID&pkey=YOUR_PUBLIC_KEY&skey=YOUR_SECRET_KEY</code></li>
                        <li>User logs in on Tradera's page</li>
                        <li>User is redirected here with userId</li>
                        <li>Call FetchToken with userId and your secret key</li>
                    </ol>
                </div>

                <h3>Current Status:</h3>
                <p>✅ Server is running and ready to receive callbacks</p>
                <p>🌐 Accessible at: <a href="http://localhost:8000">http://localhost:8000</a></p>

                <hr>
                <p><em>Keep this server running while testing the authorization flow.</em></p>
            </div>
        </body>
        </html>
        """

        self.wfile.write(html_content.encode('utf-8'))

    def handle_not_found(self):
        """Handle 404 errors"""
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>404 - Not Found</title></head>
        <body>
            <h1>404 - Page Not Found</h1>
            <p>This endpoint is not configured.</p>
            <p><a href="/">Go to home page</a></p>
        </body>
        </html>
        """

        self.wfile.write(html_content.encode('utf-8'))

    def store_token(self, token):
        """Store the token in a file for later use"""
        try:
            with open('tradera_token.txt', 'w') as f:
                f.write(f"# Tradera Authorization Token\n")
                f.write(f"# Generated at: {datetime.now().isoformat()}\n")
                f.write(f"# Use this token in your API client\n\n")
                f.write(token)
            print(f"   Token saved to: tradera_token.txt")
        except Exception as e:
            print(f"   Warning: Could not save token to file: {e}")

    def store_authorization_info(self, token, user_id, exp):
        """Store the authorization info in a file for later use"""
        try:
            with open('tradera_auth_info.txt', 'w') as f:
                f.write(f"# Tradera Authorization Information\n")
                f.write(f"# Generated at: {datetime.now().isoformat()}\n")
                f.write(f"# Use this info to call FetchToken\n\n")
                f.write(f"User ID: {user_id}\n")
                f.write(f"Expiration: {exp}\n")
                f.write(f"Token in URL: {token}\n")
                f.write(f"\n# Note: For Option 2, you need to call FetchToken\n")
                f.write(f"# with the secret key (skey) you used in the login URL\n")
            print(f"   Authorization info saved to: tradera_auth_info.txt")
        except Exception as e:
            print(f"   Warning: Could not save authorization info to file: {e}")

    def log_message(self, format, *args):
        """Custom logging to show server activity"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")

def run_server(port=8000):
    """Run the authentication server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, TraderaAuthHandler)

    print("🚀 Tradera API POC - Authentication Server")
    print("=" * 50)
    print(f"Server running on: http://localhost:{port}")
    print(f"Callback URLs:")
    print(f"  Accept: http://localhost:{port}/auth/success")
    print(f"  Reject: http://localhost:{port}/auth/failure")
    print("=" * 50)
    print("Keep this server running while testing the authorization flow.")
    print("Press Ctrl+C to stop the server.")
    print()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.server_close()

if __name__ == "__main__":
    # Check if port is available
    import socket
    port = 8000

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
    except OSError:
        print(f"⚠️  Port {port} is already in use. Trying port {port + 1}")
        port += 1

    run_server(port)
