from django.contrib import admin
from .models import Player, Team, Ground, BattingInnings, BowlingInnings, DreamTeam, DreamTeamSlot


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'is_ipl_team')
    search_fields = ('name',)


@admin.register(Ground)
class GroundAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country')
    search_fields = ('name', 'city')


class BattingInningsInline(admin.TabularInline):
    model = BattingInnings
    extra = 0


class BowlingInningsInline(admin.TabularInline):
    model = BowlingInnings
    extra = 0


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'role', 'ipl_team', 'total_matches', 'total_runs', 'total_wickets', 'batting_avg', 'strike_rate')
    list_filter = ('role', 'country', 'ipl_team', 'is_overseas')
    search_fields = ('name', 'country')
    inlines = [BattingInningsInline, BowlingInningsInline]


@admin.register(BattingInnings)
class BattingInningsAdmin(admin.ModelAdmin):
    list_display = ('player', 'opponent', 'year', 'runs', 'balls_faced', 'strike_rate', 'phase')
    list_filter = ('year', 'phase')


@admin.register(BowlingInnings)
class BowlingInningsAdmin(admin.ModelAdmin):
    list_display = ('player', 'opponent', 'year', 'wickets', 'runs_conceded', 'economy', 'phase')
    list_filter = ('year', 'phase')


class DreamTeamSlotInline(admin.TabularInline):
    model = DreamTeamSlot
    extra = 0


@admin.register(DreamTeam)
class DreamTeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    inlines = [DreamTeamSlotInline]