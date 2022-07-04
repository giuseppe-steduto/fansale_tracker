# Fansale ticket checker
Simple script to check whether there are at least a certain number of available tickets on FanSale, for a given event. 
For "available tickets" it is intended that the seats have to be next to each other.

## Dependencies
This script requires that you have Firefox and [geckodriver](https://github.com/mozilla/geckodriver/releases) installed.
In order to install the python modules required to execute this script, you can run: `pip3 install install -r requirements.txt`.

## Configuration
Clone the project, then create a `.env` file in which you will store the configuration variables:
- The number of available seats over which you want to be notified (e.g. when there are at least 5 available seats)
- The URL of the event on fansale
- The Telegram chat id on which the bot will send the message
- The API KEY for your Telegram bot

```
git clone https://github.com/giuseppe-steduto/fansale_tracker
cd fansale_tracker
nano .env
```

The .env file should look something like this:
```
API_TOKEN=<Your Telegram bot token>
CHAT_ID=<Your Telegram chat id>
MINIMUM_SEATS=2
URL=https://www.fansale.it/fansale/tickets/pop...
```
## Running
After resolving the dependencies and setting up the environment variables in the file, you can run the script by just compiling it with `python3 main.py`. 
This script is most useful when run specific intervals (for example, every 10 minutes). In that case, the best choice may be to use a cron job for running this script.

