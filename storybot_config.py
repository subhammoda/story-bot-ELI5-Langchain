import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from dotenv import load_dotenv


@dataclass
class AgentConfig:
    """Configuration for individual agents."""
    name: str
    emoji: str
    description: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None


@dataclass
class UIConfig:
    """Configuration for the user interface."""
    page_title: str = "StoryBot ELI5"
    page_icon: str = "🧠"
    layout: str = "centered"
    theme_primary_color: str = "#FF8C42"
    theme_background_color: str = "#FFF8F0"
    theme_secondary_background_color: str = "#F6AD55"
    theme_text_color: str = "#2D3748"


@dataclass
class LLMConfig:
    """Configuration for the language model."""
    model: str = "gemini-2.0-flash-001"
    temperature: float = 0.7
    max_tokens: Optional[int] = None


class StoryBotConfig:
    """Main configuration class for the StoryBot application."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Optional path to a configuration file.
        """
        load_dotenv()
        self._load_default_config()
        if config_file:
            self._load_config_file(config_file)
    
    def _load_default_config(self):
        """Load default configuration values."""
        # LLM Configuration
        self.llm_config = LLMConfig(
            model=os.getenv("LLM_MODEL", "gemini-2.0-flash-001"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "0")) if os.getenv("LLM_MAX_TOKENS") else None
        )
        
        # UI Configuration
        self.ui_config = UIConfig()
        
        # Agent Configurations
        self.agents_config = {
            "researcher": AgentConfig(
                name="Researcher",
                emoji="🧑‍🔬",
                description="Researches and gathers information about topics",
                temperature=0.3
            ),
            "simplifier": AgentConfig(
                name="Simplifier",
                emoji="📘",
                description="Simplifies complex information for children",
                temperature=0.5
            ),
            "storywriter": AgentConfig(
                name="Storywriter",
                emoji="🧙",
                description="Creates engaging stories for children",
                temperature=0.8
            ),
            "educator": AgentConfig(
                name="Educator",
                emoji="👶",
                description="Reviews and improves stories for children",
                temperature=0.4
            )
        }
        
        # API Configuration
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        # Validation
        self.min_topic_length = int(os.getenv("MIN_TOPIC_LENGTH", "3"))
        self.max_topic_length = int(os.getenv("MAX_TOPIC_LENGTH", "200"))
        
        # Error Messages
        self.error_messages = {
            "no_api_key": "Gemini API key is required. Set GEMINI_API_KEY environment variable.",
            "invalid_topic": f"Topic must be between {self.min_topic_length} and {self.max_topic_length} characters.",
            "empty_topic": "Topic cannot be empty.",
            "api_error": "An error occurred while processing your request."
        }
    
    def _load_config_file(self, config_file: str):
        """Load configuration from a file (placeholder for future implementation)."""
        # This could be extended to load from JSON, YAML, etc.
        pass
    
    def get_agent_config(self, agent_name: str) -> Optional[AgentConfig]:
        """Get configuration for a specific agent."""
        return self.agents_config.get(agent_name)
    
    def get_all_agents(self) -> Dict[str, AgentConfig]:
        """Get all agent configurations."""
        return self.agents_config.copy()
    
    def validate_api_key(self) -> bool:
        """Validate that API key is present."""
        return bool(self.api_key and self.api_key.strip())
    
    def validate_topic(self, topic: str) -> tuple[bool, Optional[str]]:
        """
        Validate a topic string.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not topic or not topic.strip():
            return False, self.error_messages["empty_topic"]
        
        topic_length = len(topic.strip())
        if topic_length < self.min_topic_length:
            return False, self.error_messages["invalid_topic"]
        
        if topic_length > self.max_topic_length:
            return False, self.error_messages["invalid_topic"]
        
        return True, None
    
    def get_error_message(self, error_type: str) -> str:
        """Get error message by type."""
        return self.error_messages.get(error_type, "An unknown error occurred.")


# Global configuration instance
_config_instance: Optional[StoryBotConfig] = None


def get_config() -> StoryBotConfig:
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = StoryBotConfig()
    return _config_instance


def set_config(config: StoryBotConfig):
    """Set the global configuration instance."""
    global _config_instance
    _config_instance = config 