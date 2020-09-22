from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse
from django.shortcuts import render
import json
import os

#utility : json database at '/static/json/schema.json'
jsonPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'json', 'schema.json'))
with open(jsonPath) as file:
    library = json.load(file)
    file.close()

#ajax : rate song in db    
def write(song):
    if song is not None:
        library.append(song)
    with open(jsonPath, 'w') as schema:
        json.dump(library, schema)

#utility : store new song in db
def store(track):
    storePath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'songs', track.name))
    with open(storePath, 'wb+') as destination:
        for chunk in track.chunks():
            destination.write(chunk)

#page : index
def index(request):
    return render(request, 'index.html')

#page : contact
def contact(request):
    return render(request, 'contact.html')

#page : artists
def artists(request):
    artist = []
    for song in library:
        if not any(x['name'] == song['artist'] for x in artist):
            artist.append({'name': song['artist'], 'albums': [song['album']],
                           'genres': [song['genre']], 'rating': song['rating']})
            continue
        singer = next(x for x in artist if x['name'] == song['artist'])
        if song['album'] not in singer['albums']:
            singer['albums'].append(song['album'])
        if song['genre'] not in singer['genres']:
            singer['genres'].append(song['genre'])
        singer['rating'] = round((song['rating'] + singer['rating']) / 2, 2)
    return render(request, 'artists.html', {'artists': artist})

#page : albums
def albums(request):
    album = []
    for song in library:
        if song['album'].lower() == 'single':
            continue
        if not any(x['name'] == song['album'] for x in album):
            album.append({'name': song['album'], 'artist': song['artist'],
                          'genre': song['genre'], 'rating': song['rating'], 'songs': 1})
            continue
        record = next(x for x in album if x['name'] == song['album'])
        record['rating'] = round((song['rating'] + record['rating']) / 2, 2)
        record['songs'] += 1
    return render(request, 'albums.html', {'albums': album})

#page : tracks
def tracks(request):
    explore = request.GET.get('search')
    if explore is not None:
        return render(request, 'tracks.html', search(explore))
    for stringType in ['album', 'artist', 'genre']:
        response = handleType(request.GET, stringType)
        if response is not None:
            return render(request, 'tracks.html', response)
    return render(request, 'tracks.html', {'tracks': library, 'type': {'name': 'all'}})

#utility : fetch records
def handleType(getRequest, name):
    stringType = getRequest.get(name)
    if stringType is None:
        return None
    track = [x for x in library if x[name] == stringType]
    return {'tracks': track, 'type': {'name': f"{name.title()}: {stringType}"}}

#ajax/page : search
def search(discover):
    track = []
    explore = discover.lower()
    for stringType in ['name', 'artist', 'album', 'genre']:
        track += [x for x in library if explore in x[stringType].lower()]
    return {'tracks': track, 'type': {'name': f"Search result for {discover}"}}

#page : genres
def genres(request):
    genre = []
    for song in library:
        if not any(x['name'] == song['genre'] for x in genre):
            genre.append({'name': song['genre'], 'songs': 1, 'artists': [song['artist']]})
            continue
        record = next(x for x in genre if x['name'] == song['genre'])
        record['songs'] += 1
        if not any(x == song['artist'] for x in record['artists']):
            record['artists'].append(song['artist'])
    return render(request, 'genres.html', {'genres': genre})

#page : top ten
def topTen(request):
    library.sort(reverse=True, key=lambda x: x['rating'])
    return render(request, 'topten.html', {'top10': library[:10]})

#page : contribute
def contribute(request):
    artist = []
    for song in library:
        if not any(x['name'] == song['artist'] for x in artist):
            artist.append({'name': song['artist'], 'albums': [song['album']]})
            continue
        singer = next(x for x in artist if x['name'] == song['artist'])
        if song['album'] not in singer['albums']:
            singer['albums'].append(song['album'])
    genre = list(set([x['genre'] for x in library]))
    return render(request, 'contribute.html', {'artists': artist, 'genres': genre})


@csrf_exempt
def rated(request):
    if not request.is_ajax():
        raise Http404
    rating = next(x for x in library if x['name'] == request.POST['song'])
    rating['rating'] = round((rating['rating'] + int(request.POST['rate'])) / 2)
    write(None)
    return HttpResponse(json.dumps({'response': f"Thank you for rating {request.POST['rate']} to {request.POST['song']}."}),
                        content_type='application/json')


@csrf_exempt
def addTrack(request):
    if not request.is_ajax():
        raise Http404
    store(request.FILES['track'])
    write({'name': request.POST['name'],
           'artist': request.POST['artist'],
           'album': request.POST['album'],
           'genre': request.POST['genre'],
           'filename': request.FILES['track'].name,
           'rating': int(request.POST['rating'])})
    return HttpResponse(json.dumps({'response': f"Thank you for contributing {request.POST['name']}."}),
                        content_type='application/json')

