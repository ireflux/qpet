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

一个非通用的Q宠大乐斗脚本，基于 Github Actions 每日执行。

## 使用

1. fork `qpet` 到自己的仓库，
2. 登录[Q宠大乐斗](https://dld.qzapp.z.qq.com/qpet/cgi-bin/phonepk?cmd=index&channel=0)获取 cookie
3. 进入自己仓库中的 `qpet`，依次进入 `Setting -> Secrets -> New repository secret`
4. 添加 Name 为 `QPET_COOKIE`，Value 为 `获取到的 cookie`
5. (可选)微信接收运行日志: 添加 Name 为 `SERVERJ_SEND_KEY`，Value 为从[Server酱](https://sct.ftqq.com/)获取到的 `SENDKEY`
6. (可选) Telegram 接收运行日志: 添加 Name 为 `TELEGRAM_BOT_TOKEN`，Value 为 Telegram Bot 的 token；添加 Name 为 `TELEGRAM_CHAT_ID`，Value 为获取到的 chat_id. 具体创建 Telegram Bot，获取 token 和 chat_id 的操作流程可查看[Telegram Bot API](https://core.telegram.org/bots/api#getting-updates)文档

## 提示

1. 大乐斗在每天下午一点开启武林大会报名，算上报名武林大会提供的5点活跃度，脚本执行完活跃度可以轻松达到50，领取两个活跃礼包。因此脚本将会在每天下午 `1：05分` 自动运行（注：工作流在运行的高负载期间存在延迟，因此运行时间不会特别精确，详情可查看 [Actions doc](https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows#scheduled-events)
2. fork 后，仓库中的 workflow 默认情况下是关闭的，需要进入 `Actions` 手动开启一下
3. 由于大乐斗的 cookie 有效时间很短（<2小时），现阶段还需要每天在脚本执行前及时更新 cookie :)
