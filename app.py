# ===== app.py =====
# Main Flask application with advanced AI chatbot capabilities

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import re
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

# ===== COMPREHENSIVE KNOWLEDGE BASE =====
KNOWLEDGE_BASE = {
    # World Leaders
    "prime minister india": "Narendra Modi is the Prime Minister of India (as of 2025). He has been serving since May 2014 and is from the Bharatiya Janata Party (BJP).",
    "pm india": "Narendra Modi is the Prime Minister of India, serving since 2014.",
    "president usa": "Donald Trump is the President of the United States (as of 2025), having won the 2024 election.",
    "prime minister singapore": "Lawrence Wong is the Prime Minister of Singapore (as of 2024). He succeeded Lee Hsien Loong in May 2024.",
    "pm singapore": "Lawrence Wong is the Prime Minister of Singapore since May 2024.",
    "prime minister uk": "Keir Starmer is the Prime Minister of the United Kingdom (as of 2024), representing the Labour Party.",
    "prime minister canada": "Justin Trudeau is the Prime Minister of Canada, serving since 2015.",
    "president france": "Emmanuel Macron is the President of France, serving since 2017.",
    "chancellor germany": "Olaf Scholz is the Chancellor of Germany, serving since 2021.",

    # AI and Machine Learning
    "artificial intelligence": "Artificial Intelligence (AI) is the simulation of human intelligence by machines. It includes learning, reasoning, problem-solving, perception, and language understanding. Modern AI uses techniques like machine learning, deep learning, and neural networks.",
    "machine learning": "Machine Learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data, learn patterns, and make decisions.",
    "deep learning": "Deep Learning is a subset of machine learning that uses artificial neural networks with multiple layers (deep networks) to extract higher-level features. It's used for image recognition, NLP, and speech recognition.",
    "neural network": "A Neural Network is a computing system inspired by biological neural networks. It consists of interconnected neurons organized in layers that process information. They're the foundation of deep learning.",
    "natural language processing": "Natural Language Processing (NLP) helps computers understand and generate human language. It powers chatbots, translation services, and assistants like Siri or Alexa.",
    "computer vision": "Computer Vision trains computers to interpret visual information. It enables object detection, face recognition, and image understanding.",

    # Companies
    "openai": "OpenAI is an AI research company founded in 2015. It created ChatGPT, GPT-4, and DALL·E.",
    "google": "Google is a multinational company known for its search engine, Android, Chrome, and AI research through DeepMind.",
    "microsoft": "Microsoft, founded by Bill Gates and Paul Allen, is known for Windows, Office, Azure, and OpenAI partnership.",
    "apple": "Apple Inc. is known for the iPhone, Mac, and its ecosystem of hardware and software products.",
    "meta": "Meta (formerly Facebook) is a company led by Mark Zuckerberg focusing on social media and the metaverse.",

    # Science & Space
    "black hole": "A black hole is a region where gravity is so strong that nothing, not even light, can escape. The first image was captured in 2019 by the Event Horizon Telescope.",
    "quantum computing": "Quantum computing uses quantum phenomena to perform computations faster for certain problems like cryptography and optimization.",
    "climate change": "Climate change refers to long-term shifts in global temperatures and weather patterns caused mainly by human activity.",

    # Crypto
    "bitcoin": "Bitcoin is the first cryptocurrency, created in 2009 by Satoshi Nakamoto, using blockchain technology.",
    "blockchain": "Blockchain is a distributed ledger system used for secure and transparent transaction recording.",

    # Geography
    "india": "India is the world's most populous country, located in South Asia. Capital: New Delhi.",
    "singapore": "Singapore is a city-state and island nation in Southeast Asia, a major tech and financial hub.",
    "united states": "The United States is a federal republic of 50 states. Capital: Washington, D.C."
}

# ===== NEXT WORD PREDICTION DATABASE =====
WORD_PREDICTIONS = {
    'hello': ['there', 'everyone', 'friend', 'how'],
    'hi': ['there', 'everyone', 'friend', 'how'],
    'good': ['morning', 'afternoon', 'evening', 'day'],
    'who': ['is', 'are', 'was'],
    'what': ['is', 'are', 'was'],
    'where': ['is', 'are', 'was'],
    'how': ['are', 'is', 'does', 'can'],
    'prime': ['minister', 'minister of'],
    'minister': ['of', 'india', 'singapore'],
    'president': ['of', 'usa', 'france'],
    'artificial': ['intelligence'],
    'machine': ['learning'],
    'deep': ['learning'],
    'neural': ['network'],
    'python': ['programming', 'language'],
}

# ===== CONVERSATION PATTERNS =====
CONVERSATION_PATTERNS = {
    r'\b(hello|hi|hey|greetings)\b': [
        "Hello! I'm an AI assistant. Ask me about AI, tech, science, or world leaders!",
        "Hi there! How can I help you today?",
        "Hey! What topic interests you — AI, tech, or current affairs?"
    ],
    r'\bhow are you\b': [
        "I'm doing great, thank you! All systems running smoothly. How about you?",
        "Feeling smart as always! How can I assist you today?"
    ],
    r'\b(thank|thanks)\b': [
        "You're very welcome! 😊",
        "Anytime! Happy to help."
    ],
    r'\b(bye|goodbye|see you)\b': [
        "Goodbye! See you soon 👋",
        "Take care! Come back anytime you want to learn more."
    ],
}

# ===== RESPONSE GENERATOR =====
def generate_response(user_message):
    msg = user_message.lower().strip()

    # Check patterns
    for pattern, responses in CONVERSATION_PATTERNS.items():
        if re.search(pattern, msg):
            return random.choice(responses)

    # Knowledge base lookup (fuzzy)
    best_match, best_score = None, 0
    for key, value in KNOWLEDGE_BASE.items():
        words = key.split()
        matches = sum(1 for w in words if w in msg)
        score = matches / len(words)
        if score > best_score and score >= 0.5:
            best_match, best_score = value, score
    if best_match:
        return best_match

    # Default
    return random.choice([
        "That's interesting! Try asking me about AI, technology, or world leaders.",
        "I may not have info on that, but I can tell you about AI, ML, or programming!",
        "Hmm, not sure about that, but I know a lot about tech, science, and global affairs."
    ])

# ===== NEXT WORD PREDICTION =====
def predict_next_words(text):
    if not text:
        return []
    text = text.lower().strip()
    words = text.split()
    if len(words) >= 2:
        key = ' '.join(words[-2:])
        if key in WORD_PREDICTIONS:
            return WORD_PREDICTIONS[key][:4]
    last = words[-1]
    if last in WORD_PREDICTIONS:
        return WORD_PREDICTIONS[last][:4]
    return []

# ===== ROUTES =====
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data.get('message', '')
    if not msg:
        return jsonify({'error': 'No message provided'}), 400
    return jsonify({'response': generate_response(msg), 'success': True})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    txt = data.get('text', '')
    return jsonify({'predictions': predict_next_words(txt), 'success': True})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# ===== RUN APP =====
if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Advanced AI Chatbot Server Starting...")
    print("=" * 60)
    print("📡 Server running on: http://localhost:5001")
    print("🤖 AI Model: Loaded with advanced knowledge base")
    print("🧠 Capabilities: World leaders, AI/ML, Tech, Science, and more")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5001)

