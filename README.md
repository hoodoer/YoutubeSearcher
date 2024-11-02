# YoutubeSearcher
Python script to leverage a YouTube search API to create CSV files of searches. Links to videos, titles, description, unique IDs and more are put into the CSV file to import into Excel. 

You can setup an exclude file to leave out youtube videos you've received in previous seaches (based on the unique video_id).

You should install Python virtual environments to isolate the libraries. 

## Install
```
mkdir YoutubeSearcher
python3 -m venv YoutubeSearcher
source YoutubeSearcher/bin/activate
cd YoutubeSearcher
git clone https://github.com/hoodoer/YoutubeSearcher
cd YoutubeSearcher
pip3 install -r requirements.txt
chmod +x youtubeSearch.py
./youtubeSearch.py ./configFile.cfg
```

Directions for configuration are in the example configuration file. 

## Contact
@hoodoer<br>
hoodoer@bitwisemunitions.dev
