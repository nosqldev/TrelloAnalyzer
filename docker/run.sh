#!/bin/sh

if [ "$#" -ne 2 ];
then
    echo "error:"
    echo "      ./run.sh Anaconda_Path TrelloAnalyzer_Path"
    exit 1
fi

if [ $USER = 'root' ];
then
    docker run --rm -it --name trello -v $1:$1 -v $2:$2 -w $2 --env PATH=$1/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env ANACONDAPATH=$1 ta
else
    sudo docker run --rm -it --name trello -v $1:$1 -v $2:$2 -w $2 --env PATH=$1/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env ANACONDAPATH=$1 ta
fi
