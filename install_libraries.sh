#!/bin/bash

# git clone https://github.com/visaub/Forum-Registrer

install_list=(
    'flask'
    'flask_login'
    'requests'
    'unidecode'
    'datetime'
    'bs4'
   )
#
# (Loop until we find an empty string.)
#
count=0
while [ "x${install_list[count]}" != "x" ]
do
   count=$(( $count + 1 ))
   echo -e 'Installing: '${install_list[count]}
   pip3 install ${install_list[count]}
done
echo -e 'Libraries installed.'

