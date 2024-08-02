import itchat
from itchat.content import TEXT, NOTE

@itchat.msg_register([TEXT, NOTE], isGroupChat=True)
def handle_revoke_msg(msg):
    if msg.type == 'Note' and '撤回了一条消息' in msg.text:
        revoked_msg_id = msg.text.split('msgid=')[1].split('&')[0]
        revoked_msg = itchat.search_chatrooms(userName=msg.fromUserName).get(revoked_msg_id)
        if revoked_msg:
            admin = itchat.search_friends(nickName='老赵')[0]['UserName']
            itchat.send(f"检测到撤回消息：{revoked_msg['Text']}", toUserName=admin)

itchat.auto_login(hotReload=True)
itchat.run()
