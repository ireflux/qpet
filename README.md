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

## 提示

1. fork 后，仓库中的 workflow 默认情况下是关闭的，需要进入 `Actions` 手动开启一下
2. 由于大乐斗的 cookie 有效时间很短（<2小时），因此需要每天在脚本执行（每天下午1：05分）前及时更新 cookie :)
