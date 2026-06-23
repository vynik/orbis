<div align="center">

# Orbis!

### A powerful, all-in-one Discord bot built with just Python

*Moderation, ticketing, utilities, and smart event tracking. All in one place.*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](#contributing)

</div>

---

## Overview

QUICK DISCLAIMER: THIS IS MY FIRST EVER BIG PROJECT I EVER MADE SO DONT MIND THE BAD CODE (IF THERE IS) :D

Orbis is a discord bot, using the discord.py, which is designed to not only assist you at saving information but also to get some clarity into your sever. Orbis as features like **server moderation** (where warns are saved in a database using sqllite3) to **support ticketing** and **member utilities**. Not only does Orbis offer a variety of commands, it also listens to many events happening in your server, so you maybe the next time know, what a person meant, after deleting it and saying: **"oh, it was nothing."**

This discord bot was made for fun and will also receive updates, when adding new functions to the bot :-)

Whether you're running a small community or a large server, this bot is built to scale with you.

---

## Features

### Moderation
- **Warn System** — Issue, remove, and review warnings against members. All warnings are stored in a **database**, so they persist across restarts and stay tied to the user.
- **Purge** — Bulk-delete messages quickly to keep channels clean.

### Support & Communication
- **Ticket System** — A fully working support ticket workflow, letting members (or staff, on their behalf) open private channels to get help, and close them when resolved.
- **Send Message as Bot** — Broadcast or send custom messages through the bot directly to channels.
- **DM Replies** — The bot can reply to direct messages, enabling private interactions and support flows.

### General / Utility
- **Ping** — Check the bot's latency and confirm it's online.
- **User Info** — Pull detailed information about any member.
- **Random GIF** — Fetch a random GIF on demand for some fun based on the Giphy API.

---

## Event Tracking

The bot doesn't just respond to commands — it actively watches your server and reacts to what happens.

| Event | What the bot does |
|-------|-------------------|
| **Startup** | On every boot, the bot picks a **random activity status** using Python's `random` library so it never looks the same twice. |
| **Message Delete** | Detects and logs when a message is deleted. |
| **Message Edit** | Detects and logs when a message is edited. |
| **Voice Activity** | Tracks when members **join**, **switch**, or **leave** voice channels. |
| **Direct Messages** | Sends a response/notification whenever someone DMs the bot. |

---

## Command Reference

| Command | Category | Description |
|---------|----------|-------------|
| `/warn_user` | Moderation | Warn a member (saved to the database). |
| `/remove_warn` | Moderation | Remove an existing warning from a member. |
| `/warn_logs` | Moderation | View the warning history for a member. |
| `/purge` | Moderation | Bulk-delete a number of messages. |
| `/send_message` | Communication | Send a message through the bot to a channel. |
| `/reply_dm` | Communication | Reply to a user's direct message via the bot. |
| `/createticket` | Tickets | Open a new support ticket. |
| `/openticketfor` | Tickets | Open a support ticket on behalf of another member. |
| `/closeticket` | Tickets | Close an existing support ticket. |
| `/ping` | General | Check the bot's latency and status. |
| `/userinfo` | General | Show detailed info about a member. |
| `/random_gif` | Fun | Send a random GIF. |

---

## Installation

### Prerequisites
- Python **3.10+**
- A **Discord Bot Token** ([create one here](https://discord.com/developers/applications))

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/vynik/orbis.git
cd YOUR_REPO

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 5. Run the bot
python main.py
```

---

## Configuration

Edit the config.json (if you need help or don't know what to insert, check out the config.example file!)

```env
discord_token=your-bot-token-here
giphy_api=your-api-token-here
dm-bot-history_id=discord-channel-ids (turn on developer mode)
vc-join-leave-log_id=discord-channel-ids (turn on developer mode)
message-del-or-edit-log_id=discord-channel-ids (turn on developer mode)
bot-message-sent-log_id=discord-channel-ids (turn on developer mode)
warn-logs_id=discord-channel-ids (turn on developer mode)
ticket-history_id=discord-channel-ids (turn on developer mode)
ticket-category_id=discord-category-ids (turn on developer mode)
# Add required API keys and database settings here
```

Quick reminder:
> **Never commit your token or `.env` file.** Make sure they're listed in your `.gitignore`.

---

## Tech Stack

- **[Python](https://www.python.org/)** — core language
- **[discord.py](https://discordpy.readthedocs.io/)** — Discord API wrapper
- **Database** — persistent storage for the warn system *sqllite3*

---

## Contributing

Contributions are welcome and appreciated! To get started:

1. **Fork** the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a **Pull Request**

Feel free to open an [issue](../../issues) or add me on discord: 4zuj for bugs, ideas, or questions.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Need help?

If you need help or want to have a custom command made by your desire, you can dm me via discord and I'll try to create the command for you (if I have time :-))

I can also help you at setting up the bot if needed to.

Discord : vynik_

---

<div align="center">

### If you like this project, consider giving it a ⭐!

Made with python by vynik.

</div>
