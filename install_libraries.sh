# git clone https://github.com/visaub/Forum-Registrer
cd Forum-Registrer

mkvirtualenv myenv36 --python=/usr/bin/python3.6
workon myenv36

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
   pip3 install --user ${install_list[count]}
done
echo -e 'Libraries installed.'

