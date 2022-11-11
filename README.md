# stacker-news-top

Telegram bot that posts new hot stories from [Stacker News](https://stacker.news/) to [telegram channel](https://t.me/stackernewstop)

## Telegram API

Bot uses [Telegram Bot API](https://core.telegram.org/bots/api) to post messages to the [telegram channel](https://t.me/stackernewstop) with [sendMessage](https://core.telegram.org/bots/api#sendmessage) request

## How to run your own `stacker-news-top`

- Clone this project
- Run `pip3 install -r requirements.txt` to install dependencies
- Create your bot via [BotFather](https://t.me/BotFather)
- Rename `conf/config-sample.yaml` to `conf/config.yaml` and
  - set `db_type` to `sqlite` or `redis`
  - replace `tg_chat_id` with your channel/chat/group id
  - replace `tg_token` with your bot token
  - you can also change the `db_name`, `redis_url`, `log_name` and `log_file`
- Run `python3 app.py` in the project folder
- Use misc/stackernews.service to run the bot as a service

## Stacker News Trending Channel

Link to join the channel: <https://t.me/stackernewstop>
