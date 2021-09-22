import re, argparse
import sys
from matplotlib import pyplot
import plistlib
import numpy as np

def findCommonTrack(fileNames):
    """
    Find common tracks in given playlist files, 
    and save them to common.txt.
    """   
    # a list of sets of track names
    trackNameSets = []
    for fileName in fileNames:
        # create a new set
        trackNames = set()
        # read in playlist
        with open(fileName, 'rb') as fp:
            plist = plistlib.load(fp)
        
        # get the tracks
        tracks = plist['Tracks']
        # iterate through the tracks
        for trackId, track in tracks.items():
            try:
                if (re.search('\d\d\/\d\d\/\d\d\s\d\:\d\d\s[PA]M', track['Name'])):
                    pass
                else:
                    # add the track name to a set
                    trackNames.add(track['Name'])
            except:
                # ignore
                pass
        
        # add to a list 
        trackNameSets.append(trackNames)
    #get the set of common tracks
    commonTracks = set.intersection(*trackNameSets)
    # write to file 
    if len(commonTracks) > 0:
        comn_file = open("common.txt", "w")
        for val in commonTracks:
            s = "%s\n" %val
            comn_file.write(s)
        comn_file.close()
        print("%d common tracks found. "
                "Track names written to common.txt."%len(commonTracks))
    else:
        print("No common tracks!")

def plotStats(fileName):
    """
    Plot some statistics by reading track information from playlist.
    """

    with open(fileName, 'rb') as fp:
        plist = plistlib.load(fp)

    # get the tracks from the playlist
    tracks = plist['Tracks']
    # create lists of songs rating and track durations
    ratings = []
    durations = []

    # iterate through the tracks
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            pass
    # ensure that vaild data was collected
    if ratings == [] or durations == []:
        print("No valid Album Rating/Total Time data in %s."%fileName)
        return


    # scatter plot
    x = np.array(durations, np.int32)
    # convert to minutes
    x = x/60000.0
    y = np.array(ratings, np.int32)
    pyplot.subplot(2, 1, 1)
    pyplot.plot(x, y, 'o')
    pyplot.axis([0, 1.05*np.max(x), -1, 1100])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track rating')

    # plot histogram
    pyplot.subplot(2, 1, 2)
    pyplot.hist(x, bins = 20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    # show plot
    pyplot.show()

def findDuplicates(fileName):
    """
    Find duplicate tracks in given playlist.
    """

    print("Finding duplicate tracks in %s..."%fileName)
    #read in a playlist
    with open(fileName, 'rb') as fp:
        plist = plistlib.load(fp)
    
    # get the track from Tracks dictionary
    tracks = plist['Tracks']  # tracks is dictionary of all the tracks
    
    #create a "track name" dicionary
    trackNames = {}
    
    #iterates through the tracks(the dictionary)
    for trackId, track in tracks.items():  # trackid is track num ex. (86) but track(dict) is info about the track
        try:
            if (re.search('\d\d\/\d\d\/\d\d\s\d\:\d\d\s[PA]M', track['Name'])):
                pass
            else:
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
            


    #store duplicates as (count, name) tuple
    duplicates = []
    for k, v in trackNames.items():
        if v[1] > 1:
            duplicates.append((v[1], k))
    # save duplicates to file
    if len(duplicates) > 0:
        print("Found %d duplicate. Track names saved to duplicate.txt"%len(duplicates))
    else:
        print("No duplicate tracks found!")

    dup_file = open("duplicate.txt", "w")
    for val in duplicates:
        dup_file.write("[%d] %s\n"%(val[0], val[1]))
    dup_file.close()  

# gather our code in a main() function

def main():
    #create parser
    descStr = """
    This program analyzes playlist files (.xml) exported from iTunes.
    """
    parser = argparse.ArgumentParser(description=descStr)
    # add a mutually excusive group of arguments
    group = parser.add_mutually_exclusive_group()

    # add expected arguments
    group.add_argument('--common', nargs='*', dest='plFiles', required=False)
    group.add_argument('--stats', dest='plFile', required=False)
    group.add_argument('--dup', dest='plFileD', required=False)

    # parse args
    args = parser.parse_args()

    if args.plFiles:
        # find common tracks
        findCommonTrack(args.plFiles)
    elif args.plFile:
        # plot stats
        plotStats(args.plFile)
    elif args.plFileD:
        findDuplicates(args.plFileD)
    else:
        print("These are not the tracks you are looking for.")

# main method 
if __name__=='__main__':
    main()