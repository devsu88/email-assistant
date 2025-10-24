"""
Email Assistant Agent

This module orchestrates the multi-agent architecture for email processing,
following the pattern from the OpenAI Agents SDK notebook.
"""

from typing import Dict, Any
from tools import process_email_with_handoff_agent


def process_email(email_text: str, api_key: str) -> Dict[str, Any]:
    """
    Processes an email using the multi-agent architecture.
    
    Args:
        email_text (str): The email content to process
        api_key (str): OpenAI API key for authentication
        
    Returns:
        Dict[str, Any]: Dictionary containing:
            - 'success': Boolean indicating if processing was successful
            - 'category': Detected email category
            - 'summary': Two-sentence email summary
            - 'reply': Suggested professional reply
            - 'error': Error message if processing failed
    """
    # Validate inputs
    if not email_text.strip():
        return {
            'success': False,
            'error': 'Email content cannot be empty. Please provide the email text to process.'
        }
    
    if not api_key.strip():
        return {
            'success': False,
            'error': 'OpenAI API key is required. Please enter your API key.'
        }
    
    # Use the handoff agent architecture
    return process_email_with_handoff_agent(email_text, api_key)
