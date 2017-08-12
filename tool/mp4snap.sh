#!/bin/sh
pid=/var/run/mp4snap
if [ -f $pid ]
   then
   echo "running"
   exit 0
fi

touch $pid

    files=$(ls *.mp4 -t | head -20)
    for file in $files
        do
        jpg=${file%.*}.jpg
        if [ ! -f $jpg ]
        then
            /ffmpeg/bin/ffmpeg  -loglevel quiet -i $file -vframes 1 -f image2 -y $jpg
          #  nohup qrsctl put -c wsim fuwa/$file   $file &
            /ffmpeg/bin/ffmpeg  -loglevel quiet -i $file -b:v 800k -vcodec libx264 -acodec libfdk_aac -ac 1  -y ttemp.mp4
            mv ttemp.mp4 ${file}
            ./tool.py $jpg
        fi
    done

rm $pid
