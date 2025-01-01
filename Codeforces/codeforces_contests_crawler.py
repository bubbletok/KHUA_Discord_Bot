import requests
import json
from datetime import datetime, timedelta

def format_duration(seconds):
    # Convert seconds to hours and minutes
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"

def format_remaining_time(seconds):
   # Convert seconds to days, hours, minutes
   if seconds <= 0:
       return "Started"
   
   days = seconds // (24 * 3600)
   remaining = seconds % (24 * 3600)
   hours = remaining // 3600
   minutes = (remaining % 3600) // 60
   
   if days > 0:
       return f"{days}d {hours}h {minutes}m"
   elif hours > 0:
       return f"{hours}h {minutes}m"
   else:
       return f"{minutes}m"

def get_contests():
    # Call the API
    url = "http://codeforces.com/api/contest.list"
    response = requests.get(url)

    # Parse JSON response
    data = response.json()
    
    # Include current timestamp in filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if data['status'] == 'OK':
        contests = data['result']
        current_time = datetime.now().timestamp()

        # Filter for ongoing and upcoming contests
        active_contests = [c for c in contests if c['startTimeSeconds'] + c['durationSeconds'] > current_time]

        # Sort by start time
        active_contests.sort(key=lambda x: x['startTimeSeconds'])
        
        contests = []

        if active_contests:
            for contest in active_contests:
                start_time = datetime.fromtimestamp(contest['startTimeSeconds'])
                duration = format_duration(contest['durationSeconds'])

                # Calculate remaining time
                if contest['startTimeSeconds'] > current_time:
                    # Contest hasn't started yet
                    remaining_time = format_remaining_time(int(contest['startTimeSeconds'] - current_time))
                    status = "UPCOMING"
                else:
                    # Contest is ongoing
                    end_time = contest['startTimeSeconds'] + contest['durationSeconds']
                    remaining_time = format_remaining_time(int(end_time - current_time))
                    status = "ONGOING"

                contests.append({
                    "name": contest['name'],
                    "status": status,
                    "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "duration": duration,
                    "remaining_time": remaining_time
                })
        else:
            print("\nNo active or upcoming contests found.")
        return contests

if __name__ == "__main__":
    get_contests()