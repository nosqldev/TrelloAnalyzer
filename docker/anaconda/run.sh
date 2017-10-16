#!/bin/sh

if [ "$#" -ne 1 ];
then
    echo "error:"
    echo "      ./run.sh TrelloAnalyzer_Path"
    exit 1
fi

if [ $USER = 'root' ];
then
    docker run --rm -it --net=host --name trello -v $1:/work -w /work/docker/anaconda ata
else
    sudo docker run --rm -it --net=host --name trello -v $1:/work -w /work/docker/anaconda ata
fi
