import json

with open('plugins/anti_revoke/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

ADMIN_NICKNAME = config.get('admin_nickname')
ADMIN_WECHAT_ID = config.get('admin_wechat_id')
