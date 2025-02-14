# YouTube Playlist Sorter by Video Duration
This command-line program allows you to sort YouTube playlists based on the duration of the videos and exports the final sorted list into a file in a CSV-like format with a tab separator (\t). 


## Prerequisites
Before running the program, ensure that you have the following installed and set up:
1. **Python**: Ensure that Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
2. **YouTube API Key**: You will need a YouTube Data API key to fetch the playlist details [How to Get YouTube Data API Key](https://www.youtube.com/watch?v=bk4X_D7gF8U).


## Setup Instructions
### Step 1: Get Your Playlist Link
To get the link to the playlist:
- Navigate to the YouTube playlist you want to sort.
- The link should look like: `https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID`.
- **For the default Watch Later playlist**: 
  - Go to your "Watch Later" playlist.
  - Click on "Shuffle".
  - Add any video to the queue and then save the queue as a playlist.

### Step 2: Create .env File
- Once you have the key, create a `.env` file inside the same folder as `main.py`.
- Add your API key to the `.env` file in the format:
```
YOUTUBE_API_KEY="your_api_key"
```

### Step 3: Install Dependencies

To install the required dependencies, open a terminal/command prompt and navigate to the project folder. Then, run the following command:
```
pip install -r requirements.txt
```

### Step 4: Run the Script
Once everything is set up, run the script with the following command:
```
python main.py [playlist_link]
```
Replace [playlist_link] with the actual URL of your YouTube playlist (obtained in Step 2).


### Step 5: Review the Output
After the script finishes executing, a new file called YoutubePlaylistSortedByDuration.txt will be generated in the same directory. This file will contain the following information for each video:
  - Video Title
  - Video Link
  - Video Duration

The list of videos will be sorted from **shortest to longest duration**.


### Step 6: Import the File to a Spreadsheet
You can easily import the generated file into applications like **Google Sheets** or **Excel**. When importing, make sure to specify the tab (\t) as the separator, as the data is formatted with tab-separated values.

Example Output Format:
The generated YoutubePlaylistSortedByDuration.txt file will look like this:

```
Title	 Link	 Duration
Mingle Game Song “Round and Round” (Lyrics) | Squid Game	 https://www.youtube.com/watch?v=NOkjVIGxju0	 0:01:06
"money money green green" Kaytoven - MONEY! (Lyrics) Good Loyal Thots Remix	 https://www.youtube.com/watch?v=BF5I3Sp4XTg	 0:01:21
Paul Russell - Lil Boo Thang (Lyrics)	 https://www.youtube.com/watch?v=hGcfGSthys0	 0:01:55
Lay Bankz - Ick (Lyrics) "he gave me the ick"	 https://www.youtube.com/watch?v=lJP88cHh-Lw	 0:02:00
Ugly Andz x Prodbycpkshawn - Yo Bunny (Pop Like This Pt.2 Remix) Lyrics	 https://www.youtube.com/watch?v=fu7VKaagUDc	 0:02:02
```
