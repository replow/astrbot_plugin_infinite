# 无限二代 AstrBot 插件

面向 AstrBot 4.29.1 的独立插件，默认关闭。管理员可在消息来源中使用：

- `/armor on`、`/armor off`、`/armor status`：开关及查看上游提示词；别名 `/破甲`。
- `/replystyle on`、`off`、`status`、`direct`、`balanced`、`detail`：控制回复风格；`on` 默认使用 `direct`，别名 `/回复风格`。

消息来源状态保存在 AstrBot 插件 KV 存储中。开启后每次模型请求追加上游提示词；模型不一定遵循，提示词会增加 token 消耗。提示词里的自动恢复和攻击模板只是模型指令，不会执行工具、自动重试或保证成功。

插件没有额外 Python 依赖。安装 ZIP 后在 WebUI 的插件列表确认已加载。若服务器上传接口超时，重写插件不一定能解决服务器侧问题。

提示词取自 [dsh-infinite-gen-2](https://github.com/xuanmingguo/dsh-infinite-gen-2) 提交 `3a701c334dd15e59c6ac663d93d313489385bbc5`，MIT 许可及版权见 `LICENSE`。
