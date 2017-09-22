#!/bin/sh

if [ $USER = 'root' ];
then
    docker build -t ata .
else
    sudo docker build -t ata .
fi
