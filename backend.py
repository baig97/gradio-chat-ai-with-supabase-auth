import os
from dotenv import load_dotenv
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = openai.OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        # Get message and history from request
        message = data.get('message', '')
        history = data.get('history', [])

        try:
            user_email = data.get('user_email', 'anonymous')
        except:
            if user_email == 'anonymous':
                return jsonify({
                    'success': False,
                    'error': 'User not authenticated'
                }), 401

        os.makedirs('user_chat_history', exist_ok=True)
        json_path = os.path.join('user_chat_history', f'{user_email}_chat_history.json')

        with open(json_path, 'w') as f:
            json.dump(history, f)

        model = 'openai/gpt-oss-20b'
        
        # Prepare the input for the API
        if isinstance(history, list) and len(history) > 0:
            # If history is provided, use it
            input_data = history + [{"role": "user", "content": message}]
        else:
            # If no history, just use the message
            input_data = message
        
        response = client.responses.create(
            model=model,
            input=input_data,
        )
        
        return jsonify({
            'success': True,
            'response': response.output_text
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/get-history', methods=['POST'])
def get_history():
    data = request.get_json()
    user_email = data.get('user_email', 'anonymous')

    json_path = os.path.join('user_chat_history', f'{user_email}_chat_history.json')

    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            history = json.load(f)
            return jsonify({
                'success': True,
                'history': history
            })
    else:
        return jsonify({
            'success': False,
            'error': 'No chat history found'
        }), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
