if [[ $(pwd) != *raw.gm-lang.org ]]
then
	echo "wrong workplace"
	exit 0
fi
# root=$(pwd)

rm -rf src_cache
mkdir src_cache

bash update.sh