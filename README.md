# traffic_cam_recorder
A simple tool that provides a JSON file containing data on all hosted cameras on fl511.com and allows one to record and save streamed footage. Most states have a website with a similar structure, so scripts can be easily modified to extract video from any other website instead.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Installation: This project is built on python 3.10.
To install dependencies, run 'python install -r requirements.txt'

To record footage, open the fl511_scraper.py file in your preferred text editor and navigate to the bottom of the script. Follow the instructions commented above the live_video_scraper() function and run the program.
IMPORTANT: The recordings are constructed from raw livestream footage into .mpeg format, so you'll need to play them with a video player that supports mpeg. VLC media player works fine for this and is free. The recordings won't play correctly on the built in video player on windows. 

The provided camera_list.json file in the resources folder is updated as of 6/23/2024. More cameras are added to the site often, so to update the file, simply run the camera_database_scraper.py script. This will replace your current camera_list.json file. The file provided contains data on 4231 cameras.

The map_code.py file is not required to use the program and doesn't interact with any other scripts, but if ran it will construct a folium map displaying the camera's positions from the camera_list.json file and store it in the resources folder. This is an html file you can open in any web browser to visualize the data collected. This map is pretty laggy even on my machine as it renders icons for all ~4000 cameras at once, so use with caution. That said, I do find this to be a preferable visualization over fl511's map as you're not able to render all camera icons at once. This map also displays the names of the cameras when you click on their icons, so it can be used to easily find cameras to record and feed the names into the fl511_scraper.py script. Both description1 and description2 are displayed, so be careful to only select one. They are separated by a comma.
