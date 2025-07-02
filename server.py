
from mcp.server.fastmcp import FastMCP
import asyncio
from dotenv import load_dotenv
import os
import logging
import google.generativeai as genai # pyright: ignore[reportAttributeAccessIssue]

import requests
import msal

load_dotenv()
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# MCP app setup
mcp = FastMCP("Python360")

# Google Gemini setup
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini = genai.GenerativeModel(os.getenv("GEMINI_MODEL"))


########################
# Helper functions
########################

AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}"
SCOPES = ["https://graph.microsoft.com/.default"]
EMAIL_ENDPOINT = "https://graph.microsoft.com/v1.0/me/messages"

def get_access_token():
    app = msal.ConfidentialClientApplication(
        os.getenv("CLIENT_ID"),
        authority=AUTHORITY,
        client_credential=os.getenv("CLIENT_SECRET"),
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" in result:
        return result["access_token"]
    raise Exception(f"Failed to obtain token: {result.get('error_description')}")

async def fetch_emails(limit=10):
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {"$top": limit, "$select": "subject,bodyPreview,receivedDateTime,from"}

    response = requests.get(EMAIL_ENDPOINT, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Graph API error: {response.status_code} - {response.text}")
    return response.json().get("value", [])



########################
# Summarize emails
########################
async def summarize_emails_gemini(emails):
    if not emails:
        return "No emails to summarize."
    
    email_texts = "\n\n".join(
        f"From: {email['from']['emailAddress']['name']}\nSubject: {email['subject']}\nBody: {email['bodyPreview']}"
        for email in emails
    )
    prompt = (
        "You are an assistant that summarizes emails. Given the following list of emails, "
        "summarize the key topics, senders, and dates.\n\n" + email_texts
    )
    summary = gemini.generate_content(prompt)
    return summary.text


########################
# MCP tools
########################

@mcp.tool()
async def summarize_outlook_emails(limit: int = 5) -> str:
    """
    Fetches the latest Outlook emails and summarizes them using Gemini.
    
    Args:
        limit (int): Number of emails to fetch.

    Returns:
        str: Summary of emails.
    """
    try:
        emails = await fetch_emails(limit)
        summary = await summarize_emails_gemini(emails)
        return summary
    except Exception as e:
        logging.error(f"Error summarizing emails: {e}", exc_info=True)
        return f"Failed to summarize emails: {str(e)}"


# Run server
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.sleep(0.1))  # Init async context
    mcp.run()
