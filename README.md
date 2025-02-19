# LLM Mailbox

A sample vulnerable web application showcasing a GenAI (LLM-based) email summarization feature for pentesters to learn how to test for prompt injection attacks. Unlike common chatbot examples, this demonstrates that GenAI vulnerabilities can exist in non-conversational use cases too.

## Background

For a deeper dive on how prompt injection can be exploited and tested—particularly using [spikee](https://labs.withsecure.com/tools/spikee)—refer to the [WithSecure™ Labs article](https://labs.withsecure.com/tools/spikee). Here’s the short summary (from the article’s TL;DR):

> - A step-by-step guide on using spikee, an open-source tool for prompt injection testing.
> - A case study of an LLM-based WebMail summarization feature (like this one) with custom datasets targeting specific attack scenarios.
> - Practical tips on dataset preparation, automated testing with Burp Suite Intruder, spikee’s custom target feature, and result interpretation.

**Note:** This project is intended purely for educational and testing purposes and should never be used in production.

## Requirements

- Python 3.x
- An OpenAI API key (added to a `.env` file with `OPENAI_API_KEY=`)

**GPT-4** is used as the underlying LLM.

## Installation & Usage

1. **Clone the repo**:
   ```bash
   git clone https://github.com/youruser/llm-mailbox.git
   cd llm-mailbox
   ```

2. **Create and configure `.env` file**:
   ```bash
   echo "OPENAI_API_KEY=YOUR_API_KEY_HERE" > .env
   ```

3. **Use the Makefile**:
   ```bash
   # Install dependencies and set up virtual environment
   make setup
   
   # Run the Flask application
   make run
   ```
   The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Testing Prompt Injection

- This application is deliberately vulnerable. Use [spikee](https://labs.withsecure.com/tools/spikee) or similar tools to launch prompt injection attacks against the email summarization feature.
- Refer to the [WithSecure™ Labs article](https://labs.withsecure.com/tools/spikee) for guidance on how to build datasets, automate attacks (e.g., via Burp Suite Intruder), and interpret the results.

## Disclaimer

This project is a learning resource (similar to Damn Vulnerable Web Applications) and **not** a production-ready product. It was developed to demonstrate prompt injection testing techniques. Use responsibly and at your own risk.
