import discord
from discord.ext import commands, tasks
from discord.ui import View, Button
import json
import os
import asyncio
from datetime import datetime, timedelta

TOKEN = "MTUwMTU1MDkxMjg4MjA4MTg3Ng.GQo9lL.tLPpqJJh3zCYcuL7gbBm7XGvWW4RSK9d50faB8"

# -------------------------
# 身份组ID
# -------------------------

# 永久会员
BETA_ROLE_ID = 1485602323139919952

# 10天会员
USER_ROLE_ID = 1500717052036644864

# 黑名单身份组
BLACK_ROLE_ID = 1500718928538894417

# 管理员身份组
ADMIN_ROLE_ID = 1500718685046833272

# 18+身份组
VERIFY18_ROLE_ID = 1505973814625042492
# -------------------------
# 频道/分类ID
# -------------------------

# 日志频道
LOG_CHANNEL_ID = 123456789

# 工单分类
TICKET_CATEGORY_ID = 123456789

# -------------------------
# Bot配置
# -------------------------

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

print("机器人启动成功")

# -------------------------
# 文件
# -------------------------

KEY_FILE = "keys.json"
USED_FILE = "used.json"
TIME_FILE = "time.json"
BLACK_FILE = "black.json"
MONEY_FILE = "money.json"
SIGN_FILE = "sign.json"

# 创建文件
for file in [
    KEY_FILE,
    USED_FILE,
    TIME_FILE,
    BLACK_FILE,
    MONEY_FILE,
    SIGN_FILE
]:

    if not os.path.exists(file):

        with open(file, "w") as f:

            json.dump({}, f)

# -------------------------
# JSON函数
# -------------------------

def load_json(file):

    with open(file, "r") as f:

        return json.load(f)

def save_json(file, data):

    with open(file, "w") as f:

        json.dump(data, f, indent=4)

# -------------------------
# 日志函数
# -------------------------

async def send_log(text):

    channel = bot.get_channel(LOG_CHANNEL_ID)

    if channel:

        await channel.send(text)

# -------------------------
# 判断管理员
# -------------------------

async def is_admin(ctx):

    member = await ctx.guild.fetch_member(
        ctx.author.id
    )

    for role in member.roles:

        if role.id == ADMIN_ROLE_ID:

            return True

    return False

# -------------------------
# 启动
# -------------------------

@bot.event
async def on_ready():

    print(f"已登录 {bot.user}")

    check_expire.start()

# -------------------------
# 自动检测会员到期
# -------------------------

@tasks.loop(minutes=1)
async def check_expire():

    data = load_json(TIME_FILE)

    now = datetime.now()

    remove_list = []

    for user_id in data:

        end_time = datetime.fromisoformat(
            data[user_id]["time"]
        )

        if now >= end_time:

            guild = bot.get_guild(
                data[user_id]["guild"]
            )

            member = guild.get_member(
                int(user_id)
            )

            role = guild.get_role(
                USER_ROLE_ID
            )

            try:

                await member.remove_roles(role)

                await send_log(
                    f"⏰ {member} 的 XiaoQ User 已到期"
                )

            except:
                pass

            remove_list.append(user_id)

    for user_id in remove_list:

        del data[user_id]

    save_json(TIME_FILE, data)

# -------------------------
# 帮助菜单
# -------------------------

@bot.slash_command(
    name="help",
    description="查看帮助菜单"
)
async def help(ctx):

    text = """
📖 XiaoQ 帮助菜单

━━━━━━━━━━━━━━

🎫 会员系统

/key 卡密
兑换卡密

/myvip
查看会员时间

━━━━━━━━━━━━━━

💰 签到系统

/sign
每日签到

/balance
查看余额

━━━━━━━━━━━━━━

🛠 管理系统

/createkey 代号
创建永久卡密

/createuserkey 代号
创建10天卡密

/delkey 卡密
删除卡密

/ban2 @用户
加入黑名单

/unban2 @用户
解除黑名单

━━━━━━━━━━━━━━

📩 工单系统

/ticketpanel
发送工单面板

/close
关闭工单

━━━━━━━━━━━━━━

🎛 面板系统

/panel
发送机器人面板

━━━━━━━━━━━━━━
"""

    await ctx.respond(text)

# -------------------------
# 每日签到
# -------------------------

@bot.slash_command(
    name="sign",
    description="每日签到"
)
async def sign(ctx):

    sign_data = load_json(SIGN_FILE)
    money_data = load_json(MONEY_FILE)

    user_id = str(ctx.author.id)

    today = datetime.now().strftime("%Y-%m-%d")

    # 已签到
    if user_id in sign_data:

        if sign_data[user_id] == today:

            await ctx.respond(
                "❌ 你今天已经签到过了"
            )

            return

    # 增加金币
    if user_id not in money_data:

        money_data[user_id] = 0

    money_data[user_id] += 100

    # 保存签到
    sign_data[user_id] = today

    save_json(SIGN_FILE, sign_data)
    save_json(MONEY_FILE, money_data)

    await ctx.respond(
        "✅ 签到成功\n💰 获得 100 金币"
    )

# -------------------------
# 查看余额
# -------------------------

@bot.slash_command(
    name="balance",
    description="查看余额"
)
async def balance(ctx):

    money_data = load_json(MONEY_FILE)

    user_id = str(ctx.author.id)

    if user_id not in money_data:

        money_data[user_id] = 0

        save_json(MONEY_FILE, money_data)

    await ctx.respond(
        f"💰 你的余额：{money_data[user_id]} 金币"
    )

# -------------------------
# 创建永久卡密
# -------------------------

@bot.slash_command(
    name="createkey",
    description="创建永久卡密"
)
async def createkey(ctx, code: str):

    await ctx.defer()

    if not await is_admin(ctx):

        await ctx.followup.send(
            "❌ 你没有权限"
        )

        return

    keys = load_json(KEY_FILE)

    key = f"XiaoQ Beta-{code}"

    if key in keys:

        await ctx.followup.send(
            "❌ 卡密已存在"
        )

        return

    keys[key] = "beta"

    save_json(KEY_FILE, keys)

    try:

        await ctx.author.send(
            f"✅ 创建成功\n\n{key}"
        )

    except:
        pass

    await send_log(
        f"🛠 {ctx.author} 创建了永久卡密\n{key}"
    )

    await ctx.followup.send(
        "✅ 已私聊发送卡密"
    )

# -------------------------
# 创建10天卡密
# -------------------------

@bot.slash_command(
    name="createuserkey",
    description="创建10天卡密"
)
async def createuserkey(ctx, code: str):

    await ctx.defer()

    if not await is_admin(ctx):

        await ctx.followup.send(
            "❌ 你没有权限"
        )

        return

    keys = load_json(KEY_FILE)

    key = f"XiaoQ User-{code}"

    if key in keys:

        await ctx.followup.send(
            "❌ 卡密已存在"
        )

        return

    keys[key] = "user"

    save_json(KEY_FILE, keys)

    try:

        await ctx.author.send(
            f"✅ 创建成功\n\n{key}"
        )

    except:
        pass

    await send_log(
        f"🛠 {ctx.author} 创建了10天卡密\n{key}"
    )

    await ctx.followup.send(
        "✅ 已私聊发送卡密"
    )

# -------------------------
# 删除卡密
# -------------------------

@bot.slash_command(
    name="delkey",
    description="删除卡密"
)
async def delkey(ctx, code: str):

    await ctx.defer()

    if not await is_admin(ctx):

        await ctx.followup.send(
            "❌ 你没有权限"
        )

        return

    keys = load_json(KEY_FILE)

    if code not in keys:

        await ctx.followup.send(
            "❌ 卡密不存在"
        )

        return

    del keys[code]

    save_json(KEY_FILE, keys)

    await ctx.followup.send(
        "✅ 删除成功"
    )

# -------------------------
# 查询会员
# -------------------------

@bot.slash_command(
    name="myvip",
    description="查看会员"
)
async def myvip(ctx):

    data = load_json(TIME_FILE)

    beta_role = ctx.guild.get_role(
        BETA_ROLE_ID
    )

    if beta_role in ctx.author.roles:

        await ctx.respond(
            "👑 你是永久 XiaoQ Beta"
        )

        return

    if str(ctx.author.id) in data:

        end_time = datetime.fromisoformat(
            data[str(ctx.author.id)]["time"]
        )

        left = end_time - datetime.now()

        days = left.days

        hours = left.seconds // 3600

        await ctx.respond(
            f"⏰ 剩余时间\n{days}天 {hours}小时"
        )

        return

    await ctx.respond(
        "❌ 你没有会员"
    )

# -------------------------
# 兑换卡密
# -------------------------

@bot.slash_command(
    name="key",
    description="兑换卡密"
)
async def key(ctx, code: str):

    await ctx.defer()

    keys = load_json(KEY_FILE)

    used = load_json(USED_FILE)

    if code not in keys:

        await ctx.followup.send(
            "❌ 卡密错误"
        )

        return

    if code in used:

        await ctx.followup.send(
            "❌ 卡密已使用"
        )

        return

    try:

        # 永久会员
        if keys[code] == "beta":

            role = ctx.guild.get_role(
                BETA_ROLE_ID
            )

            await ctx.author.add_roles(role)

            used[code] = True

            save_json(USED_FILE, used)

            await ctx.followup.send(
                "✅ XiaoQ Beta 已发放（永久）"
            )

        # 10天会员
        elif keys[code] == "user":

            role = ctx.guild.get_role(
                USER_ROLE_ID
            )

            await ctx.author.add_roles(role)

            used[code] = True

            save_json(USED_FILE, used)

            data = load_json(TIME_FILE)

            end = datetime.now() + timedelta(days=10)

            data[str(ctx.author.id)] = {

                "time": end.isoformat(),
                "guild": ctx.guild.id
            }

            save_json(TIME_FILE, data)

            await ctx.followup.send(
                "✅ XiaoQ User 已发放\n⏰ 10天后自动到期"
            )

    except Exception as e:

        await ctx.followup.send(
            f"❌ 发放失败\n{e}"
        )

# -------------------------
# 黑名单系统
# -------------------------

@bot.slash_command(
    name="ban2",
    description="拉黑用户"
)
async def ban2(ctx, user: discord.Member):

    await ctx.defer()

    if not await is_admin(ctx):

        await ctx.followup.send(
            "❌ 你没有权限"
        )

        return

    role = ctx.guild.get_role(
        BLACK_ROLE_ID
    )

    await user.add_roles(role)

    await ctx.followup.send(
        f"🚫 已拉黑 {user.mention}"
    )

@bot.slash_command(
    name="unban2",
    description="解除黑名单"
)
async def unban2(ctx, user: discord.Member):

    await ctx.defer()

    if not await is_admin(ctx):

        await ctx.followup.send(
            "❌ 你没有权限"
        )

        return

    role = ctx.guild.get_role(
        BLACK_ROLE_ID
    )

    await user.remove_roles(role)

    await ctx.followup.send(
        f"✅ 已解除 {user.mention}"
    )

# -------------------------
# 工单系统
# -------------------------

@bot.slash_command(
    name="ticketpanel",
    description="发送工单面板"
)
async def ticketpanel(ctx):

    view = View(timeout=None)

    button = Button(
        label="创建工单",
        emoji="📩",
        style=discord.ButtonStyle.green
    )

    async def callback(interaction):

        category = interaction.guild.get_channel(
            TICKET_CATEGORY_ID
        )

        channel = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category
        )

        await channel.set_permissions(
            interaction.guild.default_role,
            view_channel=False
        )

        await channel.set_permissions(
            interaction.user,
            view_channel=True,
            send_messages=True
        )

        await channel.send(
            f"📩 {interaction.user.mention} 工单已创建"
        )

        await interaction.response.send_message(
            f"✅ 工单已创建：{channel.mention}",
            ephemeral=True
        )

    button.callback = callback

    view.add_item(button)

    await ctx.respond(
        "📩 XiaoQ 工单系统",
        view=view
    )

# -------------------------
# 关闭工单
# -------------------------

@bot.slash_command(
    name="close",
    description="关闭工单"
)
async def close(ctx):

    await ctx.defer()

    if not ctx.channel.name.startswith("ticket-"):

        await ctx.followup.send(
            "❌ 这里只能在工单频道使用"
        )

        return

    await ctx.followup.send(
        "🗑 工单将在5秒后关闭"
    )

    await asyncio.sleep(5)

    await ctx.channel.delete()

# -------------------------
# 面板系统
# -------------------------

@bot.slash_command(
    name="panel",
    description="发送控制面板"
)
async def panel(ctx):

    view = View(timeout=None)

    btn1 = Button(
        label="帮助菜单",
        emoji="📖",
        style=discord.ButtonStyle.blurple
    )

    async def btn1_callback(interaction):

        await interaction.response.send_message(
            "使用 /help 查看帮助菜单",
            ephemeral=True
        )

    btn1.callback = btn1_callback

    btn2 = Button(
        label="查看会员",
        emoji="👑",
        style=discord.ButtonStyle.green
    )

    async def btn2_callback(interaction):

        await interaction.response.send_message(
            "使用 /myvip 查看会员",
            ephemeral=True
        )

    btn2.callback = btn2_callback

    btn3 = Button(
        label="每日签到",
        emoji="💰",
        style=discord.ButtonStyle.gray
    )

    async def btn3_callback(interaction):

        await interaction.response.send_message(
            "使用 /sign 进行签到",
            ephemeral=True
        )

    btn3.callback = btn3_callback

    view.add_item(btn1)
    view.add_item(btn2)
    view.add_item(btn3)

    await ctx.respond(
        "🎛 XiaoQ 控制面板",
        view=view
    )

# -------------------------
# 启动机器人
# -------------------------

# -------------------------
# 18+验证系统
# -------------------------

@bot.slash_command(
    name="verify18",
    description="18岁验证"
)
async def verify18(ctx):

    view = View(timeout=None)

    button = Button(
        label="我已满18岁",
        emoji="🔞",
        style=discord.ButtonStyle.red
    )

    async def callback(interaction):

        role = interaction.guild.get_role(
            VERIFY18_ROLE_ID
        )

        # 已有身份组
        if role in interaction.user.roles:

            await interaction.response.send_message(
                "✅ 你已经完成18+验证",
                ephemeral=True
            )

            return

        # 添加身份组
        await interaction.user.add_roles(role)

        await interaction.response.send_message(
            "🔞 18+验证成功",
            ephemeral=True
        )

        # 日志
        await send_log(
            f"🔞 {interaction.user} 完成18+验证"
        )

    button.callback = callback

    view.add_item(button)

    await ctx.respond(
        "🔞 成人验证\n\n点击下面按钮确认你已满18岁",
        view=view
    )
bot.run(TOKEN)
