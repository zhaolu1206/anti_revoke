import itchat
from itchat.content import NOTE
import re
import json

# 读取配置文件中的管理员WeChat ID或昵称
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
ADMIN_WECHAT_ID = config.get('ADMIN_WECHAT_ID')
ADMIN_WECHAT_NICKNAME = config.get('ADMIN_WECHAT_NICKNAME')

@itchat.msg_register(NOTE, isFriendChat=True, isGroupChat=True, isMpChat=True)
def anti_revoke(msg):
    if '撤回了一条消息' in msg['Content']:
        # 提取撤回的消息ID
        old_msg_id = re.search(r'<msgid>(.*?)</msgid>', msg['Content']).group(1)
        # 从消息缓存中获取撤回的消息
        old_msg = itchat.search_chatrooms(msgId=old_msg_id)
        if old_msg:
            # 发送撤回的消息给管理员
            if ADMIN_WECHAT_ID:
                itchat.send(f"检测到撤回消息：{old_msg['Text']}", toUserName=ADMIN_WECHAT_ID)
            elif ADMIN_WECHAT_NICKNAME:
                admin = itchat.search_friends(nickName=ADMIN_WECHAT_NICKNAME)[0]
                admin.send(f"检测到撤回消息：{old_msg['Text']}")

# 注册插件
def load():
    itchat.run()
