from django.core.management.base import BaseCommand
from espncricinfo.player import Player as ESPNPlayer
from espncricinfo.team import Team as ESPTeam
from players.models import Player

class Command(BaseCommand):
    help = "Fetch all players from a team or series and save to DB"

    def add_arguments(self, parser):
        parser.add_argument('--team_id', type=str, help='ESPN team ID')

    def handle(self, *args, **kwargs):
        team_id = kwargs['team_id']
        if not team_id:
            self.stdout.write(self.style.ERROR("Please provide a team ID using --team_id"))
            return

        team = ESPTeam(team_id)
        for p in team.players:  # list of ESPN player IDs in the team
            try:
                espn_player = ESPNPlayer(p['id'])
                matches = espn_player.career_stats.get('batting', {}).get('matches', 0)
                runs = espn_player.career_stats.get('batting', {}).get('runs', 0)
                wickets = espn_player.career_stats.get('bowling', {}).get('wickets', 0)

                player, created = Player.objects.update_or_create(
                    name=espn_player.name,
                    defaults={
                        'country': espn_player.country,
                        'role': espn_player.primary_role,
                        'matches': matches,
                        'runs': runs,
                        'wickets': wickets
                    }
                )

                self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'}: {player.name}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to fetch {p['id']}: {e}"))