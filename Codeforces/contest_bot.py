import os
import discord
from dotenv import load_dotenv
import codeforces_contests_crawler as contests_crawler

# load the environment variables
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)


@client.event
async def on_ready():
  print(f'We have logged in as {client.user.name}')

@client.event
async def on_message(message):
  if message.author == client.user:
      return 

  if message.content.startswith("!대회"):
    try:
        response = get_contests()
        if isinstance(response, str):
            await message.channel.send(response)
        else:
            await message.channel.send(embed=response)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        await message.channel.send("❌ 대회 정보를 가져오는 중 오류가 발생했습니다.")

def get_contests():
   try:
       contests = contests_crawler.get_contests()
       if not contests:
           return "🏁 현재 진행중이거나 예정된 대회가 없습니다."

       embed = discord.Embed(
           title="🏆 Upcoming Codeforces Contests",
           color=0x00ff00  # 초록색
       )
       
       for contest in contests:
           # 대회 정보 가져오기
           name = contest.get('name', 'Unknown')
           
           # 시작 시간 포맷팅
           full_time = contest.get('start_time', '').split()
           date = full_time[0]
           time = full_time[1][:5]  # HH:MM 형식으로 자르기
           
           if '2024-' in date:
               formatted_date = date.replace('2024-', '')
           else:
               formatted_date = date.replace('2025-', '')
           
           # 남은 시간
           remaining = contest.get('remaining_time', '')
           length = contest.get('duration', '')
           
           # 상태 표시 및 이모지 추가
           if contest.get('status') == 'ONGOING':
               status_emoji = "🔥"
               description = f"```Duration: {length}\nRemaining: {remaining}```"
           else:
               status_emoji = "⏰"
               description = f"```Start: {formatted_date} {time}\nDuration: {length}\nRemaining: {remaining}```"
           
           # 대회 정보를 필드로 추가
           embed.add_field(
               name=f"{status_emoji} {name}",
               value=description,
               inline=False
           )

       # 푸터 추가
       embed.set_footer(text="🕒 모든 시간은 한국 시간(KST) 기준입니다")
       
       return embed

   except Exception as e:
       print(f"Error in get_contests: {str(e)}")
       return "❌ 대회 정보를 가져오는 중 오류가 발생했습니다."
    
# start the bot
client.run(TOKEN)