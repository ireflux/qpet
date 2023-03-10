<h1 align="center">
  <pre>
                    _____ 
______ _______________  /_
_  __ `/__  __ \  _ \  __/
/ /_/ /__  /_/ /  __/ /_  
\__, / _  .___/\___/\__/  
  /_/  /_/                

  </pre>
</h1>

# qpet

## 简介

一个「Q宠大乐斗」脚本，使用 Github Action 执行。

## 功能

- 支持斗友、好友、帮友、侠侣等全体力消耗性乐斗
- 支持根据自身最新历练场景全活力消耗
- 支持绝大部分「必做」类任务
- 支持 Server酱、Telegram Bot 消息推送

## 使用

1. fork [qpet](https://github.com/ireflux/qpet) 到自己的仓库
2. 登录 [Q宠大乐斗](https://dld.qzapp.z.qq.com/qpet/cgi-bin/phonepk?cmd=index&channel=0) 获取 cookie
3. 从自己仓库中的 `qpet` 依次进入 `Setting -> Secrets -> New repository secret`
4. 添加 Name 为 `QPET_COOKIE`，Value 为 `获取到的 cookie`
5. (可选)微信接收运行日志: 添加 Name 为 `SERVERJ_SEND_KEY`，Value 为从 [Server酱](https://sct.ftqq.com/) 获取到的 `SENDKEY`
6. (可选) Telegram 接收运行日志: 添加 Name 为 `TELEGRAM_BOT_TOKEN`，Value 为 Telegram Bot 的 token；添加 Name 为 `TELEGRAM_CHAT_ID`，Value 为获取到的 chat_id. 具体创建 Telegram Bot，获取 token 和 chat_id 的操作流程可查看 [Telegram Bot API](https://core.telegram.org/bots/api#getting-updates) 文档
7. 手动进入 `Actions -> qpet job -> Run workflow` 执行 ~~或者每日 13：05 自动执行（由于cookie有效期太短，自动执行意义不大，取消自动）~~ 

