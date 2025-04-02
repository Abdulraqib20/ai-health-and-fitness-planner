import os
import sys
from pathlib import Path

import streamlit as st
from agno.agent import Agent
from agno.models.google.gemini import Gemini
from agno.models.groq.groq import Groq

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('config/logs/config.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(str(Path(__file__).parent.parent.resolve()))

from config.appconfig_cloud import (
    GROQ_API_KEY,
    GOOGLE_API_KEY,
)

#-----------------------------------------------------
# Configs
#-----------------------------------------------------
GEMINI_MODEL_NAME = "gemini-2.5-pro-exp-03-25"
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"

#--------------------------------------
# Streamlit App Initialization
#--------------------------------------
# Set page configuration
st.set_page_config(
    page_title="AI Health and Fitness Planner",
    page_icon="🏋️",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 0.99rem;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        # color: #4B3FFF;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 500;
        color: #6C63FF;
        margin-bottom: 1rem;
    }
    
    .sidebar {
        background-color: #F5F7FA;
        border-radius: 10px;
        padding: 1.5rem;
    }
    
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #6C5CE7;
        margin-top: 1rem;
    }
    
    .card {
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin-bottom: 1rem;
        background-color: #6C5CE7;
        color: white;
        transition: transform 0.3s ease;
    }
    .metric-card {
        background-color: #6C5CE7;
        color: white;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .card:hover {
        transform: translateY(-5px);
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    .chat-message-user {
        background-color: #E0E7FF;
        border-left: 5px solid #4B3FFF;
    }
    
    .chat-container {
        display: flex;
        flex-direction: column;
        background-color: #FAFAFA;
    }
    
    .footer {
        margin-top: 2rem;
        padding-top: 1rem;
        text-align: center;
        font-size: 0.85rem;
    }
    
    .profile-card {
        # border-radius: 12px;
        # padding: 2rem;
        # margin-bottom: 1.5rem;
        # background-color: white;
        # box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        # border-top: 5px solid #FF6B6B;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #4ECDC4, #6C63FF);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(108, 99, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 7px 14px rgba(108, 99, 255, 0.4);
    }
    
    /* Plan Cards */
    .plan-card {
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .dietary-plan {
        border-left: 5px solid #FF6B6B;
    }
    
    .fitness-plan {
        border-left: 5px solid #4ECDC4;
    }
    
    .plan-card:hover {
        transform: translateY(-5px);
    }
    
    .plan-header {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #333;
        border-bottom: 2px dashed rgba(0, 0, 0, 0.1);
        padding-bottom: 0.5rem;
    }
    
    .tip-box {
        # background-color: #F1F9FE;
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        border-left: 3px solid #4ECDC4;
    }
    
    .warning-box {
        # background-color: #FFF5F5;
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        border-left: 3px solid #FF6B6B;
    }
    
    .success-box {
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        border-left: 3px solid #48BB78;
    }
    
    /* Custom avatar for chat */
    .avatar-user {
        # background-color: #6C63FF;
        # color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 16px;
    }
    
    .avatar-assistant {
        # background-color: #4ECDC4;
        # color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 16px;
    }
    
    /* Model selector */
    .model-selector {
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    
    .model-option {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
    }
    
    .model-icon {
        margin-right: 0.5rem;
        font-size: 1.2rem;
    }
    
    /* Animation for generating plans */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(78, 205, 196, 0.5); }
        70% { box-shadow: 0 0 0 10px rgba(78, 205, 196, 0); }
        100% { box-shadow: 0 0 0 0 rgba(78, 205, 196, 0); }
    }
    
    .generating {
        animation: pulse 2s infinite;
    }
    
    .stSlider>div>div {
        # background-color: #4ECDC4 !important;
    }
    
    .stProgress>div>div>div>div {
        background-color: #6C63FF !important;
    }

    .chat-area {
        display: flex;
        flex-direction: column;
        # background-color: #FAFAFA; /* Match chat background */
        # border: 1px solid #e0e0e0; /* Optional border */
        # border-radius: 8px; /* Optional rounding */
        # margin-bottom: 1rem; /* Space below chat area */
    }

    .messages-container {
        flex-grow: 1; 
        overflow-y: auto; /* Allows scrolling for messages */
        padding: 1rem;
    }

    .input-container {
        flex-shrink: 0;
        # padding: 0.5rem 1rem; /* Padding around input */
        # background-color: white; /* Input background */
    }
</style>
""", unsafe_allow_html=True)


#--------------------------------------
# Session persistence
#--------------------------------------
@st.cache_resource
def get_persistent_state():
    """Return a persistent state object that will retain data across sessions."""
    return {
        "user_profiles": {},
        "plans": {},
        "chat_history": {}
    }

# Initialize persistent state
persistent_state = get_persistent_state()

# Initialize session state variables
if 'dietary_plan' not in st.session_state:
    logger.debug("Initializing dietary_plan in session state")
    st.session_state.dietary_plan = {}

if 'fitness_plan' not in st.session_state:
    logger.debug("Initializing fitness_plan in session state")
    st.session_state.fitness_plan = {}

if 'plans_generated' not in st.session_state:
    logger.debug("Initializing plans_generated in session state")
    st.session_state.plans_generated = False

if 'chat_history' not in st.session_state:
    logger.debug("Initializing chat_history in session state")
    st.session_state.chat_history = []

if 'user_id' not in st.session_state:
    logger.debug("Initializing user_id in session state")
    st.session_state.user_id = None

if 'selected_model' not in st.session_state:
    logger.debug("Initializing selected_model in session state")
    st.session_state.selected_model = GEMINI_MODEL_NAME
    
if 'view_profiles' not in st.session_state:
    st.session_state.view_profiles = False

if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "Profile"


#--------------------------------------
# Helper Functions
#--------------------------------------
def initialize_model(model_name):
    """Initialize the selected AI model"""
    logger.info(f"Initializing model: {model_name}")
    try:
        if model_name == GEMINI_MODEL_NAME:
            logger.debug("Initializing Gemini model")
            return Gemini(id=GEMINI_MODEL_NAME, api_key=GOOGLE_API_KEY)
        elif model_name == GROQ_MODEL_NAME:
            logger.debug("Initializing Groq model")
            return Groq(id=GROQ_MODEL_NAME, api_key=GROQ_API_KEY)
        else:
            logger.error(f"Invalid model selection: {model_name}")
            st.error("Invalid model selection")
            return None
    except Exception as e:
        logger.error(f"Error initializing model {model_name}: {str(e)}", exc_info=True)
        raise

def display_chat_history():
    """Display chat history in a Streamlit chat interface"""
    logger.debug("Displaying chat history")
    if not st.session_state.chat_history:
        logger.debug("No chat history to display")
        return
    
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message["content"])

def add_message(role, content):
    """Add a message to the chat history"""
    logger.debug(f"Adding {role} message to chat history")
    st.session_state.chat_history.append({"role": role, "content": content})
    
    if st.session_state.user_id:
        logger.debug(f"Persisting message for user {st.session_state.user_id}")
        if st.session_state.user_id not in persistent_state["chat_history"]:
            persistent_state["chat_history"][st.session_state.user_id] = []
        persistent_state["chat_history"][st.session_state.user_id].append({"role": role, "content": content})
        
def create_user_profile(user_data):
    """Create a user profile with a unique ID"""
    logger.info("Creating new user profile")
    try:
        import uuid
        user_id = str(uuid.uuid4())
        persistent_state["user_profiles"][user_id] = user_data
        logger.debug(f"Created profile for user {user_id}")
        return user_id
    except Exception as e:
        logger.error(f"Error creating user profile: {str(e)}", exc_info=True)
        raise

def display_dietary_plan(plan_content):
    """Display dietary plan in an attractive format"""
    logger.info("Displaying dietary plan")
    try:
        with st.container():
            st.markdown("<div class='plan-card dietary-plan'>", unsafe_allow_html=True)
            st.markdown("<h3 class='plan-header'>🍽️ Your Personalized Dietary Plan</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 🎯 Why this plan works")
                st.markdown(f"<div class='success-box'>{plan_content.get('why_this_plan_works', 'Information not available')}</div>", unsafe_allow_html=True)
                
                st.markdown("### 🍽️ Meal Plan")
                st.markdown(plan_content.get("meal_plan", "Plan not available"))
            
            with col2:
                st.markdown("### ⚠️ Important Considerations")
                considerations = plan_content.get("important_considerations", "").split('\n')
                for consideration in considerations:
                    if consideration.strip():
                        st.markdown(f"<div class='warning-box'>{consideration}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error displaying dietary plan: {str(e)}", exc_info=True)
        raise

def display_fitness_plan(plan_content):
    """Display fitness plan in an attractive format"""
    logger.info("Displaying fitness plan")
    try:
        
        with st.container():
            st.markdown("<div class='plan-card fitness-plan'>", unsafe_allow_html=True)
            st.markdown("<h3 class='plan-header'>💪 Your Personalized Fitness Plan</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 🎯 Goals")
                st.markdown(f"<div class='success-box'>{plan_content.get('goals', 'Goals not specified')}</div>", unsafe_allow_html=True)
                
                st.markdown("### 🏋️‍♂️ Exercise Routine")
                st.markdown(plan_content.get("routine", "Routine not available"))
            
            with col2:
                st.markdown("### 💡 Pro Tips")
                tips = plan_content.get("tips", "").split('\n')
                for tip in tips:
                    if tip.strip():
                        st.markdown(f"<div class='tip-box'>{tip}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error displaying fitness plan: {str(e)}", exc_info=True)
        raise

def stream_response(agent, context):
    """Get the full response from the agent and yield it chunk by chunk."""
    logger.info("Generating response using agent.run and simulating stream")
    full_response = ""
    try:
        # Get the complete response first
        response = agent.run(context)
        
        if hasattr(response, 'content') and response.content:
            content = response.content
            logger.debug(f"Got agent response content of length: {len(content)}")
            # Yield the content chunk by chunk
            chunk_size = 1 # Small chunk size for noticeable streaming effect
            for i in range(0, len(content), chunk_size):
                yield content[i:i+chunk_size]
            full_response = content
        else:
            logger.warning("Agent response did not have valid content.")
            yield "Sorry, I couldn't generate a valid response."
            full_response = "Sorry, I couldn't generate a valid response."
            
    except Exception as e:
        logger.error(f"Error during agent.run or streaming simulation: {str(e)}", exc_info=True)
        error_msg = f"Sorry, an error occurred while generating the response: {str(e)}"
        yield error_msg
        full_response = error_msg
    
    # Note: The full_response is now implicitly returned by st.write_stream capturing the yields

def display_user_profiles():
    """Display all user profiles in the system"""
    logger.info("Displaying all user profiles")
    if not persistent_state["user_profiles"]:
        st.info("No user profiles found")
        return
    
    with st.expander("👥 All User Profiles", expanded=True):
        for user_id, profile in persistent_state["user_profiles"].items():
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                if st.button(f"Load", key=f"load_{user_id}"):
                    st.session_state.user_id = user_id
                    
                    # Load plans if they exist
                    if user_id in persistent_state["plans"]:
                        st.session_state.dietary_plan = persistent_state["plans"][user_id]["dietary_plan"]
                        st.session_state.fitness_plan = persistent_state["plans"][user_id]["fitness_plan"]
                        st.session_state.plans_generated = True
                    
                    # Load chat history if it exists
                    if user_id in persistent_state["chat_history"]:
                        st.session_state.chat_history = persistent_state["chat_history"][user_id]
                    else:
                        st.session_state.chat_history = []
                    
                    st.rerun()
            
            with col2:
                profile_info = f"👤 **{profile.get('age')}yo, {profile.get('sex')}, {profile.get('weight')}kg** | Goals: {profile.get('fitness_goals')} | Diet: {profile.get('dietary_preferences')}"
                st.markdown(profile_info)
            
            with col3:
                if st.button(f"Delete", key=f"delete_{user_id}"):
                    # Remove user from all persistent state
                    persistent_state["user_profiles"].pop(user_id, None)
                    persistent_state["plans"].pop(user_id, None)
                    persistent_state["chat_history"].pop(user_id, None)
                    
                    # If current user is deleted, reset session
                    if st.session_state.user_id == user_id:
                        st.session_state.user_id = None
                        st.session_state.plans_generated = False
                        st.session_state.chat_history = []
                    
                    st.rerun()
            
            st.divider()


def main():
    logger.info("Starting application main function")
    st.markdown("<h1 class='main-header'>🏋️ AI Health & Fitness Planner</h1>", unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("<div class='sidebar-header'>⚙️ Model Configuration</div>", unsafe_allow_html=True)
        
        model_option = st.radio(
            "Select AI Model:",
            ["Gemini 2.5 Pro", "Llama 3.3 70B"],
            index=0,
            help="Choose which AI model to use for generating your plans"
        )
        
        # Map the selection to the model name constants
        if model_option == "Gemini 2.5 Pro":
            st.session_state.selected_model = GEMINI_MODEL_NAME
        else:
            st.session_state.selected_model = GROQ_MODEL_NAME
            
        logger.debug(f"Selected model: {model_option}")
            
        st.markdown(f"<div class='success-box'>Using: {model_option}</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='sidebar-header'>👤 User Profile</div>", unsafe_allow_html=True)
        
        if st.session_state.user_id:
            user_data = persistent_state["user_profiles"].get(st.session_state.user_id, {})
            if user_data:
                st.markdown(f"<div class='success-box'>Profile: {user_data.get('age')} years, {user_data.get('weight')}kg, {user_data.get('fitness_goals')}</div>", unsafe_allow_html=True)
                
                if st.button("Create New Profile"):
                    logger.info("User requested new profile creation")
                    st.session_state.user_id = None
                    st.session_state.plans_generated = False
                    st.session_state.chat_history = []
                    st.rerun()
        
        # Button to view all profiles
        if st.button("👥 View All Profiles"):
            st.session_state.view_profiles = True
            st.rerun()
        
        # Reset view profiles state
        if st.session_state.view_profiles:
            if st.button("❌ Hide Profiles"):
                st.session_state.view_profiles = False
                st.rerun()
    
    # Display all profiles if requested
    if st.session_state.view_profiles:
        display_user_profiles()

    # Initialize the selected model
    try:
        logger.info(f"Initializing model: {st.session_state.selected_model}")
        model = initialize_model(st.session_state.selected_model)
        
    except Exception as e:
        logger.error(f"Model initialization failed: {str(e)}", exc_info=True)
        st.error(f"❌ Error initializing model: {e}")
        return
    
    # Main content layout
    if not st.session_state.plans_generated:
        logger.info("Displaying profile collection form")
        # Profile collection form
        st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='sub-header'>👤 Complete Your Health Profile</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.number_input("Age", min_value=10, max_value=100, step=1, help="Enter your age")
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, step=0.1)
            activity_level = st.selectbox(
                "Activity Level",
                options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
                help="Choose your typical activity level"
            )
        
        with col2:
            weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, step=0.1)
            sex = st.selectbox("Sex", options=["Male", "Female", "Other"])
            fitness_goals = st.selectbox(
                "Fitness Goals",
                options=["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"],
                help="What do you want to achieve?"
            )
            
        with col3:
            dietary_preferences = st.selectbox(
                "Dietary Preferences",
                options=["No Restrictions", "Vegetarian", "Vegan", "Keto", "Gluten Free", "Low Carb", "Dairy Free"],
                help="Select your dietary preference"
            )
            
            health_conditions = st.multiselect(
                "Health Conditions",
                options=["None", "Diabetes", "Hypertension", "Heart Disease", "Joint Pain", "Obesity", "Other"],
                default=["None"],
                help="Select any relevant health conditions"
            )
            
            time_available = st.slider(
                "Time Available (minutes/day)",
                min_value=15,
                max_value=120,
                value=45,
                step=15,
                help="How much time can you dedicate to exercise daily?"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🎯 Generate My Personalized Plans", use_container_width=True):
            logger.info("User requested plan generation")
            # Store user profile
            user_data = {
                "age": age,
                "weight": weight,
                "height": height,
                "sex": sex,
                "activity_level": activity_level,
                "dietary_preferences": dietary_preferences,
                "fitness_goals": fitness_goals,
                "health_conditions": health_conditions,
                "time_available": time_available
            }
            
            # Create user ID if not exists
            if not st.session_state.user_id:
                logger.debug("Creating new user profile")
                st.session_state.user_id = create_user_profile(user_data)
            
            with st.spinner("Creating your perfect health and fitness routine..."):
                try:
                    logger.info("Initializing agents for plan generation")
                    # Initialize dietary and fitness agents
                    dietary_agent = Agent(
                        name="Dietary Expert",
                        role="Provides personalized dietary recommendations",
                        model=model,
                        instructions=[
                            "Consider the user's input, including dietary restrictions and preferences.",
                            "Suggest a detailed meal plan for the day, including breakfast, lunch, dinner, and snacks.",
                            "Provide a brief explanation of why the plan is suited to the user's goals.",
                            "Focus on clarity, coherence, and quality of the recommendations.",
                        ]
                    )

                    fitness_agent = Agent(
                        name="Fitness Expert",
                        role="Provides personalized fitness recommendations",
                        model=model,
                        instructions=[
                            "Provide exercises tailored to the user's goals.",
                            "Include warm-up, main workout, and cool-down exercises.",
                            "Explain the benefits of each recommended exercise.",
                            "Ensure the plan is actionable and detailed.",
                        ]
                    )

                    user_profile = f"""
                    Age: {age}
                    Weight: {weight}kg
                    Height: {height}cm
                    Sex: {sex}
                    Activity Level: {activity_level}
                    Dietary Preferences: {dietary_preferences}
                    Fitness Goals: {fitness_goals}
                    Health Conditions: {', '.join(health_conditions)}
                    Time Available: {time_available} minutes per day
                    """

                    dietary_plan_response = dietary_agent.run(user_profile)
                    dietary_plan = {
                        "why_this_plan_works": "High Protein, Healthy Fats, Moderate Carbohydrates, and Caloric Balance",
                        "meal_plan": dietary_plan_response.content,
                        "important_considerations": """
                        - Hydration: Drink plenty of water throughout the day
                        - Electrolytes: Monitor sodium, potassium, and magnesium levels
                        - Fiber: Ensure adequate intake through vegetables and fruits
                        - Listen to your body: Adjust portion sizes as needed
                        """
                    }

                    fitness_plan_response = fitness_agent.run(user_profile)
                    fitness_plan = {
                        "goals": "Build strength, improve endurance, and maintain overall fitness",
                        "routine": fitness_plan_response.content,
                        "tips": """
                        - Track your progress regularly
                        - Allow proper rest between workouts
                        - Focus on proper form
                        - Stay consistent with your routine
                        """
                    }

                    st.session_state.dietary_plan = dietary_plan
                    st.session_state.fitness_plan = fitness_plan
                    st.session_state.plans_generated = True
                    
                    # Store plans in persistent state
                    persistent_state["plans"][st.session_state.user_id] = {
                        "dietary_plan": dietary_plan,
                        "fitness_plan": fitness_plan
                    }
                    
                    st.rerun()

                except Exception as e:
                    logger.error(f"Plan generation failed: {str(e)}", exc_info=True)
                    st.error(f"❌ An error occurred: {str(e)}")
    
    else:
        # Use tabs for better navigation in the generated plans section
        tab1, tab2, tab3 = st.tabs(["📊 My Plans", "💬 Chat Assistant", "⚙️ Settings"])
        
        with tab1:
            # Display generated plans
            st.markdown("<h2 class='sub-header'>Your Personalized Plans</h2>", unsafe_allow_html=True)
            display_dietary_plan(st.session_state.dietary_plan)
            display_fitness_plan(st.session_state.fitness_plan)
        
        with tab2:
            st.markdown("<h2 class='sub-header'>💬 Chat with your Health & Fitness Assistant</h2>", unsafe_allow_html=True)

            # Main chat area with flex layout
            st.markdown("<div class='chat-area'>", unsafe_allow_html=True)

            # Messages container (scrollable)
            st.markdown("<div class='messages-container'>", unsafe_allow_html=True)
            # Display existing chat history first
            display_chat_history()

            # --- Handle AI Response Generation --- 
            if len(st.session_state.chat_history) > 0 and st.session_state.chat_history[-1]["role"] == "user":
                prompt = st.session_state.chat_history[-1]["content"]
                
                # Create context from plans
                dietary_plan = st.session_state.dietary_plan
                fitness_plan = st.session_state.fitness_plan
                
                context = f"""
                Dietary Plan: {dietary_plan.get('meal_plan', '')}
                Fitness Plan: {fitness_plan.get('routine', '')}
                User Question: {prompt}
                Previous Chat History: {str(st.session_state.chat_history[:-1] if len(st.session_state.chat_history) > 1 else [])}
                """
                
                # Use st.chat_message for the assistant's response area
                with st.chat_message("assistant", avatar="🤖"):
                    try:
                        # Show thinking indicator
                        thinking_placeholder = st.empty()
                        thinking_placeholder.markdown("AI is thinking...")
                        
                        logger.info("Initializing agent for response generation")
                        agent = Agent(
                            name="Health & Fitness Assistant",
                            role="Provides personalized health and fitness advice",
                            model=model,
                            markdown=True,
                            instructions=[
                                "Answer questions about the user's dietary and fitness plans.",
                                "Provide helpful, actionable advice.",
                                "Be friendly and encouraging.",
                                "If asked about something not in the plans, make reasonable recommendations based on their profile."
                            ]
                        )
                        
                        logger.debug("Streaming agent response")
                        # Use st.write_stream to display the response
                        response_generator = stream_response(agent, context)
                        full_response = st.write_stream(response_generator)
                        
                        # Clear thinking indicator
                        thinking_placeholder.empty()
                        
                        # Add the complete assistant message to history *after* streaming
                        add_message("assistant", full_response)
                        logger.info("Assistant response added to chat history")
                        # Crucially, trigger a rerun *after* adding the message to display it from history
                        st.rerun()
                        
                    except Exception as e:
                        logger.error(f"Error in response generation: {str(e)}", exc_info=True)
                        error_message = f"Sorry, I encountered an error: {str(e)}"
                        st.markdown(error_message)
                        # Add error message to history and rerun
                        if st.session_state.chat_history[-1]['content'] != error_message:
                             add_message("assistant", error_message)
                             st.rerun()

            st.markdown("</div>", unsafe_allow_html=True) # Close messages-container

            st.markdown("<div class='input-container'>", unsafe_allow_html=True)
            # Clear chat button (optional, can be placed elsewhere)
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                if st.session_state.user_id:
                    persistent_state["chat_history"][st.session_state.user_id] = []
                st.rerun()
                
            if prompt := st.chat_input("Ask about your plan or for more personalized advice..."):
                logger.info(f"User question received: {prompt}")
                add_message("user", prompt)
                # Rerun immediately to display user message and trigger AI response generation above
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True) # Close input-container

            st.markdown("</div>", unsafe_allow_html=True) # Close chat-area
        
        with tab3:
            st.markdown("<h2 class='sub-header'>⚙️ Settings & Management</h2>", unsafe_allow_html=True)
            st.markdown("Manage your profile and sessions here.")
            
            if st.button("🔄 Generate New Plans"):
                # Keep user profile but regenerate plans
                st.session_state.plans_generated = False
                st.rerun()
            
            if st.button("👤 Create New Profile"):
                # Reset everything
                st.session_state.user_id = None
                st.session_state.plans_generated = False
                st.session_state.chat_history = []
                st.rerun()

    # Footer
    st.sidebar.markdown("""
    <div class="footer">
        <p>Built with ❤️ by raqibcodes for Raqib Health</p>
    </div>
    """, unsafe_allow_html=True)



if __name__ == "__main__":
    logger.info("Application starting")
    main()
    logger.info("Application shutting down")

