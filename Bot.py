import os
import json
import time
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

HISTORY_FILE = "chat_histories.json"
BOT_PERSONALITY = "personality.cfg"
Token = "token.cfg"
Model = "YourModel" # Replace with your LLM model

# Try loading existing histories
# chat_id --> list of {role: "user"/"assistant", content: "…"} 
print("\033[93m[INFO]\033[0m Loading chat history...")
time.sleep(2)
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        chat_histories = json.load(f)
        chat_histories = {int(k): v for k, v in chat_histories.items()}
        print("\033[93m[INFO]\033[0m Successfully loaded chat history!")
        time.sleep(1)
else:
    print("\033[91m[WARNING]\033[0m No chat history file was found, or the naming convention is wrong! It should be", HISTORY_FILE)
    input("Press the enter key to continue & create a new file (first time use), or press \033[93mctrl+C\033[0m to quit...")
    print("\033[93m[INFO]\033[0m Falling back to default & creating new file...")
    chat_histories = {}

# Prompt for how the AI should act when someone talks to it
print("\033[93m[INFO]\033[0m Loading bot personality...")
time.sleep(2)
if os.path.exists(BOT_PERSONALITY):
    with open(BOT_PERSONALITY, "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read().strip()
        print("\033[93m[INFO]\033[0m Successfully loaded Bot personality!")
        time.sleep(1)
else:
    print("\033[91m[WARNING]\033[0m Bot personality config not found! It should be", BOT_PERSONALITY)
    input("Press the enter key to continue with default, or press \033[93mctrl+C\033[0m to quit...")

print("\033[93m[INFO]\033[0m Successfully finished bot loading!")
time.sleep(2)
print("\033[93m[INFO]\033[0m Use \033[93mctrl+C\033[0m to stop the bot at any time.")
print("\033[93m[INFO]\033[0m Displaying live chat feed...")

async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    chat_id = update.effective_chat.id
    text = msg.text or ""
    bot = await ctx.bot.get_me()
    bot_username = bot.username
    bot_id = bot.id

    # If an image is sent, the LLM will get [IMAGE] instead of having to process the actual picture cause im a lazy bum
    if msg.photo or (msg.document and msg.document.mime_type.startswith("image/")):
        text = "[image]"
    else:
        text = msg.text or ""

    # Decide if we should respond
    is_private = update.effective_chat.type == "private"
    is_mention = f"@{bot_username}" in text

    # Is this a reply to one of our messages?
    is_reply = (
        msg.reply_to_message is not None
        and msg.reply_to_message.from_user is not None
        and msg.reply_to_message.from_user.id == bot_id
    )

    # If its just nothing then we ignore it
    if not (is_private or is_mention or is_reply):
        print("[INFO] Other group chatter—ignored")
        return
    
    # Get sender info
    user = update.effective_user
    sender_name = f"{user.first_name} {user.last_name or ''}".strip()
    sender_username = user.username or "NoUsername"
    chat_title = update.effective_chat.title if update.effective_chat.title else "(Private Chat)"

    print(f"[USER MESSAGE] Chat: {chat_title} (ID: {chat_id}) | "
        f"From: {sender_name} (@{sender_username}) | Text: {text}")

    # Clean up text (remove the mention in a group)
    if is_mention:
        text = text.replace(f"@{bot_username}", "").strip()
        if not text:
            text = "Hey!" # If someone wants to address the bot just by calling its name (@-ing it) then we can handle that

    # Initialize history
    history = chat_histories.setdefault(chat_id, [])
    history = history[-50:] # trim history to last n turns to save context

    # Append user's message
    history.append({"role": "user", "content": text})

    # Build the full prompt to send to Ollama!!  
    # Ollama CLI expects something like: ollama chat llama3.1:8b --prompt "<full prompt here>"
    prompt_parts = [f"SYSTEM: {SYSTEM_PROMPT}\n"]
    for turn in history:
        prefix = "USER:" if turn["role"] == "user" else "ASSISTANT:"
        prompt_parts.append(f"{prefix} {turn['content']}\n")
    prompt_parts.append("ASSISTANT:")
    full_prompt = "".join(prompt_parts)

    # Show status as "Typing..."
    await ctx.bot.send_chat_action(chat_id=chat_id, action="typing")

    # Call Ollama CLI
    result = subprocess.run(
        ["ollama", "run", Model, full_prompt],
        capture_output=True, text=True, encoding="utf-8"
    )

    # Combine stdout and stderr for error checking
    combined_output = (result.stdout + result.stderr).lower()

    # Check for memory error keywords
    if "requires more system memory" in combined_output:
        reply = "Code 503 Service unavailable. Likely cause: System memory overload."
    else:
        reply = result.stdout.strip()
        if not reply:
            reply = result.stderr.strip()

        if not reply:
            reply = "Code 500 Internal Server Error"

    print("[BOT]", reply)


    # Append bot’s reply to history
    history.append({"role": "assistant", "content": reply})

    # Persist to disk
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        # Convert keys back to strings so JSON is valid
        json.dump({str(k): v for k, v in chat_histories.items()}, f, ensure_ascii=False, indent=2)

    # Send back to Telegram
    await msg.reply_text(reply)


def main():
    with open(Token) as f:
        token = f.read().strip()
    app = ApplicationBuilder().token(token).build()

    text_filter = (filters.TEXT | filters.PHOTO | filters.Document.IMAGE) & ~filters.COMMAND

    app.add_handler(MessageHandler(text_filter, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()