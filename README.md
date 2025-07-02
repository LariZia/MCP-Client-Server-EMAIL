# MCP Client-Server: Outlook Email Summarizer with Gemini

This project demonstrates an MCP-based client-server application that fetches recent **Outlook emails** via the **Microsoft Graph API** and summarizes them using **Google Gemini**. The system uses the Model Context Protocol (MCP) for structured, real-time interaction between client and server.

---

## Overview

Features:

* **Fetches Outlook emails** using Microsoft Graph API with OAuth2 (via MSAL).
* **Summarizes emails** using Google Gemini for clear, concise insights.
* Powered by **FastMCP** for a real-time tool-based interface.
* Modular and easy to extend with additional tools.

---

## Project Structure

```
.
├── pyproject.toml          # Project configuration
├── README.md               # Project documentation
├── requirements.txt        # Project dependencies 
├── client.py               # MCP client implementation
├── server.py               # MCP server with summarization tool
└── uv.lock                 # Dependency lock file
```

---

## Server Implementation

The server exposes the following tool:

### `summarize_outlook_emails`

Fetches the latest emails from an authenticated Outlook mailbox and returns a summarized view using Gemini.

**Arguments:**

* `limit` (int): Number of emails to fetch (default: 5)

**Returns:**

* A textual summary of senders, subjects, and content highlights.

---

## Client Implementation

The client connects to the server, lists the tools, and allows the user to call `summarize_outlook_emails` with a simple command-line prompt.

---

## Prerequisites

* Python 3.9+
* [uv](https://github.com/astral-sh/uv)
* API credentials in a `.env` file:

### Required Environment Variables

```
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=gemini-pro

CLIENT_ID=your_azure_app_client_id
CLIENT_SECRET=your_azure_app_client_secret
TENANT_ID=your_azure_tenant_id
```

---

## Installation

```bash
# Install all dependencies
uv add -r requirements.txt .
```

---

## Running the Example

```bash
# Run the client (which starts the server)
uv run client.py
```

---

## Example Interaction

```
Available tools: ['summarize_outlook_emails']

You: summarize_outlook_emails limit=3

Assistant:
Here’s a summary of your latest 3 emails:
- From: Alice Smith – Subject: Q3 Report Reminder – Discusses upcoming Q3 deadlines.
- From: IT Support – Subject: Scheduled Maintenance – Notifies planned server downtime.
- From: John Doe – Subject: Lunch Meeting – Proposes rescheduling this week’s lunch.

You: Exit
Exiting...
```

---

## Debugging & Inspection

You can inspect tool calls and server behavior using the MCP Inspector.

1. Start the server directly:

```bash
mcp dev server.py
```

2. Open the inspector in your browser:
   [http://localhost:5173](http://localhost:5173)

---

## Resources

* [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
* [Microsoft Graph API](https://learn.microsoft.com/en-us/graph/)
* [Google Generative AI](https://ai.google.dev/)

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
