## Description

Discord Honor Bot is a multifunction bot that has many different features, varying from fun to quality of life utilities. 

## Invite Link
  Coming Soon

## Command Syntax
  HonorBot uses discord's new slash command integration, typing '/' into the text bar will bring up available commands and information.

## Getting Started

### Dependencies

* Python 3.12.X
* Check requirements.txt for python libraries

### Installing

* Clone this Repository
* Install all requirements in requirements.txt folder using this command in your venv:
  ```
  pip install -r requirements.txt
  ```
### Starting Web Frame
* Adjust IP and port settings on bot to user specifications
*  In venv instance, CD into /DiscordBot using this command:
  ```
  cd /DiscordBot
  ```
* Run this command to initialize flask:
  ```
  python flaskapp.py
  ```
  
### Starting Discord Bot

* Put bot token from bot created in discord developer portal in config.json file
* In seperate venv instance, CD into /DiscordBot using this command:
  ```
  cd /DiscordBot
  ```
* Run this command to initialize the bot:
  ```
  python bot.py
  ```

## Version History

* 0.0
    * Initial Commit
* 1.0
    * Baseline Bot Functionality

## Inspired by

* MEE6
* Dyno
* NotSoBot
* N Word Counter Bot

## Code inspiration from:
https://github.com/hisham02x/base64-bot
https://github.com/danielzting/clearurls-discord-bot


## License

see the LICENSE file for details
