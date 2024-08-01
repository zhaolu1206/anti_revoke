import json

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

ADMIN_WECHAT_ID = config.get('ADMIN_WECHAT_ID')
ADMIN_WECHAT_NICKNAME = config.get('ADMIN_WECHAT_NICKNAME')
