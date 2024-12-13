import discord
from discord.ext import commands
from discord import app_commands
intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready(): 
    print(f"{bot.user}ログイン成功 (ID: {bot.user.id})")
    print("------")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")


@bot.tree.command(name='verify', description='認証パネルをこのチャンネルに設置します')
@app_commands.describe(role='認証時に付与するロール名')
async def verify(interaction: discord.Interaction, role: discord.Role):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("エラー: このコマンドを使用するには管理者権限が必要です。", ephemeral=True)
        return

    bot_member = interaction.guild.get_member(bot.user.id)
    if role.position >= bot_member.top_role.position:
        await interaction.response.send_message("このロールはボットよりも権限が上です。", ephemeral=True)
        return

    embed = discord.Embed(title="認証", description="下記のボタンをおして認証を完了してください", color=discord.Color.blue())
    view = discord.ui.View(timeout=None)
    button = discord.ui.Button(label="✅ 認証", style=discord.ButtonStyle.green)

    async def button_callback(interaction: discord.Interaction):
        if role in interaction.user.roles:
            await interaction.response.send_message("既にこのロールを持っています。", ephemeral=True)
            return

        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"認証が完了しました。{role.mention} を付与しました。", ephemeral=True)

    button.callback = button_callback
    view.add_item(button)
    await interaction.response.send_message(embed=embed, view=view)

    


#--------------------------
bot.run("BOTのとーくん")# |
#--------------------------
