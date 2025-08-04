import streamlit as st
import google.generativeai as genai
import requests
import json
from datetime import datetime
import os

# Configure page
st.set_page_config(
    page_title="Weather Chat Assistant",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure Gemini AI
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    st.error("❌ Gemini API key not found. Please add it to .streamlit/secrets.toml")
    st.stop()
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
@st.cache_resource
def load_gemini_model():
    return genai.GenerativeModel('gemini-1.5-flash')

model = load_gemini_model()

# Weather API configuration (using OpenWeatherMap as an example)
# You'll need to get a free API key from openweathermap.org
WEATHER_API_KEY = st.secrets.get("WEATHER_API_KEY", "")

def get_weather_data(city):
    """Fetch weather data for a given city"""
    # Try to get API key from secrets first, then from session state
    api_key = WEATHER_API_KEY or st.session_state.get('weather_api_key', '')
    if not api_key:
        return None
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            # Debug: Log the error response
            st.error(f"Weather API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Weather API Exception: {str(e)}")
        return None

def get_weather_prompt():
    """Create a system prompt for weather-focused responses"""
    return """You are a helpful weather assistant. Your primary focus is on weather-related topics only. 

Rules:
1. Only answer questions about weather, climate, meteorology, and related topics
2. If asked about non-weather topics, politely redirect the conversation back to weather
3. Provide accurate, helpful weather information
4. Be conversational and friendly
5. Suggest weather-related follow-up questions when appropriate

If someone asks about something unrelated to weather, respond with something like:
"I'm specifically designed to help with weather-related questions. Let's talk about the weather instead! You can ask me about current conditions, forecasts, climate patterns, or any other weather topics."
"""

def generate_response(user_input, weather_data=None):
    """Generate response using Gemini AI"""
    try:
        # Create context with weather data if available
        context = get_weather_prompt()
        
        if weather_data:
            context += f"\n\nCurrent weather data: {json.dumps(weather_data, indent=2)}"
        
        prompt = f"{context}\n\nUser question: {user_input}"
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Weather suggestion prompts
WEATHER_SUGGESTIONS = [
    "What's the weather like today?",
    "Will it rain tomorrow?",
    "What should I wear based on today's weather?",
    "Is it a good day for outdoor activities?",
    "What's the temperature and humidity?",
    "Tell me about the wind conditions",
    "What's the UV index today?",
    "Should I carry an umbrella?",
    "Is it going to be sunny this weekend?",
    "What's the weather forecast for the next 3 days?",
    "Explain today's weather conditions",
    "What causes different types of weather patterns?"
]

# Sidebar
with st.sidebar:
    st.title("🌤️ Weather Settings")
    
    # City input
    city = st.text_input("Enter your city:", value="New York", help="Enter city name for weather data")
    
    # Weather API key input
    if not WEATHER_API_KEY:
        st.warning("⚠️ Weather API key not configured. Get a free key from openweathermap.org")
        api_key_input = st.text_input("OpenWeatherMap API Key:", type="password")
        if api_key_input:
            st.session_state.weather_api_key = api_key_input
    else:
        st.success("✅ Weather API key configured")
    
    # Weather data display
    if city and (WEATHER_API_KEY or st.session_state.get('weather_api_key')):
        weather_data = get_weather_data(city)
        if weather_data and weather_data.get('cod') == 200:
            st.success(f"✅ Weather data loaded for {city}")
            
            # Display current weather
            st.subheader("Current Weather")
            st.write(f"🌡️ **Temperature:** {weather_data['main']['temp']}°C")
            st.write(f"🌤️ **Condition:** {weather_data['weather'][0]['description'].title()}")
            st.write(f"💧 **Humidity:** {weather_data['main']['humidity']}%")
            st.write(f"💨 **Wind:** {weather_data['wind']['speed']} m/s")
            
            # Store weather data in session state
            st.session_state.current_weather = weather_data
        else:
            st.error("❌ Could not fetch weather data")
            st.session_state.current_weather = None

# Main content
st.title("🌤️ Weather Chat Assistant")
st.subheader("Your AI-powered weather companion")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your weather assistant. Ask me anything about weather, climate, or meteorology! 🌦️"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Suggestion buttons
st.subheader("💡 Weather Question Suggestions")
cols = st.columns(3)
for i, suggestion in enumerate(WEATHER_SUGGESTIONS[:9]):
    col_idx = i % 3
    with cols[col_idx]:
        if st.button(suggestion, key=f"suggestion_{i}"):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": suggestion})
            
            # Generate and add assistant response
            weather_data = st.session_state.get('current_weather')
            response = generate_response(suggestion, weather_data)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Rerun to update the chat
            st.rerun()

# Chat input
if prompt := st.chat_input("Ask me about the weather..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking about the weather..."):
            weather_data = st.session_state.get('current_weather')
            response = generate_response(prompt, weather_data)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("**Note:** This app focuses specifically on weather-related topics. For the best experience, please ask questions about weather, climate, or meteorology!")
