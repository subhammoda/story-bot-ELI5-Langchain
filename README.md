# 🧠 StoryBot-ELI5 (LangChain Edition)

Ever wanted to understand complex topics in a way even a child can grasp? This project turns **any topic** into a delightful short story understandable by a 5-year-old — using a team of autonomous AI agents powered by **LangChain**, **Gemini 2.0 Flash**, and **Streamlit**.

## 🚀 Live Demo

**🌐 [Try the Live App](https://subhammoda-story-bot-eli5-langchain.streamlit.app/)**

Deployable on **Streamlit Cloud**

## 🎯 What It Does

When a user inputs a topic and selects an age, a multi-agent system collaborates to:

1. **Research** the topic for accurate information.
2. **Simplify** the technical language and concepts for the target age group.
3. **Weave a story** with age-appropriate metaphors and vocabulary.
4. **Review** the story for clarity and engagement for the selected age group.

## 🧩 Features

- ✨ **Natural-language input** for any topic
- 👥 **Age-adaptive storytelling** (5-50+ years old)
- 🧠 **Autonomous multi-agent reasoning** pipeline (LangChain/LangGraph)
- 📖 **Age-appropriate storytelling** using Gemini 2.0 Flash
- 📱 **Fully responsive design** for all devices
- 🛠 **Modular and extensible** agent/task architecture
- 🔧 **Object-Oriented Design** with proper encapsulation
- 🛡️ **Custom Exception Handling** for robust error management
- 🧪 **Testing Framework** included
- 📝 **Simple Language Toggle**: Option to make stories even more jargon-free and accessible for all ages (great for older adults or anyone who prefers ultra-simple language)

## 🏗️ Architecture

The project follows **Object-Oriented Programming** principles with:

### Core Classes
- **`StoryBot`**: Main orchestrator class that manages the agent pipeline
- **`BaseAgent`**: Abstract base class for all agents
- **`ResearcherAgent`**: Researches and gathers information
- **`SimplifierAgent`**: Simplifies complex information for children
- **`StorywriterAgent`**: Creates engaging stories
- **`EducatorAgent`**: Reviews and improves stories
- **`StoryBotUI`**: Manages the Streamlit user interface
- **`StoryBotConfig`**: Centralized configuration management

### Design Patterns
- **Factory Pattern**: `create_storybot()` function for easy instantiation
- **Abstract Base Classes**: `BaseAgent` for consistent agent interface
- **Configuration Pattern**: Centralized settings management
- **Exception Hierarchy**: Custom exceptions for different error types

## 🛠 Tech Stack

- LangChain — LLM framework
- Gemini 2.0 Flash — Language model backend
- Streamlit — UI for user interaction
- Custom CSS — Advanced styling and animations
- Python 3.11+

## 📂 Project Structure

```
story-bot-ELI5-Langchain/
│
├── storybot_llm_eli5_streamlit.py       # Streamlit UI (StoryBotUI class)
├── storybot_agents.py                   # Agent classes and StoryBot orchestrator
├── storybot_config.py                   # Configuration management system
├── storybot_exceptions.py               # Custom exception classes
├── test_storybot.py                     # Testing and examples
├── style.css                            # Additional CSS animations
├── .streamlit/config.toml               # Streamlit theme configuration
├── requirements.txt                     # Python dependencies
├── README.md                            # You're here!
```

## 🧪 How to Run Locally

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/story-bot-ELI5-Langchain.git
cd story-bot-ELI5-Langchain
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Your API Key

Add your Gemini API key to .env file:

```
GEMINI_API_KEY=your-gemini-api-key
```

### 4. Launch the App

```bash
streamlit run storybot_llm_eli5_streamlit.py
```

### 5. Run Tests (Optional)

```bash
python test_storybot.py
```

## ☁️ Deploy on Streamlit Cloud

Just push to GitHub and connect your repo on [Streamlit Cloud](https://streamlit.io/cloud). Set the `GEMINI_API_KEY` secret in the app settings.

## 🔧 Configuration

The app uses a centralized configuration system. You can customize:

### Environment Variables
- `GEMINI_API_KEY`: Your Gemini API key (required)
- `LLM_MODEL`: Model to use (default: "gemini-2.0-flash-001")
- `LLM_TEMPERATURE`: Model temperature (default: 0.7)
- `MIN_TOPIC_LENGTH`: Minimum topic length (default: 3)
- `MAX_TOPIC_LENGTH`: Maximum topic length (default: 200)

### Agent Configuration
Each agent can be configured with:
- Custom temperature settings
- Different prompts
- Specific behaviors

## 🧪 Testing

The project includes a comprehensive test suite:

```python
# Run all tests
python test_storybot.py

# Test specific components
from test_storybot import test_configuration, test_exceptions
test_configuration()
test_exceptions()
```

## 🔄 Usage Examples

### Basic Usage
```python
from storybot_agents import create_storybot

# Create a StoryBot instance
storybot = create_storybot()

# Generate a story for a 5-year-old (default)
result = storybot.create_story("Quantum Physics")
print(result['final_story'])

# Generate a story for a specific age
result = storybot.create_story("Quantum Physics", age=15)
print(result['final_story'])
print(f"Age group: {result['age_config']['name']}")

# Generate a story with even simpler, jargon-free language (for any age)
result = storybot.create_story("Quantum Physics", age=70, simpler_language=True)
print(result['final_story'])
```

### Advanced Usage
```python
from storybot_agents import StoryBot
from storybot_config import StoryBotConfig

# Custom configuration
config = StoryBotConfig()
config.llm_config.temperature = 0.9

# Create StoryBot with custom config
storybot = StoryBot(api_key="your-key", config=config)

# Get agent information
agent_info = storybot.get_agent_info()
print(agent_info)
```

### Error Handling
```python
from storybot_exceptions import ValidationError, PipelineError

try:
    result = storybot.create_story("")
except ValidationError as e:
    print(f"Validation error: {e.message}")
except PipelineError as e:
    print(f"Pipeline error: {e.message}")
```

## 🤝 Contributions

Contributions are welcome! Open an issue or submit a PR with improvements or ideas.

### Development Guidelines
- Follow OOP principles
- Add tests for new features
- Use the configuration system for settings
- Handle exceptions appropriately
- Document new classes and methods

## 📜 License

MIT License. Use it, remix it, share it freely.

---

> "If you can't explain it simply, you don't understand it well enough." – _Albert Einstein_ 