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


def create_email_processor_agent(api_key: str) -> Agent:
    """
    Creates the email processor agent that handles the final processing.
    This is the handoff agent that receives the processed email.
    
    Args:
        api_key (str): OpenAI API key for authentication
        
    Returns:
        Agent: Configured OpenAI Agent for final email processing
    """
    os.environ["OPENAI_API_KEY"] = api_key
    
    agent = Agent(
        name="Email Processor",
        instructions="""
        You are an Email Processor. You receive processed email data and format it for final output.
        
        You receive:
        - Category: The email category (Inquiry, Complaint, Feedback, Other)
        - Summary: Two-sentence summary of the email
        - Reply: Professional reply suggestion
        
        Format the final response in this exact structure:
        Category: [category]
        Summary: [summary]
        Reply: [reply]
        """,
        model="gpt-4o-mini",
        handoff_description="Process and format email analysis results"
    )
    
    return agent


def create_email_orchestrator_agent(api_key: str) -> Agent:
    """
    Creates the email orchestrator agent that coordinates the workflow.
    This agent uses the 3 specialized agents as tools and hands off to the processor.
    
    Args:
        api_key (str): OpenAI API key for authentication
        
    Returns:
        Agent: Configured OpenAI Agent for workflow orchestration
    """
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Create the specialized agents
    classifier_agent = create_classifier_agent(api_key)
    summarizer_agent = create_summarizer_agent(api_key)
    reply_agent = create_reply_generator_agent(api_key)
    
    # Create the email processor agent for handoff
    email_processor = create_email_processor_agent(api_key)
    
    # Convert agents to tools using .as_tool() method
    tool1 = classifier_agent.as_tool(
        tool_name="email_classifier_agent", 
        tool_description="Classifies business emails into categories (Inquiry, Complaint, Feedback, Other)"
    )
    tool2 = summarizer_agent.as_tool(
        tool_name="email_summarizer_agent", 
        tool_description="Creates concise two-sentence summaries of email content"
    )
    tool3 = reply_agent.as_tool(
        tool_name="reply_generator_agent", 
        tool_description="Generates professional reply suggestions based on email category and summary"
    )
    
    # Define tools and handoffs
    tools = [tool1, tool2, tool3]
    handoffs = [email_processor]
    
    # Create the orchestrator agent
    agent = Agent(
        name="Email Orchestrator",
        instructions="""
        You are an Email Orchestrator at Email Assistant. Your goal is to process business emails using the specialized agent tools.
        
        Follow these steps carefully:
        1. Classify Email: Use the email_classifier_agent tool to categorize the email (Inquiry, Complaint, Feedback, Other)
        2. Summarize Email: Use the email_summarizer_agent tool to create a two-sentence summary
        3. Generate Reply: Use the reply_generator_agent tool to create a professional reply suggestion
        4. Handoff for Processing: Pass the results to the 'Email Processor' agent for final formatting
        
        Crucial Rules:
        - You must use the agent tools to process the email — do not process them yourself
        - You must hand off the results to the Email Processor for final formatting
        - Ensure all three steps (classify, summarize, generate reply) are completed
        """,
        tools=tools,
        handoffs=handoffs,
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


def process_email_with_handoff_agent(email_text: str, api_key: str) -> Dict[str, Any]:
    """
    Processes an email using the orchestrator agent that coordinates the workflow.
    The orchestrator agent uses the 3 specialized agents as tools and hands off to the processor.
    
    Args:
        email_text (str): The email content to process
        api_key (str): OpenAI API key for authentication
        
    Returns:
        Dict[str, Any]: Dictionary containing category, summary, and reply
    """
    try:
        print("Starting orchestrator agent email processing...")
        
        # Create the orchestrator agent that coordinates the workflow
        orchestrator_agent = create_email_orchestrator_agent(api_key)
        
        # The orchestrator agent will coordinate the workflow using tools and handoffs
        result = run_agent_in_thread(orchestrator_agent, email_text)
        
        print("=" * 80)
        print("DEBUG: RAW OUTPUT FROM ORCHESTRATOR AGENT")
        print("=" * 80)
        print(f"Raw output length: {len(result)} characters")
        print(f"Raw output content:\n{result}")
        print("=" * 80)
        
        # Parse the orchestrator agent's structured response
        lines = result.strip().split('\n')
        
        print("DEBUG: PARSING STRUCTURED RESPONSE")
        print("=" * 80)
        print(f"Number of lines to parse: {len(lines)}")
        for i, line in enumerate(lines):
            print(f"Line {i+1}: '{line}'")
        print("=" * 80)
        
        category = "Other"
        summary = "Unable to generate summary"
        reply = "Unable to generate reply"
        
        # Parse the orchestrator agent's structured response
        current_field = None
        reply_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                if current_field == "reply":
                    reply_lines.append("")  # Preserve empty lines in reply
                continue
                
            # Look for structured output from orchestrator agent
            if line.startswith("Category:"):
                category = line.replace("Category:", "").strip()
                print(f"DEBUG: Found Category: '{category}'")
                current_field = "category"
            elif line.startswith("Summary:"):
                summary = line.replace("Summary:", "").strip()
                print(f"DEBUG: Found Summary: '{summary}'")
                current_field = "summary"
            elif line.startswith("Reply:"):
                # Start collecting reply content
                reply_content = line.replace("Reply:", "").strip()
                reply_lines = [reply_content] if reply_content else []
                current_field = "reply"
                print(f"DEBUG: Started collecting Reply: '{reply_content}'")
            elif current_field == "reply":
                # Continue collecting reply content
                reply_lines.append(line)
                print(f"DEBUG: Added to Reply: '{line}'")
        
        # Join all reply lines
        if reply_lines:
            reply = '\n'.join(reply_lines)
            print(f"DEBUG: Final Reply assembled: '{reply}'")
        else:
            reply = "Unable to generate reply"
        
        print("DEBUG: PARSING RESULTS")
        print("=" * 80)
        print(f"Category: '{category}' (length: {len(category)})")
        print(f"Summary: '{summary}' (length: {len(summary)})")
        print(f"Reply: '{reply}' (length: {len(reply)})")
        print("=" * 80)
        
        # Format the reply text to render \n characters as actual line breaks
        if reply and reply != "Unable to generate reply":
            print("DEBUG: FORMATTING REPLY TEXT")
            print("=" * 80)
            print(f"Original reply: '{reply}'")
            
            # Replace literal \n with actual line breaks
            reply = reply.replace('\\n', '\n')
            print(f"After \\n replacement: '{reply}'")
            
            # Clean up any double line breaks and format properly
            reply = '\n'.join(line.rstrip() for line in reply.split('\n'))
            print(f"After formatting: '{reply}'")
            print("=" * 80)
        
        print(f"Final parsed results - Category: {category}, Summary: {summary}, Reply: {reply}")
        
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
