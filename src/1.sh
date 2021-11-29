# process all files from input directory
#for file in input/202101[123]*jpg; do python3 1_eyes_finder.py $file; done

# in case only one file must be processed
for file in input_selected/*.jpg  
do 
    if [ ! -f $file.txt ]; then
        python3 1_eyes_finder.py $file; 
    fi
done
