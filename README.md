# Telegram Chatbot Framework
This repository provides a flexible foundation for building your own chatbot.  
Use it as-is or customize it to fit your platform and use case.

## Notes
- If you choose to run LLMs CPU-based, **expect slow response times** and especially slow startup times.
- **Remember that system prompts take TIME and EFFORT to engineer.** You cannot simply tell it to "act like a pirate" without further tweaking.
- You will have to tell the bot *how to handle* the **[image]** token it will be presented instead of the image.
- Remember to take note of how much ram your LLM will use! You do NOT want to run out of ram after you've done everything.

## Features:
### Telegram Integration
- Works directly with Telegram using the official `python-telegram-bot` library.
- Handles **text** and **photos** gracefully.

  >When sent a photo, the bot will understand that a photo has been sent. 
  >**Note!** You will have to tell the bot *how to handle* the **[image]** token it will be presented instead of the image.

 - Shows "Typing..." when processing a reply.
### Message filtering
- Ignores random group chatter **unless**:
    
    -   It’s a **private chat.**
        
    -   Someone directly **mentions** the bot with `@username`.
        
    -   Someone **replies** to a message the bot sent.
### Conversation History
-   **Saves chat history** per user/chat ID.
    
-   **Keeps** the last n turns for **context** so it doesn’t forget the thread.

### Local LLM Backend

-   Uses `subprocess` to run an **Ollama** command.
    
-   Feeds the whole conversation context to your local model via CLI.
### And more!
**Inline Debug Logging** - Prints info to the console.

**Custom Personality** - You can tweak how the bot responds.

**Portable Config** - Clean separation of bot token, personality, and history.

**Displays live chat feed** - Shows the full info of who is talking to the bot and where they are speaking from.

## Setup
[Windows System (Windows 10/11)](#windows-system-windows-1011) -or- [Linux System (Only tested on Ubundu-based distro)](#linux-system-only-tested-on-ubundu-based-distro)

-------
### Windows System (Windows 10/11):
1. Install [Ollama](https://ollama.com/download/windows) on to your system.
2. Install the LLM model you want to use with Ollama.
    -   **Example:** `ollama run llama3.1:8b`
    -   Make sure you quit back out of the model after install with `/bye`!
3. Install the singular dependency:
     -   `pip install python-telegram-bot`
4. Make your telegram bot with [@BotFather](http://t.me/botfather) if you haven't already.
5. Get your bot's token
    -   **Example:** `123456789:ABCDefGhIJKlmNoPQRsTUvwxyZ1234567890`
6. Configure the following >marked< files:

|File                |What does it do?                             |
|--------------------|---------------------------------------------|
|`Bot.py`            |**Don't** touch yet, this is the bot's file. |
|>`personality.cfg`< |This is how the bot will act.                |
|>`token.cfg`<       |Put the bot's token here!                    |

**Example** of how to format `personality.cfg`:
> You are [NAME], a [AGE] year old [DESCRIPTION] who interacts like
> [PERSONALITY TRAIT OR STYLE]. Keep your replies [LENGTH RULE]. Use
> [TONE DETAILS]. [EMOJI RULES]. Be [MOOD/STYLE] but [CONTRASTING RULE].
> Avoid [WHAT NOT TO DO].

7. Open up Bot.py and edit the line `Model =  "YourModel"` to reflect the model you are using with Ollama.
   > You can see all of your installed models by executing `ollama list` in the command prompt.
   > **Example:** `Model =  "llama3.1:8b"`
8. Open a command prompt within the folder where the previously mentioned files are. Then, launch the bot with `python .\Bot.py`!

### Linux System (Only tested on Ubundu-based distro):

1. Install [Ollama](https://ollama.com/download/linux) on to your system.
2. Install the LLM model you want to use with Ollama.
    -   **Example:** `ollama run llama3.1:8b`
    -   Make sure you quit back out of the model after install with `/bye`!
3. Script Install:
	1. Create a folder for the bot.
	2. Create a virtual environment with `python -m venv venv`
	   >You might need to use python3 instead of python. In that case, replace python with python3 for all further commands.
	3. Navigate into `cd venv/bin`
	4. Start the virtual environment with `source activate`
	5. Extract all contents of the repo into the previous `venv/` folder where every file within the repo is laid out and NOT still in a folder (You can get rid of the `readme.md` file if you wish).
	6. While in the same directory and with the virtual environment activated, install the single needed dependency with `pip install python-telegram-bot`.
4. Make your telegram bot with [@BotFather](http://t.me/botfather) if you haven't already.
5. Get your bot's token
    -   **Example:** `123456789:ABCDefGhIJKlmNoPQRsTUvwxyZ1234567890`
6. Configure the following >marked< files:

|File                |What does it do?                             |
|--------------------|---------------------------------------------|
|`Bot.py`            |**Don't** touch yet, this is the bot's file. |
|>`personality.cfg`< |This is how the bot will act.                |
|>`token.cfg`<       |Put the bot's token here!                    |

**Example** of how to format `personality.cfg`:
> You are [NAME], a [AGE] year old [DESCRIPTION] who interacts like
> [PERSONALITY TRAIT OR STYLE]. Keep your replies [LENGTH RULE]. Use
> [TONE DETAILS]. [EMOJI RULES]. Be [MOOD/STYLE] but [CONTRASTING RULE].
> Avoid [WHAT NOT TO DO].

7. Open up Bot.py and edit the line `Model =  "YourModel"` to reflect the model you are using with Ollama.
   > You can see all of your installed models by executing `ollama list` in the command prompt.
   > **Example:** `Model =  "llama3.1:8b"`
8. Open a command prompt within the folder where the previously mentioned files are. Then, launch the bot with `python .\Bot.py` (or `python3 .\Bot.py`, depending on your system)!
   > If you get `ModuleNotFoundError: python-telegram-bot`, make sure your venv is activated!

# Credits
**If you would credit me somehow, I would be overjoyed!** 
Also, please report problems directly to me, [@peeksxx](t.me/peeksxx) on Telegram!
