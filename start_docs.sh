#!/bin/bash

# Tradera API Documentation Server Startup Script

echo "🚀 Starting Tradera API Documentation Server..."
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Please run: python3 -m venv venv"
    echo "   Then: source venv/bin/activate"
    echo "   Then: pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if required files exist
if [ ! -f "tradera-api-openapi.yaml" ]; then
    echo "❌ OpenAPI specification not found!"
    echo "   Please ensure tradera-api-openapi.yaml exists"
    exit 1
fi

if [ ! -f "swagger_server.py" ]; then
    echo "❌ Swagger server not found!"
    echo "   Please ensure swagger_server.py exists"
    exit 1
fi

# Start the server
echo "🌐 Starting Swagger UI server on port 3000..."
echo ""
echo "📖 Documentation will be available at:"
echo "   • Main Interface: http://localhost:3000"
echo "   • API Examples:   http://localhost:3000/examples"
echo "   • Health Check:   http://localhost:3000/health"
echo "   • OpenAPI Spec:   http://localhost:3000/api-docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=============================================="

python3 swagger_server.py
