import gradio as gr
import requests
import os
import time
import threading
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

API_URL = "http://localhost:5000/api/chat"
HISTORY_API_URL = "http://localhost:5000/api/get-history"

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Session refresh interval in seconds (default: 50 minutes, Supabase tokens expire in 1 hour)
SESSION_REFRESH_INTERVAL = 50 * 60

# Define authentication function using Supabase
def authenticate(username, password):
    """
    Checks if the provided username and password are valid using Supabase authentication.
    Username is treated as email for Supabase sign in.
    """
    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": username,
                "password": password,
            }
        )
        
        # If sign in is successful, return True
        if response.user:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        return False

def refresh_session_periodically():
    """
    Background thread to refresh Supabase session periodically.
    """
    while True:
        time.sleep(SESSION_REFRESH_INTERVAL)
        try:
            response = supabase.auth.refresh_session()
            if response.session:
                print("Session refreshed successfully")
            else:
                print("Failed to refresh session")
        except Exception as e:
            print(f"Session refresh error: {str(e)}")

def check_and_refresh_session(request: gr.Request):
    """
    Check if session needs refresh and get user info from cookies.
    """
    try:
        # Get user info from Supabase session
        user = supabase.auth.get_user()
        if user:
            # Store user info in request session/cookies
            return user.user.email if user.user else None
        else:
            # Try to refresh session
            response = supabase.auth.refresh_session()
            if response.session:
                return response.user.email if response.user else None
    except Exception as e:
        print(f"Session check error: {str(e)}")
    return None

def load_user_history(request: gr.Request):
    """
    Load chat history from backend when user logs in.
    """
    try:
        user_email = check_and_refresh_session(request)
        
        if not user_email:
            return []
        
        # Call backend API to get history
        response = requests.post(HISTORY_API_URL, json={
            "user_email": user_email
        })
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                history = result.get('history', [])
                print(f"Loaded {len(history)} messages for {user_email}")
                return history
        
        # If no history or error, return empty list
        return []
        
    except Exception as e:
        print(f"Error loading history: {str(e)}")
        return []

def yes(message, history, request: gr.Request):
    # Check and refresh session if needed
    user_email = check_and_refresh_session(request)
    
    history = [{k: v for k, v in history_item.items() if k in ['role', 'content']} for history_item in history] if history else []

    history.append({
        "role": "user",
        "content": message,
    })

    try:
        # Call the Flask API
        response = requests.post(API_URL, json={
            "message": message,
            "history": history[:-1],  # Send history without the current message
            "user_email": user_email  # Include user email from session
        })
        
        response.raise_for_status()
        result = response.json()
        
        if result.get('success'):
            assistant_message = result.get('response')
        else:
            assistant_message = f"Error: {result.get('error', 'Unknown error')}"
            
    except requests.exceptions.RequestException as e:
        assistant_message = f"Failed to connect to backend: {str(e)}"

    return assistant_message

def vote(data: gr.LikeData):
    if data.liked:
        print("You upvoted this response: " + data.value["value"])
    else:
        print("You downvoted this response: " + data.value["value"])

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(placeholder="<strong>Your Personal Yes-Man</strong><br>Ask Me Anything")
    chatbot.like(vote, None, None)
    chat_interface = gr.ChatInterface(fn=yes, type="messages", chatbot=chatbot)
    
    # Load chat history when the page loads
    demo.load(load_user_history, None, chat_interface.chatbot_value)
    
# Launch the Gradio application with authentication
if __name__ == "__main__":
    # Start background thread for periodic session refresh
    refresh_thread = threading.Thread(target=refresh_session_periodically, daemon=True)
    refresh_thread.start()
    
    demo.launch(auth=authenticate, auth_message="Sign in with your Supabase account")