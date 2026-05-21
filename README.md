# xiaoqbot90%用AI写的10%人工写的不推荐使用如果你实在有点懒那你可以更改一下里面的bot.py注意请阅读

🤖 XiaoQ Discord bot

支持：

- 🎫 会员系统
- 💰 每日签到
- 📩 工单系统
- 🔞 18+验证
- 🎛 控制面板
- 🏓 Ping 状态
- ☁️ Railway 云部署

---

📱 开发环境

本项目主要使用：

- Railway（云部署）
- GitHub（代码仓库）
- Pydroid 3（手机Python开发）
- Discord Developer Portal（机器人后台）

---

📦 安装环境

Android 用户

安装：

Pydroid 3

用于手机编辑 Python。

Google Play 搜索：

Pydroid 3

---

GitHub

用于保存代码。

官网：

https://github.com

---

Railway

用于机器人24小时挂机。

官网：

https://railway.app

---

🤖 创建 Discord Bot

打开：

https://discord.com/developers/applications

---

创建机器人

步骤：

1. New Application
2. 输入机器人名字
3. 点击 Bot
4. Add Bot

---

开启权限

进入：

Bot → Privileged Gateway Intents

开启：

- Presence Intent
- Server Members Intent
- Message Content Intent

---

获取 TOKEN

点击：

Reset Token

复制 TOKEN。

⚠️ 不要泄露 TOKEN。

---

📂 上传 GitHub

创建仓库

GitHub：

New Repository

创建：

XiaoQ-Bot

---

上传文件

上传：

bot.py

以及：

requirements.txt

---

📜 requirements.txt

内容：

py-cord

---

☁️ Railway 部署教程

1. 登录 Railway

打开：

https://railway.app

使用 GitHub 登录。

---

2. New Project

点击：

Deploy from GitHub repo

选择：

XiaoQ-Bot

---

3. 添加 TOKEN

进入：

Variables

添加：

TOKEN=你的机器人TOKEN

---

4. 自动部署

Railway 会自动：

- 安装依赖
- 运行 bot.py
- 挂机运行

---

📱 Pydroid 3 使用教程

打开 bot.py

在 Pydroid 3 中：

打开 bot.py

即可编辑机器人代码。

---

安装库

在 Pydroid 3 终端输入：

pip install py-cord

---

本地测试

运行：

python bot.py

看到：

机器人启动成功
已登录 xxx

说明成功。

---

⚙️ 修改机器人ID

在 bot.py 修改：

BETA_ROLE_ID = 身份组ID
USER_ROLE_ID = 身份组ID
BLACK_ROLE_ID = 身份组ID
ADMIN_ROLE_ID = 身份组ID
VERIFY18_ROLE_ID = 身份组ID

LOG_CHANNEL_ID = 日志频道ID
TICKET_CATEGORY_ID = 工单分类ID

---

🏓 Ping 系统

使用：

/ping

可查看：

- 延迟
- 在线状态
- 运行时间
- 机器人名称

---

📩 工单系统

发送工单面板：

/ticketpanel

关闭工单：

/close

---

🔞 成人验证

发送18+验证：

/verify18

---

💰 每日签到

签到：

/sign

查看余额：

/balance

---

🎫 会员系统

兑换卡密：

/key 卡密

查看会员：

/myvip

创建永久卡密：

/createkey

创建10天卡密：

/createuserkey

---

🔒 安全说明

请不要公开：

- TOKEN
- Railway Variables
- 私人数据库

否则机器人可能被盗。

---

📜 开源说明

Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

你可以：
- 修改
- 学习
- 分享

禁止：
- 商业使用（付费发放等）

更多信息请参考：
https://creativecommons.org/licenses/by-nc/4.0/

请勿用于违法用途。
还有
此为卡密机器人里面禁止以付费形式发布只是不允许你把这个机器人卖给别人而不是说你不允许把卡密卖给别人你可以创建自己的卡密然后付费卖给别人
---

❤️ 作者

小清