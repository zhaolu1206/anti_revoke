import itchat
from itchat.content import TEXT, NOTE
from plugins import register, Plugin
from bridge.context import ContextType, EventContext
from bridge.reply import Reply, ReplyType
from bridge.event import Event, EventAction
import logging

logger = logging.getLogger(__name__)

@register(name="AntiRevoke", desc="A plugin to prevent message revocation", version="0.1", author="your_name", desire_priority= -1)
class AntiRevoke(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[AntiRevoke] inited")

    def on_handle_context(self, e_context: EventContext):
        if e_context['context'].type != ContextType.TEXT and e_context['context'].type != ContextType.NOTE:
            return
        msg = e_context['context']['msg']
        if e_context['context'].type == ContextType.NOTE and '撤回了一条消息' in msg.text:
            revoked_msg_id = msg.text.split('msgid=')[1].split('&')[0]
            revoked_msg = itchat.search_chatrooms(userName=msg.fromUserName).get(revoked_msg_id)
            if revoked_msg:
                admin = itchat.search_friends(nickName='老赵')[0]['UserName']
                itchat.send(f"检测到撤回消息：{revoked_msg['Text']}", toUserName=admin)
                e_context.action = EventAction.BREAK_PASS
        else:
            e_context.action = EventAction.CONTINUE
