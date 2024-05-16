import discord
from discord.ext import commands
from aiohttp import web, ClientSession
import asyncio
import secrets

client_id = 'your bot client id'
client_secret = 'your bot client secret'
redirect_uri = 'your redirect uri(turorial in readme)'

TOKEN = 'your bot token'

role_id = your role id
server_id = your server id
allowed_channel_id = your allow channel id # NEW! ALLOWED CHANNEL ID(verify channel)
log_channel_id = your log channel id

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='gv!', intents=intents)

oauth_states = {}

async def create_session():
    return ClientSession()

@bot.command()
async def oauth(ctx):
    if ctx.channel.id != allowed_channel_id:
        await ctx.message.delete()
        return await ctx.send("This command can only be used in the specified channel.", delete_after=1)

    token = secrets.token_urlsafe(16)
    state = f"{ctx.guild.id}-{ctx.author.id}-{token}"
    oauth_states[state] = (ctx.guild.id, ctx.author.id)

    oauth_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=identify%20guilds.join&state={state}"

    await ctx.author.send(f"[Verify link]({oauth_url})")

    # Delete the command message
    await ctx.message.delete()

async def assign_role(guild_id, member_id, code):
    async with await create_session() as session:
        guild = bot.get_guild(int(guild_id))
        if guild is None:
            print(f"Guild with ID {guild_id} not found.")
            return

        await _assign_role(guild, member_id, code, session)

async def _assign_role(guild, member_id, code, session):
    try:
        member = await guild.fetch_member(int(member_id))
    except discord.NotFound:
        print(f"Member with ID {member_id} not found in guild {guild.name}.")
        return

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'scope': 'identify guilds.join'
    }

    async with session.post('https://discord.com/api/oauth2/token', data=data) as resp:
        token_data = await resp.json()

    access_token = token_data['access_token']

    role = guild.get_role(role_id)
    if role is None:
        print(f"Role with ID {role_id} not found in guild {guild.name}.")
        return

    await member.add_roles(role)
    print(f"Role {role.name} has been assigned to {member.display_name}.")

    log_channel = guild.get_channel(log_channel_id)
    if log_channel:
        await log_channel.send(f"Role {role.name} has been assigned to {member.mention}.")

async def callback(request):
    code = request.query.get('code')
    state = request.query.get('state')

    if state not in oauth_states:
        return web.Response(text="Invalid OAuth2 state.", status=400)

    guild_id, member_id = oauth_states[state]

    del oauth_states[state]

    await assign_role(guild_id, member_id, code)

    redirect_url = "https://capped-uwu.github.io/GuardVerifyPage/"

    raise web.HTTPFound(location=redirect_url)

async def root_handler(request):
    return web.Response(text="uptimerobot")

async def run_bot_and_server():
    app = web.Application()
    app.router.add_get('/callback', callback)
    app.router.add_get('/', root_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner)
    await site.start()

    await bot.start(TOKEN)

asyncio.run(run_bot_and_server())
