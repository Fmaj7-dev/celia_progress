# process all files from input directory
for file in input/*jpg; do python3 1_eyes_finder.py $file; done

# in case only one file must be processed
#for file in input/20210103.jpg; do python3 1_eyes_finder.py $file; done