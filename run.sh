#!/bin/bash

PATH_MAIN=`pwd`

mkdir modpacks
mkdir tmp

python3 modpack_download.py

cd modpacks
for filename in `ls`
do
  unzip -o ${filename} manifest.json -d ${PATH_MAIN}/tmp/
  mv "${PATH_MAIN}/tmp/manifest.json" "${PATH_MAIN}/tmp/${filename}"
done

cd ${PATH_MAIN}
python3 modpack_list_analysis.py

rm -rf ./tmp
rm -rf ./modpacks
