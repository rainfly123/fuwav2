#!/bin/sh
pid=/var/run/putpic
if [ -f $pid ]
   then
   echo "running"
   exit 0
fi

touch $pid

    #files=$(ls *.jpg -t)
    files=$(ls *.jpg -t | head -20)
    for file in $files
    do
            qrsctl put -c wsim fuwa/$file   $file 
         #   rm $file
    done
   
rm $pid
