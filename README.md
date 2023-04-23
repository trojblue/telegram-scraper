# Telegram User scraper

## Installation

```bash
git clone https://github.com/trojblue/telegram-scraper
cd telegram-scraper
pip install -r requirements.txt
```

## Get bot ID

1. 去: https://my.telegram.org/apps 获取你的api_id和api_hash
2. 修改`config.ini`文件, 写入你的`api_id`和`api_hash`:

```ini
[pyrogram]
api_id = 123456
api_hash = 1234567890abcdef1234567890abcdef
```




## Usage

1. 找到需要的用户和群组id:
```bash
python pyro_get_ids
```

2. 爬取聊天记录里的图片(修改TARGET_USER_ID和TARGET_CHAT_ID):
```bash
python pyro_scrape_chat
```


