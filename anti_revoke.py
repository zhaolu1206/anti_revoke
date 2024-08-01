@plugins.register(name="anti_revoke", version="0.1", author="luke", desire_priority= -1)

import time
from wxpy import *

# 管理员的微信ID（需要提前获取）
ADMIN_ID = 'lukezhao-1206'

# 存储消息的字典
msg_dict = {}

# 消息类型映射
msg_type_map = {
    'Text': '文本',
    'Picture': '图片',
    'Recording': '语音',
    'Video': '视频',
    'Attachment': '文件',
}

# 监听消息
@bot.register(Group, except_self=False)
def handle_receive_msg(msg):
    msg_id = msg.id
    msg_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    msg_from = msg.member.name
    msg_content = msg.text if msg.type == 'Text' else msg.file_name
    msg_type = msg_type_map.get(msg.type, '其他')

    # 存储消息
    msg_dict[msg_id] = {
        'msg_from': msg_from,
        'msg_time': msg_time,
        'msg_content': msg_content,
        'msg_type': msg_type,
    }

# 监听撤回消息
@bot.register(Group, NOTE)
def handle_revoke_msg(msg):
    if '撤回了一条消息' in msg.text:
        old_msg_id = msg.text.split('msgid=')[1].split('\"')[0]
        old_msg = msg_dict.get(old_msg_id)

        if old_msg:
            send_msg = f"管理员提醒：\n{old_msg['msg_from']} 在 {old_msg['msg_time']} 撤回了一条消息：\n类型：{old_msg['msg_type']}\n内容：{old_msg['msg_content']}"
            admin = bot.friends().search(ADMIN_ID)[0]
            admin.send(send_msg)
            # 删除已发送的消息记录
            del msg_dict[old_msg_id]

# 插件初始化函数
def init():
    print("防撤回插件已加载")

if __name__ == "__main__":
    init()
