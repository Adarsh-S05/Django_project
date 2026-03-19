import random
from django.core.management.base import BaseCommand
from players.models import Player, Team, Ground, BattingInnings, BowlingInnings


class Command(BaseCommand):
    help = "Seed the database with 50+ real cricket players, teams, grounds, and sample innings data"

    def handle(self, *args, **kwargs):
        self.stdout.write("🏏 Seeding cricket data...")

        # Clear existing data
        BattingInnings.objects.all().delete()
        BowlingInnings.objects.all().delete()
        Player.objects.all().delete()
        Team.objects.all().delete()
        Ground.objects.all().delete()

        # ---- TEAMS ----
        teams_data = [
            ('Mumbai Indians', 'MI', '#004BA0', True),
            ('Chennai Super Kings', 'CSK', '#FCCA06', True),
            ('Royal Challengers Bengaluru', 'RCB', '#EC1C24', True),
            ('Kolkata Knight Riders', 'KKR', '#3A225D', True),
            ('Delhi Capitals', 'DC', '#004C93', True),
            ('Rajasthan Royals', 'RR', '#EA1A85', True),
            ('Sunrisers Hyderabad', 'SRH', '#FF822A', True),
            ('Punjab Kings', 'PBKS', '#ED1B24', True),
            ('Gujarat Titans', 'GT', '#1C1C1C', True),
            ('Lucknow Super Giants', 'LSG', '#A72056', True),
            # International teams
            ('India', 'IND', '#0066B3', False),
            ('Australia', 'AUS', '#FFD700', False),
            ('England', 'ENG', '#002147', False),
            ('Pakistan', 'PAK', '#01411C', False),
            ('South Africa', 'SA', '#007A4D', False),
            ('New Zealand', 'NZ', '#000000', False),
            ('West Indies', 'WI', '#7B0041', False),
            ('Sri Lanka', 'SL', '#0D1E71', False),
            ('Bangladesh', 'BAN', '#006A4E', False),
            ('Afghanistan', 'AFG', '#000000', False),
        ]
        teams = {}
        for name, short, color, is_ipl in teams_data:
            t = Team.objects.create(name=name, short_name=short, logo_color=color, is_ipl_team=is_ipl)
            teams[short] = t
        self.stdout.write(f"  ✅ Created {len(teams)} teams")

        # ---- GROUNDS ----
        grounds_data = [
            ('Wankhede Stadium', 'Mumbai', 'India'),
            ('M. A. Chidambaram Stadium', 'Chennai', 'India'),
            ('M. Chinnaswamy Stadium', 'Bengaluru', 'India'),
            ('Eden Gardens', 'Kolkata', 'India'),
            ('Arun Jaitley Stadium', 'Delhi', 'India'),
            ('Sawai Mansingh Stadium', 'Jaipur', 'India'),
            ('Rajiv Gandhi Intl Cricket Stadium', 'Hyderabad', 'India'),
            ('IS Bindra Stadium', 'Mohali', 'India'),
            ('Narendra Modi Stadium', 'Ahmedabad', 'India'),
            ('Ekana Cricket Stadium', 'Lucknow', 'India'),
            ('DY Patil Stadium', 'Navi Mumbai', 'India'),
            ('Brabourne Stadium', 'Mumbai', 'India'),
            ('Melbourne Cricket Ground', 'Melbourne', 'Australia'),
            ('Sydney Cricket Ground', 'Sydney', 'Australia'),
            ("Lord's Cricket Ground", 'London', 'England'),
            ('The Oval', 'London', 'England'),
            ('Dubai Intl Cricket Stadium', 'Dubai', 'UAE'),
            ('Sharjah Cricket Stadium', 'Sharjah', 'UAE'),
        ]
        grounds = []
        for name, city, country in grounds_data:
            g = Ground.objects.create(name=name, city=city, country=country)
            grounds.append(g)
        self.stdout.write(f"  ✅ Created {len(grounds)} grounds")

        # ---- PLAYERS ----
        players_data = [
            # (name, country, is_overseas, role, batting_style, bowling_style, ipl_team_short, bio,
            #  matches, runs, wickets, bat_avg, bowl_avg, sr, econ, high, best_bowl, 100s, 50s, catches, stumpings)
            ('Virat Kohli', 'India', False, 'Batsman', 'Right-hand bat', 'Right-arm medium', 'RCB',
             'One of the greatest batsmen in cricket history. Known for his aggressive batting and chase master abilities.',
             237, 7263, 4, 37.25, 0, 130.02, 0, 113, '1/13', 7, 50, 109, 0),

            ('Rohit Sharma', 'India', False, 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 'MI',
             'The Hitman. Captain of MI with record 5 IPL titles. Known for effortless pull shots and big scores.',
             243, 6211, 15, 29.05, 0, 130.39, 0, 109, '1/8', 2, 42, 101, 0),

            ('Jasprit Bumrah', 'India', False, 'Bowler', 'Right-hand bat', 'Right-arm fast', 'MI',
             'Premier fast bowler with unorthodox action. Deadly yorkers and miserly death bowling specialist.',
             120, 56, 145, 5.6, 23.64, 69.14, 7.39, 16, '5/10', 0, 0, 20, 0),

            ('MS Dhoni', 'India', False, 'WK-Batsman', 'Right-hand bat', 'Right-arm medium', 'CSK',
             'Captain Cool. Greatest finisher in IPL history. Led CSK to 5 IPL titles.',
             264, 5243, 0, 38.09, 0, 135.2, 0, 84, '0/0', 0, 24, 132, 40),

            ('AB de Villiers', 'South Africa', True, 'Batsman', 'Right-hand bat', 'Right-arm medium', 'RCB',
             'Mr. 360. One of the most innovative batsmen ever. Could hit any ball to any part of the ground.',
             184, 5162, 12, 39.71, 0, 151.69, 0, 133, '2/3', 3, 40, 99, 0),

            ('Sunil Narine', 'West Indies', True, 'All-Rounder', 'Left-hand bat', 'Right-arm offbreak', 'KKR',
             'Mystery spinner turned explosive opener. KKR legend with devastating carrom ball.',
             177, 1640, 168, 14.29, 24.83, 162.73, 6.67, 109, '5/19', 1, 2, 44, 0),

            ('Rashid Khan', 'Afghanistan', True, 'Bowler', 'Right-hand bat', 'Right-arm legbreak', 'GT',
             'Best T20 leg-spinner in the world. Incredibly consistent with a lethal googly.',
             109, 362, 130, 9.28, 20.36, 128.37, 6.33, 34, '4/24', 0, 0, 41, 0),

            ('Pat Cummins', 'Australia', True, 'Bowler', 'Right-hand bat', 'Right-arm fast', 'SRH',
             'Australian captain and premium fast bowler. Smart bowler with great control.',
             50, 213, 56, 10.65, 27.85, 130.67, 8.23, 29, '4/34', 0, 0, 14, 0),

            ('David Warner', 'Australia', True, 'Batsman', 'Left-hand bat', 'Right-arm legbreak', 'DC',
             'Pocket dynamo. SRH legend and devastating opener with aggressive intent.',
             184, 6565, 2, 41.2, 0, 139.96, 0, 126, '1/7', 4, 55, 91, 0),

            ('Jos Buttler', 'England', True, 'WK-Batsman', 'Right-hand bat', 'N/A', 'RR',
             'Explosive keeper-batsman. Scored 4 centuries in IPL 2022. Rajasthan Royals captain.',
             89, 3399, 0, 38.18, 0, 149.71, 0, 124, '0/0', 4, 22, 35, 12),

            ('Ravindra Jadeja', 'India', False, 'All-Rounder', 'Left-hand bat', 'Slow left-arm orthodox', 'CSK',
             'Sir Jadeja. Complete cricketer — electric fielder, reliable bat, and master spin bowler.',
             226, 2692, 152, 26.39, 28.41, 127.45, 7.59, 62, '5/16', 0, 9, 82, 0),

            ('Rishabh Pant', 'India', False, 'WK-Batsman', 'Left-hand bat', 'N/A', 'DC',
             'Fearless left-handed keeper-batsman. Young sensation with explosive power-hitting ability.',
             109, 3182, 0, 34.69, 0, 148.72, 0, 128, '0/0', 1, 17, 54, 13),

            ('Hardik Pandya', 'India', False, 'All-Rounder', 'Right-hand bat', 'Right-arm fast', 'MI',
             'Power-hitting all-rounder. Can change the game with bat and ball. Gujarat Titans\' title-winning captain.',
             131, 2340, 68, 27.88, 30.56, 147.49, 9.07, 91, '3/17', 0, 8, 42, 0),

            ('Yuzvendra Chahal', 'India', False, 'Bowler', 'Right-hand bat', 'Right-arm legbreak', 'RR',
             'India and RCB\'s leading leg-spinner. Holds the record for most wickets by an Indian in IPL.',
             145, 67, 187, 4.47, 22.49, 91.78, 7.58, 8, '5/40', 0, 0, 42, 0),

            ('Shubman Gill', 'India', False, 'Batsman', 'Right-hand bat', 'Right-arm medium', 'GT',
             'Elegant young batsman. Gujarat Titans captain with a classic batting technique.',
             82, 2755, 0, 35.32, 0, 133.17, 0, 129, '0/0', 4, 16, 34, 0),

            ('Faf du Plessis', 'South Africa', True, 'Batsman', 'Right-hand bat', 'Right-arm legbreak', 'RCB',
             'Experienced RCB captain. Gritty opener with impeccable timing and calm temperament.',
             145, 4571, 1, 34.37, 0, 133.24, 0, 96, '0/0', 0, 33, 74, 0),

            ('Kagiso Rabada', 'South Africa', True, 'Bowler', 'Left-hand bat', 'Right-arm fast', 'PBKS',
             'South African pace spearhead. Aggressive wicket-taking fast bowler with raw pace.',
             63, 103, 84, 6.87, 23.51, 87.29, 8.27, 15, '4/21', 0, 0, 14, 0),

            ('KL Rahul', 'India', False, 'WK-Batsman', 'Right-hand bat', 'N/A', 'LSG',
             'Stylish opener and keepr. Orange Cap winner with elegant batting.',
             132, 4683, 0, 45.46, 0, 134.61, 0, 132, '0/0', 4, 36, 47, 5),

            ('Ravichandran Ashwin', 'India', False, 'All-Rounder', 'Right-hand bat', 'Right-arm offbreak', 'RR',
             'Master off-spinner. One of the smartest cricketers. Innovator of the carrom ball.',
             193, 709, 180, 11.82, 26.89, 116.07, 6.89, 46, '4/34', 0, 0, 47, 0),

            ('Trent Boult', 'New Zealand', True, 'Bowler', 'Right-hand bat', 'Left-arm fast', 'RR',
             'Left-arm swing king. Lethal with the new ball and a powerplay specialist.',
             76, 92, 93, 5.11, 25.93, 96.84, 8.01, 14, '4/18', 0, 0, 16, 0),

            ('Sanju Samson', 'India', False, 'WK-Batsman', 'Right-hand bat', 'N/A', 'RR',
             'Flamboyant keeper-batsman. RR captain known for breathtaking sixes.',
             158, 4141, 0, 29.15, 0, 136.82, 0, 119, '0/0', 2, 24, 62, 20),

            ('Mohammed Shami', 'India', False, 'Bowler', 'Right-hand bat', 'Right-arm fast', 'GT',
             'Seam bowling veteran. Deadly with the new ball and at the death. GT and India spearhead.',
             101, 53, 109, 3.29, 26.03, 73.61, 8.42, 10, '4/20', 0, 0, 14, 0),

            ('Shreyas Iyer', 'India', False, 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 'KKR',
             'Middle-order maestro. KKR captain with excellent skills against spin.',
             115, 3127, 1, 31.59, 0, 125.78, 0, 96, '0/0', 0, 23, 53, 0),

            ('Andre Russell', 'West Indies', True, 'All-Rounder', 'Right-hand bat', 'Right-arm fast', 'KKR',
             'Dre Russ — the ultimate T20 muscle man. Fearsome hitter and handy fast bowler.',
             114, 2035, 89, 28.26, 25.23, 177.88, 9.19, 88, '3/19', 0, 8, 62, 0),

            ('Quinton de Kock', 'South Africa', True, 'WK-Batsman', 'Left-hand bat', 'N/A', 'LSG',
             'Explosive South African keeper-opener. Aggressive left-hander with brilliant power.',
             92, 2981, 0, 33.14, 0, 138.22, 0, 140, '0/0', 2, 18, 42, 7),

            ('Bhuvneshwar Kumar', 'India', False, 'Bowler', 'Right-hand bat', 'Right-arm medium', 'SRH',
             'Swing bowling master. Purple Cap winner with exceptional control in powerplay and death.',
             170, 327, 165, 7.43, 26.17, 98.2, 7.28, 25, '5/19', 0, 0, 30, 0),

            ('Suryakumar Yadav', 'India', False, 'Batsman', 'Right-hand bat', 'Right-arm medium', 'MI',
             'Mr. 360 of India. The best T20 batsman in the world with 360-degree shot-making ability.',
             136, 3778, 0, 32.38, 0, 147.63, 0, 103, '0/0', 1, 27, 56, 0),

            ('Glenn Maxwell', 'Australia', True, 'All-Rounder', 'Right-hand bat', 'Right-arm offbreak', 'RCB',
             'The Big Show. Match-winner with destructive hitting and handy off-spin.',
             116, 2458, 30, 24.09, 36.37, 155.74, 8.81, 95, '2/23', 0, 13, 50, 0),

            ('Ishan Kishan', 'India', False, 'WK-Batsman', 'Left-hand bat', 'N/A', 'MI',
             'Power-hitting young keeper-batsman. Explosive opener with brute force.',
             105, 2644, 0, 28.59, 0, 136.3, 0, 99, '0/0', 0, 19, 44, 9),

            ('Mohammed Siraj', 'India', False, 'Bowler', 'Right-hand bat', 'Right-arm fast', 'RCB',
             'Yo Siraj! Rising pace star of Indian cricket. RCB\'s strike bowler with searing pace.',
             83, 32, 72, 3.2, 29.38, 52.46, 8.67, 7, '4/21', 0, 0, 10, 0),

            ('Axar Patel', 'India', False, 'All-Rounder', 'Left-hand bat', 'Slow left-arm orthodox', 'DC',
             'Left-arm spin all-rounder. Reliable with bat and ball, and a gun fielder.',
             118, 1220, 105, 15.64, 28.34, 131.18, 7.26, 65, '3/21', 0, 2, 33, 0),

            ('Mitchell Starc', 'Australia', True, 'Bowler', 'Left-hand bat', 'Left-arm fast', 'KKR',
             'Left-arm thunderbolt. One of the fastest bowlers in the world with devastating yorkers.',
             26, 43, 34, 7.17, 21.88, 81.13, 7.82, 13, '3/24', 0, 0, 5, 0),

            ('Kuldeep Yadav', 'India', False, 'Bowler', 'Left-hand bat', 'Left-arm chinaman', 'DC',
             'Rare left-arm wrist spinner. Talented wicket-taker with sharp turn and guile.',
             75, 75, 72, 5.0, 27.32, 91.46, 8.06, 12, '4/20', 0, 0, 18, 0),

            ('Devon Conway', 'New Zealand', True, 'Batsman', 'Left-hand bat', 'Right-arm offbreak', 'CSK',
             'Technically sound Kiwi batsman. Consistent run-scorer and superb fielder.',
             34, 1167, 0, 35.36, 0, 136.52, 0, 92, '0/0', 0, 10, 16, 0),

            ('Ruturaj Gaikwad', 'India', False, 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 'CSK',
             'CSK\'s young prince. Orange Cap winner with classy strokeplay and temperament.',
             54, 2035, 0, 39.13, 0, 131.07, 0, 108, '0/0', 2, 15, 22, 0),

            ('Yashasvi Jaiswal', 'India', False, 'Batsman', 'Left-hand bat', 'Right-arm legbreak', 'RR',
             'Young prodigy. Left-handed explosive opener for Rajasthan Royals with incredible talent.',
             42, 1632, 0, 39.8, 0, 163.69, 0, 124, '0/0', 1, 12, 17, 0),

            ('Marcus Stoinis', 'Australia', True, 'All-Rounder', 'Right-hand bat', 'Right-arm medium', 'LSG',
             'Australian power-hitter and useful medium-pace bowler.',
             68, 1330, 30, 23.33, 34.3, 139.16, 8.75, 89, '2/23', 0, 5, 29, 0),

            ('Rahul Tripathi', 'India', False, 'Batsman', 'Right-hand bat', 'Right-arm legbreak', 'CSK',
             'Consistent IPL performer. Elegant stroke player with good game awareness.',
             82, 2220, 0, 28.46, 0, 140.23, 0, 93, '0/0', 0, 16, 38, 0),

            ('Deepak Chahar', 'India', False, 'Bowler', 'Right-hand bat', 'Right-arm medium', 'CSK',
             'Swing bowling specialist. Deadly with the new ball in powerplay overs.',
             78, 193, 67, 10.16, 28.42, 109.66, 7.8, 39, '4/13', 0, 0, 15, 0),

            ('Nicholas Pooran', 'West Indies', True, 'WK-Batsman', 'Left-hand bat', 'N/A', 'LSG',
             'Caribbean power-hitter. Explosive keeper-batsman with ability to clear any boundary.',
             72, 1438, 0, 23.57, 0, 151.79, 0, 77, '0/0', 0, 6, 22, 4),

            ('Rinku Singh', 'India', False, 'Batsman', 'Left-hand bat', 'N/A', 'KKR',
             'King of last-over finishes. KKR hero who hit 5 sixes in an over to win a match.',
             48, 1197, 0, 34.2, 0, 149.44, 0, 67, '0/0', 0, 7, 24, 0),

            ('Harshal Patel', 'India', False, 'Bowler', 'Right-hand bat', 'Right-arm medium', 'PBKS',
             'Purple Cap winner with record 32 wickets in a season. Master of slower balls.',
             106, 336, 117, 10.18, 24.28, 117.89, 8.61, 36, '5/27', 0, 0, 25, 0),

            ('Shimron Hetmyer', 'West Indies', True, 'Batsman', 'Left-hand bat', 'N/A', 'RR',
             'Caribbean six-hitting machine. Power finisher in the lower middle order.',
             58, 1083, 0, 30.08, 0, 156.49, 0, 59, '0/0', 0, 3, 25, 0),

            ('Prithvi Shaw', 'India', False, 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 'DC',
             'Fearless opener with attacking mindset. Youngest Indian to score a Test century on debut.',
             60, 1588, 0, 22.97, 0, 147.41, 0, 99, '0/0', 0, 10, 21, 0),

            ('Sam Curran', 'England', True, 'All-Rounder', 'Left-hand bat', 'Left-arm medium', 'PBKS',
             'Young English all-rounder. Record IPL auction buy. Left-arm skilled pace bowling.',
             51, 490, 52, 14.85, 27.12, 133.88, 8.63, 55, '4/11', 0, 1, 19, 0),

            ('Rahul Chahar', 'India', False, 'Bowler', 'Right-hand bat', 'Right-arm legbreak', 'PBKS',
             'Young leg-spinner with sharp googly. Previously MI\'s lead spinner.',
             65, 22, 55, 2.75, 28.51, 51.16, 7.73, 5, '4/27', 0, 0, 17, 0),

            ('Arshdeep Singh', 'India', False, 'Bowler', 'Left-hand bat', 'Left-arm fast', 'PBKS',
             'Death overs specialist. Left-arm pacer with brilliant yorker execution.',
             75, 18, 76, 2.57, 25.01, 51.43, 8.89, 5, '5/32', 0, 0, 11, 0),

            ('Devdutt Padikkal', 'India', False, 'Batsman', 'Left-hand bat', 'N/A', 'RCB',
             'Elegant left-handed opener. Scored a century in his debut IPL season.',
             58, 1597, 0, 27.53, 0, 128.35, 0, 101, '0/0', 1, 10, 26, 0),

            ('Wriddhiman Saha', 'India', False, 'WK-Batsman', 'Right-hand bat', 'N/A', 'GT',
             'Experienced wicket-keeper. Known for razor-sharp glovework behind the stumps.',
             170, 2427, 0, 22.08, 0, 127.04, 0, 115, '0/0', 1, 6, 92, 32),

            ('Shardul Thakur', 'India', False, 'All-Rounder', 'Right-hand bat', 'Right-arm medium', 'CSK',
             'Lord Shardul. Medium pace all-rounder who can bowl crucial spells and hit lusty blows.',
             80, 352, 67, 11.73, 29.49, 131.34, 8.92, 36, '3/28', 0, 0, 22, 0),

            ('Travis Head', 'Australia', True, 'Batsman', 'Left-hand bat', 'Right-arm offbreak', 'SRH',
             'Aggressive Australian top-order batsman. Known for big scores in pressure situations.',
             23, 835, 0, 36.3, 0, 153.49, 0, 102, '0/0', 1, 6, 8, 0),
        ]

        ipl_teams_map = {short: t for short, t in teams.items() if len(short) <= 4}

        created_players = []
        for p in players_data:
            (name, country, overseas, role, bat_style, bowl_style, ipl_short, bio,
             matches, runs, wickets, bat_avg, bowl_avg, sr, econ, high, best_bowl,
             centuries, fifties, catches, stumpings) = p

            player = Player.objects.create(
                name=name,
                country=country,
                is_overseas=overseas,
                role=role,
                batting_style=bat_style,
                bowling_style=bowl_style,
                ipl_team=teams.get(ipl_short),
                bio=bio,
                total_matches=matches,
                total_runs=runs,
                total_wickets=wickets,
                batting_avg=bat_avg,
                bowling_avg=bowl_avg,
                strike_rate=sr,
                economy_rate=econ,
                highest_score=high,
                best_bowling=best_bowl,
                centuries=centuries,
                half_centuries=fifties,
                catches=catches,
                stumpings=stumpings,
            )
            created_players.append(player)

        self.stdout.write(f"  ✅ Created {len(created_players)} players")

        # ---- GENERATE INNINGS DATA ----
        self.stdout.write("  ⏳ Generating innings data...")
        ipl_team_objs = [t for t in teams.values() if t.is_ipl_team]
        indian_grounds = [g for g in grounds if g.country == 'India']
        years = list(range(2018, 2026))

        batting_innings_batch = []
        bowling_innings_batch = []

        for player in created_players:
            # Generate batting innings for batsmen and all-rounders
            if player.role in ('Batsman', 'All-Rounder', 'WK-Batsman'):
                num_innings = random.randint(20, 60)
                for _ in range(num_innings):
                    year = random.choice(years)
                    opponent = random.choice(ipl_team_objs)
                    ground = random.choice(indian_grounds)
                    phase = random.choice(['powerplay', 'middle', 'death'])

                    # Generate realistic runs based on player caliber
                    base_avg = player.batting_avg if player.batting_avg > 0 else 25
                    runs = max(0, int(random.gauss(base_avg * 0.8, base_avg * 0.6)))
                    balls = max(1, int(runs / (player.strike_rate / 100))) if player.strike_rate > 0 else max(1, random.randint(5, 30))
                    fours = random.randint(0, min(runs // 4, 12))
                    sixes = random.randint(0, min(runs // 6, 8))
                    sr = (runs / balls * 100) if balls > 0 else 0

                    batting_innings_batch.append(BattingInnings(
                        player=player,
                        opponent=opponent,
                        ground=ground,
                        year=year,
                        runs=runs,
                        balls_faced=balls,
                        fours=fours,
                        sixes=sixes,
                        strike_rate=round(sr, 2),
                        is_not_out=random.random() < 0.25,
                        phase=phase,
                    ))

            # Generate bowling innings for bowlers and all-rounders
            if player.role in ('Bowler', 'All-Rounder'):
                num_innings = random.randint(20, 50)
                for _ in range(num_innings):
                    year = random.choice(years)
                    opponent = random.choice(ipl_team_objs)
                    ground = random.choice(indian_grounds)
                    phase = random.choice(['powerplay', 'middle', 'death'])

                    overs = round(random.uniform(1, 4), 1)
                    base_econ = player.economy_rate if player.economy_rate > 0 else 8.0
                    runs_conceded = max(0, int(overs * random.gauss(base_econ, 2)))
                    wickets = random.choices([0, 1, 2, 3, 4], weights=[40, 30, 20, 7, 3])[0]
                    econ = (runs_conceded / overs) if overs > 0 else 0

                    bowling_innings_batch.append(BowlingInnings(
                        player=player,
                        opponent=opponent,
                        ground=ground,
                        year=year,
                        overs=overs,
                        maidens=1 if random.random() < 0.05 else 0,
                        runs_conceded=runs_conceded,
                        wickets=wickets,
                        economy=round(econ, 2),
                        phase=phase,
                    ))

        BattingInnings.objects.bulk_create(batting_innings_batch)
        BowlingInnings.objects.bulk_create(bowling_innings_batch)

        self.stdout.write(f"  ✅ Created {len(batting_innings_batch)} batting innings")
        self.stdout.write(f"  ✅ Created {len(bowling_innings_batch)} bowling innings")
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Seeding complete! {len(created_players)} players with full stats."))
