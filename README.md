# AI Health & Fitness Planner 🏋️

A sophisticated web app that provides personalized health and fitness plans using advanced AI models. Built with Agno and powered by Gemini and Llama AI models.

## 🌟 Features

- **Personalized Health Profiles**: Create and manage detailed health profiles with age, weight, height, activity level, and more
- **AI-Powered Plans**: Generate customized dietary and fitness plans based on your profile
- **Interactive Chat Assistant**: Get real-time advice and answers about your health and fitness journey
- **Multiple AI Models**: Choose between Gemini 2.5 Pro and Llama 3.3 70B for plan generation
- **Persistent Storage**: Save and load your profiles and plans across sessions
- **Modern UI**: Beautiful, responsive interface with intuitive navigation
- **Real-time Streaming**: Watch AI responses appear in real-time with a typing effect

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Models**: 
  - Google Gemini 2.5 Pro
  - Llama 3.3 70B (via Groq)
- **State Management**: Streamlit Session State
- **Styling**: Custom CSS with modern design elements

## 📋 Prerequisites

- Python 3.8 or higher
- Google API Key for Gemini
- Groq API Key for Llama model
- Required Python packages (see requirements.txt)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/Abdulraqib20/ai-health-and-fitness-planner.git
cd ai-competitor-analysis
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your API keys:
   - Create a `config` directory
   - Add your API keys to `config/appconfig_cloud.py`:
```python
GOOGLE_API_KEY = "your-gemini-api-key"
GROQ_API_KEY = "your-groq-api-key"
```

## 💻 Usage

1. Start the application:
```bash
streamlit run src/main2.py
```

2. Open your browser and navigate to the provided URL (typically http://localhost:8501)

3. Create your health profile by filling in the required information

4. Generate personalized dietary and fitness plans

5. Use the chat assistant to get advice and answers about your health journey

## 📱 Features in Detail

### Health Profile Creation
- Age, weight, height, and sex
- Activity level selection
- Fitness goals
- Dietary preferences
- Health conditions
- Available time for exercise

### AI-Generated Plans
- **Dietary Plan**:
  - Personalized meal recommendations
  - Nutritional guidelines
  - Important considerations
  - Hydration and electrolyte advice

- **Fitness Plan**:
  - Customized exercise routines
  - Warm-up and cool-down exercises
  - Progress tracking tips
  - Form and safety guidelines

### Chat Assistant
- Real-time responses
- Context-aware advice
- Streaming response display
- Persistent chat history

## 🔒 Security

- API keys are stored securely in configuration files
- User data is managed through session state
- Persistent storage for user profiles and plans

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- Built with ❤️ by raqibcodes for Raqib Health
- Powered by Google Gemini and Llama AI models
- Styled with Streamlit and custom CSS

## 📞 Support

For support, please open an issue in the GitHub repository or contact abdulraqibshakir03@gmail.com
