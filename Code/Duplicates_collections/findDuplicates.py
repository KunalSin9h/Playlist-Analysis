"""
Function to process track name and their duration and find the 
count of duplicates if any.

# UNTested!

Author: Kunal Singh 
Email: pykunalsingh@gmail.com
"""

def findDuplicates(fileName):
    print("Finding duplicate tracks in %s..."%fileName)
    #read in a playlist
    plist = plistlib.readPlist(fileName)
    # get the track from Tracks dictionary
    tracks = plist['Tracks']  # tracks is dictionary of all the tracks
    
    #create a "track name" dicionary
    trackNames = {}
    
    #iterates through the tracks(the dictionary)
    for trackId, track in tracks.items():  # trackid is track num ex. (86) but track(dict) is info about the track
        try:
            name = track['Name']
            duration = track['Total Time']
            # look for existing entries
            if name in trackNames:
                #if name and duration match, increment the count
                # round the track length to nearest second
                if duration//1000 == trackNames[name][0]//1000: #tuple[0]
                    count = trackNames[name][1] # tuple[1]
                    trackNames[name] = (duration, count+1)
            else:
                # add dictionary entry as tuple (duration , count)
                trackNames[name] = (duration, 1)
        except:
            pass
            
           

