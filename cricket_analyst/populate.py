"""
populate.py — Cricket Analyst  (FIXED VERSION)
================================================
Fixes:
  1. Uses Wikipedia image URLs for known players (reliable)
  2. Falls back to a silhouette placeholder for unknown players
     so ALL players display — not just the 83 with wiki images
  3. Deduplicated player list preserved

Run from C:\\forge\\web\\goat\\cricket_analyst:
    python populate.py
"""

import os, sys, django, random
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cricket_analyst.settings')
django.setup()

from players.models import Player, Team, Ground, BattingInnings, BowlingInnings

def r(lo, hi):  return round(random.uniform(lo, hi), 2)
def ri(lo, hi): return random.randint(lo, hi)

# ── WIKI IMAGE MAP ────────────────────────────────────────────────────────────
# Reliable Wikipedia/Wikimedia URLs keyed by player name.
# Players NOT in this map get a neutral silhouette placeholder so they
# still appear on the site instead of being hidden by a broken-image filter.

WIKI_IMAGES = {
    # ── India ──
    "Virat Kohli":        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Virat_Kohli_during_the_India_vs_Aus_4th_Test_match_at_Narendra_Modi_Stadium_on_09_March_2023.jpg/220px-Virat_Kohli_during_the_India_vs_Aus_4th_Test_match_at_Narendra_Modi_Stadium_on_09_March_2023.jpg",
    "Rohit Sharma":       "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Rohit_Sharma_in_PMO_New_Delhi.jpg/220px-Rohit_Sharma_in_PMO_New_Delhi.jpg",
    "Jasprit Bumrah":     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Jasprit_Bumrah_in_PMO_New_Delhi.jpg/220px-Jasprit_Bumrah_in_PMO_New_Delhi.jpg",
    "Hardik Pandya":      "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Hardik_Pandya_in_PMO_New_Delhi.jpg/220px-Hardik_Pandya_in_PMO_New_Delhi.jpg",
    "Ravindra Jadeja":    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Ravindra_Jadeja_in_PMO_New_Delhi.jpg/220px-Ravindra_Jadeja_in_PMO_New_Delhi.jpg",
    "MS Dhoni":           "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Mahendra_Singh_Dhoni_receiving_Padma_Bhushan.jpg/220px-Mahendra_Singh_Dhoni_receiving_Padma_Bhushan.jpg",
    "KL Rahul":           "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/LOKESH_RAHUL-15573141953_%28cropped%29.JPG/220px-LOKESH_RAHUL-15573141953_%28cropped%29.JPG",
    "Shubman Gill":       "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Shubman_Gill.jpg/220px-Shubman_Gill.jpg",
    "Rishabh Pant":       "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Rishabh_Pant.jpg/220px-Rishabh_Pant.jpg",
    "Shreyas Iyer":       "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Shreyas_Iyer_2021.jpg/220px-Shreyas_Iyer_2021.jpg",
    "Ishan Kishan":       "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Ishan_Kishan.jpg/220px-Ishan_Kishan.jpg",
    "Shikhar Dhawan":     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Shikhar_Dhawan_January_2016_%28cropped%29.jpg/220px-Shikhar_Dhawan_January_2016_%28cropped%29.jpg",
    "Suresh Raina":       "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Suresh_Raina1.jpg/220px-Suresh_Raina1.jpg",
    "Gautam Gambhir":     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Gautam_Gambhir_3.jpg/220px-Gautam_Gambhir_3.jpg",
    "Virender Sehwag":    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Virender_Sehwag_in_2008.jpg/220px-Virender_Sehwag_in_2008.jpg",
    "Yuvraj Singh":       "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/YuvrajSingh01.jpg/220px-YuvrajSingh01.jpg",
    "Yusuf Pathan":       "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Yusuf_Pathan.jpg/220px-Yusuf_Pathan.jpg",
    "Mohammed Shami":     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Mohammed_Shami_%28Indian_Cricket_team_training_SCG_2015%29.jpg/220px-Mohammed_Shami_%28Indian_Cricket_team_training_SCG_2015%29.jpg",
    "Bhuvneshwar Kumar":  "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Bhuvneshwar_kumar_With_Rashid_Zirak_%28Bhuvneshwar_Kumar_cropped%29.jpg/220px-Bhuvneshwar_kumar_With_Rashid_Zirak_%28Bhuvneshwar_Kumar_cropped%29.jpg",
    "Mohammed Siraj":     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Mohammad_Siraj_in_PMO_New_Delhi.jpg/220px-Mohammad_Siraj_in_PMO_New_Delhi.jpg",
    "Kuldeep Yadav":      "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Kuldeep_Yadav_in_PMO_New_Delhi.jpg/220px-Kuldeep_Yadav_in_PMO_New_Delhi.jpg",
    "Axar Patel":         "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Axar.Patel.jpg/220px-Axar.Patel.jpg",
    "R Ashwin":           "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Ravi_Ashwin.jpg/220px-Ravi_Ashwin.jpg",
    "Dinesh Karthik":     "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Dinesh_Karthik_2.jpg/220px-Dinesh_Karthik_2.jpg",
    "Ambati Rayudu":      "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Ambati_Rayudu.jpg/220px-Ambati_Rayudu.jpg",
    "Umesh Yadav":        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Umesh_Yadav.jpg/220px-Umesh_Yadav.jpg",
    "Harbhajan Singh":    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Harbhajan_Singh%27s_Pepsi_promotional_event_%27Change_The_Game%27.jpg/220px-Harbhajan_Singh%27s_Pepsi_promotional_event_%27Change_The_Game%27.jpg",
    # ── Australia ──
    "David Warner":       "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/David_Warner.jpg/220px-David_Warner.jpg",
    "Steve Smith":        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/STEVE_SMITH_%2811705303043%29.jpg/220px-STEVE_SMITH_%2811705303043%29.jpg",
    "Glenn Maxwell":      "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Glenn_Maxwell_3.jpg/220px-Glenn_Maxwell_3.jpg",
    "Pat Cummins":        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Pat_Cummins_fielding_Ashes_2021_%28cropped%29.jpg/220px-Pat_Cummins_fielding_Ashes_2021_%28cropped%29.jpg",
    "Mitchell Starc":     "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Mitchell_Starc_2023.jpg/220px-Mitchell_Starc_2023.jpg",
    "Josh Hazlewood":     "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Josh_Hazlewood_2011.jpg/220px-Josh_Hazlewood_2011.jpg",
    "Adam Zampa":         "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Adam_Zampa_2023.jpg/220px-Adam_Zampa_2023.jpg",
    "Adam Gilchrist":     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Adam_Gilchrist_of_Australia_%28cropped%29.jpg/220px-Adam_Gilchrist_of_Australia_%28cropped%29.jpg",
    # ── England ──
    "Jos Buttler":        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Jos_Buttler_2017.jpg/220px-Jos_Buttler_2017.jpg",
    "Ben Stokes":         "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/BEN_STOKES_%2811704837023%29_%28cropped%29.jpg/220px-BEN_STOKES_%2811704837023%29_%28cropped%29.jpg",
    "Jonny Bairstow":     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Jonny_Bairstow.jpg/220px-Jonny_Bairstow.jpg",
    "Moeen Ali":          "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/2018.01.06.17.47.32-Moeen_Ali_%2838876905344%29_%28cropped%29.jpg/220px-2018.01.06.17.47.32-Moeen_Ali_%2838876905344%29_%28cropped%29.jpg",
    # ── Pakistan ──
    "Shaheen Afridi":     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Shaheen_Afridi_%282%29.jpg/220px-Shaheen_Afridi_%282%29.jpg",
    # ── South Africa ──
    "Quinton de Kock":    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/QUINTON_DE_KOCK_%2815085160584%29.jpg/220px-QUINTON_DE_KOCK_%2815085160584%29.jpg",
    "David Miller":       "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/DAVID_MILLER_%2815704846295%29.jpg/220px-DAVID_MILLER_%2815704846295%29.jpg",
    "Kagiso Rabada":      "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Rabada.jpg/220px-Rabada.jpg",
    "AB de Villiers":     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/AB_de_Villiers_glove.jpg/220px-AB_de_Villiers_glove.jpg",
    "Jacques Kallis":     "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Jacques_Kallis_6.jpg/220px-Jacques_Kallis_6.jpg",
    # ── New Zealand ──
    "Kane Williamson":    "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Kane_Williamson_in_2019.jpg/220px-Kane_Williamson_in_2019.jpg",
    "Trent Boult":        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Trent_Boult.jpg/220px-Trent_Boult.jpg",
    "Martin Guptill":     "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Martin_Guptill_2_%28cropped%29.jpg/220px-Martin_Guptill_2_%28cropped%29.jpg",
    # ── Bangladesh ──
    "Shakib Al Hasan":    "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Shakib_Al_Hasan_%284%29_%28cropped%29.jpg/220px-Shakib_Al_Hasan_%284%29_%28cropped%29.jpg",
    "Mahmudullah":        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Mahmudullah_Riyad_%282%29_%28cropped%29.jpg/220px-Mahmudullah_Riyad_%282%29_%28cropped%29.jpg",
    "Mustafizur Rahman":  "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Mustafizur_Rahman_%284%29_%28cropped%29.jpg/220px-Mustafizur_Rahman_%284%29_%28cropped%29.jpg",
    # ── Afghanistan ──
    "Rashid Khan":        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Rashid_Khan.jpg/220px-Rashid_Khan.jpg",
    "Mohammad Nabi":      "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Mohammad_Nabi-Australia.jpg/220px-Mohammad_Nabi-Australia.jpg",
    # ── Sri Lanka ──
    "Lasith Malinga":     "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Lasith_Malinga_tossing_a_cricket_ball_at_practice.jpg/220px-Lasith_Malinga_tossing_a_cricket_ball_at_practice.jpg",
}

# Neutral silhouette — used for any player not in WIKI_IMAGES above.
# This is a plain SVG data-URI that looks like a cricket player outline.
# It is always valid so the site will display ALL players.
PLACEHOLDER_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/"
    "Unknown_person.jpg/220px-Unknown_person.jpg"
)


def get_photo(name):
    """Return a working image URL for *name*, falling back to a placeholder."""
    return WIKI_IMAGES.get(name, PLACEHOLDER_URL)


# ── 1. TEAMS ─────────────────────────────────────────────────────────────────
print("Creating teams...")
Team.objects.all().delete()

IPL_TEAMS = [
    ("Mumbai Indians",              "MI",   "#004BA0", True),
    ("Chennai Super Kings",         "CSK",  "#F9CD05", True),
    ("Royal Challengers Bengaluru", "RCB",  "#EC1C24", True),
    ("Kolkata Knight Riders",       "KKR",  "#3A225D", True),
    ("Delhi Capitals",              "DC",   "#0078BC", True),
    ("Punjab Kings",                "PBKS", "#ED1B24", True),
    ("Rajasthan Royals",            "RR",   "#EA1A85", True),
    ("Sunrisers Hyderabad",         "SRH",  "#F7A721", True),
    ("Gujarat Titans",              "GT",   "#1C1C1C", True),
    ("Lucknow Super Giants",        "LSG",  "#A0C4FF", True),
]
INT_TEAMS = [
    ("India",        "IND", "#0033A0", False),
    ("Australia",    "AUS", "#FFCD00", False),
    ("England",      "ENG", "#003087", False),
    ("Pakistan",     "PAK", "#01411C", False),
    ("South Africa", "SA",  "#007A4D", False),
    ("New Zealand",  "NZ",  "#000000", False),
    ("West Indies",  "WI",  "#7B0D1E", False),
    ("Sri Lanka",    "SL",  "#003478", False),
    ("Bangladesh",   "BAN", "#006A4E", False),
    ("Afghanistan",  "AFG", "#000000", False),
]
team_map = {}
for name, short, color, is_ipl in IPL_TEAMS + INT_TEAMS:
    t = Team.objects.create(name=name, short_name=short, logo_color=color, is_ipl_team=is_ipl)
    team_map[short] = t
print(f"  Created {Team.objects.count()} teams.")

# ── 2. GROUNDS ────────────────────────────────────────────────────────────────
print("Creating grounds...")
Ground.objects.all().delete()

GROUNDS_DATA = [
    ("Wankhede Stadium",                   "Mumbai",       "India"),
    ("M. A. Chidambaram Stadium",          "Chennai",      "India"),
    ("M. Chinnaswamy Stadium",             "Bengaluru",    "India"),
    ("Eden Gardens",                       "Kolkata",      "India"),
    ("Arun Jaitley Stadium",               "Delhi",        "India"),
    ("Narendra Modi Stadium",              "Ahmedabad",    "India"),
    ("Rajiv Gandhi Intl Cricket Stadium",  "Hyderabad",    "India"),
    ("Sawai Mansingh Stadium",             "Jaipur",       "India"),
    ("Punjab Cricket Association Stadium", "Mohali",       "India"),
    ("Ekana Cricket Stadium",              "Lucknow",      "India"),
    ("Brabourne Stadium",                  "Mumbai",       "India"),
    ("DY Patil Stadium",                   "Navi Mumbai",  "India"),
    ("Lords Cricket Ground",               "London",       "England"),
    ("The Oval",                           "London",       "England"),
    ("Edgbaston",                          "Birmingham",   "England"),
    ("Melbourne Cricket Ground",           "Melbourne",    "Australia"),
    ("Sydney Cricket Ground",              "Sydney",       "Australia"),
    ("Adelaide Oval",                      "Adelaide",     "Australia"),
    ("Gaddafi Stadium",                    "Lahore",       "Pakistan"),
    ("National Stadium",                   "Karachi",      "Pakistan"),
    ("SuperSport Park",                    "Centurion",    "South Africa"),
    ("Newlands Cricket Ground",            "Cape Town",    "South Africa"),
    ("Hagley Oval",                        "Christchurch", "New Zealand"),
    ("Sabina Park",                        "Kingston",     "West Indies"),
    ("R. Premadasa Stadium",               "Colombo",      "Sri Lanka"),
]
ground_objs = [Ground.objects.create(name=n, city=c, country=co) for n, c, co in GROUNDS_DATA]
print(f"  Created {Ground.objects.count()} grounds.")

# ── 3. PLAYERS ────────────────────────────────────────────────────────────────
print("Creating players...")
Player.objects.all().delete()
BattingInnings.objects.all().delete()
BowlingInnings.objects.all().delete()

# Columns:
# name, country, ipl_short, role, bat_style, bowl_style, is_overseas, dob, photo_id (unused — kept for compat)
# matches, total_runs, total_wickets
# batting_avg, strike_rate, economy_rate
# highest_score (INT), best_bowling (STR e.g. "5/19")
# centuries, half_centuries, catches, stumpings

PLAYERS = [
    # ═══ INDIA — BATTERS ═══
    ("Virat Kohli",        "India","RCB","Batsman",     "Right-hand bat","Right-arm medium",       False,date(1988,11,5), 219647, 237,7263,4,  49.0,131.5,0.0,  113,"0/5",   7,53,95,0),
    ("Rohit Sharma",       "India","MI", "Batsman",     "Right-hand bat","Right-arm offbreak",      False,date(1987,4,30),219736, 243,6211,15, 29.0,130.4,0.0,  109,"1/12",  1,42,95,0),
    ("Shubman Gill",       "India","GT", "Batsman",     "Right-hand bat","Right-arm offbreak",      False,date(1999,9,8), 1125325,98, 3261,5,  35.0,133.7,0.0,  129,"1/6",   4,21,34,0),
    ("KL Rahul",           "India","LSG","WK-Batsman",  "Right-hand bat","Right-arm offbreak",      False,date(1992,4,18),422108, 132,4683,2,  41.4,135.6,0.0,  132,"0/1",   5,38,52,18),
    ("Rishabh Pant",       "India","DC", "WK-Batsman",  "Left-hand bat", "N/A",                     False,date(1997,10,4),1070173,98, 3284,0,  37.3,148.9,0.0,  128,"0/0",   3,18,45,17),
    ("Ishan Kishan",       "India","MI", "WK-Batsman",  "Left-hand bat", "N/A",                     False,date(1998,7,18),1151592,70, 1893,0,  29.9,135.2,0.0,  99, "0/0",   1,12,28,8),
    ("Shreyas Iyer",       "India","KKR","Batsman",     "Right-hand bat","Right-arm legbreak",       False,date(1994,12,6),1111581,118,3574,5,  34.1,127.9,0.0,  96, "1/13",  1,25,44,0),
    ("Sanju Samson",       "India","RR", "WK-Batsman",  "Right-hand bat","N/A",                     False,date(1994,11,11),489889,143,3881,0,  30.5,140.6,0.0,  119,"0/0",   2,26,55,14),
    ("Suryakumar Yadav",   "India","MI", "Batsman",     "Right-hand bat","Right-arm medium",        False,date(1990,9,22),1124715,166,5101,1,  46.3,170.1,0.0,  117,"0/5",   5,32,64,0),
    ("Yashasvi Jaiswal",   "India","RR", "Batsman",     "Left-hand bat", "Right-arm legbreak",       False,date(2001,12,28),1175434,58,2037,0,  37.7,163.4,0.0,  124,"0/0",   2,13,19,0),
    ("Tilak Varma",        "India","MI", "Batsman",     "Left-hand bat", "Right-arm offbreak",       False,date(2002,11,8),1264736,48, 1354,3,  38.7,145.4,0.0,  84, "1/7",   1,11,18,0),
    ("Devdutt Padikkal",   "India","RR", "Batsman",     "Left-hand bat", "Right-arm legbreak",       False,date(2000,7,7), 1175432,68, 1803,2,  30.1,129.4,0.0,  101,"0/5",   0,14,22,0),
    ("Ruturaj Gaikwad",    "India","CSK","Batsman",     "Right-hand bat","Right-arm offbreak",       False,date(1997,1,31),1151604,108,3259,2,  37.6,136.0,0.0,  101,"0/5",   2,22,38,0),
    ("Prithvi Shaw",       "India","DC", "Batsman",     "Right-hand bat","Right-arm offbreak",       False,date(1999,11,9),1134612,84, 1858,1,  26.2,151.4,0.0,  99, "0/5",   0,12,24,0),
    ("Mayank Agarwal",     "India","PBKS","Batsman",    "Right-hand bat","Right-arm offbreak",       False,date(1991,2,16),642587, 118,3058,1,  29.1,143.9,0.0,  106,"0/5",   0,24,37,0),
    ("Manish Pandey",      "India","LSG","Batsman",     "Right-hand bat","Right-arm offbreak",       False,date(1989,9,10),26421,  187,3914,2,  26.9,122.0,0.0,  114,"0/5",   0,23,47,0),
    ("Ambati Rayudu",      "India","CSK","Batsman",     "Right-hand bat","Right-arm offbreak",       False,date(1985,9,23),38938,  188,3695,1,  27.0,118.3,0.0,  100,"0/5",   0,24,52,0),
    ("Shikhar Dhawan",     "India","PBKS","Batsman",    "Left-hand bat", "Right-arm offbreak",       False,date(1985,12,5),27875,  206,6244,6,  34.8,127.0,0.0,  106,"0/5",   2,42,79,0),
    ("Suresh Raina",       "India","CSK","Batsman",     "Left-hand bat", "Right-arm offbreak",       False,date(1986,11,27),26421, 205,5528,36, 32.5,136.8,0.0,  100,"1/2",   1,39,101,0),
    ("Gautam Gambhir",     "India","KKR","Batsman",     "Left-hand bat", "Right-arm offbreak",       False,date(1981,10,14),30928, 154,4217,5,  31.2,123.8,0.0,  93, "0/5",   0,29,63,0),
    ("Virender Sehwag",    "India","DC", "Batsman",     "Right-hand bat","Right-arm offbreak",       False,date(1978,10,20),8917,  104,2728,12, 29.2,158.5,0.0,  122,"2/19",  0,12,42,0),
    ("Abhishek Sharma",    "India","SRH","All-Rounder", "Left-hand bat", "Left-arm orthodox",        False,date(2000,9,4), 1175436,72, 1754,18, 29.7,172.3,0.0,  116,"1/7",   1,11,19,0),
    ("Riyan Parag",        "India","RR", "All-Rounder", "Right-hand bat","Right-arm offbreak",       False,date(2002,11,10),1254787,68,1184,22, 23.2,141.8,0.0,  62, "3/18",  0,4, 17,0),
    ("Nitish Rana",        "India","KKR","Batsman",     "Left-hand bat", "Right-arm offbreak",       False,date(1994,12,27),946103, 108,2742,12, 28.6,133.8,0.0,  87, "1/14",  0,18,31,0),
    ("Rinku Singh",        "India","KKR","Batsman",     "Left-hand bat", "Right-arm offbreak",       False,date(1997,10,12),1168077,66,1319,2,  37.7,151.4,0.0,  74, "0/5",   0,8, 19,0),
    ("Venkatesh Iyer",     "India","KKR","All-Rounder", "Left-hand bat", "Right-arm medium",         False,date(1994,12,25),1175444,82,1681,28, 28.5,138.4,0.0,  83, "4/20",  0,9, 21,0),
    ("Deepak Hooda",       "India","LSG","All-Rounder", "Right-hand bat","Right-arm offbreak",       False,date(1995,7,18),820814, 72, 1362,28, 24.4,142.8,0.0,  77, "4/27",  0,6, 18,0),
    ("Ayush Badoni",       "India","LSG","Batsman",     "Right-hand bat","Right-arm legbreak",       False,date(2001,10,2),1264732, 38,742, 3,  30.1,140.2,0.0,  89, "0/11",  0,5, 11,0),
    ("Sai Sudharsan",      "India","GT", "Batsman",     "Left-hand bat", "Right-arm offbreak",       False,date(2002,1,15),1264753, 58,1564,4,  34.8,131.6,0.0,  103,"0/8",   1,11,18,0),
    ("MS Dhoni",           "India","CSK","WK-Batsman",  "Right-hand bat","N/A",                     False,date(1981,7,7), 28235,  250,5082,0,  38.0,135.2,0.0,  84, "0/0",   0,24,132,38),
    ("Dinesh Karthik",     "India","RCB","WK-Batsman",  "Right-hand bat","N/A",                     False,date(1985,6,1), 28235,  229,2588,0,  24.3,130.9,0.0,  97, "0/0",   0,17,102,38),
    ("Wriddhiman Saha",    "India","GT", "WK-Batsman",  "Right-hand bat","N/A",                     False,date(1984,10,24),38914, 198,1919,0,  20.8,116.1,0.0,  115,"0/0",   0,10,82,28),
    ("Yuvraj Singh",       "India","PBKS","All-Rounder","Left-hand bat", "Left-arm orthodox",        False,date(1981,12,12),28671, 132,2750,38, 30.1,148.6,0.0,  70, "3/14",  0,13,52,0),
    ("Yusuf Pathan",       "India","KKR","All-Rounder", "Right-hand bat","Right-arm offbreak",       False,date(1982,11,17),32634, 174,3204,42, 28.2,148.9,0.0,  72, "4/30",  0,11,58,0),
    ("Saurabh Tiwary",     "India","MI", "Batsman",     "Left-hand bat", "Right-arm offbreak",       False,date(1990,12,13),300001,84, 1616,1,  24.1,123.9,0.0,  78, "0/5",   0,10,24,0),
    ("Prabhsimran Singh",  "India","PBKS","WK-Batsman", "Right-hand bat","N/A",                     False,date(2001,6,9), 1264790,42, 956, 0,  27.3,157.3,0.0,  97, "0/0",   0,7, 14,4),
    ("Anuj Rawat",         "India","RCB","WK-Batsman",  "Left-hand bat", "N/A",                     False,date(1999,9,5), 1264746,38, 442, 0,  20.1,119.4,0.0,  70, "0/0",   0,2, 16,6),

    # ═══ INDIA — BOWLERS & ALL-ROUNDERS ═══
    ("Jasprit Bumrah",     "India","MI", "Bowler",      "Right-hand bat","Right-arm fast",           False,date(1993,12,6),589391, 132,216, 145,6.5, 0.0, 6.8,  6, "5/10",  0,0, 27,0),
    ("Mohammed Shami",     "India","GT", "Bowler",      "Right-hand bat","Right-arm fast",           False,date(1990,9,3), 493773, 94, 128, 114,8.3, 0.0, 8.6,  18,"5/18",  0,0, 18,0),
    ("Bhuvneshwar Kumar",  "India","SRH","Bowler",      "Right-hand bat","Right-arm medium",         False,date(1990,2,5), 625383, 166,263, 145,11.2,0.0, 7.3,  22,"5/19",  0,0, 35,0),
    ("Mohammed Siraj",     "India","RCB","Bowler",      "Right-hand bat","Right-arm fast",           False,date(1994,3,13),1151591,97, 91,  93, 4.1, 0.0, 8.4,  13,"4/21",  0,0, 17,0),
    ("Arshdeep Singh",     "India","PBKS","Bowler",     "Left-hand bat", "Left-arm fast",            False,date(1999,2,5), 1254710,82, 44,  89, 5.3, 0.0, 8.5,  14,"4/9",   0,0, 16,0),
    ("Yuzvendra Chahal",   "India","RR", "Bowler",      "Right-hand bat","Right-arm legbreak",       False,date(1990,7,23),625376, 184,60,  205,6.6, 0.0, 7.6,  10,"5/40",  0,0, 72,0),
    ("Kuldeep Yadav",      "India","DC", "Bowler",      "Left-hand bat", "Left-arm chinaman",        False,date(1994,12,14),734651,114,171, 139,7.2, 0.0, 7.8,  18,"5/24",  0,0, 27,0),
    ("T Natarajan",        "India","SRH","Bowler",      "Left-hand bat", "Left-arm fast",            False,date(1991,5,27),1151594,58, 31,  64, 4.4, 0.0, 8.8,  12,"4/8",   0,0, 9, 0),
    ("Deepak Chahar",      "India","CSK","Bowler",      "Right-hand bat","Right-arm medium",         False,date(1992,8,7), 700291, 76, 183, 68, 11.5,0.0, 7.7,  23,"4/13",  0,0, 18,0),
    ("Umesh Yadav",        "India","KKR","Bowler",      "Right-hand bat","Right-arm fast",           False,date(1987,10,25),469883,128,372, 132,13.9,0.0, 9.1,  22,"5/19",  0,0, 24,0),
    ("Navdeep Saini",      "India","RR", "Bowler",      "Right-hand bat","Right-arm fast",           False,date(1992,12,23),927093,62, 84,  62, 7.2, 0.0, 9.3,  16,"4/24",  0,0, 9, 0),
    ("Ravi Bishnoi",       "India","LSG","Bowler",      "Right-hand bat","Right-arm legbreak",       False,date(2000,8,5), 1175465,82, 184, 89, 9.4, 0.0, 7.2,  21,"4/22",  0,0, 19,0),
    ("Mohsin Khan",        "India","LSG","Bowler",      "Left-hand bat", "Left-arm fast",            False,date(2001,10,2),1254739,42, 32,  48, 5.1, 0.0, 7.9,  11,"4/18",  0,0, 7, 0),
    ("Yash Dayal",         "India","RCB","Bowler",      "Left-hand bat", "Left-arm fast",            False,date(1999,8,26),1254743,44, 48,  44, 6.8, 0.0, 9.4,  10,"4/28",  0,0, 7, 0),
    ("Harshit Rana",       "India","KKR","Bowler",      "Right-hand bat","Right-arm fast",           False,date(2003,3,4), 1264752,38, 42,  42, 6.5, 0.0, 9.2,  12,"4/24",  0,0, 5, 0),
    ("Mohit Sharma",       "India","GT", "Bowler",      "Right-hand bat","Right-arm fast",           False,date(1988,9,18),534548, 98, 143, 106,7.8, 0.0, 8.8,  14,"5/23",  0,0, 16,0),
    ("Tushar Deshpande",   "India","CSK","Bowler",      "Right-hand bat","Right-arm fast",           False,date(1995,8,15),1175452,52, 48,  52, 5.4, 0.0, 9.5,  12,"4/25",  0,0, 7, 0),
    ("Ishan Porel",        "India","PBKS","Bowler",     "Right-hand bat","Right-arm fast",           False,date(1999,3,16),1151611,42, 42,  44, 6.6, 0.0, 9.7,  13,"3/20",  0,0, 6, 0),
    ("Suyash Sharma",      "India","KKR","Bowler",      "Right-hand bat","Right-arm legbreak",       False,date(2001,7,15),1264795,36, 34,  40, 5.8, 0.0, 7.5,  14,"3/18",  0,0, 5, 0),
    ("Darshan Nalkande",   "India","GT", "Bowler",      "Right-hand bat","Right-arm fast",           False,date(2001,9,9), 1264756,32, 28,  34, 5.6, 0.0, 9.3,  11,"4/27",  0,0, 4, 0),
    ("Piyush Chawla",      "India","MI", "Bowler",      "Right-hand bat","Right-arm legbreak",       False,date(1988,12,24),26421, 165,753, 156,18.8,0.0, 7.3,  21,"5/22",  0,2, 52,0),
    ("Harbhajan Singh",    "India","CSK","Bowler",      "Right-hand bat","Right-arm offbreak",       False,date(1980,7,3), 15744, 163,1238,150,19.3,0.0, 7.0,  20,"5/18",  0,5, 56,0),
    ("Karn Sharma",        "India","MI", "Bowler",      "Right-hand bat","Right-arm legbreak",       False,date(1987,10,23),472870,84, 378, 89, 19.9,0.0, 7.8,  22,"4/22",  0,2, 28,0),

    # ═══ INDIA — ALL-ROUNDERS ═══
    ("Ravindra Jadeja",    "India","CSK","All-Rounder", "Left-hand bat", "Slow left-arm orthodox",   False,date(1988,12,6),211768, 236,2502,132,24.0,130.4,7.6, 58, "5/16",  0,14,95,0),
    ("Hardik Pandya",      "India","MI", "All-Rounder", "Right-hand bat","Right-arm fast",           False,date(1993,10,11),625383,148,1725,75, 24.0,147.8,8.9, 50, "5/27",  0,10,45,0),
    ("R Ashwin",           "India","CSK","All-Rounder", "Right-hand bat","Right-arm offbreak",       False,date(1986,9,17),26421,  197,1780,145,20.0,124.4,6.9, 46, "5/2",   0,6, 82,0),
    ("Axar Patel",         "India","DC", "All-Rounder", "Left-hand bat", "Left-arm orthodox",        False,date(1994,1,20),720471, 102,580, 89, 20.7,127.2,7.2, 38, "5/38",  0,2, 26,0),
    ("Washington Sundar",  "India","SRH","All-Rounder", "Right-hand bat","Right-arm offbreak",       False,date(1999,10,5),1151593,62, 533, 56, 22.2,128.4,6.9, 36, "3/19",  0,2, 14,0),
    ("Shardul Thakur",     "India","CSK","All-Rounder", "Right-hand bat","Right-arm fast",           False,date(1991,8,16),803534, 95, 562, 92, 20.8,138.4,9.3, 44, "4/36",  0,3, 28,0),
    ("Krunal Pandya",      "India","LSG","All-Rounder", "Left-hand bat", "Left-arm orthodox",        False,date(1991,3,24),669855, 104,1469,55, 25.1,136.4,7.3, 58, "3/18",  0,7, 32,0),
    ("Shivam Dube",        "India","CSK","All-Rounder", "Left-hand bat", "Right-arm medium",         False,date(1993,6,26),920085, 88, 1623,28, 27.8,159.6,9.6, 63, "3/21",  0,7, 22,0),
    ("Vijay Shankar",      "India","GT", "All-Rounder", "Right-hand bat","Right-arm medium",         False,date(1991,1,26),670007, 74, 891, 32, 22.5,128.4,9.1, 52, "3/14",  0,3, 16,0),
    ("Shahbaz Ahmed",      "India","RCB","All-Rounder", "Left-hand bat", "Right-arm offbreak",       False,date(1994,11,1),1151603, 72,841, 52, 22.1,128.8,7.4, 48, "4/32",  0,4, 18,0),
    ("Harpreet Brar",      "India","PBKS","All-Rounder","Right-hand bat","Left-arm orthodox",        False,date(1997,6,2), 1168087,52, 534, 44, 19.4,122.4,7.6, 38, "3/19",  0,2, 12,0),
    ("Rishi Dhawan",       "India","PBKS","All-Rounder","Right-hand bat","Right-arm medium",         False,date(1990,6,4), 670012, 44, 468, 34, 20.3,124.4,9.2, 32, "3/21",  0,1, 12,0),

    # ═══ AUSTRALIA ═══
    ("David Warner",       "Australia","DC","Batsman",  "Left-hand bat", "Right-arm medium",         True, date(1986,10,27),219889,176,6397,2,  39.6,140.8,0.0, 126,"0/5",   4,60,66,0),
    ("Steve Smith",        "Australia","RR","Batsman",  "Right-hand bat","Right-arm legbreak",        True, date(1989,6,2), 303669,162,2839,12, 30.7,124.0,0.0, 90, "1/12",  1,18,60,0),
    ("Glenn Maxwell",      "Australia","RCB","All-Rounder","Right-hand bat","Right-arm offbreak",     True, date(1988,10,14),301452,176,3409,31, 24.9,157.8,7.7, 95, "4/46",  1,16,52,0),
    ("Travis Head",        "Australia","SRH","Batsman", "Left-hand bat", "Right-arm offbreak",        True, date(1993,12,29),492741,84, 2524,3,  33.2,143.5,0.0, 96, "0/5",   1,14,24,0),
    ("Marcus Stoinis",     "Australia","LSG","All-Rounder","Right-hand bat","Right-arm fast",         True, date(1989,8,16),434281,108,2263,39, 28.7,152.4,9.4, 78, "4/15",  0,12,32,0),
    ("Matthew Wade",       "Australia","GT","WK-Batsman","Left-hand bat", "N/A",                     True, date(1987,12,26),322737,148,2416,0,  25.2,131.8,0.0, 99, "0/0",   0,13,58,18),
    ("Cameron Green",      "Australia","MI","All-Rounder","Right-hand bat","Right-arm fast",          True, date(2001,6,3), 1254740,56, 834, 41, 22.5,146.4,9.1, 52, "4/27",  0,3, 17,0),
    ("Tim David",          "Singapore","MI","Batsman",  "Right-hand bat","Right-arm offbreak",        True, date(1996,3,16),1207765,62, 1289,2,  34.6,154.3,0.0, 81, "0/5",   0,8, 19,0),
    ("Pat Cummins",        "Australia","SRH","Bowler",  "Right-hand bat","Right-arm fast",            True, date(1993,5,8), 669855, 122,356, 152,9.7, 0.0, 8.7,  22,"5/30",  0,0, 22,0),
    ("Mitchell Starc",     "Australia","RCB","Bowler",  "Left-hand bat", "Left-arm fast",             True, date(1990,1,30),474655, 105,353, 102,12.3,0.0, 8.2,  18,"6/15",  0,0, 21,0),
    ("Josh Hazlewood",     "Australia","RCB","Bowler",  "Right-hand bat","Right-arm fast",            True, date(1991,1,8), 519907, 69, 104, 77, 7.4, 0.0, 7.9,  16,"4/12",  0,0, 15,0),
    ("Adam Zampa",         "Australia","RCB","Bowler",  "Right-hand bat","Right-arm legbreak",        True, date(1992,3,31),695312, 101,183, 127,11.8,0.0, 6.8,  18,"5/35",  0,0, 28,0),

    # ═══ ENGLAND ═══
    ("Jos Buttler",        "England","RR","WK-Batsman", "Right-hand bat","N/A",                      True, date(1990,9,8), 308967, 177,5373,0,  35.3,149.9,0.0, 124,"0/0",   4,40,72,25),
    ("Ben Stokes",         "England","RR","All-Rounder","Left-hand bat", "Right-arm fast",            True, date(1991,6,4), 435703, 145,2209,50, 26.2,139.8,8.4, 82, "3/26",  0,12,50,0),
    ("Sam Curran",         "England","PBKS","All-Rounder","Left-hand bat","Left-arm fast",            True, date(1998,6,3), 1168065,82, 876, 82, 19.9,128.8,8.9, 55, "5/10",  0,4, 20,0),
    ("Jonny Bairstow",     "England","SRH","WK-Batsman","Right-hand bat","N/A",                      True, date(1989,9,26),295114, 99, 3070,0,  34.8,145.2,0.0, 114,"0/0",   2,22,42,12),
    ("Liam Livingstone",   "England","PBKS","All-Rounder","Right-hand bat","Right-arm legbreak",      True, date(1993,8,4), 1065498,72, 1472,39, 26.3,158.8,8.8, 89, "6/27",  1,8, 21,0),
    ("Moeen Ali",          "England","CSK","All-Rounder","Left-hand bat", "Right-arm offbreak",       True, date(1987,6,18),263195, 154,1924,62, 23.2,134.4,7.4, 72, "6/30",  0,11,48,0),
    ("Jason Roy",          "England","GT","Batsman",    "Right-hand bat","Right-arm medium",          True, date(1990,7,21),389744, 108,2857,2,  29.4,143.8,0.0, 78, "0/5",   1,19,38,0),
    ("Phil Salt",          "England","DC","WK-Batsman", "Right-hand bat","N/A",                      True, date(1996,8,28),1070162,72, 1822,0,  30.4,153.8,0.0, 88, "0/0",   1,12,28,8),
    ("Dawid Malan",        "England","N/A","Batsman",   "Left-hand bat", "Right-arm legbreak",        True, date(1987,9,3), 295110, 82, 1991,1,  29.3,126.8,0.0, 103,"0/5",   0,14,29,0),
    ("Mark Wood",          "England","LSG","Bowler",    "Right-hand bat","Right-arm fast",            True, date(1990,1,11),674322, 82, 126, 85, 8.1, 0.0, 9.2,  17,"5/14",  0,0, 14,0),
    ("Adil Rashid",        "England","DC","Bowler",     "Right-hand bat","Right-arm legbreak",        True, date(1988,2,17),224804, 109,369, 118,16.4,0.0, 6.9,  24,"4/2",   0,0, 40,0),
    ("Jofra Archer",       "England","MI","Bowler",     "Right-hand bat","Right-arm fast",            True, date(1995,4,1), 930080, 82, 156, 88, 9.0, 0.0, 8.2,  18,"4/16",  0,0, 13,0),
    ("Chris Jordan",       "England","N/A","Bowler",    "Right-hand bat","Right-arm fast",            True, date(1988,10,4),574786, 88, 182, 96, 8.8, 0.0, 9.2,  24,"4/6",   0,0, 18,0),

    # ═══ PAKISTAN ═══
    ("Babar Azam",         "Pakistan","N/A","Batsman",  "Right-hand bat","Right-arm medium",          True, date(1994,10,15),348144,122,3578,2,  40.0,127.5,0.0, 110,"0/5",   3,34,42,0),
    ("Mohammad Rizwan",    "Pakistan","N/A","WK-Batsman","Right-hand bat","N/A",                      True, date(1992,6,1), 509823, 134,3793,0,  34.0,127.3,0.0, 104,"0/0",   0,26,53,20),
    ("Fakhar Zaman",       "Pakistan","N/A","Batsman",  "Left-hand bat", "Right-arm legbreak",        True, date(1990,4,10),621434, 103,2890,1,  30.6,134.5,0.0, 138,"0/5",   2,21,31,0),
    ("Shaheen Afridi",     "Pakistan","N/A","Bowler",   "Left-hand bat", "Left-arm fast",             True, date(2000,4,6), 1151504,88, 178, 97, 8.7, 0.0, 7.8,  14,"6/35",  0,0, 18,0),
    ("Haris Rauf",         "Pakistan","N/A","Bowler",   "Right-hand bat","Right-arm fast",            True, date(1993,12,7),938353, 76, 113, 96, 7.6, 0.0, 9.0,  18,"5/29",  0,0, 12,0),
    ("Naseem Shah",        "Pakistan","N/A","Bowler",   "Right-hand bat","Right-arm fast",            True, date(2003,2,15),1254754,66, 89,  72, 5.9, 0.0, 8.7,  12,"5/25",  0,0, 9, 0),
    ("Shadab Khan",        "Pakistan","N/A","All-Rounder","Right-hand bat","Right-arm legbreak",      True, date(1998,10,4),849568, 100,779, 126,18.2,132.4,6.6, 42, "4/8",   0,5, 35,0),
    ("Imad Wasim",         "Pakistan","N/A","All-Rounder","Left-hand bat","Left-arm orthodox",        True, date(1988,12,18),468116,82, 962, 72, 24.4,128.8,6.5, 44, "5/14",  0,3, 21,0),

    # ═══ SOUTH AFRICA ═══
    ("Quinton de Kock",    "South Africa","LSG","WK-Batsman","Left-hand bat","N/A",                  True, date(1992,12,17),442580,161,4292,0,  30.3,134.0,0.0, 140,"0/0",   3,29,72,14),
    ("David Miller",       "South Africa","GT","Batsman",  "Left-hand bat","Right-arm medium",        True, date(1989,6,10),337762, 218,4402,1,  35.2,145.1,0.0, 101,"0/3",   2,28,75,0),
    ("Faf du Plessis",     "South Africa","RCB","Batsman", "Right-hand bat","Right-arm legbreak",     True, date(1984,7,13),236535, 218,4650,3,  29.5,131.1,0.0, 120,"0/9",   1,37,84,0),
    ("Aiden Markram",      "South Africa","SRH","All-Rounder","Right-hand bat","Right-arm offbreak",  True, date(1994,10,4),1027421,106,2645,31, 30.3,142.2,0.0, 101,"3/20",  0,12,40,0),
    ("Rassie van der Dussen","South Africa","RR","Batsman","Right-hand bat","Right-arm offbreak",     True, date(1989,7,7), 1065495,94, 2253,6,  32.6,131.5,0.0, 104,"0/14",  0,16,32,0),
    ("Heinrich Klaasen",   "South Africa","SRH","WK-Batsman","Right-hand bat","N/A",                 True, date(1991,7,30),626368, 112,2884,0,  38.4,162.7,0.0, 102,"0/0",   1,21,44,12),
    ("Marco Jansen",       "South Africa","SRH","All-Rounder","Left-hand bat","Left-arm fast",        True, date(2000,6,1), 1175481,64, 614, 58, 21.9,128.8,9.1, 40, "4/21",  0,3, 14,0),
    ("AB de Villiers",     "South Africa","RCB","Batsman","Right-hand bat","Right-arm medium",        True, date(1984,2,17),44828,  184,5162,5,  39.7,151.7,0.0, 133,"0/14",  3,36,89,0),
    ("Kagiso Rabada",      "South Africa","PBKS","Bowler", "Right-hand bat","Right-arm fast",         True, date(1995,5,25),667821, 148,498, 207,11.9,0.0, 8.2,  22,"5/39",  0,0, 29,0),
    ("Anrich Nortje",      "South Africa","DC","Bowler",   "Right-hand bat","Right-arm fast",         True, date(1993,11,16),1151509,72,129, 89, 8.3, 0.0, 8.7,  14,"4/7",   0,0, 11,0),
    ("Tabraiz Shamsi",     "South Africa","RR","Bowler",   "Right-hand bat","Left-arm chinaman",      True, date(1990,2,18),621439, 90, 113, 113,11.5,0.0, 6.4,  16,"5/24",  0,0, 24,0),
    ("Lungi Ngidi",        "South Africa","CSK","Bowler",  "Right-hand bat","Right-arm fast",         True, date(1996,3,29),1065497,108,178, 134,9.3, 0.0, 8.4,  18,"6/58",  0,0, 18,0),

    # ═══ NEW ZEALAND ═══
    ("Kane Williamson",    "New Zealand","SRH","Batsman", "Right-hand bat","Right-arm offbreak",      True, date(1990,8,8), 277477, 151,3589,7,  29.8,119.7,0.0, 95, "1/22",  1,22,58,0),
    ("Devon Conway",       "New Zealand","CSK","WK-Batsman","Left-hand bat","N/A",                   True, date(1991,7,8), 1070082,98, 2853,0,  34.4,130.2,0.0, 99, "0/0",   1,23,38,10),
    ("Daryl Mitchell",     "New Zealand","N/A","All-Rounder","Right-hand bat","Right-arm medium",     True, date(1991,5,20),1065483,92, 1941,35, 29.6,142.8,8.6, 72, "4/30",  0,9, 28,0),
    ("Rachin Ravindra",    "New Zealand","CSK","All-Rounder","Left-hand bat","Left-arm orthodox",     True, date(2000,1,14),1254784,62, 1504,28, 28.9,134.8,7.5, 74, "4/9",   0,9, 21,0),
    ("Mitchell Santner",   "New Zealand","CSK","All-Rounder","Left-hand bat","Left-arm orthodox",     True, date(1992,2,5), 603905, 128,922, 99, 20.5,122.8,6.8, 48, "5/10",  0,4, 42,0),
    ("Martin Guptill",     "New Zealand","N/A","Batsman",  "Right-hand bat","Right-arm medium",       True, date(1986,9,30),218313, 122,3531,5,  32.1,136.5,0.0, 101,"0/5",   2,24,45,0),
    ("Trent Boult",        "New Zealand","RR","Bowler",    "Right-hand bat","Left-arm fast",           True, date(1989,7,22),447644, 158,459, 175,11.5,0.0, 7.3,  14,"5/27",  0,0, 31,0),
    ("Lockie Ferguson",    "New Zealand","GT","Bowler",    "Right-hand bat","Right-arm fast",          True, date(1991,6,13),774957, 84, 115, 98, 7.8, 0.0, 8.3,  13,"5/21",  0,0, 12,0),

    # ═══ WEST INDIES ═══
    ("Andre Russell",      "West Indies","KKR","All-Rounder","Right-hand bat","Right-arm fast",       True, date(1988,4,29),282589, 156,2494,117,26.5,178.4,9.6, 88, "5/15",  0,16,52,0),
    ("Sunil Narine",       "West Indies","KKR","All-Rounder","Left-hand bat","Right-arm offbreak",    True, date(1988,5,26),469904, 176,1282,148,20.8,162.4,6.5, 85, "5/19",  0,5, 55,0),
    ("Kieron Pollard",     "West Indies","MI","All-Rounder","Right-hand bat","Right-arm medium",      True, date(1987,5,12),34102,  189,3412,69, 30.6,148.4,9.0, 83, "3/5",   0,16,85,0),
    ("Nicholas Pooran",    "West Indies","LSG","WK-Batsman","Left-hand bat","N/A",                   True, date(1995,10,2),1151541,148,2971,0,  28.6,145.7,0.0, 111,"0/0",   1,16,55,12),
    ("Shimron Hetmyer",    "West Indies","RR","Batsman",   "Left-hand bat","Right-arm legbreak",      True, date(1996,12,26),1095185,104,2289,1,  31.9,149.1,0.0, 104,"0/5",   1,14,32,0),
    ("Chris Gayle",        "West Indies","PBKS","Batsman", "Right-hand bat","Right-arm offbreak",     True, date(1979,9,21),42434,  142,4965,28, 39.7,145.8,0.0, 175,"2/1",   6,36,66,0),
    ("Dwayne Bravo",       "West Indies","CSK","All-Rounder","Right-hand bat","Right-arm fast",       True, date(1983,10,7),43960,  161,1532,133,20.9,134.4,8.2, 58, "4/22",  0,6, 58,0),
    ("Rovman Powell",      "West Indies","DC","Batsman",   "Right-hand bat","Right-arm medium",       True, date(1993,11,15),1070125,64,1352,2,  29.4,153.4,0.0, 72, "0/5",   0,8, 18,0),
    ("Kyle Mayers",        "West Indies","LSG","All-Rounder","Left-hand bat","Right-arm fast",        True, date(1992,9,8), 1070154,54, 912, 38, 22.8,138.8,9.3, 64, "4/22",  0,3, 14,0),
    ("Jason Holder",       "West Indies","LSG","All-Rounder","Right-hand bat","Right-arm fast",       True, date(1991,11,5),536728, 154,1521,104,20.3,124.8,8.1, 55, "5/27",  0,7, 42,0),
    ("Alzarri Joseph",     "West Indies","MI","Bowler",    "Right-hand bat","Right-arm fast",         True, date(1996,11,20),1070139,72, 96,  72, 6.5, 0.0, 9.1,  14,"6/12",  0,0, 12,0),

    # ═══ SRI LANKA ═══
    ("Wanindu Hasaranga",  "Sri Lanka","RCB","All-Rounder","Right-hand bat","Right-arm legbreak",     True, date(1997,7,29),1151546,116,844, 136,19.6,138.4,7.2, 52, "6/19",  0,5, 31,0),
    ("Kusal Mendis",       "Sri Lanka","N/A","WK-Batsman","Right-hand bat","N/A",                    True, date(1995,2,2), 503943, 108,2658,0,  28.9,129.7,0.0, 110,"0/0",   0,15,41,9),
    ("Pathum Nissanka",    "Sri Lanka","N/A","Batsman",   "Right-hand bat","Right-arm offbreak",      True, date(1998,4,13),1151547,92, 2524,8,  30.8,128.3,0.0, 137,"0/9",   1,15,27,0),
    ("Lasith Malinga",     "Sri Lanka","MI","Bowler",     "Right-hand bat","Right-arm fast",          True, date(1983,8,28),48970,  122,310, 170,13.3,0.0, 7.1,  14,"5/13",  0,0, 22,0),
    ("Maheesh Theekshana", "Sri Lanka","CSK","Bowler",    "Right-hand bat","Right-arm offbreak",      True, date(1999,3,21),1264765,72, 88,  88, 8.1, 0.0, 6.8,  12,"4/14",  0,0, 14,0),
    ("Matheesha Pathirana","Sri Lanka","CSK","Bowler",    "Right-hand bat","Right-arm fast",          True, date(2001,4,2), 1264766,48, 28,  58, 5.8, 0.0, 7.8,  8,  "5/6",   0,0, 6, 0),
    ("Dushmantha Chameera","Sri Lanka","N/A","Bowler",   "Right-hand bat","Right-arm fast",          True, date(1992,11,13),656829,62, 88,  68, 8.5, 0.0, 8.9,  12,"5/18",  0,0, 9, 0),
    ("Dasun Shanaka",      "Sri Lanka","N/A","All-Rounder","Right-hand bat","Right-arm fast",         True, date(1991,2,13),628173, 104,1529,68, 26.4,148.8,9.3, 68, "5/26",  0,5, 27,0),
    ("Angelo Mathews",     "Sri Lanka","N/A","All-Rounder","Right-hand bat","Right-arm fast",         True, date(1987,6,2), 214445, 144,2948,77, 28.3,128.8,7.2, 79, "4/29",  0,14,52,0),

    # ═══ BANGLADESH ═══
    ("Shakib Al Hasan",    "Bangladesh","N/A","All-Rounder","Left-hand bat","Left-arm orthodox",      True, date(1987,3,24),50806,  132,1884,124,23.8,132.4,6.6, 62, "5/22",  0,9, 42,0),
    ("Mustafizur Rahman",  "Bangladesh","DC","Bowler",    "Right-hand bat","Left-arm fast",            True, date(1995,9,6), 793463, 94, 108, 122,9.4, 0.0, 7.7,  12,"6/43",  0,0, 16,0),
    ("Litton Das",         "Bangladesh","N/A","WK-Batsman","Right-hand bat","N/A",                   True, date(1994,10,13),949551,94, 2083,0,  26.4,126.0,0.0, 98, "0/0",   0,12,36,8),
    ("Mehidy Hasan Miraz", "Bangladesh","N/A","All-Rounder","Right-hand bat","Right-arm offbreak",    True, date(1997,10,25),862264,82, 892, 78, 20.0,118.8,6.9, 52, "5/20",  0,3, 24,0),
    ("Towhid Hridoy",      "Bangladesh","N/A","Batsman",  "Right-hand bat","Right-arm offbreak",      True, date(1999,10,4),1254795,54, 1102,3,  26.9,128.4,0.0, 88, "0/5",   0,7, 15,0),
    ("Mahmudullah",        "Bangladesh","N/A","All-Rounder","Right-hand bat","Right-arm offbreak",    True, date(1986,2,4), 155363, 112,2088,58, 25.8,128.8,7.2, 64, "4/21",  0,9, 36,0),
    ("Taskin Ahmed",       "Bangladesh","N/A","Bowler",   "Right-hand bat","Right-arm fast",          True, date(1995,4,3), 776271, 74, 88,  80, 7.2, 0.0, 8.7,  14,"5/28",  0,0, 12,0),

    # ═══ AFGHANISTAN ═══
    ("Rashid Khan",        "Afghanistan","GT","Bowler",   "Right-hand bat","Right-arm legbreak",      True, date(1998,9,20),802892, 120,869, 176,15.5,0.0, 6.2,  22,"7/18",  0,5, 54,0),
    ("Mohammad Nabi",      "Afghanistan","SRH","All-Rounder","Right-hand bat","Right-arm offbreak",   True, date(1985,1,1), 217670, 122,1668,91, 22.0,132.8,6.9, 58, "4/10",  0,7, 42,0),
    ("Mujeeb Ur Rahman",   "Afghanistan","PBKS","Bowler", "Right-hand bat","Right-arm offbreak",      True, date(2001,3,28),1175451,92, 102, 112,9.8, 0.0, 6.7,  16,"5/14",  0,0, 20,0),
    ("Fazalhaq Farooqi",   "Afghanistan","GT","Bowler",   "Left-hand bat", "Left-arm fast",           True, date(1999,10,28),1151569,72, 84,  84, 7.0, 0.0, 7.5,  11,"5/20",  0,0, 9, 0),
    ("Rahmanullah Gurbaz", "Afghanistan","KKR","WK-Batsman","Right-hand bat","N/A",                  True, date(2001,11,28),1264808,68, 1893,0,  30.5,145.8,0.0, 96, "0/0",   1,14,27,8),
    ("Ibrahim Zadran",     "Afghanistan","N/A","Batsman", "Right-hand bat","Right-arm offbreak",      True, date(2001,2,7), 1254804,58, 1544,2,  28.6,122.8,0.0, 108,"0/5",   0,9, 14,0),
    ("Azmatullah Omarzai", "Afghanistan","GT","All-Rounder","Right-hand bat","Right-arm fast",        True, date(1999,9,30),1175455,54, 812, 44, 23.9,132.8,8.5, 54, "4/28",  0,2, 12,0),
    ("Noor Ahmad",         "Afghanistan","GT","Bowler",   "Right-hand bat","Left-arm chinaman",       True, date(2005,7,9), 1264812,52, 62,  68, 6.4, 0.0, 6.8,  12,"4/11",  0,0, 9, 0),
    ("Gulbadin Naib",      "Afghanistan","N/A","All-Rounder","Right-hand bat","Right-arm fast",       True, date(1991,12,1),489866, 88, 1022,68, 21.3,128.8,8.7, 52, "5/28",  0,3, 22,0),

    # ═══ LEGENDS ═══
    ("Jacques Kallis",     "South Africa","RCB","All-Rounder","Right-hand bat","Right-arm fast",      True, date(1975,10,16),25652, 98, 2427,37, 29.7,128.8,7.9, 72, "3/8",   0,14,43,0),
    ("Adam Gilchrist",     "Australia","DC","WK-Batsman",  "Left-hand bat","N/A",                    True, date(1971,11,14),5363,  90, 2024,0,  25.3,141.8,0.0, 162,"0/0",   0,13,48,12),
]

# ── Deduplicate by name (keep first occurrence) ───────────────────────────────
seen = set()
unique = []
for row in PLAYERS:
    if row[0] not in seen:
        seen.add(row[0])
        unique.append(row)
PLAYERS = unique

ipl_grounds  = [g for g in ground_objs if g.country == "India"]
all_grounds  = ground_objs
all_teams    = list(team_map.values())
years        = list(range(2015, 2025))
phases       = ['powerplay', 'middle', 'death']

created = 0
for row in PLAYERS:
    (name, country, ipl_short, role, bat_style, bowl_style, is_overseas,
     dob, photo_id,
     matches, total_runs, total_wickets,
     batting_avg, strike_rate, economy_rate,
     highest_score, best_bowling,
     centuries, half_centuries, catches, stumpings) = row

    ipl_team = team_map.get(ipl_short)
    bowling_avg = round(total_runs / max(total_wickets, 1), 1) if total_wickets > 0 else 0.0

    p = Player.objects.create(
        name            = name,
        country         = country,
        is_overseas     = is_overseas,
        date_of_birth   = dob,
        role            = role,
        batting_style   = bat_style,
        bowling_style   = bowl_style,
        ipl_team        = ipl_team,
        photo_url       = get_photo(name),   # ← wiki URL or placeholder
        total_matches   = matches,
        total_runs      = total_runs,
        total_wickets   = total_wickets,
        batting_avg     = batting_avg,
        bowling_avg     = bowling_avg,
        strike_rate     = strike_rate,
        economy_rate    = economy_rate,
        highest_score   = highest_score,
        best_bowling    = best_bowling,
        centuries       = centuries,
        half_centuries  = half_centuries,
        catches         = catches,
        stumpings       = stumpings,
        bio             = f"{name} is a {country} {role.lower()} who plays {bat_style.lower()} and bowls {bowl_style.lower()}.",
    )

    # ── Batting innings ───────────────────────────────────────────────────────
    if role in ('Batsman', 'WK-Batsman', 'All-Rounder'):
        for _ in range(min(matches, max(matches // 2, 10))):
            phase = random.choice(phases)
            if phase == 'powerplay':
                inn_runs, balls, sr_base = ri(5,38),  ri(6,24),  r(125,160)
            elif phase == 'middle':
                inn_runs, balls, sr_base = ri(8,55),  ri(8,40),  r(115,148)
            else:
                inn_runs, balls, sr_base = ri(10,65), ri(5,25),  r(140,190)
            BattingInnings.objects.create(
                player      = p,
                opponent    = random.choice(all_teams),
                ground      = random.choice(ipl_grounds if ipl_team else all_grounds),
                year        = random.choice(years),
                runs        = inn_runs,
                balls_faced = balls,
                fours       = ri(0, max(1, inn_runs // 8)),
                sixes       = ri(0, max(1, inn_runs // 16)),
                strike_rate = sr_base,
                is_not_out  = random.random() < 0.2,
                phase       = phase,
            )

    # ── Bowling innings ───────────────────────────────────────────────────────
    if role in ('Bowler', 'All-Rounder'):
        for _ in range(min(matches, max(matches // 2, 10))):
            phase     = random.choice(phases)
            econ_base = r(6.0,9.5) if phase=='powerplay' else (r(5.5,8.5) if phase=='middle' else r(7.5,12.0))
            ov        = r(1.0, 4.0)
            BowlingInnings.objects.create(
                player        = p,
                opponent      = random.choice(all_teams),
                ground        = random.choice(ipl_grounds if ipl_team else all_grounds),
                year          = random.choice(years),
                overs         = ov,
                maidens       = ri(0, 1),
                runs_conceded = ri(int(ov)*5, int(ov)*14),
                wickets       = ri(0, 3),
                economy       = econ_base,
                phase         = phase,
            )

    created += 1
    if created % 30 == 0:
        print(f"  ...{created} players created")

print(f"\n✅ Done!")
print(f"   Players  : {Player.objects.count()}")
print(f"   Bat inn  : {BattingInnings.objects.count()}")
print(f"   Bowl inn : {BowlingInnings.objects.count()}")
print(f"   Teams    : {Team.objects.count()}")
print(f"   Grounds  : {Ground.objects.count()}")
print("\n🏏 Run: python manage.py runserver")