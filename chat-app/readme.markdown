# ChatFlow - Real-time WebSocket Chat Application

A modern, real-time chat application built with FastAPI backend and vanilla JavaScript frontend featuring beautiful glassmorphism design and WebSocket communication.

![ChatFlow Frontend](chatapp.png)

## 🚀 Features

- **Real-time messaging** using WebSocket connections
- **User authentication** with JWT tokens
- **Room-based chat** system for organized conversations
- **Responsive design** that works on all devices
- **PostgreSQL database** for persistent data storage
- **Interactive API documentation** with FastAPI's automatic docs

## 🏗️ Architecture

### Backend (FastAPI)
The backend is built using FastAPI, providing:
- RESTful API endpoints for user management and room operations
- WebSocket endpoints for real-time chat functionality
- JWT-based authentication system
- PostgreSQL database integration
- Automatic API documentation at `localhost:8000/docs`

### Frontend (Vanilla JavaScript)
The frontend features:
- Modern glassmorphism design with gradient backgrounds
- Real-time WebSocket communication
- Responsive chat interface with message bubbles
- Connection status indicators
- Modal-based room joining system

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- Modern web browser with WebSocket support

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd chat-app
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DATABASE_NAME = ""
DATABASE_USER = ""
DATABASE_PASSWORD = ""
DATABASE_HOST = ""
DATABASE_PORT = ""


# JWT Configuration
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Optional: Additional configuration
DEBUG=True
```

### 4. Database Setup
Make sure PostgreSQL is running and create the database:
```sql
CREATE DATABASE chatflow_db;
```

### 5. Run the Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **API Server**: `localhost:8000`
- **API Documentation**: `localhost:8000/docs`
- **Frontend**: Serve the HTML file using any web server

## 🔧 API Usage

### 1. User Registration & Authentication
Visit `localhost:8000/docs` to access the interactive API documentation where you can:

- **Sign up** new users
- **Login** existing users to get JWT tokens
- **Create chat rooms** for organized conversations

### 2. WebSocket Connection
Once you have a room created and a valid JWT token, connect to the WebSocket endpoint:

```javascript
const roomId = "your-room-id";
const token = "your-jwt-token";
const wsUrl = `ws://localhost:8000/ws/${roomId}?token=${token}`;
const websocket = new WebSocket(wsUrl);
```

### 3. Frontend Usage
1. Open the HTML file in your browser
2. Enter your **Room ID** (created via API)
3. Enter your **JWT Token** (obtained from login API)
4. Start chatting in real-time!

## 🗂️ Project Structure



## 🎯 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Register a new user |
| POST | `/auth/login` | User login (returns JWT token) |
| POST | `/rooms/create` | Create a new chat room |
| WebSocket | `/ws/{room_id}?token={jwt}` | Real-time chat connection |

## 🌟 Frontend Features

- **Real-time Status**: Connection status indicator with animated pulse
- **Message Bubbles**: Distinct styling for own messages vs others
- **Smooth Animations**: Messages slide in with elegant transitions
- **Responsive Layout**: Works perfectly on desktop and mobile devices
- **Auto-reconnection**: Automatically attempts to reconnect on connection loss
- **Smart Username Detection**: Extracts username from JWT token payload

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **WebSocket Authorization**: Token validation for WebSocket connections
- **Environment Variables**: Sensitive data stored securely in `.env`
- **Input Validation**: Proper validation on both frontend and backend

## 🚀 Deployment

### Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
For support and questions, please open an issue in the GitHub repository or contact the development team.

---

Made with FastAPI and modern web technologies