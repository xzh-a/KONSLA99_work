import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
from discord.utils import get

# 봇 설정: 기본 의도(intents)와 함께 봇 인스턴스를 생성합니다.
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

# 활성 주문 상태를 추적하는 딕셔너리
active_orders = {}

# '나중에 배차' 상태를 추적하는 딕셔너리
later_dispatch_users = {}

# 멤버간 역할 회수를 저장하는 딕셔너리

# 역할 초기화 함수
# 버튼을 눌러서 새로운 역할을 부여받을 떄 기존의 역할을 제거한다.
async def clear_roles(member):
    roles_to_clear = ['바로배차', '나중에 배차', '배차 됨','member']  # 초기화할 역할 이름 리스트
    for role_name in roles_to_clear:
        role = get(member.guild.roles, name=role_name)
        if role:
            await member.remove_roles(role)


# 봇이 준비되면 콘솔에 메시지를 출력합니다.
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# 완료증명 명령어: 사용자가 콜 완료를 증명할 때 사용합니다.
@bot.command(name='완료증명', help='콜 완료를 증명합니다.')
async def complete_call(ctx, member: discord.Member):
    await ctx.send(f'{member.name}의 콜이 완료되었습니다.')

############################################################################################################################################################
# 아래 내용은 버튼에 관한 내용
############################################################################################################################################################
class DispatchView(discord.ui.View):
    def __init__(self):
        super().__init__()

    # 바로 배차 버튼
    @discord.ui.button(label="바로배차", style=discord.ButtonStyle.green, custom_id="immediate_dispatch")
    async def handle_immediate_dispatch(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = interaction.user
        member_role = get(guild.roles, name="member")

        # "member" 역할이 있는지 먼저 확인하고 응답을 보냅니다.
        if member_role not in member.roles:
            await interaction.response.send_message(f"죄송합니다, {member.display_name}님. 이 버튼은 'member' 역할을 가진 사용자만 사용할 수 있습니다.", ephemeral=True)
            return
        else:
            # 역할 확인 후 바로 응답을 보냅니다.
            await interaction.response.send_message(f"{member.display_name}님, 배차 요청이 처리 중입니다.", ephemeral=True)
        
        # 역할 변경 및 추가 작업은 응답 후 비동기적으로 수행합니다.
        await clear_roles(member)  # 역할 초기화
        immediate_role = get(guild.roles, name="바로배차")
        dispatched_role = get(guild.roles, name="배차 됨")
        if immediate_role and dispatched_role:
            await member.add_roles(immediate_role, dispatched_role)
            #주문자가 주문 내역을 첨부 가능하도록 수정할 것
            call_order_details = "여기에 콜 주문 내역을 입력하세요."
            await member.send(call_order_details)
        else:
            await member.send("필요한 역할을 찾을 수 없습니다.")
            
    # 나중에 배차 버튼
    @discord.ui.button(label="나중에 배차", style=discord.ButtonStyle.red, custom_id="later_dispatch")
    async def handle_later_dispatch(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = interaction.user
        member_role = get(guild.roles, name="member")

        # "member" 역할이 있는지 먼저 확인하고 응답을 보냅니다.
        if member_role not in member.roles:
            await interaction.response.send_message(f"죄송합니다, {member.display_name}님. 이 버튼은 'member' 역할을 가진 사용자만 사용할 수 있습니다.", ephemeral=True)
            return
        else:
            # 역할 확인 후 바로 응답을 보냅니다.
            await interaction.response.send_message(f"{member.display_name}님, 나중에 배차 요청이 처리 중입니다.", ephemeral=True)
            later_dispatch_users[member.id] = True  # 사용자 상태 업데이트

        # 역할 변경 및 추가 작업은 응답 후 비동기적으로 수행합니다.
        await clear_roles(member)
        later_dispatch_role = get(guild.roles, name="나중에 배차")
        if later_dispatch_role:
            await member.add_roles(later_dispatch_role)
            # 3분 대기 후 추가 작업을 수행합니다.
            await asyncio.sleep(180)  # 3분 대기
            await clear_roles(member)
            if member_role:  # 'member' 역할이 아직 유효한 경우 다시 추가
                await member.add_roles(member_role)

    

############################################################################################################################################################
# 아래 내용은 관리자 명령어에 관한 내용
############################################################################################################################################################

# 주문 명령어는 역할이  Master등급인 경우에만 사용이 가능합니다.
# 해당 명령어가 실행 되는 경우 주문-배차 채널에 <나중에 배차>역할을 제외한 나머지 사용자에게 
# 버튼을 포함하여 메시지를 보냅니다.
                                    
@bot.command(name='주문')
# 주문 명령어를 실행시 콜 내용을 우선적으로 게시할 수 있도록한다.
async def order(ctx):
    master_role = discord.utils.get(ctx.guild.roles, name="Master")
    later_dispatch_role = discord.utils.get(ctx.guild.roles, name="나중에 배차")

    if master_role in ctx.author.roles:
        channel = discord.utils.get(ctx.guild.text_channels, name="주문-배차")
        if channel:
            # '나중에 배차' 역할이 있는 사용자, 봇, 'Master' 역할 사용자를 제외하고
            # 모든 사용자에게 채널에 메시지를 한 번만 게시합니다.
            excluded_roles = [later_dispatch_role, master_role]
            # 해당 역할을 가지고 있지 않은 사용자에게만 메시지를 보냅니다.
            # 이 메시지는 채널에 일반적으로 게시되므로 모든 사람이 볼 수 있지만,
            # '나중에 배차' 역할을 가진 사람은 반응하지 못하도록 합니다.
            message_content = "배차를 선택해주세요:"
            view = DispatchView()  # 모든 사용자에 대해 동일한 View를 사용
            await channel.send(message_content, view=view)
            await ctx.send(f"주문 메시지가 {channel.mention} 채널에 게시되었습니다.")
            active_orders[ctx.guild.id] = True
        else:
            await ctx.send("'주문-배차' 채널을 찾을 수 없습니다.")
    else:
        await ctx.send("이 명령어는 'Master' 역할을 가진 사용자만 사용할 수 있습니다.")

        

############################################################################################################################################################
# 아래 내용은 유저 명령어에 관한 내용
############################################################################################################################################################
        
#바로배차 명령어
@bot.command(name='바로배차')
async def immediate_dispatch_command(ctx):
    # 활성 주문이 있는지 확인
    if ctx.guild and active_orders.get(ctx.guild.id):
        member = ctx.author
        await clear_roles(member)  # 역할 초기화
        immediate_role = get(ctx.guild.roles, name="바로배차")
        dispatched_role = get(ctx.guild.roles, name="배차 됨")
        if immediate_role and dispatched_role:
            await member.add_roles(immediate_role, dispatched_role)
            call_order_details = "여기에 콜 주문 내역을 입력하세요."
            await member.send(call_order_details)
            await ctx.send(f"{member.display_name}님, 배차 요청이 성공적으로 처리되었습니다.")
            # 주문 처리 완료 후, 활성 주문 상태 업데이트
            active_orders[ctx.guild.id] = False
        else:
            await ctx.send("필요한 역할을 찾을 수 없습니다.")
    else:
        await ctx.send("현재 활성 주문이 없습니다.")

#나중에 배차 명령어        
@bot.command(name='나중에 배차')
async def later_dispatch_command(ctx):
    if ctx.guild and ctx.author.id not in later_dispatch_users:
        member = ctx.author
        await clear_roles(member)  # 역할 초기화
        later_dispatch_role = get(ctx.guild.roles, name="나중에 배차")
        if later_dispatch_role:
            await member.add_roles(later_dispatch_role)
            await ctx.send(f"{member.display_name}님, 나중에 배차가 선택되었습니다. 3분 후에 다시 시도해 주세요.")
            later_dispatch_users[member.id] = True
            await asyncio.sleep(180)  # 3분 대기
            del later_dispatch_users[member.id]  # 딜레이 후 상태 제거
        else:
            await ctx.send("필요한 역할을 찾을 수 없습니다.")
    else:
        await ctx.send("이미 나중에 배차가 선택되었거나 진행 중입니다.")

# 배차 취소 명령어
@bot.command(name='배차 취소')
async def cancle_command(ctx):
    #여기 부터 수정하면 됩니다.

    if ctx.guild and ctx.author.id not in later_dispatch_users:
        member = ctx.author
        await clear_roles(member)  # 역할 초기화
        later_dispatch_role = get(ctx.guild.roles, name="나중에배차")
        if later_dispatch_role:
            await member.add_roles(later_dispatch_role)
            await ctx.send(f"{member.display_name}님, 나중에 배차가 선택되었습니다. 3분 후에 다시 시도해 주세요.")
            later_dispatch_users[member.id] = True
            await asyncio.sleep(180)  # 3분 대기
            del later_dispatch_users[member.id]  # 딜레이 후 상태 제거
        else:
            await ctx.send("필요한 역할을 찾을 수 없습니다.")
    else:
        await ctx.send("이미 나중에 배차가 선택되었거나 진행 중입니다.")        
# 완료증명 명령어

###########################################################################################################
        
bot.run('MTIxNjY2NjI1MTY0NTAyNjM3NQ.G0pp_W.LLPaheYQ3vuieo9PAxsrzyW5_uTZ4UyWpTNFBc')

#https://discord.com/oauth2/authorize?client_id=1216666251645026375&permissions=8&scope=bot
#