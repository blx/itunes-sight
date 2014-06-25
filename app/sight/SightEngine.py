#!/usr/bin/env python

from __future__ import division
from itertools import groupby
import os.path
import plistlib as pll
import urllib2
import mimetypes

import mutagen.mp4, mutagen.id3


class Track(dict):
    
    # Track is guaranteed to have these keys (ie. no KeyError for them) although they might be empty
    guaranteedkeys = ("Track ID, Name, Artist, Album Artist, Album, Genre, Kind"
                      "Size, Total Time, Disc Number, Disc Count, Track Number"
                      "Track Count, Year, Sort Album Artist, Sort Artist, Persistent ID"
                      "Location, Play Count"
                     ).split(', ')
    
    def __init__(self, *args, **kw):
        super(Track, self).__init__({k: None for k in self.guaranteedkeys})
        self.update(*args, **kw)
        
        if not self.get('Play Count'):
            self['Play Count'] = 0


class Album(dict):
    
    def __init__(self, *args, **kw):
        super(Album, self).__init__(*args, **kw)
        
        if not set(['Tracks', 'Artist', 'Album']).issubset(self.keys()):
            raise ValueError("Album must have at least Tracks[], Artist, Album fields.")
        


def sortTracksByPlays(tracks):
    return sorted(tracks,
                  key=lambda t: (-t['Play Count'],
                                  t['Artist'],
                                  t['Name']))


def groupByAlbum(tracks):
    keyfunc = lambda t: (t['Album'], t['Album Artist'], t['Artist'])
    
    tr = [t for t in sorted(tracks, key=keyfunc) if not t.get('Has Video')]
    
    albums = []     # will be list of lists of Track
    albumnames = []
    
    for k, g in groupby(tr, keyfunc):
        albums.append(list(g))
        albumnames.append(k)
    
    return (albums, albumnames)
    

def calculateAlbumPlayCounts(albums):        
    albums = [Album({'Tracks' :  tr,
                     'Artist' :  tr[0].get('Album Artist') or tr[0]['Artist'],
                     'Album'  :  tr[0]['Album'],
                     'Year'   :  tr[0]['Year'],
                     'Album Play Count' : sum(t['Play Count'] for t in tr) / len(tr)**0.5,
                     'Seconds Spent Listening' : sum(t['Play Count'] * t['Total Time'] / 1000 for t in tr)
                   }) for tr in albums]
    
    maxplaycount = max(a['Album Play Count'] for a in albums)
    
    for a in albums:
        a['Album Play Count Normalised'] = a['Album Play Count'] / maxplaycount * 100
    
    return albums



class SightEngine:
    
    def __init__(self, infile):
        self.pl = pll.readPlist(infile)
        self.v = {
            'Catalog File' : infile,
            'Catalog File Size' : os.path.getsize(infile),
            'Music Folder' : urllib2.unquote(self.pl.get('Music Folder'))
        }
        self.tracks = [Track(t) for t in self.pl['Tracks'].itervalues()]

        self.albums = calculateAlbumPlayCounts(groupByAlbum(self.tracks)[0])


    def getTrackByPID(self, persistentid):
        return next((t for t in self.tracks if t['Persistent ID'] == persistentid), False)


    def printMostPlayed(self, n):
        plays = sortTracksByPlays(self.tracks)

        for t in plays[:n]:
            print('[{}] {} - {}'.format(t['Play Count'],
                                        t['Name'],
                                        t['Artist']))


    def getMostPlayedAlbums(self, n=None):
        return sorted(self.albums, key=lambda a: (-a.get('Album Play Count'),
                                                   a['Artist'],
                                                   a['Album']))[:n]
    
    
    def getPlayCountsByAlbumYear(self):
        playcountsbyyear = []
        years = []
        keyfn = lambda a: a.get('Year')
        
        for k, g in groupby(sorted(self.albums, key=keyfn), key=keyfn):
            if not k:
                continue
            
            albums = list(g)
            year = albums[0].get('Year')
            playcounts = sum(tr['Play Count'] for alb in albums for tr in alb['Tracks'])
            albumslist = [{k: a[k] for k in ['Album', 'Artist']} for a in albums]
            
            playcountsbyyear.append({'year': year, 'playCount': playcounts, 'albums': albumslist})
            years.append(k)
        
        return playcountsbyyear    # list of {year: int, playCount: int}
    
    
    def getArtwork(self, persistentid):
        track = self.getTrackByPID(persistentid)
        path = urllib2.unquote(track.get('Location')).decode('utf8').replace('file://localhost', '')
        
        typeguess = mimetypes.guess_type(path)[0]
        
        if 'mp4a' in typeguess:
            file = mutagen.mp4.MP4(path)
            artwork = file.tags.get('covr')
            return artwork[0] if artwork else None
        
        elif 'audio/mpeg' in typeguess:
            file = mutagen.id3.ID3(path)
            try:
                artwork = file.getall('APIC')[0].data
            except IndexError:
                return None
            
            return artwork
        
        return None




def run():
    return SightEngine("/Users/bc/Music/iTunes/iTunes Music Library.xml")    


if __name__ == "__main__":
    se = run()
    se.printMostPlayed(25)
    