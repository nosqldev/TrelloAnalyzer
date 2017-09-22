#!/bin/sh

if [ "$#" -ne 1 ];
then
    echo "error:"
    echo "      ./run.sh TrelloAnalyzer_Path"
    exit 1
fi

if [ $USER = 'root' ];
then
    docker run --rm -it --name trello -v $1:$1 -w $1/docker/anaconda ata
else
    sudo docker run --rm -it --name trello -v $1:$1 -w $1/docker/anaconda ata
fi
