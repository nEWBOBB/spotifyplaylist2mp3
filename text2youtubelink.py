from youtubesearchpython import VideosSearch

# Öffnen der Eingabedatei und Lesen der Suchbegriffe
with open('input.txt', 'r') as f:
    search_terms = f.readlines()

# Durchsuchen von YouTube für jeden Suchbegriff und Speichern des ersten Suchergebnisses
with open('output.txt', 'w') as f:
    for term in search_terms:
        # Entfernen von Zeilenumbrüchen aus den Suchbegriffen
        term = term.strip()
        # Durchsuchen von YouTube für den Suchbegriff
        search = VideosSearch(term, limit=1)
        # Speichern des Links zum ersten Suchergebnis
        results = search.result()
        link = results['result'][0]['link']
        # Schreiben des Links in die Ausgabedatei
        f.write(link + '\n')
