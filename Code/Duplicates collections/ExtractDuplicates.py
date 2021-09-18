"""
Function to and extract info about count of duplicate tracks 
and write on duplicate.txt file.

Author: Kunal Singh
Email: pykunalsingh@gmail.com
"""
#store duplicates as (count, name) tuple
duplicates = []
for k, v in findDuplicates.trackNames.items():
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