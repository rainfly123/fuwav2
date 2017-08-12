#!/bin/sh
pid=/var/run/movsnap
if [ -f $pid ]
   then
   echo "running"
   exit 0
fi

touch $pid

    files=$(ls *.mov -t | head -20)
    for file in $files
        do
        jpg=${file%.*}.jpg
        if [ ! -f $jpg ]
        then
            /ffmpeg/bin/ffmpeg  -loglevel quiet -i $file -vframes 1 -f image2 -y $jpg
          #  nohup qrsctl put -c wsim fuwa/$file   $file & 
            /ffmpeg/bin/ffmpeg  -loglevel quiet -i $file -b:v 800k -vcodec libx264 -acodec libfdk_aac -ac 1  -y temp.mp4
            mv temp.mp4 ${file}
            ./tool.py $jpg
        fi
    done

rm $pid
