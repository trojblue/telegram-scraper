# Telegram User scraper

## Installation

```bash
git clone https://github.com/trojblue/telegram-scraper
cd telegram-scraper
pip install -r requirements.txt
```

## Get bot ID

1. go to: https://my.telegram.org/apps and obtain `api_id` and `api_hash`
2. modify`config.ini`file and replace with your own credentials:

```ini
[pyrogram]
api_id = 123456
api_hash = 1234567890abcdef1234567890abcdef
```

## Usage

1. find the required user and group IDs:

```bash
python pyro_get_ids
```

2. scrape images (modify TARGET_USER_ID and TARGET_CHAT_ID):

```bash
python pyro_scrape_chat
```


