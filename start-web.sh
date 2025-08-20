#!/bin/bash

# Startup script for Puzzle Solver Web Interface (Fase 2)

echo "🚀 Starting Puzzle Solver - Fase 2"
echo "================================="

# Check if we're in the right directory
if [ ! -f "main.py" ] || [ ! -d "web-frontend" ] || [ ! -d "api-backend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Install backend dependencies if needed
echo "📦 Setting up Python backend..."
cd api-backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

# Start Python backend
echo "🐍 Starting Python API backend on port 8000..."
if check_port 8000; then
    echo "⚠️  Port 8000 is already in use. Killing existing process..."
    pkill -f "python.*main.py" || true
    sleep 2
fi

python main.py &
BACKEND_PID=$!
echo "Backend started with PID: $BACKEND_PID"

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 3

# Check if backend is running
if ! check_port 8000; then
    echo "❌ Failed to start backend on port 8000"
    exit 1
fi
echo "✅ Backend is running on http://localhost:8000"

# Move to frontend directory
cd ../web-frontend

# Install frontend dependencies if needed
echo "📦 Setting up Node.js frontend..."
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

# Start frontend
echo "🌐 Starting Next.js frontend on port 3000..."
if check_port 3000; then
    echo "⚠️  Port 3000 is already in use. Killing existing process..."
    pkill -f "next" || true
    sleep 2
fi

npm run dev &
FRONTEND_PID=$!
echo "Frontend started with PID: $FRONTEND_PID"

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 5

echo ""
echo "🎉 Puzzle Solver is now running!"
echo "================================"
echo "🌐 Frontend: http://localhost:3000"
echo "🔗 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "To stop the servers:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
}

# Trap Ctrl+C and cleanup
trap cleanup INT

# Wait for user to stop
wait
