import time
import os
from flask import Flask, jsonify, request, render_template
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o",
    max_tokens=None,
    temperature=0
)

def llm_summary(emails):
    messages = []
    summary_prompt = f"Summarize the following users' mailbox focussing only on the most essential information:\n{emails}"
    messages.append(("user", summary_prompt))
    
    try:
        summary = llm.invoke(messages)
        return summary.content
    except Exception as e:
        print(f"Error during LLM completion: {e}")
        raise


app = Flask(__name__)

MOCK_EMAILS = [
    {
        "id": 1,
        "sender": "alice@example.com",
        "subject": "Project Kickoff Reminder",
        "body": (
            "Hi Team,\n\n"
            "This is a reminder about the project kickoff meeting scheduled for tomorrow at 10 AM in the main conference room.\n\n"
            "The agenda includes:\n"
            "- Discussing project goals and objectives.\n"
            "- Reviewing key milestones and timelines.\n"
            "- Assigning initial tasks and responsibilities to team members.\n\n"
            "Please make sure to review the project brief sent in my earlier email, particularly the sections on expected deliverables and budget constraints. "
            "I’d also appreciate it if you could come prepared with questions or suggestions for streamlining the initial phases of the project.\n\n"
            "Looking forward to seeing everyone there. Please be on time as we have a lot to cover.\n\n"
            "Best regards,\nAlice"
        ),
        "date": "2025-01-14",
    },
    {
        "id": 2,
        "sender": "bob@example.org",
        "subject": "Vacation Notice and Delegation of Tasks",
        "body": (
            "Hi Team,\n\n"
            "As mentioned earlier, I’ll be on vacation starting Monday, January 16th, and returning on Monday, January 23rd. "
            "During this time, I’ll have limited access to emails and may not be able to respond promptly.\n\n"
            "To ensure smooth operations while I’m away, please note the following:\n\n"
            "- Sarah will be the point of contact for all ongoing projects. She has been fully briefed and is equipped to handle immediate concerns.\n"
            "- For the marketing campaign, please finalize the creative assets and ensure they are ready for review by next Thursday. "
            "Reach out to Jane for additional support on design-related tasks.\n"
            "- The monthly sales report draft should be prepared by January 20th. I’ve shared the required data sources with Peter; please assist him if needed.\n\n"
            "If there are any urgent matters requiring my input before I leave, kindly flag them by tomorrow evening so I can address them. "
            "Otherwise, I trust that the team will handle everything effectively in my absence.\n\n"
            "Thank you for your cooperation, and I look forward to catching up after my return.\n\n"
            "Best,\nBob"
        ),
        "date": "2025-01-12",
    },
    {
        "id": 3,
        "sender": "support@mockservice.com",
        "subject": "Password Reset Request",
        "body": (
            "Hi,\n\n"
            "We received a request to reset the password for your MockService account.\n\n"
            "If you didn’t request this, you can safely ignore this email. Otherwise, you can reset your password using the link below:\n\n"
            "Reset Password: https://mockservice.com/reset-password?token=abc123xyz789\n\n"
            "This link will expire in 24 hours. If the link has expired, you can request a new one by visiting the password reset page.\n\n"
            "Thank you,\nThe MockService Team"
        ),
        "date": "2025-01-10",
    },
]

@app.route("/")
def index():
    """Serve the single-page app."""
    return render_template("index.html")


@app.route("/api/emails")
def list_emails():
    """Return the list of mock emails."""
    return jsonify(MOCK_EMAILS)


@app.route("/api/emails/<int:email_id>")
def get_email(email_id):
    """Return details for a single email, looked up by ID."""
    for email in MOCK_EMAILS:
        if email["id"] == email_id:
            return jsonify(email)
    return jsonify({"error": "Email not found"}), 404

@app.route("/api/summarize", methods=["POST"])
def summarize():
    """
    Accepts an array of raw documents (strings) and returns a single summary.
    """
    data = request.get_json()
    documents = data.get("documents", [])
    
    if not documents:
        return jsonify({"error": "No documents provided"}), 400

    # Combine all documents into one text block for summarization
    combined_text = "\n\n".join(documents)
    return jsonify({"summary": llm_summary(combined_text)
})


if __name__ == "__main__":
    app.run(debug=True)
