# slack-starterbot

A simple, modern Python-powered starter Slack bot built with [Slack Bolt](https://slack.dev/bolt-python/) and **Socket Mode**.

This bot responds to mentions (e.g. `@StarterBot do something`) and direct messages with helpful starter replies, providing a clean foundation for your own custom Slack bot commands.

---

## Features

- **Modern Architecture**: Uses the official `slack_bolt` framework with Socket Mode (no public URL or ngrok required for local development).
- **Python 3 Compatible**: Fully compatible with modern Python (3.8 through 3.13+).
- **Direct Mention & DM Support**: Listens for `@bot-name` mentions in channels and direct messages.
- **Robust Error Handling & Logging**: Comprehensive logging and friendly token validation to prevent silent failures and `No handlers could be found` errors.
- **`.env` Support**: Automatically loads tokens from a `.env` file via `python-dotenv`.

---

## Prerequisites

- Python 3.8+
- A Slack workspace where you have permission to install apps

---

## Slack App Configuration Guide

1. **Create an App**:
   - Go to [Slack API: Your Apps](https://api.slack.com/apps).
   - Click **Create New App** > **From scratch**.
   - Name your bot (e.g., `StarterBot`) and select your workspace.

2. **Enable Socket Mode**:
   - In the left sidebar, navigate to **Socket Mode** and toggle **Enable Socket Mode** on.
   - When prompted to generate an App-Level Token, give it a name (e.g., `socket-mode-token`) and ensure it has the `connections:write` scope.
   - Copy the generated token starting with `xapp-...`. This is your `SLACK_APP_TOKEN`.

3. **Configure Bot Scopes**:
   - In the left sidebar, go to **OAuth & Permissions**.
   - Scroll down to **Scopes** > **Bot Token Scopes** and add:
     - `app_mentions:read` (Allows the bot to receive mentions like `@StarterBot`)
     - `chat:write` (Allows the bot to post messages)
     - `im:history` (Allows the bot to receive direct messages)

4. **Subscribe to Bot Events**:
   - In the left sidebar, go to **Event Subscriptions** and toggle **Enable Events** on.
   - Under **Subscribe to bot events**, add:
     - `app_mention`
     - `message.im`
   - Click **Save Changes** at the bottom.

5. **Install to Workspace**:
   - Under **OAuth & Permissions**, click **Install to Workspace** and authorize the bot.
   - Copy the **Bot User OAuth Token** starting with `xoxb-...`. This is your `SLACK_BOT_TOKEN`.

---

## Installation & Running

### 1. Clone the repository
```bash
git clone https://github.com/mattmakai/slack-starterbot.git
cd slack-starterbot
```

### 2. Set up virtual environment & install dependencies
```bash
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 3. Configure Tokens
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and fill in your tokens:
```env
SLACK_BOT_TOKEN=xoxb-your-bot-user-token
SLACK_APP_TOKEN=xapp-your-app-level-token
```

*(Alternatively, you can export them directly in your shell environment without using `.env`.)*

### 4. Run the Bot
```bash
python starterbot.py
```

You should see output similar to:
```text
2026-10-19 12:00:00 [INFO] starterbot: Connecting to Slack via Socket Mode...
2026-10-19 12:00:01 [INFO] starterbot: ⚡ Starter Bot is connected and running!
```

---

## Usage in Slack

1. Invite the bot to any channel:
   ```text
   /invite @StarterBot
   ```
2. Mention the bot with a command:
   ```text
   @StarterBot do something
   ```
   **Response**: `Sure...write some more code then I can do that!`
3. Send an unrecognized command:
   ```text
   @StarterBot hello
   ```
   **Response**: `Not sure what you mean. Try *do*.`
4. You can also send direct messages to `@StarterBot` with the same commands.

---

## Extending the Bot

To add custom commands, expand `handle_command` in `starterbot.py`:

```python
def handle_command(command, say):
    if command.startswith("do"):
        say("Sure...write some more code then I can do that!")
    elif command.startswith("help"):
        say("Available commands: *do*, *help*, *ping*")
    elif command.startswith("ping"):
        say("Pong! 🏓")
    else:
        say("Not sure what you mean. Try *do*.")
```

---

## Troubleshooting

- **`Configuration Error: SLACK_BOT_TOKEN is missing`**:
  Ensure your `.env` file exists and contains a valid `xoxb-...` token.
- **`Configuration Error: SLACK_APP_TOKEN is missing`**:
  Ensure Socket Mode is enabled in your Slack App settings and your token begins with `xapp-...`.
- **Bot doesn't respond in channels**:
  Verify you invited the bot to the channel (`/invite @StarterBot`) and granted the `app_mentions:read` scope.
