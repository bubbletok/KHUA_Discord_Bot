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
      current_upcoming_contests = get_contests()
      await message.channel.send(current_upcoming_contests)

def get_contests():
   try:
       contests = contests_crawler.get_contests()
       if not contests:
           return "🏁 현재 진행중이거나 예정된 대회가 없습니다."

       response = "🏆 **Codeforces Contests**\n```\n"
       
       # 각 열의 너비 설정
       name_width = 40
       start_width = 25  # 시작 시간 열 너비 증가
       length_width = 10
       remaining_width = 20
       status_width = 15
       
       # 헤더 추가
       headers = (
           f"{'Name':<{name_width}}"
           f"{'Start':<{start_width}}"
           f"{'Length':<{length_width}}"
           f"{'Remaining':<{remaining_width}}"
           f"{'Status':<{status_width}}"
       )
       response += headers + "\n"
       response += "=" * (name_width + start_width + length_width + remaining_width + status_width) + "\n"

       for contest in contests:
           # 대회 이름 길이 제한
           name = contest.get('name', 'Unknown')[:name_width].ljust(name_width)
           
           # 시작 시간 포맷팅 (날짜 + 시간)
           full_time = contest.get('start_time', '').split()
           date = full_time[0]
           time = full_time[1][:5]  # HH:MM 형식으로 자르기
           
           if '2024-' in date:
               formatted_date = date.replace('2024-', '')
           else:
               formatted_date = date.replace('2025-', '')
               
           start = f"{formatted_date} {time}".ljust(start_width)
           
           # 진행 시간 포맷팅
           length = contest.get('duration', '').ljust(length_width)
           
           # 남은 시간 포맷팅
           remaining = contest.get('remaining_time', '').ljust(remaining_width)
           
           # 상태 표시 및 이모지 추가
           if contest.get('status') == 'ONGOING':
               status = "🔥 Running"
           else:
               status = "⏰ Before start"
           status = status.ljust(status_width)
           
           # 한 줄로 조합
           contest_info = f"{name}{start}{length}{remaining}{status}"
           response += contest_info + "\n"
       
       response += "```"
       
       # 푸터 추가
       response += "\n📢 **Commands:**"
       response += "\n`!대회` - 대회 목록 조회"
       response += "\n\n🔔 **Notice:**"
       response += "\n- 모든 시간은 한국 시간(KST) 기준입니다."
       response += "\n- 대회 시작 전에 미리 등록하는 것을 잊지 마세요!"
       
       return response

   except Exception as e:
       print(f"Error in get_contests: {str(e)}")
       return "❌ 대회 정보를 가져오는 중 오류가 발생했습니다."
    
# start the bot
client.run(TOKEN)