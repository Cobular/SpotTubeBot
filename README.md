# SpotTubeBot

This bot converts spotify links to YouTube links! It has both a discord and a telegram implementation, see below for instructions to add.

## Discord

https://discord.com/oauth2/authorize?client_id=863293069204914216&scope=bot%20applications.commands&permissions=2147486784

### Discord Usage

* `/convert <spotify-url>` converts the individual spotify url to YouTube
* `/add_channel <channel (optional)>` adds the current channel (or the specified channel) to the watchlist, meaning the bot will automatically convert any spotify links it sees.
* `/remove_channel <channel (optional)>` removes the current channel (or the specified channel) from the watchlist, meaning it will no longer automatically convert any spotify links it sees. 

Any spotify link sent in a channel on the watchlist will automatically be converted if possible.

# Telegram

Just type `@SpotTubeBot` in any channel or DM, then paste the link in after.
