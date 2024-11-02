#!/usr/bin/env python3

# simple Python script for 
# searching YouTube with an API key
# and putting results into a CSV file for
# import into Excel or some other spreadsheet
# 
# Contact for help:
# @hoodoer
# hoodoer@bitwisemunitions.dev


import argparse
import csv
from googleapiclient.discovery import build



# This is the function that performs the 
# youtube search
def youtube_search(query, max_results, api_key):
    # Replace 'YOUR_API_KEY' with your actual YouTube Data API key
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Search for videos
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results
    )
    response = request.execute()

    # Get the video informaiton
    videos = []
    for item in response.get('items', []):
        video_id       = item['id']['videoId']
        title          = item['snippet']['title']
        description    = item['snippet']['description']
        channel_name   = item['snippet']['channelTitle']
        published_date = item['snippet']['publishedAt']
        video_id       = item['id']['videoId']
        video_url      = f"https://www.youtube.com/watch?v={video_id}"

        videos.append({
            'title': title,
            'url': video_url,
            'description': description,
            'channel_name': channel_name,
            'published_date': published_date,
            'video_id': video_id,
            'search_term': query
        })

    return videos




# Pull the config info from the file
def parse_config_file(config_file):
    # Reasonable default if one isn't in the config file
    max_results = 100
    search_terms = []
    exclude_file = "NONE"

    with open(config_file, 'r') as file:
        for line in file:
            line = line.strip()

            # Make sure we ignore comment lines in the file
            if not line or line.startswith('#'):
                continue

            if line.startswith("max_results="):
                try:
                    max_results = int(line.split("=", 1)[1].strip())
                except ValueError:
                    print("Invalid max_results value in the config file, using default value")
            elif line.startswith("search_term="):
                term = line.split("=", 1)[1].strip().strip('"')
                search_terms.append(term)
            elif line.startswith("api_key="):
                api_key = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("output_file="):
                output_file = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("exclude_file="):
                exclude_file = line.split("=", 1)[1].strip().strip('"')
               


    print("Configuration:")
    print("   Using API Key: " + api_key)
    print("   Using max_results of: " + str(max_results))
    print("   Using search terms:")
    for term in search_terms:
        print("     -" + term)
    print("   Results to be saved in: " + output_file)
    print()
    print("Starting...")
    print()

    return max_results, search_terms, api_key, output_file, exclude_file



def write_to_csv(filename, videos):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
       # fieldnames = ['Title', 'URL', 'Description', 'Channel', 'Published', 'Unique ID', 'Search Term']
        fieldnames = ['title', 'url', 'description', 'channel_name', 'published_date', 'video_id', 'search_term']
 
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()

        for video in videos:
            video['url'] = f'=HYPERLINK("{video["url"]}", "Video Link")'
            writer.writerow(video)


def main():
    parser = argparse.ArgumentParser(description="Search YouTube videos by keywword")
    parser.add_argument("config_file", type=str, help="Path to configuration file")
    args = parser.parse_args()


    # Get our search configuration
    max_results, search_terms, api_key, output_file, exclude_file = parse_config_file(args.config_file)

    # Let's go find our videos
    all_videos = []

    # We're going to track which videos have already been 
    # returned in a prior search so we can use multiple
    # search terms without having duplicate hits
    seen_video_ids = set()


    # Do we have videos we want to exclude from the search results?
    if exclude_file != "NONE":
        print("Excluding previously seen videos listed in: " + exclude_file)
        with open(exclude_file, 'r') as file:
            for line in file:
                line = line.strip()
                print("-- Excluding video_id: " + line)
                seen_video_ids.add(line)




    for search_term in search_terms:
        videos = youtube_search(search_term, max_results, api_key)

        for video in videos:
            # Get the unique video id
            # check if we've already seen it in results
            video_id = video['video_id']

            if video_id not in seen_video_ids:
                # we haven't had this video result yet, add it to the list
                seen_video_ids.add(video_id)
                all_videos.append(video)


    # Print the results
    # for video in all_videos:
    #     print(f"Title: {video['title']}")
    #     print(f"URL: {video['url']}")
    #     print(f"Description: {video['description']}")
    #     print(f"Channel: {video['channel_name']}")
    #     print(f"Published Date: {video['published_date']}")
    #     print(f"Unique ID: {video['video_id']}")
    #     print(f"Search Term: {video['search_term']}")
       
    #     print()


    # Create the CSV file
    write_to_csv(output_file, all_videos)


    print()
    print("Done.")



if __name__ == "__main__":
    main()
