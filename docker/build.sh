#!/bin/sh

if [ $USER = 'root' ];
then
    docker build -t ta .
else
    sudo docker build -t ta .
fi
