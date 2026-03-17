import os
import django
import urllib.request
import urllib.parse
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cricket_analyst.settings')
django.setup()

from players.models import Player

def get_wiki_image(name):
    query_name = urllib.parse.quote(name.replace(' ', '_'))
    url = f'https://en.wikipedia.org/w/api.php?action=query&titles={query_name}&prop=pageimages&format=json&pithumbsize=500'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        pages = data.get('query', {}).get('pages', {})
        for page_id in pages:
            if page_id != '-1':
                source = pages[page_id].get('thumbnail', {}).get('source')
                if source:
                    return source
    except Exception as e:
        print(f"Error fetching for {name}: {e}")
    return ''

players = Player.objects.all()
count = 0
for player in players:
    img_url = get_wiki_image(player.name)
    if not img_url:
        print(f"No image found for {player.name}, trying alternative...")
        if ' ' in player.name:
            # try just the first and last name if there's a middle name, etc.
            img_url = get_wiki_image(player.name.split()[0] + ' ' + player.name.split()[-1])
    
    if img_url:
        player.photo_url = img_url
        player.save()
        print(f"Updated {player.name} -> {img_url}")
        count += 1
    else:
        print(f"Still no image for {player.name}")

print(f"Successfully updated {count} players' photos.")
