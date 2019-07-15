echo "Setting up python environment for Walking Marvin."

#install pip extensions
pip install -r requirements.txt

#download env from repo branch
mkdir dltemp
cd dltemp
curl -OL "https://github.com/qwolf1999/Walking_Marvin/archive/env.zip"
unzip env.zip

#copy env folder to gym
GYMPATH=$(pip show gym | grep Location | cut -f2 -d' ')
GYMPATH=$GYMPATH"/gym/"
cp -rf Walking_Marvin-env/envs/ $GYMPATH

#clean up
cd ..
rm -rf dltemp

echo "Done!"