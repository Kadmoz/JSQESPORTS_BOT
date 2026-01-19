# JSQ ESPORTS Discord Bot

## Overview
A Discord bot for managing F1 simracing league schedules and tournaments for JSQ ESPORTS. The bot allows users to view tournament calendars, get race reminders, and manage league information.

## Project Structure
- `bot.py` - Main bot code with all commands and functionality
- `requirements.txt` - Python dependencies (discord.py)
- `torneos.json` - Data file storing tournament information (created at runtime)

## Setup Requirements
- **DISCORD_TOKEN** - A Discord bot token is required. Get one from the [Discord Developer Portal](https://discord.com/developers/applications)

## Bot Commands
### User Commands
- `!calendario` or `!cal` - View the full weekly tournament schedule
- `!hoy` - View today's races
- `!proxima` or `!pc` - View the next upcoming race
- `!info <tournament>` - Get detailed info about a specific tournament
- `!ayuda_bot` - Show all available commands

### Admin Commands (require administrator permissions)
- `!actualizar <tournament> | hora: HH:MM | admin: Name | stream: URL` - Update tournament info
- `!nuevo_torneo <day> <name>` - Add a new tournament
- `!eliminar_torneo <name>` - Remove a tournament
- `!canal_recordatorios` - Set the current channel to receive race reminders

## Running the Bot
The bot runs as a background process via the "Discord Bot" workflow. It will connect to Discord and stay online as long as the workflow is running.

## Deployment
For production, deploy as a VM (always-on) since Discord bots need to maintain a persistent connection.
