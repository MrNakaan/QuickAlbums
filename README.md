# Quick Albums

Quick Albums is a fast and easy way to spin up a no-frills server for serving up image galleries. To get running, you only need to do 4 things:

1. Install Python 3.4+
2. Install requirements: `pip install -r requirements.txt`
3. Build your `definitions.txt` file
4. Run quickAlbums.py

The hardest part of this is probably going to be building your definitions file. In `definitions.txt`, each line specifies an album that you want served up. It does this with a pipe (|) delimited list with 4 items. The first item is the album title. The second item is a tilde (~) delimited list of tags for that album. The third item is the path to the directory containing the album. Finally, the fourth item is the name of the HTML file that will be generated for that album. See below for an example.

`Marvel Cinematic Universe Movie Posters|Marvel~Iron Man~Thor~Rocket Raccoon|/var/albums/mcu_posters|mcu`
