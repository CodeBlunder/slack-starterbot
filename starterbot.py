import os
import re
import sys
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configure logging to provide clear diagnostics and avoid missing-handler warnings
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("starterbot")

# Constants
EXAMPLE_COMMAND = "do"

# Retrieve tokens
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")


def validate_tokens():
    """Validates that necessary Slack tokens are present and correctly formatted."""
    missing = []
    if not SLACK_BOT_TOKEN:
        missing.append("- SLACK_BOT_TOKEN is missing. Requires a Bot User OAuth Token (starts with 'xoxb-').")
    elif not SLACK_BOT_TOKEN.startswith("xoxb-"):
        logger.warning("SLACK_BOT_TOKEN usually starts with 'xoxb-'. Ensure you are using a Bot Token, not a User Token.")

    if not SLACK_APP_TOKEN:
        missing.append("- SLACK_APP_TOKEN is missing. Requires an App-Level Token for Socket Mode (starts with 'xapp-').")
    elif not SLACK_APP_TOKEN.startswith("xapp-"):
        logger.warning("SLACK_APP_TOKEN usually starts with 'xapp-'. Ensure you are using an App-Level Token.")

    if missing:
        logger.error("Configuration Error:\n" + "\n".join(missing))
        logger.error("Set these variables in your environment or a local .env file. See README.md for setup instructions.")
        sys.exit(1)


validate_tokens()

# Initialize Slack Bolt App
app = App(token=SLACK_BOT_TOKEN)


def handle_command(command, say):
    """Executes bot command if the command is known."""
    default_response = f"Not sure what you mean. Try *{EXAMPLE_COMMAND}*."
    response = None

    # This is where you can implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    say(response or default_response)


@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    """
    Handles when the bot is mentioned in a channel.
    Strips the leading mention tag and processes the remaining text as a command.
    """
    text = body.get("event", {}).get("text", "")
    # Remove leading <@USERID> mention
    command = re.sub(r"^<@.+?>\s*", "", text).strip()
    logger.info(f"Received mention command: {command}")
    handle_command(command, say)


@app.event("message")
def handle_message_events(body, say, logger):
    """
    Handles direct messages sent to the bot (channel_type == 'im').
    Ignores message subtypes like edits or system messages.
    """
    event = body.get("event", {})
    if event.get("channel_type") == "im" and "subtype" not in event:
        command = event.get("text", "").strip()
        logger.info(f"Received direct message command: {command}")
        handle_command(command, say)


if __name__ == "__main__":
    logger.info("Connecting to Slack via Socket Mode...")
    try:
        handler = SocketModeHandler(app, SLACK_APP_TOKEN)
        logger.info("⚡ Starter Bot is connected and running!")
        handler.start()
    except Exception as e:
        logger.exception("Failed to connect or run Starter Bot: %s", e)
        sys.exit(1)
