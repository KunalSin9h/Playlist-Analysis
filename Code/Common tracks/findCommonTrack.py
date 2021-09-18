"""
given: many files , function will iterate through each file and find a set of
all Tracks and append the sets to a list , after processing all files
we get a list of all sets of tracks.
now by finding the set intersection will yeild the common tracks between the files.

Author: Kunal Singh 
Email: pykunalsingh@gmail.com
"""

def findCommonTrack(fileNames):   # fileNames = list of playlist filenames
    # a list of sets of track names
    trackNameSets = []
    for fileName in fileNames:
        # create a new set
        trackNames = set()
        # read in playlist
        with open(fileName, 'rb') as fb:
            plist = plistlib.load(fb)
        
        # get the tracks
        tracks = plist['Tracks']
        # iterate through the tracks
        for trackId, track in tracks.items():
            try:
                # add the track name to a set
                trackNames.add(track['Name'])
            except:
                # ignore
                pass
        
        # add to a list 
        trackNamesSets.append(trackNames)
    #get the set of common tracks
    commonTracks = set.intersection(*trackNameSets)
    # write to file 
    if len(commonTracks) > 0:
        comn_file = open("common.txt", "w")
        for val in commonTracks:
            s = "%s\n" %val
            comn_file.write(s.encode("UTF-8"))
        comn_file.close()
        print("%d common tracks found. "
                "Track names written to common.txt."%len(commonTracks))
    else:
        print("No common tracks!")
