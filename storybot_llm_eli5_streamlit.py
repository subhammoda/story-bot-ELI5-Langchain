import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add better error handling for imports
try:
    from storybot_agents import StoryBot, create_storybot
    from storybot_config import get_config
    from storybot_exceptions import (
        StoryBotException, APIKeyError, ValidationError, 
        LLMError, AgentError, PipelineError, UIError
    )
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("Please check that all dependencies are installed correctly.")
    st.stop()

# Custom CSS for enhanced styling with new theme
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
    }
    
    /* Title styling */
    .title-text {
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Subtitle styling */
    .subtitle-text {
        color: #2D3748;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 1rem;
        font-size: 1.1rem;
        background: rgba(255, 255, 255, 0.9);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border-radius: 25px;
        border: none;
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
        padding: 1rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        width: 100%;
        max-width: 300px;
        margin: 0 auto;
        display: block;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Center button container */
    .button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
    }
    
    /* Story container styling */
    .story-container {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    /* Success message styling */
    .success-message {
        background: linear-gradient(45deg, #48BB78, #38A169);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    /* Warning message styling */
    .warning-message {
        background: linear-gradient(45deg, #F6AD55, #ED8936);
        color: #2D3748;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    /* Error message styling */
    .error-message {
        background: linear-gradient(45deg, #F56565, #E53E3E);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #718096;
        font-style: italic;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid #E2E8F0;
    }
    
    /* Loading animation */
    .loading-container {
        text-align: center;
        padding: 2rem;
    }
    
    /* Emoji decorations */
    .emoji-decoration {
        font-size: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Agent info styling */
    .agent-info {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .agent-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .agent-card {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# Configure page
st.set_page_config(
    page_title="Story Bot LLM - ELI5", 
    page_icon="🧠", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Check for API key
if not os.getenv('GEMINI_API_KEY'):
    st.markdown('<div class="error-message">⚠️ GEMINI_API_KEY not found in environment variables!</div>', unsafe_allow_html=True)
    st.info("Please add your Gemini API key to the environment variables.")
    st.stop()

# Initialize StoryBot
try:
    storybot = create_storybot()
except Exception as e:
    st.markdown('<div class="error-message">Failed to initialize StoryBot!</div>', unsafe_allow_html=True)
    st.error(f"Error: {str(e)}")
    st.stop()

# Main container
with st.container():
    st.markdown('<div class="emoji-decoration">🧠✨📚</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="title-text">Story Bot LLM - Explain Like I\'m 5</h1>', unsafe_allow_html=True)
    
    st.markdown('<p class="subtitle-text">Ever wondered how to explain <span style="background: linear-gradient(45deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: bold;">quantum physics</span>, <span style="background: linear-gradient(45deg, #764ba2, #667eea); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: bold;">machine learning</span>, or even <span style="background: linear-gradient(45deg, #9f7aea, #667eea); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: bold;">black holes</span> to a 5-year-old? This app uses a team of intelligent AI agents to do just that. Powered by LangChain and Gemini 2.0 Flash, it takes any topic you enter, researches it, simplifies it, and transforms it into a fun, age-appropriate story — just like a children\'s book. Whether you\'re a parent, teacher, or just curious, this is the perfect way to make complex ideas beautifully simple.</p>', unsafe_allow_html=True)

# Input section with enhanced styling
st.markdown('<div class="emoji-decoration">🎯</div>', unsafe_allow_html=True)
st.markdown("**Enter a topic you'd like explained as a story for a 5-year-old:**")
topic = st.text_input("Topic", 
                      placeholder="e.g., photosynthesis, gravity, or how computers work",
                      label_visibility="collapsed")

# Generate button with enhanced styling - centered
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button("🚀 Generate Magical Story", type="primary"):
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not topic.strip():
        st.markdown('<div class="warning-message">Please enter a topic to generate a story!</div>', unsafe_allow_html=True)
    else:
        with st.spinner("🪄 The AI agents are working their magic..."):
            try:
                # Call the new StoryBot system
                result = storybot.create_story(topic)
                
                st.markdown('<div class="success-message">🎉 Story generated successfully!</div>', unsafe_allow_html=True)
                
                # Display only the final story in a beautiful container
                final_story = result.get('final_story', result['review'])
                
                st.markdown('<div class="story-container"><h3>📖 Your Story</h3> <p>' + final_story + '</p></div>', 
                unsafe_allow_html=True)
                
                # Add some decorative elements
                st.markdown('<div class="emoji-decoration">🌟✨🎭</div>', unsafe_allow_html=True)

            except Exception as e:
                st.markdown('<div class="error-message">Something went wrong while generating the story. Please try again.</div>', unsafe_allow_html=True)
                st.exception(e)
                st.info("If this is a deployment issue, please check the logs for more details.")
else:
    st.markdown('</div>', unsafe_allow_html=True)

# Agent information section
with st.expander("🤖 Meet the AI Crew"):
    st.markdown("""
    <div class="agent-info">
        <h4 style="text-align: center; margin-bottom: 1rem;">Our AI Agents Work Together to Create Perfect Stories</h4>
        <div class="agent-grid">
            <div class="agent-card">
                <h5>🧑‍🔬 Researcher</h5>
                <p style="font-size: 0.9rem;">Gathers accurate information about your topic</p>
            </div>
            <div class="agent-card">
                <h5>📘 Simplifier</h5>
                <p style="font-size: 0.9rem;">Makes complex concepts easy to understand</p>
            </div>
            <div class="agent-card">
                <h5>🧙 Storywriter</h5>
                <p style="font-size: 0.9rem;">Creates engaging stories with fun characters</p>
            </div>
            <div class="agent-card">
                <h5>👶 Educator</h5>
                <p style="font-size: 0.9rem;">Reviews and ensures age-appropriate content</p>
            </div>
        </div>
        <p style="text-align: center; margin-top: 1rem; font-size: 0.9rem; color: #666;">
            💡 Check the console/terminal for detailed logs of each step!
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer with enhanced styling
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("**Built using LangChain, Gemini 2.0 Flash and Streamlit | © SubhamModa 2025**")
st.markdown("</div>", unsafe_allow_html=True) 