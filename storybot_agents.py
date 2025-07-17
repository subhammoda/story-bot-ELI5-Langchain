import logging
from abc import ABC, abstractmethod
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain.schema.messages import AIMessage
from typing import Dict, Any, Optional

from storybot_config import get_config, AgentConfig
from storybot_exceptions import (
    APIKeyError, ValidationError, LLMError, AgentError, PipelineError
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base class for all agents in the StoryBot pipeline."""
    
    def __init__(self, llm: GoogleGenerativeAI, config: AgentConfig):
        """
        Initialize the base agent.
        
        Args:
            llm: The language model instance.
            config: Configuration for this agent.
        """
        self.llm = llm
        self.config = config
        self.chain = self._create_chain()
    
    @abstractmethod
    def _create_chain(self) -> RunnableSequence:
        """Create the LangChain runnable sequence for this agent."""
        pass
    
    def process(self, **kwargs) -> str:
        """
        Process input and return output.
        
        Args:
            **kwargs: Input parameters for the agent.
            
        Returns:
            The processed output from the agent.
            
        Raises:
            AgentError: If processing fails.
        """
        try:
            result = self.chain.invoke(kwargs)
            
            # Extract content from AIMessage if needed
            if isinstance(result, AIMessage):
                result_content = result.content
            else:
                result_content = str(result)
            
            # Log the agent's output to console
            logger.info(f"\n{'='*50}")
            logger.info(f"{self.config.emoji} {self.config.name}")
            logger.info(f"{'='*50}")
            logger.info(f"Input: {kwargs}")
            logger.info(f"Output: {result_content}")
            logger.info(f"{'='*50}\n")
            
            return result_content
        except Exception as e:
            raise AgentError(
                f"Failed to process input in {self.config.name}: {str(e)}",
                agent_name=self.config.name
            ) from e
    
    @property
    def name(self) -> str:
        """Get the agent's name."""
        return self.config.name
    
    @property
    def emoji(self) -> str:
        """Get the agent's emoji."""
        return self.config.emoji


class ResearcherAgent(BaseAgent):
    """Agent responsible for researching and gathering information about a topic."""
    
    def __init__(self, llm: GoogleGenerativeAI, config: AgentConfig):
        super().__init__(llm, config)
    
    def _create_chain(self) -> RunnableSequence:
        prompt = PromptTemplate(
            input_variables=["topic"],
            template="""
            You are an Information Research Specialist with over 15 years of experience in academic and applied research. 
            You've developed a reputation for distilling large volumes of information into clear, actionable insights. 
            You've worked across scientific, technical, and policy domains, and are skilled at separating credible sources from noise. 
            You believe that clarity begins with rigorously sourced facts and that even complex ideas can be made understandable with the right foundation.

            Your goal is to gather accurate and relevant information about a given topic from reliable sources.

            Research the topic '{topic}' and summarize the key points in simple terms.
            
            Expected output: A short, accurate summary of the topic using non-technical language.
            """
        )
        return prompt | self.llm


class SimplifierAgent(BaseAgent):
    """Agent responsible for simplifying complex information for children."""
    
    def __init__(self, llm: GoogleGenerativeAI, config: AgentConfig):
        super().__init__(llm, config)
    
    def _create_chain(self) -> RunnableSequence:
        prompt = PromptTemplate(
            input_variables=["research", "age_group_name", "complexity_level", "vocabulary_level", "concept_depth"],
            template="""
            You are a Language Simplifier and Analogy Creator with over a decade of experience working as a science communicator and education consultant. 
            You've helped leading research institutions translate dense material into accessible content for different age groups. 
            You specialize in using analogy, metaphor, and age-appropriate principles to craft explanations that resonate with your target audience. 
            You believe that true understanding starts with empathy for your audience.

            Your goal is to convert complex topics into age-appropriate explanations using analogies and clear language.

            Age Group: {age_group_name}
            Complexity Level: {complexity_level}
            Vocabulary Level: {vocabulary_level}
            Concept Depth: {concept_depth}

            Take the following research summary and simplify it using analogies and language appropriate for this age group:

            {research}
            
            Expected output: A simplified, analogy-rich explanation suitable for the specified age group.
            """
        )
        return prompt | self.llm


class StorywriterAgent(BaseAgent):
    """Agent responsible for creating engaging stories for children."""
    
    def __init__(self, llm: GoogleGenerativeAI, config: AgentConfig):
        super().__init__(llm, config)
    
    def _create_chain(self) -> RunnableSequence:
        prompt = PromptTemplate(
            input_variables=["simple", "age_group_name", "complexity_level", "vocabulary_level", "concept_depth"],
            template="""
            You are a Creative Storyteller with over 12 published storybooks and a background in developmental psychology. 
            You are known for creating narratives that both engage and educate across different age groups. 
            You've spent years refining the craft of weaving core concepts into memorable stories that spark curiosity in learners of all ages. 
            Your storytelling style is imaginative but always grounded in a clear learning goal.

            Your goal is to turn simplified concepts into engaging and imaginative stories suitable for the target age group.

            Age Group: {age_group_name}
            Complexity Level: {complexity_level}
            Vocabulary Level: {vocabulary_level}
            Concept Depth: {concept_depth}

            Create an engaging story for this age group that incorporates the following simplified explanation in a fun and imaginative way:

            {simple}
            
            Expected output: A story that teaches the concept through a narrative appropriate for the specified age group.
            """
        )
        return prompt | self.llm


class EducatorAgent(BaseAgent):
    """Agent responsible for reviewing and improving stories for children."""
    
    def __init__(self, llm: GoogleGenerativeAI, config: AgentConfig):
        super().__init__(llm, config)
    
    def _create_chain(self) -> RunnableSequence:
        prompt = PromptTemplate(
            input_variables=["story", "age_group_name", "complexity_level", "vocabulary_level", "concept_depth"],
            template="""
            You are an Educational Quality Reviewer with 20 years of experience in education across different age groups. 
            You've taught and designed curricula for learners of all ages. 
            You specialize in aligning content with cognitive and emotional development stages for different age groups. 
            You're skilled at identifying what works—and what doesn't—for various age ranges, and you have a critical eye for making sure materials are not just entertaining, but pedagogically sound.

            Your goal is to ensure the story is pedagogically sound, age-appropriate, and aligned with the target age group's comprehension levels.

            Age Group: {age_group_name}
            Complexity Level: {complexity_level}
            Vocabulary Level: {vocabulary_level}
            Concept Depth: {concept_depth}

            Review the following story and provide ONLY the final polished story that is ready for this age group. Add a small paragraph at the end of the story that connects the topic to the story.
            
            IMPORTANT: Keep the final story under 5000 characters to ensure it's concise and engaging.
            
            Do not include any explanations, reviews, or commentary - just the story itself:

            {story}
            
            Expected output: ONLY the final polished story (under 5000 characters), nothing else.
            """
        )
        return prompt | self.llm


class StoryBot:
    """Main class that orchestrates the multi-agent pipeline for creating ELI5 stories."""
    
    def __init__(self, api_key: str = None, config=None):
        """
        Initialize the StoryBot with all agents.
        
        Args:
            api_key: Gemini API key. If None, will try to load from environment.
            config: Configuration instance. If None, will use global config.
        """
        self.config = config or get_config()
        
        # Validate API key
        if api_key is None:
            if not self.config.validate_api_key():
                raise APIKeyError(self.config.get_error_message("no_api_key"))
            api_key = self.config.api_key
        
        # Initialize LLM
        try:
            self.llm = GoogleGenerativeAI(
                model=self.config.llm_config.model,
                google_api_key=api_key,
                temperature=self.config.llm_config.temperature
            )
        except Exception as e:
            raise LLMError("Failed to initialize language model", original_error=e)
        
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all agents in the pipeline."""
        try:
            agents_config = self.config.get_all_agents()
            
            self.researcher = ResearcherAgent(
                self.llm, agents_config["researcher"]
            )
            self.simplifier = SimplifierAgent(
                self.llm, agents_config["simplifier"]
            )
            self.storywriter = StorywriterAgent(
                self.llm, agents_config["storywriter"]
            )
            self.educator = EducatorAgent(
                self.llm, agents_config["educator"]
            )
            
            self.agents = [
                self.researcher,
                self.simplifier,
                self.storywriter,
                self.educator
            ]
        except Exception as e:
            raise PipelineError("Failed to initialize agents", step="initialization") from e
    
    def create_story(self, topic: str, age: int = 5, simpler_language: bool = False) -> Dict[str, Any]:
        """
        Create a complete age-appropriate story from a given topic.
        
        Args:
            topic: The topic to research and turn into a story.
            age: The target age for the story (default: 5).
            simpler_language: If True, use even simpler, jargon-free language (for older adults or anyone who prefers it).
        
        Returns:
            Dictionary containing the output from each agent in the pipeline.
        
        Raises:
            ValidationError: If topic is invalid.
            PipelineError: If story creation fails.
        """
        # Validate topic
        is_valid, error_message = self.config.validate_topic(topic)
        if not is_valid:
            raise ValidationError(error_message, field="topic")
        
        # Validate age
        if age < 5 or age > 100:
            raise ValidationError("Age must be between 5 and 100", field="age")
        
        # Get age-specific configuration
        age_config = self.config.get_age_config(age)
        
        try:
            logger.info(f"\nStarting story creation for topic: '{topic}' for age {age} ({age_config['name']}) | Simpler Language: {simpler_language}")
            logger.info(f"{'='*60}")
            
            # Execute the pipeline with age configuration
            research = self.researcher.process(topic=topic)
            # If simpler_language is True, override complexity/vocab for extra simplicity
            if simpler_language:
                # Use the lowest complexity/vocab/concept settings
                simple = self.simplifier.process(
                    research=research,
                    age_group_name=age_config['name'] + " (Simpler Language Mode)",
                    complexity_level="very_simple",
                    vocabulary_level="basic",
                    concept_depth="fundamental"
                )
                story = self.storywriter.process(
                    simple=simple,
                    age_group_name=age_config['name'] + " (Simpler Language Mode)",
                    complexity_level="very_simple",
                    vocabulary_level="basic",
                    concept_depth="fundamental"
                )
                review = self.educator.process(
                    story=story,
                    age_group_name=age_config['name'] + " (Simpler Language Mode)",
                    complexity_level="very_simple",
                    vocabulary_level="basic",
                    concept_depth="fundamental"
                )
            else:
                simple = self.simplifier.process(
                    research=research, 
                    age_group_name=age_config['name'],
                    complexity_level=age_config['complexity'],
                    vocabulary_level=age_config['vocabulary'],
                    concept_depth=age_config['concepts']
                )
                story = self.storywriter.process(
                    simple=simple, 
                    age_group_name=age_config['name'],
                    complexity_level=age_config['complexity'],
                    vocabulary_level=age_config['vocabulary'],
                    concept_depth=age_config['concepts']
                )
                review = self.educator.process(
                    story=story, 
                    age_group_name=age_config['name'],
                    complexity_level=age_config['complexity'],
                    vocabulary_level=age_config['vocabulary'],
                    concept_depth=age_config['concepts']
                )
            
            logger.info(f"\nStory creation completed successfully!")
            logger.info(f"Final story length: {len(review)} characters")
            logger.info(f"{'='*60}\n")
            
            return {
                "topic": topic,
                "age": age,
                "age_group": self.config.get_age_group(age),
                "age_config": age_config,
                "research": research,
                "simple": simple,
                "story": story,
                "review": review,
                "final_story": review,  # For UI display
                "agents_used": [agent.name for agent in self.agents],
                "simpler_language": simpler_language
            }
        except Exception as e:
            raise PipelineError(
                f"Failed to create story for topic '{topic}' for age {age}: {str(e)}",
                step="story_creation"
            ) from e
    
    def get_agent_info(self) -> Dict[str, str]:
        """Get information about all agents in the pipeline."""
        return {agent.name: agent.emoji for agent in self.agents}
    
    def validate_topic(self, topic: str) -> bool:
        """
        Validate if a topic is suitable for processing.
        
        Args:
            topic: The topic to validate.
            
        Returns:
            True if topic is valid, False otherwise.
        """
        is_valid, _ = self.config.validate_topic(topic)
        return is_valid
    
    def get_agent_by_name(self, name: str) -> Optional[BaseAgent]:
        """
        Get an agent by name.
        
        Args:
            name: The name of the agent to retrieve.
            
        Returns:
            The agent if found, None otherwise.
        """
        for agent in self.agents:
            if agent.name.lower() == name.lower():
                return agent
        return None


# Factory function for easy instantiation
def create_storybot(api_key: str = None, config=None) -> StoryBot:
    """
    Factory function to create a StoryBot instance.
    
    Args:
        api_key: Gemini API key. If None, will try to load from environment.
        config: Configuration instance. If None, will use global config.
        
    Returns:
        Configured StoryBot instance.
    """
    return StoryBot(api_key=api_key, config=config)


# Backward compatibility function
def run_storybot_pipeline(topic: str, age: int = 5) -> Dict[str, Any]:
    """
    Legacy function for backward compatibility.
    
    Args:
        topic: The topic to research and turn into a story.
        age: The target age for the story (default: 5).
        
    Returns:
        Dictionary containing the output from each agent in the pipeline.
    """
    storybot = create_storybot()
    return storybot.create_story(topic, age=age) 