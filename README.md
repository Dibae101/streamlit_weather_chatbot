# Weather Chat Assistant 🌤️

An AI-powered weather chatbot built with Streamlit and Google's Gemini AI. This application provides intelligent weather-related conversations and real-time weather data.

## Features

- 🤖 **AI-Powered Chat**: Uses Google Gemini AI for intelligent weather conversations
- 🌡️ **Real-time Weather Data**: Fetches current weather conditions for any city
- 💬 **Weather-Focused**: Designed specifically for weather-related queries
- 🎯 **Smart Suggestions**: Pre-built weather question suggestions
- 🔒 **Weather-Only Responses**: Politely redirects non-weather questions back to weather topics

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dibae101/streamlit_weather_chatbot.git
   cd streamlit_weather_chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get API Keys**
   - The Gemini AI API key is already configured in the app
   - Get a free OpenWeatherMap API key from [openweathermap.org](https://openweathermap.org/api)

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Configuration

### Weather API Setup
1. Sign up for a free account at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your API key
3. Enter it in the sidebar when running the app, or
4. Create a `.streamlit/secrets.toml` file:
   ```toml
   WEATHER_API_KEY = "your_openweathermap_api_key_here"
   ```

## Usage

1. **Start the app** and enter your city name in the sidebar
2. **Ask weather questions** using the chat interface
3. **Use suggestion buttons** for quick weather queries
4. **Get real-time weather data** displayed in the sidebar

### Example Questions
- "What's the weather like today?"
- "Should I carry an umbrella?"
- "Is it a good day for outdoor activities?"
- "What's the temperature and humidity?"
- "Tell me about wind conditions"

## Project Structure

```
streamlit_weather_chatbot/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
└── README.md             # Project documentation
```

## Technologies Used

- **Streamlit**: Web app framework
- **Google Gemini AI**: AI conversational model
- **OpenWeatherMap API**: Real-time weather data
- **Python**: Programming language

## Features in Detail

### 🤖 AI Chat Interface
- Powered by Google's Gemini AI model
- Context-aware responses with weather data
- Maintains conversation history
- Weather-focused prompt engineering

### 🌡️ Weather Data Integration
- Real-time weather information
- Temperature, humidity, wind speed
- Weather conditions and descriptions
- City-based weather lookup

### 🎯 Smart Suggestions
- Pre-built weather question templates
- One-click question submission
- Variety of weather-related topics
- Encourages user engagement

### 🔒 Topic Enforcement
- Automatically detects non-weather questions
- Politely redirects to weather topics
- Maintains focus on weather assistance
- Educational weather responses

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Built with ❤️ using Streamlit and Google Gemini AI**
