from pathlib import Path

from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.provider import ProviderRequest
from astrbot.api.star import Context, Star


STYLES = {
    "direct": ("简洁", "先给结论。只保留回答问题所需的信息。"),
    "balanced": ("标准", "先回答问题，再按需补充理由、步骤或例子。"),
    "detail": ("详细", "先给结论，再说明关键依据和步骤。适合时补充例子。"),
}
PROMPT = (Path(__file__).parent / "infinite-gen-2.md").read_text(encoding="utf-8").strip()


class InfinitePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("armor", alias={"破甲"})
    async def armor(self, event: AstrMessageEvent, action: str = "status"):
        """为当前消息来源开关无限二代提示词。"""
        event.should_call_llm(False)
        key = f"armor:{event.unified_msg_origin}"
        action = action.casefold()
        if action == "on":
            await self.put_kv_data(key, True)
        elif action == "off":
            await self.delete_kv_data(key)
        elif action != "status":
            yield event.plain_result("用法：/armor on | off | status")
            return
        enabled = await self.get_kv_data(key, False)
        status = "已开启" if enabled else "已关闭"
        yield event.plain_result(f"当前会话破甲提示词：{status}。")

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("replystyle", alias={"回复风格"})
    async def reply_style(self, event: AstrMessageEvent, action: str = "status"):
        """为当前消息来源设置回复风格。"""
        event.should_call_llm(False)
        key = f"style:{event.unified_msg_origin}"
        action = action.casefold()
        if action == "off":
            await self.delete_kv_data(key)
        elif action == "on":
            await self.put_kv_data(key, "direct")
        elif action in STYLES:
            await self.put_kv_data(key, action)
        elif action != "status":
            yield event.plain_result("用法：/replystyle on | off | status | direct | balanced | detail")
            return
        style = await self.get_kv_data(key, None)
        label = STYLES[style][0] if style in STYLES else "关闭"
        yield event.plain_result(f"当前会话回复风格：{label}。")

    @filter.on_llm_request()
    async def apply_prompts(self, event: AstrMessageEvent, req: ProviderRequest):
        sections = []
        enabled = await self.get_kv_data(f"armor:{event.unified_msg_origin}", False)
        if enabled and PROMPT not in (req.system_prompt or ""):
            sections.append(PROMPT)
        style = await self.get_kv_data(f"style:{event.unified_msg_origin}", None)
        if style in STYLES:
            instruction = "[AstrBot 回复风格]\n" + STYLES[style][1]
            if instruction not in (req.system_prompt or ""):
                sections.append(instruction)
        if sections:
            req.system_prompt = "\n\n".join(part for part in [req.system_prompt, *sections] if part)
