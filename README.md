# 📧 Email Assistant Agent

An AI-powered email processing application built with OpenAI Agents SDK and Gradio. This application automatically classifies, summarizes, and generates professional reply suggestions for business emails using a sophisticated multi-agent architecture.

## 🚀 Features

- **Email Classification**: Automatically categorizes emails into Inquiry, Complaint, Feedback, or Other
- **Smart Summarization**: Creates concise two-sentence summaries of email content
- **Reply Generation**: Suggests professional, contextually appropriate responses
- **Multi-Agent Architecture**: 5 specialized agents with proper handoff mechanism for optimal results
- **User-Friendly Interface**: Clean two-column Gradio interface with examples
- **Content Flagging**: Manual flagging system for inappropriate content
- **External Examples**: Email examples loaded from external text file
- **HTML Formatting**: Proper rendering of email replies with line breaks

## 🛠️ Technical Stack

- **OpenAI Agents SDK**: For AI agent orchestration and tool management
- **Gradio**: For the web interface
- **OpenAI GPT-4o-mini**: For cost-effective AI processing
- **Python 3.8+**: Core runtime

## 📋 Requirements

- Python 3.8 or higher
- OpenAI API key
- Internet connection for API calls

## 🚀 Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd email-assistant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the interface**:
   Open your browser and go to `http://localhost:7860`

### Hugging Face Spaces Deployment

1. **Create a new Space** on Hugging Face
2. **Upload all files** to your Space
3. **Configure the Space**:
   - **SDK**: Gradio
   - **Hardware**: CPU Basic
   - **Visibility**: Public or Private
4. **Deploy**: The Space will automatically build and deploy

## 📖 Usage

1. **Enter your OpenAI API key** in the left column
2. **Paste your email content** in the email text area (or click on examples)
3. **Click Submit** to process the email through the multi-agent system
4. **View the results** in the right column:
   - Detected email category
   - Two-sentence summary
   - Suggested professional reply
5. **Flag inappropriate content** using the red flag button if needed

## 🔧 Configuration

### Environment Variables

The application can be configured using environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (optional if using UI input)

### Model Configuration

The application uses `gpt-4o-mini` by default for cost efficiency. To change the model, modify the `model` parameter in `agent.py`:

```python
agent = Agent(
    # ... other parameters
    model="gpt-4o"  # Change to your preferred model
)
```

## 📁 Project Structure

```
email-assistant/
├── app.py              # Main Gradio application with two-column layout
├── agent.py            # Multi-agent orchestration wrapper
├── tools.py            # 5 specialized agents with handoff mechanism
├── email_examples.txt  # Email examples loaded from external file
├── flagged_content/    # Directory for flagged inappropriate content
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔍 How It Works

1. **Multi-Agent Architecture**: 5 specialized agents with proper handoff mechanism:
   - `EmailClassifierAgent`: Categorizes emails into business categories
   - `EmailSummarizerAgent`: Creates concise two-sentence summaries
   - `ReplyGeneratorAgent`: Generates professional reply suggestions
   - `EmailProcessorAgent`: Handles final formatting and output
   - `EmailOrchestratorAgent`: Coordinates the workflow using tools and handoffs

2. **Agent Orchestration**: The system processes emails using the OpenAI Agents SDK pattern:
   - **Email Orchestrator** receives the email input
   - **Uses Tools**: Calls the 3 specialized agents as tools (classifier, summarizer, reply generator)
   - **Handoff Mechanism**: Delegates final processing to the Email Processor agent
   - **Structured Output**: Returns formatted results with category, summary, and reply

3. **User Interface**: Gradio provides a clean two-column interface:
   - **Left Column**: API key input, email content, examples, and controls
   - **Right Column**: Analysis results with HTML formatting and flag functionality

## 🛡️ Security & Privacy

- **API Key Security**: Your OpenAI API key is only used for the current session and is not stored
- **Data Privacy**: Email content is sent to OpenAI for processing but not stored locally
- **Content Flagging**: Manual flagging system saves inappropriate content to `flagged_content/` directory
- **Error Handling**: Comprehensive error handling for API failures and invalid inputs

## 🐛 Troubleshooting

### Common Issues

1. **"Invalid API Key" Error**:
   - Verify your OpenAI API key is correct
   - Ensure you have sufficient credits in your OpenAI account

2. **"Rate Limit Exceeded" Error**:
   - Wait a few minutes before trying again
   - Consider upgrading your OpenAI plan for higher rate limits

3. **"Network Error"**:
   - Check your internet connection
   - Verify OpenAI services are operational

### Debug Mode

To enable debug logging, set the environment variable:
```bash
export GRADIO_DEBUG=1
```

## 📝 Example Usage

### Input Email:
```
Subject: Issue with my account

Hi Support,

I'm having trouble logging into my account. I keep getting an error message and I'm sure my password is correct. This is urgent as I need to access my account for an important project.

Please help!

Thanks,
John
```

### Output:
- **Category**: Complaint
- **Summary**: Customer is experiencing login issues with their account and needs urgent assistance to access their account for an important project.
- **Suggested Reply**: 
  ```
  Subject: Re: Issue with my account
  
  Dear John,
  
  Thank you for reaching out regarding your account access issues. I understand how frustrating this must be, and I want to help resolve this quickly for you.
  
  Please try clearing your browser cache and cookies, and if the problem persists, I'll escalate this to our technical team immediately.
  
  Best regards,
  Support Team
  ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section above
- Review OpenAI API documentation
- Open an issue in the repository

---

**Built with ❤️ using OpenAI Agents SDK and Gradio**