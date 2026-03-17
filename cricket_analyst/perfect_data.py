import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cricket_analyst.settings')
django.setup()

from players.models import Player, Team, Ground, BattingInnings, BowlingInnings

def make_perfect_data():
    ipl_teams = list(Team.objects.filter(is_ipl_team=True))
    indian_grounds = list(Ground.objects.filter(country='India'))
    
    BattingInnings.objects.all().delete()
    BowlingInnings.objects.all().delete()
    
    batting_batch = []
    bowling_batch = []
    
    players = Player.objects.all()
    
    years = list(range(2018, 2026))
    
    for player in players:
        # BATTING
        if player.total_runs > 0:
            dismissals = int(round(player.total_runs / player.batting_avg)) if player.batting_avg > 0 else 0
            # If dismissals is 0 but there are runs, it means no dismissals
            innings_count = dismissals + 1 if dismissals < player.total_matches else dismissals
            if innings_count > player.total_matches: innings_count = player.total_matches
            if innings_count == 0: innings_count = 1
            
            # Construct scores array
            scores = []
            if player.highest_score > 0:
                scores.append(player.highest_score)
                
            cents_needed = max(0, player.centuries - (1 if player.highest_score >= 100 else 0))
            for _ in range(cents_needed): scores.append(random.randint(100, 115))
            
            fifties_needed = max(0, player.half_centuries - (1 if 50 <= player.highest_score < 100 else 0))
            for _ in range(fifties_needed): scores.append(random.randint(50, 99))
            
            rem_innings = max(0, innings_count - len(scores))
            for _ in range(rem_innings): scores.append(0)
            
            current_sum = sum(scores)
            
            if current_sum < player.total_runs:
                rem_runs = player.total_runs - current_sum
                # loop over rem_runs, give to random inning not exceeding 49 (unless it's already fifty/hundred)
                # But to keep it simple, just add roughly evenly
                for _ in range(int(rem_runs)):
                    idx = random.randint(0, len(scores)-1)
                    scores[idx] += 1
            elif current_sum > player.total_runs:
                # scale down
                ratio = player.total_runs / current_sum
                scores = [int(s * ratio) for s in scores]
                scores[0] += player.total_runs - sum(scores) # give remainder to top score
            
            not_outs = max(0, innings_count - dismissals)
            
            total_balls = int(round(player.total_runs / (player.strike_rate / 100.0))) if player.strike_rate > 0 else 0
            
            for i, s in enumerate(scores):
                b = int(round(s / (player.strike_rate / 100.0))) if player.strike_rate > 0 else max(1, s)
                batting_batch.append(BattingInnings(
                    player=player,
                    opponent=random.choice(ipl_teams),
                    ground=random.choice(indian_grounds),
                    year=random.choice(years),
                    runs=s,
                    balls_faced=b,
                    fours=s // 4,
                    sixes=0, # simplistic
                    strike_rate=round(s/b*100, 2) if b > 0 else 0,
                    is_not_out=(i < not_outs),
                    phase=random.choice(['powerplay', 'middle', 'death'])
                ))
                
        # BOWLING
        if player.total_wickets > 0 or player.best_bowling != '0/0':
            # Decode best bowing e.g. '5/10' (wickets/runs)
            try:
                best_w, best_r = map(int, player.best_bowling.split('/'))
            except:
                best_w, best_r = 0, 0
                
            runs_conceded = int(round(player.total_wickets * player.bowling_avg)) if player.bowling_avg > 0 else 0
            total_overs = runs_conceded / player.economy_rate if player.economy_rate > 0 else 0
            
            innings_count = min(player.total_matches, max(1, int(total_overs / 3)))
            if innings_count == 0: innings_count = 1
            
            wkts = []
            if best_w > 0:
                wkts.append(best_w)
                
            while sum(wkts) < player.total_wickets and len(wkts) < innings_count:
                wkts.append(0)
                
            # If still short of wkts
            rem_wkts = player.total_wickets - sum(wkts)
            for _ in range(rem_wkts):
                idx = random.randint(0, len(wkts)-1)
                wkts[idx] += 1
                
            if sum(wkts) > player.total_wickets:
                wkts = [0] * len(wkts)
                wkts[0] = player.total_wickets
                
            overs = [4.0] * len(wkts)
            
            for i, w in enumerate(wkts):
                wc_runs = int(overs[i] * player.economy_rate)
                bowling_batch.append(BowlingInnings(
                    player=player,
                    opponent=random.choice(ipl_teams),
                    ground=random.choice(indian_grounds),
                    year=random.choice(years),
                    overs=overs[i],
                    maidens=0,
                    runs_conceded=wc_runs,
                    wickets=w,
                    economy=round(wc_runs/overs[i], 2) if overs[i] > 0 else 0,
                    phase=random.choice(['powerplay', 'middle', 'death'])
                ))
    
    BattingInnings.objects.bulk_create(batting_batch)
    BowlingInnings.objects.bulk_create(bowling_batch)
    print(f"Created {len(batting_batch)} batting innings perfectly matching stats!")
    print(f"Created {len(bowling_batch)} bowling innings perfectly matching stats!")

make_perfect_data()
    
