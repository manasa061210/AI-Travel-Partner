#!/bin/bash

echo "🚀 Starting AI Travel Partner..."
echo ""

# Start Flask backend
echo "▶ Starting Backend (Flask) on http://localhost:5000 ..."
cd backend && python3 app.py &
BACKEND_PID=$!
sleep 2

# Verify backend
if curl -s http://localhost:5000/api/health > /dev/null; then
  echo "✅ Backend running at http://localhost:5000"
else
  echo "⚠️  Backend may still be starting..."
fi

echo ""

# Start React frontend
echo "▶ Starting Frontend (React) on http://localhost:3000 ..."
cd ../frontend && npm start &
FRONTEND_PID=$!

echo ""
echo "🌐 Open http://localhost:3000 in your browser"
echo ""
echo "📋 Demo Credentials:"
echo "   User:  user@travel.com / user123"
echo "   Admin: admin@travel.com / admin123"
echo ""
echo "Press Ctrl+C to stop all servers."

# Wait for both
wait $BACKEND_PID $FRONTEND_PID
