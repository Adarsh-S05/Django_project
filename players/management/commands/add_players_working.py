"""
WORKING VERSION - Matches your Player model exactly
Save as: cricket_analyst/players/management/commands/add_players_working.py
Run: python manage.py add_players_working
"""

from django.core.management.base import BaseCommand
from players.models import Player
import requests
from django.core.files.base import ContentFile
import time

class Command(BaseCommand):
    help = 'Add 50 top cricket players (matches your model)'

    def handle(self, *args, **kwargs):
        players = [
            # INDIA
            {'name': 'Virat Kohli', 'role': 'Batsman', 'country': 'India', 'total_matches': 295, 'total_runs': 13848, 'total_wickets': 4, 'batting_avg': 58.18, 'bowling_avg': 0, 'strike_rate': 93.54, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170661/virat-kohli.jpg'},
            {'name': 'Rohit Sharma', 'role': 'Batsman', 'country': 'India', 'total_matches': 262, 'total_runs': 10866, 'total_wickets': 8, 'batting_avg': 49.16, 'bowling_avg': 0, 'strike_rate': 90.30, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170942/rohit-sharma.jpg'},
            {'name': 'Jasprit Bumrah', 'role': 'Bowler', 'country': 'India', 'total_matches': 143, 'total_runs': 58, 'total_wickets': 181, 'batting_avg': 6.44, 'bowling_avg': 23.85, 'strike_rate': 125.00, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170658/jasprit-bumrah.jpg'},
            {'name': 'Hardik Pandya', 'role': 'All-Rounder', 'country': 'India', 'total_matches': 103, 'total_runs': 2050, 'total_wickets': 79, 'batting_avg': 29.28, 'bowling_avg': 35.44, 'strike_rate': 126.54, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170929/hardik-pandya.jpg'},
            {'name': 'KL Rahul', 'role': 'WK-Batsman', 'country': 'India', 'total_matches': 72, 'total_runs': 2863, 'total_wickets': 0, 'batting_avg': 45.28, 'bowling_avg': 0, 'strike_rate': 86.77, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170937/kl-rahul.jpg'},
            {'name': 'Ravindra Jadeja', 'role': 'All-Rounder', 'country': 'India', 'total_matches': 201, 'total_runs': 2756, 'total_wickets': 220, 'batting_avg': 32.97, 'bowling_avg': 36.50, 'strike_rate': 86.31, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170618/ravindra-jadeja.jpg'},
            {'name': 'Rishabh Pant', 'role': 'WK-Batsman', 'country': 'India', 'total_matches': 84, 'total_runs': 2838, 'total_wickets': 0, 'batting_avg': 44.34, 'bowling_avg': 0, 'strike_rate': 107.23, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170933/rishabh-pant.jpg'},
            {'name': 'Shubman Gill', 'role': 'Batsman', 'country': 'India', 'total_matches': 47, 'total_runs': 2145, 'total_wickets': 0, 'batting_avg': 51.31, 'bowling_avg': 0, 'strike_rate': 96.61, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226492/shubman-gill.jpg'},
            {'name': 'Mohammed Siraj', 'role': 'Bowler', 'country': 'India', 'total_matches': 47, 'total_runs': 89, 'total_wickets': 69, 'batting_avg': 8.08, 'bowling_avg': 32.52, 'strike_rate': 77.39, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226338/mohammed-siraj.jpg'},
            {'name': 'Mohammed Shami', 'role': 'Bowler', 'country': 'India', 'total_matches': 106, 'total_runs': 338, 'total_wickets': 195, 'batting_avg': 9.11, 'bowling_avg': 24.59, 'strike_rate': 78.48, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170931/mohammed-shami.jpg'},
            {'name': 'Suryakumar Yadav', 'role': 'Batsman', 'country': 'India', 'total_matches': 68, 'total_runs': 2340, 'total_wickets': 0, 'batting_avg': 43.33, 'bowling_avg': 0, 'strike_rate': 172.70, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226495/suryakumar-yadav.jpg'},
            
            # AUSTRALIA
            {'name': 'Steve Smith', 'role': 'Batsman', 'country': 'Australia', 'total_matches': 161, 'total_runs': 5966, 'total_wickets': 29, 'batting_avg': 44.89, 'bowling_avg': 47.58, 'strike_rate': 89.24, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170624/steven-smith.jpg'},
            {'name': 'Pat Cummins', 'role': 'Bowler', 'country': 'Australia', 'total_matches': 120, 'total_runs': 668, 'total_wickets': 188, 'batting_avg': 13.91, 'bowling_avg': 27.02, 'strike_rate': 90.19, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170920/pat-cummins.jpg'},
            {'name': 'David Warner', 'role': 'Batsman', 'country': 'Australia', 'total_matches': 161, 'total_runs': 6932, 'total_wickets': 0, 'batting_avg': 45.30, 'bowling_avg': 0, 'strike_rate': 97.26, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170895/david-warner.jpg'},
            {'name': 'Mitchell Starc', 'role': 'Bowler', 'country': 'Australia', 'total_matches': 115, 'total_runs': 708, 'total_wickets': 241, 'batting_avg': 14.32, 'bowling_avg': 21.38, 'strike_rate': 91.61, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170625/mitchell-starc.jpg'},
            {'name': 'Glenn Maxwell', 'role': 'All-Rounder', 'country': 'Australia', 'total_matches': 141, 'total_runs': 4027, 'total_wickets': 76, 'batting_avg': 34.01, 'bowling_avg': 43.71, 'strike_rate': 126.07, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170896/glenn-maxwell.jpg'},
            {'name': 'Travis Head', 'role': 'Batsman', 'country': 'Australia', 'total_matches': 71, 'total_runs': 2552, 'total_wickets': 15, 'batting_avg': 40.51, 'bowling_avg': 47.73, 'strike_rate': 117.66, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226341/travis-head.jpg'},
            {'name': 'Josh Hazlewood', 'role': 'Bowler', 'country': 'Australia', 'total_matches': 71, 'total_runs': 148, 'total_wickets': 112, 'batting_avg': 7.03, 'bowling_avg': 26.81, 'strike_rate': 65.05, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170897/josh-hazlewood.jpg'},
            {'name': 'Adam Zampa', 'role': 'Bowler', 'country': 'Australia', 'total_matches': 90, 'total_runs': 235, 'total_wickets': 148, 'batting_avg': 8.39, 'bowling_avg': 29.24, 'strike_rate': 123.03, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170899/adam-zampa.jpg'},
            {'name': 'Marnus Labuschagne', 'role': 'Batsman', 'country': 'Australia', 'total_matches': 48, 'total_runs': 1546, 'total_wickets': 12, 'batting_avg': 39.64, 'bowling_avg': 46.08, 'strike_rate': 88.16, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226340/marnus-labuschagne.jpg'},
            {'name': 'Mitchell Marsh', 'role': 'All-Rounder', 'country': 'Australia', 'total_matches': 92, 'total_runs': 2265, 'total_wickets': 46, 'batting_avg': 29.80, 'bowling_avg': 40.43, 'strike_rate': 110.49, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170898/mitchell-marsh.jpg'},
            
            # ENGLAND
            {'name': 'Joe Root', 'role': 'Batsman', 'country': 'England', 'total_matches': 176, 'total_runs': 6843, 'total_wickets': 32, 'batting_avg': 47.55, 'bowling_avg': 44.31, 'strike_rate': 87.06, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170665/joe-root.jpg'},
            {'name': 'Ben Stokes', 'role': 'All-Rounder', 'country': 'England', 'total_matches': 126, 'total_runs': 3455, 'total_wickets': 78, 'batting_avg': 38.38, 'bowling_avg': 42.14, 'strike_rate': 95.72, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170628/ben-stokes.jpg'},
            {'name': 'Jos Buttler', 'role': 'WK-Batsman', 'country': 'England', 'total_matches': 183, 'total_runs': 5418, 'total_wickets': 0, 'batting_avg': 40.43, 'bowling_avg': 0, 'strike_rate': 119.90, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170630/jos-buttler.jpg'},
            {'name': 'Jofra Archer', 'role': 'Bowler', 'country': 'England', 'total_matches': 42, 'total_runs': 184, 'total_wickets': 66, 'batting_avg': 13.14, 'bowling_avg': 26.36, 'strike_rate': 116.45, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c171023/jofra-archer.jpg'},
            {'name': 'Mark Wood', 'role': 'Bowler', 'country': 'England', 'total_matches': 72, 'total_runs': 315, 'total_wickets': 109, 'batting_avg': 10.50, 'bowling_avg': 33.39, 'strike_rate': 111.70, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170632/mark-wood.jpg'},
            {'name': 'Harry Brook', 'role': 'Batsman', 'country': 'England', 'total_matches': 29, 'total_runs': 1134, 'total_wickets': 0, 'batting_avg': 54.00, 'bowling_avg': 0, 'strike_rate': 121.02, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c475548/harry-brook.jpg'},
            {'name': 'Jonny Bairstow', 'role': 'WK-Batsman', 'country': 'England', 'total_matches': 111, 'total_runs': 3498, 'total_wickets': 0, 'batting_avg': 47.28, 'bowling_avg': 0, 'strike_rate': 104.64, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170629/jonny-bairstow.jpg'},
            {'name': 'Sam Curran', 'role': 'All-Rounder', 'country': 'England', 'total_matches': 62, 'total_runs': 671, 'total_wickets': 82, 'batting_avg': 19.74, 'bowling_avg': 30.12, 'strike_rate': 117.89, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226345/sam-curran.jpg'},
            
            # PAKISTAN
            {'name': 'Babar Azam', 'role': 'Batsman', 'country': 'Pakistan', 'total_matches': 120, 'total_runs': 5729, 'total_wickets': 0, 'batting_avg': 56.72, 'bowling_avg': 0, 'strike_rate': 89.23, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170926/babar-azam.jpg'},
            {'name': 'Shaheen Afridi', 'role': 'Bowler', 'country': 'Pakistan', 'total_matches': 62, 'total_runs': 214, 'total_wickets': 119, 'batting_avg': 8.23, 'bowling_avg': 22.20, 'strike_rate': 85.60, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226334/shaheen-shah-afridi.jpg'},
            {'name': 'Mohammad Rizwan', 'role': 'WK-Batsman', 'country': 'Pakistan', 'total_matches': 82, 'total_runs': 3134, 'total_wickets': 0, 'batting_avg': 49.44, 'bowling_avg': 0, 'strike_rate': 86.79, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226298/mohammad-rizwan.jpg'},
            {'name': 'Haris Rauf', 'role': 'Bowler', 'country': 'Pakistan', 'total_matches': 66, 'total_runs': 122, 'total_wickets': 103, 'batting_avg': 7.18, 'bowling_avg': 27.28, 'strike_rate': 127.08, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226336/haris-rauf.jpg'},
            {'name': 'Fakhar Zaman', 'role': 'Batsman', 'country': 'Pakistan', 'total_matches': 77, 'total_runs': 3095, 'total_wickets': 0, 'batting_avg': 43.59, 'bowling_avg': 0, 'strike_rate': 95.07, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170923/fakhar-zaman.jpg'},
            
            # SOUTH AFRICA
            {'name': 'Quinton de Kock', 'role': 'WK-Batsman', 'country': 'South Africa', 'total_matches': 143, 'total_runs': 6425, 'total_wickets': 0, 'batting_avg': 44.62, 'bowling_avg': 0, 'strike_rate': 96.26, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170906/quinton-de-kock.jpg'},
            {'name': 'Kagiso Rabada', 'role': 'Bowler', 'country': 'South Africa', 'total_matches': 102, 'total_runs': 357, 'total_wickets': 165, 'batting_avg': 8.02, 'bowling_avg': 27.30, 'strike_rate': 94.44, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170635/kagiso-rabada.jpg'},
            {'name': 'Aiden Markram', 'role': 'Batsman', 'country': 'South Africa', 'total_matches': 70, 'total_runs': 2305, 'total_wickets': 15, 'batting_avg': 41.16, 'bowling_avg': 42.93, 'strike_rate': 91.18, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226350/aiden-markram.jpg'},
            {'name': 'David Miller', 'role': 'Batsman', 'country': 'South Africa', 'total_matches': 157, 'total_runs': 3832, 'total_wickets': 3, 'batting_avg': 38.70, 'bowling_avg': 0, 'strike_rate': 138.47, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170905/david-miller.jpg'},
            {'name': 'Heinrich Klaasen', 'role': 'WK-Batsman', 'country': 'South Africa', 'total_matches': 71, 'total_runs': 2186, 'total_wickets': 0, 'batting_avg': 43.72, 'bowling_avg': 0, 'strike_rate': 103.79, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226357/heinrich-klaasen.jpg'},
            
            # NEW ZEALAND
            {'name': 'Kane Williamson', 'role': 'Batsman', 'country': 'New Zealand', 'total_matches': 169, 'total_runs': 6951, 'total_wickets': 39, 'batting_avg': 47.95, 'bowling_avg': 46.71, 'strike_rate': 81.74, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170644/kane-williamson.jpg'},
            {'name': 'Trent Boult', 'role': 'Bowler', 'country': 'New Zealand', 'total_matches': 117, 'total_runs': 520, 'total_wickets': 202, 'batting_avg': 9.64, 'bowling_avg': 24.45, 'strike_rate': 92.85, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170645/trent-boult.jpg'},
            {'name': 'Devon Conway', 'role': 'WK-Batsman', 'country': 'New Zealand', 'total_matches': 56, 'total_runs': 2113, 'total_wickets': 0, 'batting_avg': 44.02, 'bowling_avg': 0, 'strike_rate': 88.40, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c475581/devon-conway.jpg'},
            {'name': 'Lockie Ferguson', 'role': 'Bowler', 'country': 'New Zealand', 'total_matches': 57, 'total_runs': 156, 'total_wickets': 93, 'batting_avg': 7.63, 'bowling_avg': 26.51, 'strike_rate': 107.59, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226361/lockie-ferguson.jpg'},
            {'name': 'Daryl Mitchell', 'role': 'All-Rounder', 'country': 'New Zealand', 'total_matches': 52, 'total_runs': 1475, 'total_wickets': 25, 'batting_avg': 37.82, 'bowling_avg': 38.08, 'strike_rate': 111.06, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226360/daryl-mitchell.jpg'},
            
            # WEST INDIES
            {'name': 'Andre Russell', 'role': 'All-Rounder', 'country': 'West Indies', 'total_matches': 84, 'total_runs': 1919, 'total_wickets': 80, 'batting_avg': 23.51, 'bowling_avg': 31.92, 'strike_rate': 173.33, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170650/andre-russell.jpg'},
            {'name': 'Nicholas Pooran', 'role': 'WK-Batsman', 'country': 'West Indies', 'total_matches': 88, 'total_runs': 2229, 'total_wickets': 0, 'batting_avg': 28.58, 'bowling_avg': 0, 'strike_rate': 122.96, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226344/nicholas-pooran.jpg'},
            {'name': 'Jason Holder', 'role': 'All-Rounder', 'country': 'West Indies', 'total_matches': 149, 'total_runs': 1792, 'total_wickets': 169, 'batting_avg': 24.21, 'bowling_avg': 32.91, 'strike_rate': 100.39, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170648/jason-holder.jpg'},
            {'name': 'Rovman Powell', 'role': 'All-Rounder', 'country': 'West Indies', 'total_matches': 96, 'total_runs': 1723, 'total_wickets': 16, 'batting_avg': 27.46, 'bowling_avg': 43.81, 'strike_rate': 129.55, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226366/rovman-powell.jpg'},
            
            # SRI LANKA
            {'name': 'Wanindu Hasaranga', 'role': 'All-Rounder', 'country': 'Sri Lanka', 'total_matches': 54, 'total_runs': 658, 'total_wickets': 92, 'batting_avg': 16.88, 'bowling_avg': 16.77, 'strike_rate': 133.60, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226379/wanindu-hasaranga.jpg'},
            {'name': 'Pathum Nissanka', 'role': 'Batsman', 'country': 'Sri Lanka', 'total_matches': 50, 'total_runs': 1712, 'total_wickets': 0, 'batting_avg': 38.00, 'bowling_avg': 0, 'strike_rate': 83.37, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c475600/pathum-nissanka.jpg'},
            {'name': 'Kusal Mendis', 'role': 'WK-Batsman', 'country': 'Sri Lanka', 'total_matches': 179, 'total_runs': 4897, 'total_wickets': 0, 'batting_avg': 31.19, 'bowling_avg': 0, 'strike_rate': 82.86, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170653/kusal-mendis.jpg'},
            
            # BANGLADESH
            {'name': 'Shakib Al Hasan', 'role': 'All-Rounder', 'country': 'Bangladesh', 'total_matches': 247, 'total_runs': 7570, 'total_wickets': 317, 'batting_avg': 37.66, 'bowling_avg': 29.37, 'strike_rate': 83.05, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170904/shakib-al-hasan.jpg'},
            {'name': 'Mustafizur Rahman', 'role': 'Bowler', 'country': 'Bangladesh', 'total_matches': 89, 'total_runs': 92, 'total_wickets': 149, 'batting_avg': 5.11, 'bowling_avg': 23.27, 'strike_rate': 92.93, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c170913/mustafizur-rahman.jpg'},
            {'name': 'Litton Das', 'role': 'WK-Batsman', 'country': 'Bangladesh', 'total_matches': 67, 'total_runs': 2006, 'total_wickets': 0, 'batting_avg': 33.43, 'bowling_avg': 0, 'strike_rate': 84.15, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226371/litton-das.jpg'},
            
            # AFGHANISTAN
            {'name': 'Rashid Khan', 'role': 'All-Rounder', 'country': 'Afghanistan', 'total_matches': 98, 'total_runs': 1022, 'total_wickets': 170, 'batting_avg': 15.03, 'bowling_avg': 18.62, 'strike_rate': 128.70, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226373/rashid-khan.jpg'},
            {'name': 'Mohammad Nabi', 'role': 'All-Rounder', 'country': 'Afghanistan', 'total_matches': 153, 'total_runs': 3402, 'total_wickets': 161, 'batting_avg': 26.98, 'bowling_avg': 31.75, 'strike_rate': 108.28, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c226374/mohammad-nabi.jpg'},
            {'name': 'Rahmanullah Gurbaz', 'role': 'WK-Batsman', 'country': 'Afghanistan', 'total_matches': 68, 'total_runs': 2378, 'total_wickets': 0, 'batting_avg': 37.78, 'bowling_avg': 0, 'strike_rate': 125.08, 'image_url': 'https://www.cricbuzz.com/a/img/v1/152x152/i1/c475613/rahmanullah-gurbaz.jpg'},
        ]
        
        self.stdout.write(self.style.SUCCESS(f'Adding {len(players)} players...'))
        
        added = 0
        skipped = 0
        
        for i, data in enumerate(players, 1):
            name = data['name']
            
            if Player.objects.filter(name=name).exists():
                self.stdout.write(self.style.WARNING(f'{i}/{len(players)} ⊗ {name}'))
                skipped += 1
                continue
            
            image_url = data.pop('image_url', None)
            
            try:
                player = Player.objects.create(**data)
                
                if image_url:
                    try:
                        r = requests.get(image_url, timeout=10)
                        if r.status_code == 200:
                            player.photo_url = image_url
                            player.save()
                            self.stdout.write(self.style.SUCCESS(f'{i}/{len(players)} ✓ {name} + image'))
                        else:
                            self.stdout.write(self.style.SUCCESS(f'{i}/{len(players)} ✓ {name}'))
                        time.sleep(0.1)
                    except:
                        self.stdout.write(self.style.SUCCESS(f'{i}/{len(players)} ✓ {name}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'{i}/{len(players)} ✓ {name}'))
                
                added += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'{i}/{len(players)} ✗ {name}: {str(e)[:50]}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n{"="*50}'))
        self.stdout.write(self.style.SUCCESS(f'✅ DONE! Added: {added} | Skipped: {skipped}'))
        self.stdout.write(self.style.SUCCESS(f'{"="*50}'))
