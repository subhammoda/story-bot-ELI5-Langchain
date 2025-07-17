"""
Test file for StoryBot OOP implementation.
This file demonstrates how to use the StoryBot classes and provides examples.
"""

import os
from storybot_agents import StoryBot, create_storybot
from storybot_config import StoryBotConfig, get_config
from storybot_exceptions import (
    StoryBotException, APIKeyError, ValidationError, 
    LLMError, AgentError, PipelineError
)


def test_configuration():
    """Test the configuration system."""
    print("Testing Configuration System...")
    
    # Test default configuration
    config = get_config()
    print(f"Default config loaded: {config.llm_config.model}")
    
    # Test agent configurations
    agents = config.get_all_agents()
    print(f"Found {len(agents)} agents:")
    for name, agent_config in agents.items():
        print(f"   - {agent_config.emoji} {agent_config.name}: {agent_config.description}")
    
    # Test validation
    test_topics = ["", "a", "Quantum Physics", "x" * 201]
    for topic in test_topics:
        is_valid, error = config.validate_topic(topic)
        print(f"   Topic '{topic[:20]}...': {'Valid' if is_valid else f'{error}'}")


def test_exceptions():
    """Test custom exception handling."""
    print("\nTesting Exception System...")
    
    try:
        raise APIKeyError("Test API key error")
    except APIKeyError as e:
        print(f"Caught APIKeyError: {e.message} (Code: {e.error_code})")
    
    try:
        raise ValidationError("Test validation error", field="topic")
    except ValidationError as e:
        print(f"Caught ValidationError: {e.message} (Field: {e.field})")
    
    try:
        raise PipelineError("Test pipeline error", step="testing")
    except PipelineError as e:
        print(f"Caught PipelineError: {e.message} (Step: {e.step})")


def test_storybot_creation():
    """Test StoryBot creation and initialization."""
    print("\nTesting StoryBot Creation...")
    
    # Test with API key from environment
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("No API key found in environment. Skipping StoryBot tests.")
        return False
    
    try:
        # Test factory function
        storybot = create_storybot()
        print("StoryBot created successfully using factory function")
        
        # Test direct instantiation
        config = get_config()
        storybot2 = StoryBot(api_key=api_key, config=config)
        print("StoryBot created successfully using direct instantiation")
        
        # Test agent info
        agent_info = storybot.get_agent_info()
        print(f"Agent info retrieved: {len(agent_info)} agents")
        
        return True
        
    except Exception as e:
        print(f"Failed to create StoryBot: {str(e)}")
        return False


def test_story_creation():
    """Test story creation functionality."""
    print("\nTesting Story Creation...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("No API key found. Skipping story creation test.")
        return
    
    try:
        storybot = create_storybot()
        
        # Test topic validation
        test_topic = "Photosynthesis"
        is_valid = storybot.validate_topic(test_topic)
        print(f"Topic validation: '{test_topic}' is {'valid' if is_valid else 'invalid'}")
        
        # Test story creation (commented out to avoid API calls during testing)
        # print("Creating story (this may take a moment)...")
        # result = storybot.create_story(test_topic)
        # print(f"Story created successfully!")
        # print(f"   Topic: {result['topic']}")
        # print(f"   Agents used: {result['agents_used']}")
        
        print("Story creation test completed (API call skipped)")
        
    except Exception as e:
        print(f"Story creation test failed: {str(e)}")


def test_agent_retrieval():
    """Test agent retrieval functionality."""
    print("\nTesting Agent Retrieval...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("No API key found. Skipping agent retrieval test.")
        return
    
    try:
        storybot = create_storybot()
        
        # Test getting agents by name
        agent_names = ["Researcher", "Simplifier", "Storywriter", "Educator"]
        for name in agent_names:
            agent = storybot.get_agent_by_name(name)
            if agent:
                print(f"Found agent: {agent.emoji} {agent.name}")
            else:
                print(f"Agent not found: {name}")
        
        # Test getting non-existent agent
        agent = storybot.get_agent_by_name("NonExistentAgent")
        if agent is None:
            print("Correctly returned None for non-existent agent")
        else:
            print("Should have returned None for non-existent agent")
            
    except Exception as e:
        print(f"Agent retrieval test failed: {str(e)}")


def test_age_adaptive_storytelling():
    """Test age-adaptive storytelling functionality."""
    print("\nTesting Age-Adaptive Storytelling...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("No API key found. Skipping age-adaptive test.")
        return
    
    try:
        storybot = create_storybot()
        config = get_config()
        
        # Test different age groups
        ages = [6, 12, 18, 30, 45, 60]
        
        for age in ages:
            # Test age configuration
            age_config = config.get_age_config(age)
            age_group = config.get_age_group(age)
            
            print(f"   Age {age}: {age_config['emoji']} {age_config['name']}")
            print(f"      Complexity: {age_config['complexity']}")
            print(f"      Vocabulary: {age_config['vocabulary']}")
            print(f"      Concepts: {age_config['concepts']}")
            
            # Test story creation with age parameter (commented out to avoid API calls)
            # result = storybot.create_story("gravity", age=age)
            # assert result["age"] == age
            # assert result["age_group"] == age_group
            # print(f"      ✅ Story created successfully")
        
        print("   ✅ Age-adaptive configuration test passed!")
        
    except Exception as e:
        print(f"   ❌ Age-adaptive test failed: {str(e)}")


def main():
    """Run all tests."""
    print("Starting StoryBot OOP Tests...\n")
    
    # Run tests
    test_configuration()
    test_exceptions()
    
    if test_storybot_creation():
        test_story_creation()
        test_agent_retrieval()
        test_age_adaptive_storytelling()
    
    print("\nAll tests completed!")


if __name__ == "__main__":
    main() 