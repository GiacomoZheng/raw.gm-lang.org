if [[ $(pwd) != *raw.gm-lang.org ]]
then
	echo "wrong workplace"
	exit 0
fi
# root=$(pwd)

python3 index.py