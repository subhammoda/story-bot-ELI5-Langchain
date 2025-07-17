"""Custom exceptions for the StoryBot application."""


class StoryBotException(Exception):
    """Base exception class for StoryBot application."""
    
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class APIKeyError(StoryBotException):
    """Raised when API key is missing or invalid."""
    
    def __init__(self, message: str = "API key is missing or invalid"):
        super().__init__(message, "API_KEY_ERROR")


class ValidationError(StoryBotException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message, "VALIDATION_ERROR")


class LLMError(StoryBotException):
    """Raised when there's an error with the language model."""
    
    def __init__(self, message: str, original_error: Exception = None):
        self.original_error = original_error
        super().__init__(message, "LLM_ERROR")


class AgentError(StoryBotException):
    """Raised when there's an error with an agent."""
    
    def __init__(self, message: str, agent_name: str = None):
        self.agent_name = agent_name
        super().__init__(message, "AGENT_ERROR")


class PipelineError(StoryBotException):
    """Raised when there's an error in the story generation pipeline."""
    
    def __init__(self, message: str, step: str = None):
        self.step = step
        super().__init__(message, "PIPELINE_ERROR")