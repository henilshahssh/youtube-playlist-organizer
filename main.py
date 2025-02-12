
from collections import defaultdict
from typing import List, Any
import sys
import requests
import isodate
from dotenv import load_dotenv
import os

def getPlaylistId(arguments: List[str]):
    if len(arguments) == 2:
        playlistId = arguments[1]
        playlistId = playlistId.split("t=")[-1]
    else:
        print("Usage: Only one argument is allowed – the playlist ID.")
        exit(0)

    return playlistId

def getPlaylistItems(playlistId: str, key: str):
    baseUrl = "https://www.googleapis.com/youtube/v3/playlistItems?"
    playlist = "playlistId=" + playlistId
    apiKey = "&key=" + key
    part = "&part=snippet,contentDetails"
    fields = "&fields=nextPageToken,items(snippet/title,contentDetails/videoId)"
    maxResults = "&maxResults=50"
    pageToken = ""

    videoDetails = defaultdict(list)

    while True:
        url = baseUrl + playlist + apiKey + part + fields + maxResults + pageToken

        try:
            apiResponse = requests.get(url)
            if apiResponse.status_code == 200:
                responses = apiResponse.json()
                items = responses['items']

                for item in items:
                    id = item['contentDetails']['videoId']
                    title = item['snippet']['title']
                    videoDetails[id].append(title)
                
                nextPageToken = responses.get('nextPageToken')
                if nextPageToken: 
                    pageToken = "&pageToken=" + nextPageToken
                else:
                    break

            else:
                print('Error:', apiResponse.status_code) 
        except requests.exceptions.RequestException as e:
            print('Error:', e)
    
    return videoDetails

def getVideoIds(videoDetails: defaultdict[Any, list]):
    ids = list(videoDetails.keys())
    chunkSize = 50 # max api limit since pageToken doesnt work with id for video info api

    chunks = [ids[i:i + chunkSize] for i in range(0, len(ids), chunkSize)]
    result = [','.join(chunk) for chunk in chunks]

    return result

def getVideoDuration(videoDetails: defaultdict[Any, list], videoIds: str, key:str):
    baseUrl = "https://www.googleapis.com/youtube/v3/videos?"
    id = "id=" + videoIds
    apiKey = "&key=" + key
    part = "&part=contentDetails"
    fields = "&fields=items(id,contentDetails/duration)"
    maxResults = "&maxResults=50"

    url = baseUrl + id + apiKey + part + fields + maxResults

    try:
        apiResponse = requests.get(url)
        if apiResponse.status_code == 200:
            responses = apiResponse.json()
            items = responses['items']

            for item in items:
                id = item['id']
                duration = item['contentDetails']['duration']
                duration = isodate.parse_duration(duration)
                videoDetails[id].append(duration)
        else:
            print('Error:', apiResponse.status_code) 
    except requests.exceptions.RequestException as e:
        print('Error:', e)
    
    return videoDetails

def getAllVideoDuration(videoIds: list[str], videoDetails: defaultdict[Any, list], apiKey: str):
    for videoId in videoIds:
        videoDetails = getVideoDuration(videoDetails, videoId, apiKey)
    return videoDetails

def sortVideoDetails(videoDetails: defaultdict[Any, list]):
    return dict(sorted(videoDetails.items(), key=lambda item: item[1][1], reverse=True))

def outputToFile(sortedVideoDetails: defaultdict[Any, list]):
    with open("YoutubePlaylistSortedByDuration.txt", "w", encoding='utf-8') as file:
        separator = '\t'
        file.write(f'Title{separator} Link{separator} Duration\n')
        for id, value in sortedVideoDetails.items():
            title = value[0]
            link = "https://www.youtube.com/watch?v=" + id
            duration = value[1]
            file.write(f"{title}{separator} {link}{separator} {duration}\n")

if __name__ == "__main__":
    load_dotenv()
    apiKey = os.getenv("YOUTUBE_API_KEY")
    arguments = sys.argv

    playlistId = getPlaylistId(arguments)
    videoDetails = getPlaylistItems(playlistId, apiKey)
    videoIds = getVideoIds(videoDetails)
    videoDetails = getAllVideoDuration(videoIds, videoDetails, apiKey)
    sortedVideoDetails = sortVideoDetails(videoDetails)
    outputToFile(sortedVideoDetails)