"""
Email Assistant Agents

This module defines three specialized agents and one handoff agent:
- EmailClassifierAgent: categorizes emails into business categories
- EmailSummarizerAgent: creates concise summaries of email content
- ReplyGeneratorAgent: generates professional reply suggestions
- EmailHandoffAgent: orchestrates the workflow between the three agents
"""

from agents import Agent, Runner
import os
import asyncio
import threading
from typing import Dict, Any


def create_classifier_agent(api_key: str) -> Agent:
    """
    Creates a specialized agent for email classification.
    
    Args:
        api_key (str): OpenAI API key for authentication
        
    Returns:
        Agent: Configured OpenAI Agent for email classification
    """
    os.environ["OPENAI_API_KEY"] = api_key
    
    agent = Agent(
        name="Email Classifier Agent",
        instructions="""
        You are a specialized email classification agent. Your task is to analyze business emails and categorize them into one of four categories:
        
        - Inquiry: Questions, requests for information, or help
        - Complaint: Issues, problems, or dissatisfaction  
        - Feedback: Suggestions, opinions, or general feedback
        - Other: Any email that doesn't fit the above categories
        
        Analyze the email content carefully and return only the category name.
        """,
        model="gpt-4o-mini"
    )
    
    return agent


def create_summarizer_agent(api_key: str) -> Agent:
    """
    Creates a specialized agent for email summarization.
    
    Args:
        api_key (str): OpenAI API key for authentication
        
    Returns:
        Agent: Configured OpenAI Agent for email summarization
    """
    os.environ["OPENAI_API_KEY"] = api_key
    
    agent = Agent(
        name="Email Summarizer Agent",
        instructions="""
        You are a specialized email summarization agent. Your task is to create a concise two-sentence summary of business emails.
        
        Your summary should:
        - Capture the main points and context of the email
        - Be professional and clear
        - Be exactly two sentences long
        - Focus on the key information and intent
        
        Return only the summary, no additional commentary.
        """,
        model="gpt-4o-mini"
    )
    
    return agent


def create_reply_generator_agent(api_key: str) -> Agent:
    """
    Creates a specialized agent for reply generation.
    
    Args:
        api_key (str): OpenAI API key for authentication
        
    Returns:
        Agent: Configured OpenAI Agent for reply generation
    """
    os.environ["OPENAI_API_KEY"] = api_key
    
    agent = Agent(
        name="Reply Generator Agent",
        instructions="""
        You are a specialized reply generation agent. Your task is to create professional, contextually appropriate responses to business emails.
        
        Your reply should:
        - Acknowledge the customer's message appropriately
        - Address the specific category and content
        - Maintain a helpful and professional tone
        - Provide next steps or solutions when applicable
        - Be polite and customer-focused
        
        Return only the reply suggestion, no additional commentary.
        """,
        model="gpt-4o-mini"
    )
    
    return agent


def create_handoff_agent(api_key: str) -> Agent:
    """
    Creates the handoff agent that orchestrates the workflow.
    
    Args:
        api_key (str): OpenAI API key for authentication
        
    Returns:
        Agent: Configured OpenAI Agent for workflow orchestration
    """
    os.environ["OPENAI_API_KEY"] = api_key
    
    agent = Agent(
        name="Email Handoff Agent",
        instructions="""
        You are the handoff agent responsible for orchestrating email processing workflow.
        
        Your task is to:
        1. First, hand off the email to the Email Classifier Agent to get the category
        2. Then, hand off the email to the Email Summarizer Agent to get the summary
        3. Finally, hand off both the category and summary to the Reply Generator Agent to get the reply
        
        Always use the handoff mechanism to delegate tasks to the specialized agents.
        Return the final results in a structured format.
        """,
        model="gpt-4o-mini"
    )
    
    return agent


def run_agent_in_thread(agent: Agent, input_text: str) -> str:
    """
    Runs an agent in a separate thread with its own event loop.
    
    Args:
        agent (Agent): The agent to run
        input_text (str): The input text for the agent
        
    Returns:
        str: The agent's response
    """
    def run_agent():
        try:
            print(f"Running {agent.name}...")
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = Runner.run_sync(agent, input_text, max_turns=5)
                print(f"{agent.name} completed successfully")
                return result.final_output
            finally:
                loop.close()
        except Exception as e:
            print(f"{agent.name} failed: {e}")
            raise e
    
    # Run the agent in a separate thread to avoid event loop conflicts
    result_container = [None]
    exception_container = [None]
    
    def thread_target():
        try:
            result_container[0] = run_agent()
        except Exception as e:
            exception_container[0] = e
    
    thread = threading.Thread(target=thread_target)
    thread.start()
    thread.join()
    
    if exception_container[0]:
        raise exception_container[0]
    
    return result_container[0]


def process_email_with_agents(email_text: str, api_key: str) -> Dict[str, Any]:
    """
    Processes an email using the multi-agent architecture.
    
    Args:
        email_text (str): The email content to process
        api_key (str): OpenAI API key for authentication
        
    Returns:
        Dict[str, Any]: Dictionary containing category, summary, and reply
    """
    try:
        print("Starting multi-agent email processing...")
        
        # Create all agents
        classifier_agent = create_classifier_agent(api_key)
        summarizer_agent = create_summarizer_agent(api_key)
        reply_agent = create_reply_generator_agent(api_key)
        
        # Step 1: Classify the email
        print("Step 1: Classifying email...")
        category = run_agent_in_thread(classifier_agent, email_text)
        category = category.strip()
        
        # Step 2: Summarize the email
        print("Step 2: Summarizing email...")
        summary = run_agent_in_thread(summarizer_agent, email_text)
        summary = summary.strip()
        
        # Step 3: Generate reply
        print("Step 3: Generating reply...")
        reply_input = f"Category: {category}\nSummary: {summary}\nOriginal Email: {email_text}"
        reply = run_agent_in_thread(reply_agent, reply_input)
        reply = reply.strip()
        
        return {
            'success': True,
            'category': category,
            'summary': summary,
            'reply': reply,
            'error': None
        }
        
    except Exception as e:
        error_message = str(e)
        
        # Provide user-friendly error messages
        if "api_key" in error_message.lower() or "authentication" in error_message.lower():
            error_message = "Invalid OpenAI API key. Please check your API key and try again."
        elif "rate" in error_message.lower() or "limit" in error_message.lower():
            error_message = "Rate limit exceeded. Please wait a moment and try again."
        elif "network" in error_message.lower() or "connection" in error_message.lower():
            error_message = "Network error. Please check your internet connection and try again."
        else:
            error_message = f"An error occurred while processing the email: {error_message}"
        
        return {
            'success': False,
            'error': error_message,
            'category': None,
            'summary': None,
            'reply': None
        }
