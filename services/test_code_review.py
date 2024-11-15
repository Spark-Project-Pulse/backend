# test_code_review.py
from ai_model_service import code_review  # Adjust 'ai_model_service' to the actual module name if different

# Sample test data
project_title = "Spotify Playlist Project"
project_description = '''By utilizing the Open AI API and Spotipy API, this repository allows users to submit a desired playlist theme and have an AI generated playlist automatically created in your Spotify account. I have included two versions of the program - a terminal based program as well as a program including a simple front end which is locally hosted using Flask.

Some playlist theme examples include: "best pop songs from the 2010's", "classical music for studying", "best songs from the artist coldplay", "upbeat songs for a morning run", etc.
The more specific the prompt, the easier it will be for Open AI to interpret.

Keep in mind the AI provided by Open AI is only trained up to September 2021, so it may not know current artists, songs, or music trends.'''
file_name = "main.py"
file_content = '''import json

openai.api_key = "YOUR API KEY"

numSongs = input("Number of Songs (max 50): ")
while int(numSongs) > 50:
    numSongs = input("Number of Songs (max 50): ")
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  max_tokens=1000,
  temperature=0,
  messages=[
    {"role": "system", "content": "You are an assistant that only responds in JSON. Create a list of unique songs based off the user given theme. Include title and artist in your response. An example response is: title: Clocks artist: Coldplay."},
    {"role": "user", "content": "The theme is {0}. Create a list of {1} songs.".format(theme, numSongs)}
  ]
)

content = json.loads(response.choices[0].message.content)
songs_list = []
for i in range(int(numSongs)):
    currSong = content['songs'][i]['title']
    currArtist = content['songs'][i]['artist']
    q = "artist:{0} track:{1}".format(currArtist, currSong)
    results = sp.search(q)
    if len(results["tracks"]["items"]) != 0:
      songs_list.append(results["tracks"]["items"][0]["uri"])
    else:
       q = "track:{0}".format(currSong)
       results = sp.search(q)
       if len(results["tracks"]["items"]) != 0:
        songs_list.append(results["tracks"]["items"][0]["uri"])
playlist_id = sp.user_playlists(username)["items"][0]["id"]
sp.user_playlist_add_tracks(username, playlist_id, songs_list)
'''

# Call the function
suggestions = code_review(project_title, project_description, file_name, file_content)

# Print the output for review
if suggestions:
    print("Suggestions:")
    for suggestion in suggestions:
        print(suggestion)
else:
    print("No suggestions returned or an error occurred.")
