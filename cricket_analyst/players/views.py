import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum, Avg, Count, Max, Q, F
from .models import Player, Team, Ground, BattingInnings, BowlingInnings, DreamTeam, DreamTeamSlot


def home(request):
    """Homepage with search, stats overview, and featured players."""
    total_players = Player.objects.count()
    total_teams = Team.objects.count()
    total_grounds = Ground.objects.count()
    total_dreamteams = DreamTeam.objects.count()
    featured_players = Player.objects.order_by('-total_runs')[:6]

    return render(request, 'players/home.html', {
        'total_players': total_players,
        'total_teams': total_teams,
        'total_grounds': total_grounds,
        'total_dreamteams': total_dreamteams,
        'featured_players': featured_players,
    })


def player_list(request):
    """Filterable, searchable player list."""
    players = Player.objects.all()

    # Filters
    role_filter = request.GET.get('role', '')
    country_filter = request.GET.get('country', '')
    team_filter = request.GET.get('team', '')
    search_query = request.GET.get('q', '')

    if role_filter:
        players = players.filter(role=role_filter)
    if country_filter:
        players = players.filter(country=country_filter)
    if team_filter:
        players = players.filter(ipl_team_id=team_filter)
    if search_query:
        players = players.filter(name__icontains=search_query)

    countries = Player.objects.values_list('country', flat=True).distinct().order_by('country')
    teams = Team.objects.filter(is_ipl_team=True).order_by('name')

    return render(request, 'players/player_list.html', {
        'players': players,
        'role_filter': role_filter,
        'country_filter': country_filter,
        'team_filter': team_filter,
        'search_query': search_query,
        'countries': countries,
        'teams': teams,
    })


def player_detail(request, pk):
    """Comprehensive player stats dashboard."""
    player = get_object_or_404(Player, pk=pk)

    # Year-by-year batting
    year_batting_stats = (
        BattingInnings.objects.filter(player=player)
        .values('year')
        .annotate(
            innings=Count('id'),
            total_runs=Sum('runs'),
            total_fours=Sum('fours'),
            total_sixes=Sum('sixes'),
            avg=Avg('runs'),
            avg_sr=Avg('strike_rate'),
        )
        .order_by('year')
    )

    # Year-by-year bowling
    year_bowling_stats = (
        BowlingInnings.objects.filter(player=player)
        .values('year')
        .annotate(
            innings=Count('id'),
            total_overs=Sum('overs'),
            total_wickets=Sum('wickets'),
            total_runs=Sum('runs_conceded'),
            avg_econ=Avg('economy'),
        )
        .order_by('year')
    )

    # vs Teams batting
    team_batting_stats = (
        BattingInnings.objects.filter(player=player)
        .values('opponent__name')
        .annotate(
            innings=Count('id'),
            total_runs=Sum('runs'),
            avg=Avg('runs'),
            avg_sr=Avg('strike_rate'),
            best=Max('runs'),
        )
        .order_by('-total_runs')
    )

    # vs Teams bowling
    team_bowling_stats = (
        BowlingInnings.objects.filter(player=player)
        .values('opponent__name')
        .annotate(
            innings=Count('id'),
            total_wickets=Sum('wickets'),
            total_runs=Sum('runs_conceded'),
            avg_econ=Avg('economy'),
        )
        .order_by('-total_wickets')
    )

    # Ground stats
    ground_batting_stats = (
        BattingInnings.objects.filter(player=player)
        .values('ground__name')
        .annotate(
            innings=Count('id'),
            total_runs=Sum('runs'),
            avg=Avg('runs'),
            avg_sr=Avg('strike_rate'),
        )
        .order_by('-total_runs')
    )

    # Phase stats - batting
    phase_batting_stats = (
        BattingInnings.objects.filter(player=player)
        .values('phase')
        .annotate(
            innings=Count('id'),
            total_runs=Sum('runs'),
            avg_sr=Avg('strike_rate'),
            total_fours=Sum('fours'),
            total_sixes=Sum('sixes'),
        )
        .order_by('phase')
    )

    # Phase stats - bowling
    phase_bowling_stats = (
        BowlingInnings.objects.filter(player=player)
        .values('phase')
        .annotate(
            innings=Count('id'),
            total_wickets=Sum('wickets'),
            total_runs=Sum('runs_conceded'),
            avg_econ=Avg('economy'),
        )
        .order_by('phase')
    )

    # Format-wise batting
    format_batting_stats = (
        BattingInnings.objects.filter(player=player)
        .values('match_type')
        .annotate(
            innings=Count('id'),
            total_runs=Sum('runs'),
            avg=Avg('runs'),
            avg_sr=Avg('strike_rate'),
            total_fours=Sum('fours'),
            total_sixes=Sum('sixes'),
        )
        .order_by('match_type')
    )

    # Format-wise bowling
    format_bowling_stats = (
        BowlingInnings.objects.filter(player=player)
        .values('match_type')
        .annotate(
            innings=Count('id'),
            total_overs=Sum('overs'),
            total_wickets=Sum('wickets'),
            total_runs=Sum('runs_conceded'),
            avg_econ=Avg('economy'),
        )
        .order_by('match_type')
    )

    return render(request, 'players/player_detail.html', {
        'player': player,
        'year_batting_stats': year_batting_stats,
        'year_bowling_stats': year_bowling_stats,
        'team_batting_stats': team_batting_stats,
        'team_bowling_stats': team_bowling_stats,
        'ground_batting_stats': ground_batting_stats,
        'phase_batting_stats': phase_batting_stats,
        'phase_bowling_stats': phase_bowling_stats,
        'format_batting_stats': format_batting_stats,
        'format_bowling_stats': format_bowling_stats,
    })


def player_search_api(request):
    """JSON endpoint for AJAX player search."""
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse({'players': []})

    players = Player.objects.filter(name__icontains=q)[:10]
    data = [{
        'id': p.pk,
        'name': p.name,
        'country': p.country,
        'role': p.role,
        'total_runs': p.total_runs,
        'total_wickets': p.total_wickets,
        'photo_url': p.photo_url,
    } for p in players]

    return JsonResponse({'players': data})


# --- Dream Team Views ---

def dreamteam_builder(request):
    """Dream XI builder page."""
    all_players = Player.objects.select_related('ipl_team').all()
    return render(request, 'players/dreamteam.html', {
        'all_players': all_players,
    })


def dreamteam_list_view(request):
    """List all saved dream teams."""
    teams = DreamTeam.objects.prefetch_related('slots__player').all()
    return render(request, 'players/dreamteam_list.html', {
        'teams': teams,
    })


def dreamteam_save(request):
    """Save a dream team via AJAX JSON POST."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
        name = data.get('name', 'My Dream XI')
        slots_data = data.get('slots', [])

        if not slots_data:
            return JsonResponse({'error': 'No players in the team'}, status=400)

        # Validate overseas count
        player_ids = [s['player_id'] for s in slots_data]
        overseas_count = Player.objects.filter(pk__in=player_ids, is_overseas=True).count()
        if overseas_count > 4:
            return JsonResponse({'error': f'Too many overseas players ({overseas_count}/4)'}, status=400)

        team = DreamTeam.objects.create(name=name)
        for slot in slots_data:
            DreamTeamSlot.objects.create(
                dream_team=team,
                player_id=slot['player_id'],
                slot_number=slot['slot_number'],
                role_label=slot.get('role_label', ''),
            )

        return JsonResponse({'success': True, 'team_id': team.pk})

    except (json.JSONDecodeError, KeyError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_POST
def dreamteam_delete(request, pk):
    """Delete a saved dream team."""
    team = get_object_or_404(DreamTeam, pk=pk)
    team.delete()
    return redirect('dreamteam_list_view')


# --- Matchup Views ---

def matchup_analyzer(request):
    """Matchup analysis page."""
    batsmen = Player.objects.filter(
        Q(role='Batsman') | Q(role='All-Rounder') | Q(role='WK-Batsman')
    ).order_by('name')
    bowlers = Player.objects.filter(
        Q(role='Bowler') | Q(role='All-Rounder')
    ).order_by('name')

    return render(request, 'players/matchups.html', {
        'batsmen': batsmen,
        'bowlers': bowlers,
    })


def matchup_data_api(request):
    """JSON endpoint for matchup data between two players."""
    batsman_id = request.GET.get('batsman')
    bowler_id = request.GET.get('bowler')

    if not batsman_id or not bowler_id:
        return JsonResponse({'error': 'Both batsman and bowler IDs required'}, status=400)

    batsman = get_object_or_404(Player, pk=batsman_id)
    bowler = get_object_or_404(Player, pk=bowler_id)

    # Phase-wise batting stats
    bat_phases = {}
    for phase in ['powerplay', 'middle', 'death']:
        qs = BattingInnings.objects.filter(player=batsman, phase=phase)
        agg = qs.aggregate(
            runs=Sum('runs'),
            sr=Avg('strike_rate'),
            innings=Count('id'),
        )
        bat_phases[phase] = {
            'runs': agg['runs'] or 0,
            'sr': round(agg['sr'] or 0, 1),
            'innings': agg['innings'],
        }

    # Phase-wise bowling stats
    bowl_phases = {}
    for phase in ['powerplay', 'middle', 'death']:
        qs = BowlingInnings.objects.filter(player=bowler, phase=phase)
        agg = qs.aggregate(
            wickets=Sum('wickets'),
            econ=Avg('economy'),
            innings=Count('id'),
        )
        bowl_phases[phase] = {
            'wickets': agg['wickets'] or 0,
            'econ': round(agg['econ'] or 0, 1),
            'innings': agg['innings'],
        }

    return JsonResponse({
        'batsman': {
            'name': batsman.name,
            'total_runs': batsman.total_runs,
            'total_matches': batsman.total_matches,
            'batting_avg': batsman.batting_avg,
            'strike_rate': batsman.strike_rate,
            'centuries': batsman.centuries,
            'half_centuries': batsman.half_centuries,
            'photo_url': batsman.photo_url,
        },
        'bowler': {
            'name': bowler.name,
            'total_wickets': bowler.total_wickets,
            'total_matches': bowler.total_matches,
            'bowling_avg': bowler.bowling_avg,
            'economy_rate': bowler.economy_rate,
            'best_bowling': bowler.best_bowling,
            'photo_url': bowler.photo_url,
        },
        'batsman_phases': bat_phases,
        'bowler_phases': bowl_phases,
    })