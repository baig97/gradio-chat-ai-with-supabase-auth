# Gradio Chat AI with Supabase Authentication

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![Gradio](https://img.shields.io/badge/Gradio-Latest-orange.svg)](https://gradio.app/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎓 Educational Project Overview

This is an **educational project** designed to demonstrate best practices in building a modern, production-ready AI chat application. It showcases the integration of multiple technologies including:

- **Frontend-Backend Separation**: Clean architecture with Flask API backend and Gradio frontend
- **User Authentication**: Supabase-based authentication with session management
- **Persistent Chat History**: User-specific conversation storage and retrieval
- **AI Integration**: Groq API integration for fast LLM responses
- **Session Management**: Automatic session refresh to maintain long-running conversations

### 🌟 Importance & Learning Outcomes

This project serves as a comprehensive learning resource for developers interested in:

1. **Building Scalable AI Applications**: Learn how to structure an AI chat application with proper separation of concerns
2. **Authentication Implementation**: Understand modern authentication flows using Supabase
3. **State Management**: Explore session management and persistent storage patterns
4. **API Design**: Study RESTful API design for AI chat applications
5. **UI/UX with Gradio**: Master Gradio's ChatInterface for rapid prototyping
6. **Production Readiness**: Implement features like error handling, session refresh, and data persistence

## ✨ Features

- 🔐 **Secure Authentication** - Supabase-powered user authentication
- 💬 **AI Chat Interface** - Interactive chat powered by Groq's LLM models
- 📝 **Persistent History** - Automatic save and load of conversation history
- 🔄 **Session Management** - Automatic session refresh (every 50 minutes)
- 👍 **User Feedback** - Upvote/downvote chat responses
- 🎨 **Modern UI** - Clean, responsive Gradio interface
- 🔌 **API-First Architecture** - Decoupled backend for easy integration

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────────────┐
│                   Frontend (Gradio)                       │
│  ┌───────────────────────────────────────────────────┐    │
│  │  • User Authentication (Supabase)                 │    │
│  │  • Chat Interface                                 │    │
│  │  • Session Management                             │    │
│  │  • History Loading on Login                       │    │
│  └───────────────────────────────────────────────────┘    │
└─────────────────────┬─────────────────────────────────────┘
                      │ HTTP/REST API
┌─────────────────────▼─────────────────────────────────────┐
│                   Backend (Flask)                         │
│  ┌───────────────────────────────────────────────────┐    │
│  │  • /api/chat - Process chat messages              │    │
│  │  • /api/get-history - Retrieve user history       │    │
│  │  • /api/health - Health check                     │    │
│  │  • Chat History Storage (JSON files)              │    │
│  └───────────────────────────────────────────────────┘    │
└─────────────────────┬─────────────────────────────────────┘
                      │
┌─────────────────────▼─────────────────────────────────────┐
│                 External Services                         │
│  • Groq API (LLM Processing)                              │
│  • Supabase (Authentication & User Management)            │
└───────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8+** installed
- **pip** package manager
- **Groq API Key** - Sign up at [Groq Console](https://console.groq.com/)
- **Supabase Account** - Create a project at [Supabase](https://supabase.com/)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd gradio-chat-ai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```bash
cp sample.env .env
```

Edit `.env` and add your credentials:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

#### Getting Your API Keys:

**Groq API Key:**
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key

**Supabase Credentials:**
1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Create a new project or select existing one
3. Go to Project Settings → API
4. Copy the **Project URL** and **anon/public key**

### 4. Set Up Supabase Authentication

1. In your Supabase dashboard, go to **Authentication** → **Providers**
2. Enable **Email** authentication
3. Create test users via **Authentication** → **Users** → **Add User**
4. Note: For production, configure email templates and SMTP settings

### 5. Run the Application

**Terminal 1 - Start Backend:**
```bash
python backend.py
```

The Flask backend will start on `http://localhost:5000`

**Terminal 2 - Start Frontend:**
```bash
python frontend.py
```

The Gradio interface will open automatically in your browser at `http://localhost:7860`

### 6. Login and Chat

1. Use your Supabase user credentials (email and password)
2. Start chatting with the AI assistant
3. Your conversation history is automatically saved

## 📁 Project Structure

```
gradio-chat-ai/
├── backend.py              # Flask API server
├── frontend.py             # Gradio chat interface
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── sample.env             # Sample environment file
├── user_chat_history/     # Stored chat histories (JSON files)
└── README.md              # This file
```

## 🔧 Configuration

### Backend Configuration (`backend.py`)

- **Port**: Default `5000` (configurable in `app.run()`)
- **Host**: `0.0.0.0` (accessible from network)
- **CORS**: Enabled for frontend access
- **History Storage**: `user_chat_history/` directory

### Frontend Configuration (`frontend.py`)

- **API URL**: `http://localhost:5000/api/chat`
- **Session Refresh**: Every 50 minutes (3000 seconds)
- **Authentication**: Supabase email/password
- **Port**: Auto-assigned by Gradio (typically `7860`)

## 🔒 Security Considerations

### ⚠️ Important for Educational Purposes

This project demonstrates core concepts but should be enhanced before production use:

1. **Environment Variables**: Never commit `.env` file to version control
2. **API Keys**: Rotate keys regularly and use different keys for development/production
3. **Chat History**: Currently stored in local JSON files - consider encrypted database storage
4. **HTTPS**: Use HTTPS in production environments
5. **Input Validation**: Add comprehensive input sanitization
6. **Rate Limiting**: Implement rate limiting on API endpoints
7. **Error Handling**: Enhance error messages to avoid exposing sensitive information

## 🎯 API Endpoints

### `POST /api/chat`
Process chat messages and generate AI responses.

**Request:**
```json
{
  "message": "Hello, how are you?",
  "history": [
    {"role": "user", "content": "Previous message"},
    {"role": "assistant", "content": "Previous response"}
  ],
  "user_email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "response": "AI generated response"
}
```

### `POST /api/get-history`
Retrieve user's chat history.

**Request:**
```json
{
  "user_email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "history": [
    {"role": "user", "content": "Message"},
    {"role": "assistant", "content": "Response"}
  ]
}
```

### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## 🧪 Testing

### Manual Testing

1. **Authentication Test**: Try logging in with valid/invalid credentials
2. **Chat Test**: Send messages and verify AI responses
3. **History Test**: Logout and login again to verify history persistence
4. **Session Test**: Wait for session refresh (or reduce timeout) to test auto-refresh

### Testing Different Models

Modify the `model` parameter in `backend.py`:

```python
model = 'llama-3.3-70b-versatile'  # Fast, versatile model
# model = 'mixtral-8x7b-32768'     # Alternative model
```

## 🎓 Learning Exercises

For students and learners, try these enhancements:

1. **Add Message Search**: Implement search functionality in chat history
2. **Multiple Conversations**: Allow users to have multiple separate conversation threads
3. **Export History**: Add functionality to export chat history as PDF or text
4. **Custom Themes**: Implement Gradio theming for different UI styles
5. **Streaming Responses**: Modify to stream AI responses in real-time
6. **Database Integration**: Replace JSON storage with PostgreSQL or MongoDB
7. **Analytics Dashboard**: Track usage statistics and popular queries
8. **Multi-language Support**: Add internationalization (i18n)

## 🐛 Troubleshooting

### Common Issues

**Issue**: `Import "flask" could not be resolved`
```bash
pip install flask flask-cors
```

**Issue**: `Supabase authentication failing`
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Check if user exists in Supabase dashboard
- Ensure email authentication is enabled

**Issue**: `Backend not connecting`
- Verify backend is running on port 5000
- Check firewall settings
- Ensure CORS is enabled in `backend.py`

**Issue**: `Chat history not loading`
- Check `user_chat_history/` directory permissions
- Verify user email format matches Supabase email
- Check backend logs for errors

## 🤝 Contributing

This is an educational project and contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📚 Additional Resources

- [Gradio Documentation](https://www.gradio.app/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [Groq API Documentation](https://console.groq.com/docs)
- [OpenAI Python SDK](https://github.com/openai/openai-python)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Built with ❤️ as an educational project to demonstrate modern AI application development.

## ⭐ Acknowledgments

- **Gradio Team** - For the amazing UI framework
- **Groq** - For lightning-fast LLM inference
- **Supabase** - For seamless authentication
- **Flask Community** - For the robust web framework

---

**Note**: This is an educational project intended for learning purposes. Always follow security best practices when deploying to production environments.

For questions, issues, or suggestions, please open an issue on GitHub.
