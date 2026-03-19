from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    logo_color = models.CharField(max_length=7, default='#1a8f5c')  # hex color
    is_ipl_team = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Ground(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.city}"


class Player(models.Model):
    ROLE_CHOICES = [
        ('Batsman', 'Batsman'),
        ('Bowler', 'Bowler'),
        ('All-Rounder', 'All-Rounder'),
        ('WK-Batsman', 'Wicket-Keeper Batsman'),
    ]
    BATTING_STYLE_CHOICES = [
        ('Right-hand bat', 'Right-hand bat'),
        ('Left-hand bat', 'Left-hand bat'),
    ]
    BOWLING_STYLE_CHOICES = [
        ('Right-arm fast', 'Right-arm fast'),
        ('Right-arm medium', 'Right-arm medium'),
        ('Left-arm fast', 'Left-arm fast'),
        ('Left-arm medium', 'Left-arm medium'),
        ('Right-arm offbreak', 'Right-arm offbreak'),
        ('Right-arm legbreak', 'Right-arm legbreak'),
        ('Left-arm orthodox', 'Left-arm orthodox'),
        ('Left-arm chinaman', 'Left-arm chinaman'),
        ('Slow left-arm orthodox', 'Slow left-arm orthodox'),
        ('N/A', 'N/A'),
    ]

    name = models.CharField(max_length=150)
    country = models.CharField(max_length=80)
    is_overseas = models.BooleanField(default=False, help_text="Overseas player for IPL purposes")
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    batting_style = models.CharField(max_length=50, choices=BATTING_STYLE_CHOICES, default='Right-hand bat')
    bowling_style = models.CharField(max_length=50, choices=BOWLING_STYLE_CHOICES, default='N/A')
    ipl_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='players')
    photo_url = models.URLField(blank=True, default='')
    bio = models.TextField(blank=True, default='')

    # Career aggregates
    total_matches = models.IntegerField(default=0)
    total_runs = models.IntegerField(default=0)
    total_wickets = models.IntegerField(default=0)
    batting_avg = models.FloatField(default=0.0)
    bowling_avg = models.FloatField(default=0.0)
    strike_rate = models.FloatField(default=0.0)
    economy_rate = models.FloatField(default=0.0)
    highest_score = models.IntegerField(default=0)
    best_bowling = models.CharField(max_length=20, default='0/0')
    centuries = models.IntegerField(default=0)
    half_centuries = models.IntegerField(default=0)
    catches = models.IntegerField(default=0)
    stumpings = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class BattingInnings(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='batting_innings')
    opponent = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='batting_against')
    ground = models.ForeignKey(Ground, on_delete=models.SET_NULL, null=True, blank=True)
    year = models.IntegerField()
    runs = models.IntegerField(default=0)
    balls_faced = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)
    strike_rate = models.FloatField(default=0.0)
    is_not_out = models.BooleanField(default=False)
    phase = models.CharField(max_length=20, choices=[
        ('powerplay', 'Powerplay (1-6)'),
        ('middle', 'Middle Overs (7-15)'),
        ('death', 'Death Overs (16-20)'),
    ], default='middle')

    def __str__(self):
        return f"{self.player.name} vs {self.opponent.short_name} ({self.year}): {self.runs}({self.balls_faced})"

    class Meta:
        verbose_name_plural = "Batting innings"


class BowlingInnings(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='bowling_innings')
    opponent = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='bowling_against')
    ground = models.ForeignKey(Ground, on_delete=models.SET_NULL, null=True, blank=True)
    year = models.IntegerField()
    overs = models.FloatField(default=0.0)
    maidens = models.IntegerField(default=0)
    runs_conceded = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    economy = models.FloatField(default=0.0)
    phase = models.CharField(max_length=20, choices=[
        ('powerplay', 'Powerplay (1-6)'),
        ('middle', 'Middle Overs (7-15)'),
        ('death', 'Death Overs (16-20)'),
    ], default='middle')

    def __str__(self):
        return f"{self.player.name} vs {self.opponent.short_name} ({self.year}): {self.wickets}/{self.runs_conceded}"

    class Meta:
        verbose_name_plural = "Bowling innings"


class DreamTeam(models.Model):
    name = models.CharField(max_length=100, default='My Dream XI')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_at']


class DreamTeamSlot(models.Model):
    dream_team = models.ForeignKey(DreamTeam, on_delete=models.CASCADE, related_name='slots')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    slot_number = models.IntegerField()  # 1-12
    role_label = models.CharField(max_length=30, blank=True, default='')

    class Meta:
        unique_together = ('dream_team', 'slot_number')
        ordering = ['slot_number']

    def __str__(self):
        return f"Slot {self.slot_number}: {self.player.name}"