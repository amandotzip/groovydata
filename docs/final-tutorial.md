# Analyzing the Data of the Spotify Regional Top 200 Songs to Predict Success
Amanuel Awoke

Ferzam Mohammad

Josue Velasquez



![d](https://i.guim.co.uk/img/media/ae483ce4f1bfc5497fee1b5387711d1ff0172ec9/232_0_3268_1963/master/3268.jpg?width=1200&quality=85&auto=format&fit=max&s=fcfceea59329a6bee9c9b75dd8d7a055)

[Image from The Guardian](https://www.theguardian.com/music/2020/mar/19/musicians-ask-spotify-to-triple-payments-to-cover-lost-concert-revenue)

# Introduction
## Motivation
The music industry has changed a lot in the last decade with the introduction of streaming services like Apple Music or Spotify. Services like Spotify allow users to livestream music for personal consumption, often for free or for a subscription fee. These services have made it easier to consume music and have increased opportunities for people to start producing music, but they have also changed how musicians make money. Whenever a user listens to a song on a streaming service, the service typically keeps track of the number of “plays” that song has. Music artists are then paid a small amount based on the number of plays they have accumulated for their music. Given how little these artists are paid from streaming services, maximizing the amount of revenue made from a song seems pretty valuable for those looking to push out music to these services. Play count also indicates where a song stands in the streaming services’ popularity lists, and making it onto their top 100 or 200 songs is a factor considered in whether these songs are added to global, official top songs charts i.e. Billboard 200.
 
Our group thought it would be interesting to see if we could try to make predictions for how popular a song might be given different features for a song (e.g. the genre of the song, how fast or slow it is, the key the song is written in, the time of year a song was released, how many listeners an artist already gets on average, etc.). If we can indicate how many plays a song will get, we can give a prediction for how much money a song will make on a streaming service. Much like the Moneyball scenario, it’s possible that artists are focusing on producing music that meets criteria which they think makes a song popular when, in reality, they should be focusing on other aspects of their music. Understanding what components of a song make it popular would help artists figure out the best way to produce music in order to make money off of these streaming services.

The Moneyball story demonstrated the importance of data science in producing a strong baseball team, and while music is different from sports, our project should hopefully reflect similar data science practices in order to reach a valuable conclusion. It may be relatively straightforward to look at aspects like which genres make the most money or whether a song by Taylor Swift will end up on the top 200 chart given her “incredibly loyal fanbase” of over 40 million people, but maybe there are other similarities between popular songs that could indicate factors which help make a song more popular. Data science practices like t-tests (maybe) or machine learning models help us here by giving us tools to help identify characteristics in a song, clarify how those characteristics might relate to play count, and predict what the play count (or popularity) for a similar song could be given factors that we have determined have an affect on play count (or popularity)
<One valuable conclusion might be the LACK OF money artists are being paid from streaming services, or how little they make off streaming services alone>

From this point forward when we use the word "track" it is synonymous with "song."

## Goal Hypothesis
Are there traits of a song that can be used to determine future success? If so, what are they?
## Defining Success
We are defining the success of a track by its appearance on the Top 200, as well as its ranking on the Top 200 (the higher the better).


# Collect Data

This is the first step in the data lifecycle where we must identify information to web scrape. We gather data from the [Spotify Charts Regional Top 200](https://spotifycharts.com/regional) to first identify which songs had the highest stream counts in the United States, dating back to January 1st 2017, to current day. Spotify Charts provides tracks with the highest stream count, their top 200 rank, and the artist(s) who created that song. Spotify Charts already compiles the data into Excel tables, so it isn't necessary to directly scrape from the website. If you wanted to download one yourself, at the top right of the website, select a date you'd like to download in the dropdown, then select further up "Download to CSV." The pandas method read_csv() was used to process the Excel files into dataframes.




```python
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import spotipy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

Since there were consistent download URLs of Excel sheets in relation to the date they recorded, we used a looped to retreive the links then later download all sheets.


```python
# Collect links from spotify charts top 200 streams per day
ref_str = "https://spotifycharts.com/regional/global/daily/"
ref_arr = []
# gets every day from janurary 2017 to October 2020

for year in range(2017, 2018):
    date = ""
    
    endingMonth = 12
    if year == 2020:
        endingMonth = 10
        
    for month in range (1, endingMonth + 1):
       
        dayCount = -1

        #gets proper day count per month
        thirtyDayCountMonths = [4, 6, 9, 11]
        if month == 2:
            dayCount = 29
        elif month in thirtyDayCountMonths:
            dayCount = 30
        else:
            dayCount = 31

        if int(month) < 10:
            month = "0" + str(month)

        #Get specific days
        # for day in range (1, daycount + 1):
        #     if int(day) < 10:
        #       day = "0" + str(day)

        date = str(year) + "-" + str(month) + "-" + "01" + "/download"
        date = ref_str + date
        ref_arr.append(date)

ref_arr
```




    ['https://spotifycharts.com/regional/global/daily/2017-01-01/download',
     'https://spotifycharts.com/regional/global/daily/2017-02-01/download',
     'https://spotifycharts.com/regional/global/daily/2017-03-01/download',
     'https://spotifycharts.com/regional/global/daily/2017-04-01/download',
     'https://spotifycharts.com/regional/global/daily/2017-05-01/download',
     'https://spotifycharts.com/regional/global/daily/2017-06-01/download',
     'https://spotifycharts.com/regional/global/daily/2017-07-01/download',
     'https://spotifycharts.com/regional/global/daily/2017-08-01/download',
     'https://spotifycharts.com/regional/global/daily/2017-09-01/download',
     'https://spotifycharts.com/regional/global/daily/2017-10-01/download',
     'https://spotifycharts.com/regional/global/daily/2017-11-01/download',
     'https://spotifycharts.com/regional/global/daily/2017-12-01/download']




```python
#Loop downloading and appending of dataframes 

df = pd.DataFrame(columns =['position', 'track_name', 'artist', 'streams', 'url', 'date'] )
#make dir to save to
path = "sheets"
folderExists = False
try:
    os.mkdir(path)
except FileExistsError:
    print ("Folder already exists")
    folderExists = True

for i in ref_arr:

    r = requests.get(i, allow_redirects = True)
    #String manipulation to read from the correct csv files
    date = i[48:58]
    fileName = "regional-global-daily-" + date + ".csv"
    if not folderExists:
        print("Downloading... " + fileName)
        open(fileName, "wb").write(r.content)

        os.rename(fileName, "sheets/" + fileName)

    df_new = pd.read_csv(path + "/" + fileName)
    df_new.columns= ['position', 'track_name', 'artist', 'streams', 'url']
    df_new['date'] = date
    
    df_new = df_new.iloc[1:] #deletes junk row from csv conversion
    df = df.append(df_new)

print("Done")
df = df.reset_index() # Sets index back to being the regular 0-based index. This is really helpful when trying to add more to the dataframe later, because otherwise there are lots of duplicate indices
df['streams'] = df['streams'].astype(int) #streams are a string of a num, must wrap as type int always
```

    Folder already exists
    Done
    

## Wrangled data into dataframe


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>position</th>
      <th>track_name</th>
      <th>artist</th>
      <th>streams</th>
      <th>url</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>Starboy</td>
      <td>The Weeknd</td>
      <td>3135625</td>
      <td>https://open.spotify.com/track/5aAx2yezTd8zXrk...</td>
      <td>2017-01-01</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2</td>
      <td>Closer</td>
      <td>The Chainsmokers</td>
      <td>3015525</td>
      <td>https://open.spotify.com/track/7BKLCZ1jbUBVqRi...</td>
      <td>2017-01-01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>3</td>
      <td>Let Me Love You</td>
      <td>DJ Snake</td>
      <td>2545384</td>
      <td>https://open.spotify.com/track/4pdPtRcBmOSQDlJ...</td>
      <td>2017-01-01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>4</td>
      <td>Rockabye (feat. Sean Paul &amp; Anne-Marie)</td>
      <td>Clean Bandit</td>
      <td>2356604</td>
      <td>https://open.spotify.com/track/5knuzwU65gJK7IF...</td>
      <td>2017-01-01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>5</td>
      <td>One Dance</td>
      <td>Drake</td>
      <td>2259887</td>
      <td>https://open.spotify.com/track/1xznGGDReH1oQq0...</td>
      <td>2017-01-01</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2395</th>
      <td>196</td>
      <td>196</td>
      <td>Rockabye (feat. Sean Paul &amp; Anne-Marie)</td>
      <td>Clean Bandit</td>
      <td>552118</td>
      <td>https://open.spotify.com/track/5knuzwU65gJK7IF...</td>
      <td>2017-12-01</td>
    </tr>
    <tr>
      <th>2396</th>
      <td>197</td>
      <td>197</td>
      <td>Rake It Up (feat. Nicki Minaj)</td>
      <td>Yo Gotti</td>
      <td>551576</td>
      <td>https://open.spotify.com/track/4knL4iPxPOZjQzT...</td>
      <td>2017-12-01</td>
    </tr>
    <tr>
      <th>2397</th>
      <td>198</td>
      <td>198</td>
      <td>New Freezer (feat. Kendrick Lamar)</td>
      <td>Rich The Kid</td>
      <td>550167</td>
      <td>https://open.spotify.com/track/4pYZLpX23Vx8rwD...</td>
      <td>2017-12-01</td>
    </tr>
    <tr>
      <th>2398</th>
      <td>199</td>
      <td>199</td>
      <td>All Night</td>
      <td>Steve Aoki</td>
      <td>548039</td>
      <td>https://open.spotify.com/track/5mAxA6Q1SIym6dP...</td>
      <td>2017-12-01</td>
    </tr>
    <tr>
      <th>2399</th>
      <td>200</td>
      <td>200</td>
      <td>113</td>
      <td>Booba</td>
      <td>546878</td>
      <td>https://open.spotify.com/track/6xqAP7kpdgCy8lE...</td>
      <td>2017-12-01</td>
    </tr>
  </tbody>
</table>
<p>2400 rows × 7 columns</p>
</div>



# Data Processing

[Spotipy](https://spotipy.readthedocs.io/en/2.16.1/#) is a lightweight Python library for the [Spotify Web API](https://developer.spotify.com/documentation/web-api/) used to retrieve more detailed data for tracks now that their names have been retrieved from the Spotify Top 200. We must first authenticate our usage of the API.


```python
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


SPOTIPY_CLIENT_ID="ea1a162fbc6f413990542b76ab82a168"
SPOTIPY_CLIENT_SECRET="a09882042ce54f158fdd2b6baaf2b26d"
SPOTIPY_CLIENT_REDIRECT="http://www.cs.umd.edu/class/fall2020/cmsc320-0201/"

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_CLIENT_REDIRECT))


```

We're going to start by using the Spotify API to get more information about all the tracks we found in the top 200's chart for the timeframe we described above. The Spotify API gives us the ability to get "audio features" from a song given a song id that Spotify creates for every track. These "audio features" include characteristics like loudness, positivity, danceability, how energetic the song is, the speed of the song, and a couple other similar characteristics that have been determined by Spotify using their own machine learning algorithms.

First, we do need to get an id for every song and artist in our dataframe to be able to make queries through the Spotify API for a specific track or artist. Here, we get track and artist ids, and we also make a query for the audio features of each track id. We're doing these together for code efficiency, just because a large number of queries through the Spotify API can take time.


```python
import xlsxwriter
import openpyxl

artist_id_list = []
track_id_list = []
popularity_index_list = []
follower_count_list = []
audio_features_df = pd.DataFrame()

genre_list = []
genre_filter = ["rap", "pop", "edm", "rock", "other"]



#if cached df exists dont search again, else search again
if not os.path.exists("cached_df.xlsx"):
    #Take each song and lookup its audio features, then create a dataframe for them
    print("Searching...")
    for index, row in df.iterrows():
        trackName = row['track_name']
        track_id = ""
        artist_id = ""
        # We need to check if our track_name received was a nan value. Idk how these got in here, but there are nans
        if(type(trackName) == str):
            #delimit with +'s for spotipy search query
            trackNameWithoutSpaces = '+'.join(trackName.split())
            searchQuery = sp.search(trackNameWithoutSpaces, 1, 0)
            if (len(searchQuery['tracks']['items']) != 0):
                
                track_object = searchQuery['tracks']['items'][0]
                track_id = track_object['id']
                track_id_list.append(track_id)

                #if there are several artists, return the first artist
                artist_object = track_object['artists'][0] if type(track_object['artists']) is list else track_object['artists']
                artist_id = artist_object['id']
                artist_id_list.append(artist_id)

    
                artist_object_real = sp.artist(artist_id)
                # print(artist_object_real)
                followers_object = artist_object_real['followers']
                followers_value = followers_object['total']
                follower_count_list.append(followers_value)
                popularity_value = artist_object_real['popularity']
                popularity_index_list.append(popularity_value)

                # if artist_object_real['genres']
                    # genre_value = "Rap"
                # genre_list.append(genre_value)
                # print(genre_list)



                # print(popularity_index_list)


            # If our query returned nothing then append a nan in the place of artist and track for this entry
            else:
                artist_id_list.append(np.nan)
                track_id_list.append(np.nan)
                
                popularity_index_list.append(np.nan)
                follower_count_list.append(np.nan)

                genre_list.append(np.nan)
        # If we had stored a nan, then just plan to append a nan in this position
        else:
            artist_id_list.append(np.nan)
            track_id_list.append(np.nan)
            
            popularity_index_list.append(np.nan)
            follower_count_list.append(np.nan)

            genre_list.append(np.nan)

       
        #Defining audio features as nan to begin    
        audiofeatures = {'duration_ms' : np.nan, 'key' : np.nan, 'mode' : np.nan, 'time_signature' : np.nan, 'acousticness' : np.nan, 'danceability' : np.nan, 'energy' : np.nan, 'instrumentalness' : np.nan, 'liveness' : np.nan, 'loudness' : np.nan, 'speechiness' : np.nan, 'valence' : np.nan, 'tempo' : np.nan, 'id' : np.nan, 'uri' : np.nan, 'track_href' : np.nan, 'analysis_url' : np.nan, 'type' : np.nan, }

        # If we successfully found a track when we did our search, then get the audio features for that
        if (track_id != ""):
            audiofeatures = sp.audio_features(track_id)[0]
        #Append the audio features
        audio_features_df = audio_features_df.append(audiofeatures, ignore_index=True)

    #adds artist id list 
    audio_features_df['artist_id'] = artist_id_list 
    audio_features_df['popularity_index'] = popularity_index_list
    audio_features_df['follower_count'] = follower_count_list

    # audio_features_df['genre'] = genre_list

    # Store the created data frame into the cache
    writer = pd.ExcelWriter('cached_df.xlsx', engine='openpyxl')
    audio_features_df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    
else: #access the cached df if it exist
 
    print("Cached dataframe found.")
    audio_features_df = pd.read_excel("cached_df.xlsx", engine = "openpyxl")
    audio_features_df.drop(["Unnamed: 0"], axis=1, inplace=True) #delete position row since rank alraedy has this information

audio_features_df
```

    Cached dataframe found.
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>acousticness</th>
      <th>analysis_url</th>
      <th>danceability</th>
      <th>duration_ms</th>
      <th>energy</th>
      <th>id</th>
      <th>instrumentalness</th>
      <th>key</th>
      <th>liveness</th>
      <th>loudness</th>
      <th>...</th>
      <th>speechiness</th>
      <th>tempo</th>
      <th>time_signature</th>
      <th>track_href</th>
      <th>type</th>
      <th>uri</th>
      <th>valence</th>
      <th>artist_id</th>
      <th>popularity_index</th>
      <th>follower_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.14100</td>
      <td>https://api.spotify.com/v1/audio-analysis/7MXV...</td>
      <td>0.679</td>
      <td>230453.0</td>
      <td>0.587</td>
      <td>7MXVkk9YMctZqd1Srtv4MB</td>
      <td>0.000006</td>
      <td>7.0</td>
      <td>0.137</td>
      <td>-7.015</td>
      <td>...</td>
      <td>0.2760</td>
      <td>186.003</td>
      <td>4.0</td>
      <td>https://api.spotify.com/v1/tracks/7MXVkk9YMctZ...</td>
      <td>audio_features</td>
      <td>spotify:track:7MXVkk9YMctZqd1Srtv4MB</td>
      <td>0.486</td>
      <td>1Xyo4u8uXC1ZmMpatF05PJ</td>
      <td>94.0</td>
      <td>26720759.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.41400</td>
      <td>https://api.spotify.com/v1/audio-analysis/7BKL...</td>
      <td>0.748</td>
      <td>244960.0</td>
      <td>0.524</td>
      <td>7BKLCZ1jbUBVqRi2FVlTVw</td>
      <td>0.000000</td>
      <td>8.0</td>
      <td>0.111</td>
      <td>-5.599</td>
      <td>...</td>
      <td>0.0338</td>
      <td>95.010</td>
      <td>4.0</td>
      <td>https://api.spotify.com/v1/tracks/7BKLCZ1jbUBV...</td>
      <td>audio_features</td>
      <td>spotify:track:7BKLCZ1jbUBVqRi2FVlTVw</td>
      <td>0.661</td>
      <td>69GGBxA162lTqCwzJG5jLp</td>
      <td>84.0</td>
      <td>17093912.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.23500</td>
      <td>https://api.spotify.com/v1/audio-analysis/3ibK...</td>
      <td>0.656</td>
      <td>256733.0</td>
      <td>0.578</td>
      <td>3ibKnFDaa3GhpPGlOUj7ff</td>
      <td>0.000000</td>
      <td>7.0</td>
      <td>0.118</td>
      <td>-8.970</td>
      <td>...</td>
      <td>0.0922</td>
      <td>94.514</td>
      <td>4.0</td>
      <td>https://api.spotify.com/v1/tracks/3ibKnFDaa3Gh...</td>
      <td>audio_features</td>
      <td>spotify:track:3ibKnFDaa3GhpPGlOUj7ff</td>
      <td>0.556</td>
      <td>20s0P9QLxGqKuCsGwFsp7w</td>
      <td>69.0</td>
      <td>2055274.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.40600</td>
      <td>https://api.spotify.com/v1/audio-analysis/5knu...</td>
      <td>0.720</td>
      <td>251088.0</td>
      <td>0.763</td>
      <td>5knuzwU65gJK7IF5yJsuaW</td>
      <td>0.000000</td>
      <td>9.0</td>
      <td>0.180</td>
      <td>-4.068</td>
      <td>...</td>
      <td>0.0523</td>
      <td>101.965</td>
      <td>4.0</td>
      <td>https://api.spotify.com/v1/tracks/5knuzwU65gJK...</td>
      <td>audio_features</td>
      <td>spotify:track:5knuzwU65gJK7IF5yJsuaW</td>
      <td>0.742</td>
      <td>6MDME20pz9RveH9rEXvrOM</td>
      <td>80.0</td>
      <td>4092589.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.00776</td>
      <td>https://api.spotify.com/v1/audio-analysis/1zi7...</td>
      <td>0.792</td>
      <td>173987.0</td>
      <td>0.625</td>
      <td>1zi7xx7UVEFkmKfv06H8x0</td>
      <td>0.001800</td>
      <td>1.0</td>
      <td>0.329</td>
      <td>-5.609</td>
      <td>...</td>
      <td>0.0536</td>
      <td>103.967</td>
      <td>4.0</td>
      <td>https://api.spotify.com/v1/tracks/1zi7xx7UVEFk...</td>
      <td>audio_features</td>
      <td>spotify:track:1zi7xx7UVEFkmKfv06H8x0</td>
      <td>0.370</td>
      <td>3TVXtAsR1Inumwj472S9r4</td>
      <td>96.0</td>
      <td>51374698.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2395</th>
      <td>0.40600</td>
      <td>https://api.spotify.com/v1/audio-analysis/5knu...</td>
      <td>0.720</td>
      <td>251088.0</td>
      <td>0.763</td>
      <td>5knuzwU65gJK7IF5yJsuaW</td>
      <td>0.000000</td>
      <td>9.0</td>
      <td>0.180</td>
      <td>-4.068</td>
      <td>...</td>
      <td>0.0523</td>
      <td>101.965</td>
      <td>4.0</td>
      <td>https://api.spotify.com/v1/tracks/5knuzwU65gJK...</td>
      <td>audio_features</td>
      <td>spotify:track:5knuzwU65gJK7IF5yJsuaW</td>
      <td>0.742</td>
      <td>6MDME20pz9RveH9rEXvrOM</td>
      <td>80.0</td>
      <td>4092589.0</td>
    </tr>
    <tr>
      <th>2396</th>
      <td>0.02200</td>
      <td>https://api.spotify.com/v1/audio-analysis/4knL...</td>
      <td>0.910</td>
      <td>276333.0</td>
      <td>0.444</td>
      <td>4knL4iPxPOZjQzTUlELGSY</td>
      <td>0.000000</td>
      <td>1.0</td>
      <td>0.137</td>
      <td>-8.126</td>
      <td>...</td>
      <td>0.3440</td>
      <td>149.953</td>
      <td>4.0</td>
      <td>https://api.spotify.com/v1/tracks/4knL4iPxPOZj...</td>
      <td>audio_features</td>
      <td>spotify:track:4knL4iPxPOZjQzTUlELGSY</td>
      <td>0.530</td>
      <td>6Ha4aES39QiVjR0L2lwuwq</td>
      <td>75.0</td>
      <td>3109571.0</td>
    </tr>
    <tr>
      <th>2397</th>
      <td>0.04050</td>
      <td>https://api.spotify.com/v1/audio-analysis/2EgB...</td>
      <td>0.884</td>
      <td>191938.0</td>
      <td>0.698</td>
      <td>2EgB4n6XyBsuNUbuarr4eG</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.195</td>
      <td>-9.101</td>
      <td>...</td>
      <td>0.3640</td>
      <td>140.068</td>
      <td>4.0</td>
      <td>https://api.spotify.com/v1/tracks/2EgB4n6XyBsu...</td>
      <td>audio_features</td>
      <td>spotify:track:2EgB4n6XyBsuNUbuarr4eG</td>
      <td>0.575</td>
      <td>1pPmIToKXyGdsCF6LmqLmI</td>
      <td>78.0</td>
      <td>2419234.0</td>
    </tr>
    <tr>
      <th>2398</th>
      <td>0.00410</td>
      <td>https://api.spotify.com/v1/audio-analysis/0dXN...</td>
      <td>0.538</td>
      <td>197640.0</td>
      <td>0.804</td>
      <td>0dXNQ8dckG4eYfEtq9zcva</td>
      <td>0.000000</td>
      <td>8.0</td>
      <td>0.330</td>
      <td>-5.194</td>
      <td>...</td>
      <td>0.0358</td>
      <td>144.992</td>
      <td>4.0</td>
      <td>https://api.spotify.com/v1/tracks/0dXNQ8dckG4e...</td>
      <td>audio_features</td>
      <td>spotify:track:0dXNQ8dckG4eYfEtq9zcva</td>
      <td>0.507</td>
      <td>7gAppWoH7pcYmphCVTXkzs</td>
      <td>76.0</td>
      <td>4082406.0</td>
    </tr>
    <tr>
      <th>2399</th>
      <td>0.00805</td>
      <td>https://api.spotify.com/v1/audio-analysis/0leV...</td>
      <td>0.740</td>
      <td>266672.0</td>
      <td>0.510</td>
      <td>0leVyLipY7A8ruhkIBqc0E</td>
      <td>0.000375</td>
      <td>9.0</td>
      <td>0.128</td>
      <td>-8.042</td>
      <td>...</td>
      <td>0.0780</td>
      <td>141.534</td>
      <td>5.0</td>
      <td>https://api.spotify.com/v1/tracks/0leVyLipY7A8...</td>
      <td>audio_features</td>
      <td>spotify:track:0leVyLipY7A8ruhkIBqc0E</td>
      <td>0.089</td>
      <td>0JOxt5QOwq0czoJxvSc5hS</td>
      <td>70.0</td>
      <td>168927.0</td>
    </tr>
  </tbody>
</table>
<p>2400 rows × 21 columns</p>
</div>




```python

#Append audio features to master dataframe
df['track_id'] = audio_features_df['id']
df['duration_ms'] = audio_features_df['duration_ms']
df['acousticness'] = audio_features_df['acousticness']
df['danceability'] = audio_features_df['danceability']
df['energy'] = audio_features_df['energy']
df['instrumentalness'] = audio_features_df['instrumentalness']
df['liveness'] = audio_features_df['liveness']
df['loudness'] = audio_features_df['loudness']
df['speechiness'] = audio_features_df['speechiness']
df['valence'] = audio_features_df['valence']
df['tempo'] = audio_features_df['tempo']
df['artist_id'] = audio_features_df['artist_id']
df['popularity_index'] = audio_features_df['popularity_index']
df['follower_count'] = audio_features_df['follower_count']

df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>position</th>
      <th>track_name</th>
      <th>artist</th>
      <th>streams</th>
      <th>url</th>
      <th>date</th>
      <th>track_id</th>
      <th>duration_ms</th>
      <th>acousticness</th>
      <th>...</th>
      <th>energy</th>
      <th>instrumentalness</th>
      <th>liveness</th>
      <th>loudness</th>
      <th>speechiness</th>
      <th>valence</th>
      <th>tempo</th>
      <th>artist_id</th>
      <th>popularity_index</th>
      <th>follower_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>Starboy</td>
      <td>The Weeknd</td>
      <td>3135625</td>
      <td>https://open.spotify.com/track/5aAx2yezTd8zXrk...</td>
      <td>2017-01-01</td>
      <td>7MXVkk9YMctZqd1Srtv4MB</td>
      <td>230453.0</td>
      <td>0.14100</td>
      <td>...</td>
      <td>0.587</td>
      <td>0.000006</td>
      <td>0.137</td>
      <td>-7.015</td>
      <td>0.2760</td>
      <td>0.486</td>
      <td>186.003</td>
      <td>1Xyo4u8uXC1ZmMpatF05PJ</td>
      <td>94.0</td>
      <td>26720759.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2</td>
      <td>Closer</td>
      <td>The Chainsmokers</td>
      <td>3015525</td>
      <td>https://open.spotify.com/track/7BKLCZ1jbUBVqRi...</td>
      <td>2017-01-01</td>
      <td>7BKLCZ1jbUBVqRi2FVlTVw</td>
      <td>244960.0</td>
      <td>0.41400</td>
      <td>...</td>
      <td>0.524</td>
      <td>0.000000</td>
      <td>0.111</td>
      <td>-5.599</td>
      <td>0.0338</td>
      <td>0.661</td>
      <td>95.010</td>
      <td>69GGBxA162lTqCwzJG5jLp</td>
      <td>84.0</td>
      <td>17093912.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>3</td>
      <td>Let Me Love You</td>
      <td>DJ Snake</td>
      <td>2545384</td>
      <td>https://open.spotify.com/track/4pdPtRcBmOSQDlJ...</td>
      <td>2017-01-01</td>
      <td>3ibKnFDaa3GhpPGlOUj7ff</td>
      <td>256733.0</td>
      <td>0.23500</td>
      <td>...</td>
      <td>0.578</td>
      <td>0.000000</td>
      <td>0.118</td>
      <td>-8.970</td>
      <td>0.0922</td>
      <td>0.556</td>
      <td>94.514</td>
      <td>20s0P9QLxGqKuCsGwFsp7w</td>
      <td>69.0</td>
      <td>2055274.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>4</td>
      <td>Rockabye (feat. Sean Paul &amp; Anne-Marie)</td>
      <td>Clean Bandit</td>
      <td>2356604</td>
      <td>https://open.spotify.com/track/5knuzwU65gJK7IF...</td>
      <td>2017-01-01</td>
      <td>5knuzwU65gJK7IF5yJsuaW</td>
      <td>251088.0</td>
      <td>0.40600</td>
      <td>...</td>
      <td>0.763</td>
      <td>0.000000</td>
      <td>0.180</td>
      <td>-4.068</td>
      <td>0.0523</td>
      <td>0.742</td>
      <td>101.965</td>
      <td>6MDME20pz9RveH9rEXvrOM</td>
      <td>80.0</td>
      <td>4092589.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>5</td>
      <td>One Dance</td>
      <td>Drake</td>
      <td>2259887</td>
      <td>https://open.spotify.com/track/1xznGGDReH1oQq0...</td>
      <td>2017-01-01</td>
      <td>1zi7xx7UVEFkmKfv06H8x0</td>
      <td>173987.0</td>
      <td>0.00776</td>
      <td>...</td>
      <td>0.625</td>
      <td>0.001800</td>
      <td>0.329</td>
      <td>-5.609</td>
      <td>0.0536</td>
      <td>0.370</td>
      <td>103.967</td>
      <td>3TVXtAsR1Inumwj472S9r4</td>
      <td>96.0</td>
      <td>51374698.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2395</th>
      <td>196</td>
      <td>196</td>
      <td>Rockabye (feat. Sean Paul &amp; Anne-Marie)</td>
      <td>Clean Bandit</td>
      <td>552118</td>
      <td>https://open.spotify.com/track/5knuzwU65gJK7IF...</td>
      <td>2017-12-01</td>
      <td>5knuzwU65gJK7IF5yJsuaW</td>
      <td>251088.0</td>
      <td>0.40600</td>
      <td>...</td>
      <td>0.763</td>
      <td>0.000000</td>
      <td>0.180</td>
      <td>-4.068</td>
      <td>0.0523</td>
      <td>0.742</td>
      <td>101.965</td>
      <td>6MDME20pz9RveH9rEXvrOM</td>
      <td>80.0</td>
      <td>4092589.0</td>
    </tr>
    <tr>
      <th>2396</th>
      <td>197</td>
      <td>197</td>
      <td>Rake It Up (feat. Nicki Minaj)</td>
      <td>Yo Gotti</td>
      <td>551576</td>
      <td>https://open.spotify.com/track/4knL4iPxPOZjQzT...</td>
      <td>2017-12-01</td>
      <td>4knL4iPxPOZjQzTUlELGSY</td>
      <td>276333.0</td>
      <td>0.02200</td>
      <td>...</td>
      <td>0.444</td>
      <td>0.000000</td>
      <td>0.137</td>
      <td>-8.126</td>
      <td>0.3440</td>
      <td>0.530</td>
      <td>149.953</td>
      <td>6Ha4aES39QiVjR0L2lwuwq</td>
      <td>75.0</td>
      <td>3109571.0</td>
    </tr>
    <tr>
      <th>2397</th>
      <td>198</td>
      <td>198</td>
      <td>New Freezer (feat. Kendrick Lamar)</td>
      <td>Rich The Kid</td>
      <td>550167</td>
      <td>https://open.spotify.com/track/4pYZLpX23Vx8rwD...</td>
      <td>2017-12-01</td>
      <td>2EgB4n6XyBsuNUbuarr4eG</td>
      <td>191938.0</td>
      <td>0.04050</td>
      <td>...</td>
      <td>0.698</td>
      <td>0.000000</td>
      <td>0.195</td>
      <td>-9.101</td>
      <td>0.3640</td>
      <td>0.575</td>
      <td>140.068</td>
      <td>1pPmIToKXyGdsCF6LmqLmI</td>
      <td>78.0</td>
      <td>2419234.0</td>
    </tr>
    <tr>
      <th>2398</th>
      <td>199</td>
      <td>199</td>
      <td>All Night</td>
      <td>Steve Aoki</td>
      <td>548039</td>
      <td>https://open.spotify.com/track/5mAxA6Q1SIym6dP...</td>
      <td>2017-12-01</td>
      <td>0dXNQ8dckG4eYfEtq9zcva</td>
      <td>197640.0</td>
      <td>0.00410</td>
      <td>...</td>
      <td>0.804</td>
      <td>0.000000</td>
      <td>0.330</td>
      <td>-5.194</td>
      <td>0.0358</td>
      <td>0.507</td>
      <td>144.992</td>
      <td>7gAppWoH7pcYmphCVTXkzs</td>
      <td>76.0</td>
      <td>4082406.0</td>
    </tr>
    <tr>
      <th>2399</th>
      <td>200</td>
      <td>200</td>
      <td>113</td>
      <td>Booba</td>
      <td>546878</td>
      <td>https://open.spotify.com/track/6xqAP7kpdgCy8lE...</td>
      <td>2017-12-01</td>
      <td>0leVyLipY7A8ruhkIBqc0E</td>
      <td>266672.0</td>
      <td>0.00805</td>
      <td>...</td>
      <td>0.510</td>
      <td>0.000375</td>
      <td>0.128</td>
      <td>-8.042</td>
      <td>0.0780</td>
      <td>0.089</td>
      <td>141.534</td>
      <td>0JOxt5QOwq0czoJxvSc5hS</td>
      <td>70.0</td>
      <td>168927.0</td>
    </tr>
  </tbody>
</table>
<p>2400 rows × 21 columns</p>
</div>




```python
#visualization
#plotting all the new metrics in our dataframe vs streams
df['streams'] = df['streams'].astype(float)
df['position'] = df['position'].astype(int)
#this shows what got number 1? (below)
# df.loc[df['position'] == 1].head(10) # Previously this was showing that every 
```

# Data Visualization

We've now gathered and manipulated valuable data for each track for each day recorded. The key elements are the following:
- Track Name
- Artist Name
- Stream Count
- Popularity value 
- Number of Followers
- Position on Top 200
- Date on the Top 200 (most songs stay for many days)

The following details define the patterns and properties of music, the way they sound, and what mood they instill:
- Duration
  - The duration of the track in milliseconds.
- Acousticness
  - A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic. 
- Energy
  - Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy. 
- Instrumentalness
  - Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
- Liveness
  - Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live.
- Loudness
  - The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.
- Speechiness 
  - Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks. 
- Valence
  - A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry). 
- Tempo
  - The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. 

The following are more extraneous details for identifying tracks in the data wrangling:
- Track ID
- Artist ID 
- URL



Using this data, we begin trying to observe what traits of a song bring success.
First we observe that there is a standard distrubtion of stream counts, meaning the mean stream count will most likely fall from 1-1.05 million.


```python
#Histogram takes 100 random tracks, takes the average of all their streams, then does this 100 times
#Is a standarrd deviation


from scipy.stats import normaltest
from numpy.random import seed
from numpy.random import randn


alpha = 0.05
data = []
for i in range(0,100):
    data.append(np.mean(df['streams'].sample(n=100)))
plt.hist(data)
plt.xlabel("Estimate")
plt.ylabel("Frequency")

```




    Text(0, 0.5, 'Frequency')




    
![svg](output_21_1.svg)
    


Our goal is to determine if there certain values of song properties that result in extremely high or low success.
We create a dataframe that only saves the entry of a song at its peak stream count in the Top 200, meaning
we are comparing all the peaks.


```python
# Creating version of table with no duplicates, keeping the last seen version of each song. It is a fair representation of success.

no_dupes_df = df.copy()
no_dupes_df = no_dupes_df.sort_values('streams', ascending=False).drop_duplicates(['artist', 'duration_ms', 'acousticness', 'danceability', 'energy'], keep='first') 
no_dupes_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>position</th>
      <th>track_name</th>
      <th>artist</th>
      <th>streams</th>
      <th>url</th>
      <th>date</th>
      <th>track_id</th>
      <th>duration_ms</th>
      <th>acousticness</th>
      <th>...</th>
      <th>energy</th>
      <th>instrumentalness</th>
      <th>liveness</th>
      <th>loudness</th>
      <th>speechiness</th>
      <th>valence</th>
      <th>tempo</th>
      <th>artist_id</th>
      <th>popularity_index</th>
      <th>follower_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>200</th>
      <td>1</td>
      <td>1</td>
      <td>Shape of You</td>
      <td>Ed Sheeran</td>
      <td>7549041.0</td>
      <td>https://open.spotify.com/track/7qiZfU4dY1lWllz...</td>
      <td>2017-02-01</td>
      <td>7qiZfU4dY1lWllzX7mPBI3</td>
      <td>233713.0</td>
      <td>0.5810</td>
      <td>...</td>
      <td>0.652</td>
      <td>0.000000</td>
      <td>0.0931</td>
      <td>-3.183</td>
      <td>0.0802</td>
      <td>0.931</td>
      <td>95.977</td>
      <td>6eUKZXaKkcviH0Ku9w2n3V</td>
      <td>91.0</td>
      <td>73345259.0</td>
    </tr>
    <tr>
      <th>1000</th>
      <td>1</td>
      <td>1</td>
      <td>Despacito - Remix</td>
      <td>Luis Fonsi</td>
      <td>7332260.0</td>
      <td>https://open.spotify.com/track/5CtI0qwDJkDQGwX...</td>
      <td>2017-06-01</td>
      <td>6rPO02ozF3bM7NnOV4h6s2</td>
      <td>228827.0</td>
      <td>0.2280</td>
      <td>...</td>
      <td>0.816</td>
      <td>0.000000</td>
      <td>0.0967</td>
      <td>-4.353</td>
      <td>0.1670</td>
      <td>0.816</td>
      <td>178.085</td>
      <td>4V8Sr092TqfHkfAA5fXXqG</td>
      <td>78.0</td>
      <td>9035487.0</td>
    </tr>
    <tr>
      <th>2000</th>
      <td>1</td>
      <td>1</td>
      <td>rockstar</td>
      <td>Post Malone</td>
      <td>5755610.0</td>
      <td>https://open.spotify.com/track/7wGoVu4Dady5GV0...</td>
      <td>2017-11-01</td>
      <td>7ytR5pFWmSjzHJIeQkgog4</td>
      <td>181733.0</td>
      <td>0.2470</td>
      <td>...</td>
      <td>0.690</td>
      <td>0.000000</td>
      <td>0.1010</td>
      <td>-7.956</td>
      <td>0.1640</td>
      <td>0.497</td>
      <td>89.977</td>
      <td>4r63FhuTkUYltbVAg5TQnk</td>
      <td>93.0</td>
      <td>5174251.0</td>
    </tr>
    <tr>
      <th>1600</th>
      <td>1</td>
      <td>1</td>
      <td>Look What You Made Me Do</td>
      <td>Taylor Swift</td>
      <td>5547962.0</td>
      <td>https://open.spotify.com/track/6uFsE1JgZ20EXyU...</td>
      <td>2017-09-01</td>
      <td>1P17dC1amhFzptugyAO7Il</td>
      <td>211853.0</td>
      <td>0.2040</td>
      <td>...</td>
      <td>0.709</td>
      <td>0.000014</td>
      <td>0.1260</td>
      <td>-6.471</td>
      <td>0.1230</td>
      <td>0.506</td>
      <td>128.070</td>
      <td>06HL4z0CvFAxyc27GXpf02</td>
      <td>97.0</td>
      <td>34579892.0</td>
    </tr>
    <tr>
      <th>1001</th>
      <td>2</td>
      <td>2</td>
      <td>I'm the One</td>
      <td>DJ Khaled</td>
      <td>5208996.0</td>
      <td>https://open.spotify.com/track/72Q0FQQo32KJloi...</td>
      <td>2017-06-01</td>
      <td>1jYiIOC5d6soxkJP81fxq2</td>
      <td>288877.0</td>
      <td>0.0533</td>
      <td>...</td>
      <td>0.667</td>
      <td>0.000000</td>
      <td>0.1340</td>
      <td>-4.267</td>
      <td>0.0367</td>
      <td>0.817</td>
      <td>80.984</td>
      <td>0QHgL1lAIqAw0HtD7YldmP</td>
      <td>82.0</td>
      <td>5405048.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>193</th>
      <td>194</td>
      <td>194</td>
      <td>Famous</td>
      <td>Kanye West</td>
      <td>336134.0</td>
      <td>https://open.spotify.com/track/19a3JfW8BQwqHWU...</td>
      <td>2017-01-01</td>
      <td>19a3JfW8BQwqHWUMbcqSx8</td>
      <td>196040.0</td>
      <td>0.0711</td>
      <td>...</td>
      <td>0.735</td>
      <td>0.000000</td>
      <td>0.0975</td>
      <td>-3.715</td>
      <td>0.1170</td>
      <td>0.409</td>
      <td>173.935</td>
      <td>5K4W6rqBFWDnAN6FQUkS6x</td>
      <td>90.0</td>
      <td>12912141.0</td>
    </tr>
    <tr>
      <th>196</th>
      <td>197</td>
      <td>197</td>
      <td>Oh Lord</td>
      <td>MiC LOWRY</td>
      <td>331792.0</td>
      <td>https://open.spotify.com/track/1sTUEdVO85YU8Ym...</td>
      <td>2017-01-01</td>
      <td>1ISsiC4Fw6f96kZQegLGiJ</td>
      <td>198253.0</td>
      <td>0.4070</td>
      <td>...</td>
      <td>0.738</td>
      <td>0.000000</td>
      <td>0.1300</td>
      <td>-6.921</td>
      <td>0.2620</td>
      <td>0.219</td>
      <td>176.071</td>
      <td>6fOMl44jA4Sp5b9PpYCkzz</td>
      <td>84.0</td>
      <td>4600363.0</td>
    </tr>
    <tr>
      <th>197</th>
      <td>198</td>
      <td>198</td>
      <td>Superstition - Single Version</td>
      <td>Stevie Wonder</td>
      <td>331376.0</td>
      <td>https://open.spotify.com/track/5lXcSvHRVjQJ3LB...</td>
      <td>2017-01-01</td>
      <td>1h2xVEoJORqrg71HocgqXd</td>
      <td>245493.0</td>
      <td>0.0380</td>
      <td>...</td>
      <td>0.634</td>
      <td>0.006400</td>
      <td>0.0385</td>
      <td>-12.115</td>
      <td>0.0725</td>
      <td>0.872</td>
      <td>100.499</td>
      <td>7guDJrEfX3qb6FEbdPA5qi</td>
      <td>80.0</td>
      <td>4654921.0</td>
    </tr>
    <tr>
      <th>198</th>
      <td>199</td>
      <td>199</td>
      <td>Secrets</td>
      <td>The Weeknd</td>
      <td>331233.0</td>
      <td>https://open.spotify.com/track/3DX4Y0egvc0slLc...</td>
      <td>2017-01-01</td>
      <td>1NhPKVLsHhFUHIOZ32QnS2</td>
      <td>224693.0</td>
      <td>0.0717</td>
      <td>...</td>
      <td>0.764</td>
      <td>0.000000</td>
      <td>0.1150</td>
      <td>-6.223</td>
      <td>0.0366</td>
      <td>0.376</td>
      <td>148.021</td>
      <td>5Pwc4xIPtQLFEnJriah9YJ</td>
      <td>83.0</td>
      <td>11061770.0</td>
    </tr>
    <tr>
      <th>199</th>
      <td>200</td>
      <td>200</td>
      <td>Ni**as In Paris</td>
      <td>JAY-Z</td>
      <td>325951.0</td>
      <td>https://open.spotify.com/track/2KpCpk6HjXXLb7n...</td>
      <td>2017-01-01</td>
      <td>4Li2WHPkuyCdtmokzW2007</td>
      <td>219333.0</td>
      <td>0.1270</td>
      <td>...</td>
      <td>0.858</td>
      <td>0.000000</td>
      <td>0.3490</td>
      <td>-5.542</td>
      <td>0.3110</td>
      <td>0.775</td>
      <td>140.022</td>
      <td>3nFkdlSjzX9mRTtwJOzDYB</td>
      <td>85.0</td>
      <td>5812536.0</td>
    </tr>
  </tbody>
</table>
<p>657 rows × 21 columns</p>
</div>




```python
plt.scatter(no_dupes_df['popularity_index'], no_dupes_df['streams'])
plt.title('Streams in Relation to Popularity')
plt.xlabel('popularity value')
plt.ylabel('streams in millions')

```




    Text(0, 0.5, 'streams in millions')




    
![svg](output_24_1.svg)
    



```python
plt.scatter(no_dupes_df['follower_count'], no_dupes_df['streams'])
plt.title('Streams in Relation to Follower Count')
plt.xlabel('number of artist followers')
plt.ylabel('streams in millions')
```




    Text(0, 0.5, 'streams in millions')




    
![svg](output_25_1.svg)
    



```python
plt.scatter(no_dupes_df['duration_ms'], no_dupes_df['streams'])
plt.title('Streams in Relation to Song Duration')
plt.xlabel('duration in milliseconds')
plt.ylabel('streams in millions')
```




    Text(0, 0.5, 'streams in millions')




    
![svg](output_26_1.svg)
    



```python
plt.scatter(no_dupes_df['acousticness'],no_dupes_df['streams'])
plt.title('Streams in Relation to Acousticness')
plt.xlabel('acousticness scale of 0-1')
plt.ylabel('streams in millions')
```




    Text(0, 0.5, 'streams in millions')




    
![svg](output_27_1.svg)
    



```python
plt.scatter(no_dupes_df['danceability'],no_dupes_df['streams'])
plt.title('Streams in Relation to Danceability')
plt.xlabel('danceability scale of 0-1')
plt.ylabel('streams in millions')
```




    Text(0, 0.5, 'streams in millions')




    
![svg](output_28_1.svg)
    



```python
plt.scatter(no_dupes_df['energy'],no_dupes_df['streams'])
plt.title('Streams in Relation to Energy')
plt.xlabel('energy scale of 0-1')
plt.ylabel('streams in millions')
```




    Text(0, 0.5, 'streams in millions')




    
![svg](output_29_1.svg)
    



```python
plt.scatter(no_dupes_df['instrumentalness'],no_dupes_df['streams'])
plt.title('Streams in Relation to Instrumentalness')
plt.xlabel('instrumentalness scale of 0-1')
plt.ylabel('streams in millions')
```




    Text(0, 0.5, 'streams in millions')




    
![svg](output_30_1.svg)
    



```python
plt.scatter(no_dupes_df['liveness'],no_dupes_df['streams'])
plt.title('Streams in Relation to Liveness')
plt.xlabel('liveness scale of 0-1') 
plt.ylabel('streams in millions')
```




    Text(0, 0.5, 'streams in millions')




    
![svg](output_31_1.svg)
    



```python
plt.scatter(no_dupes_df['loudness'],no_dupes_df['streams'])
plt.title('Streams in Relation to Loudness')
plt.xlabel('loudness scale')
plt.ylabel('streams in millions')
```




    Text(0, 0.5, 'streams in millions')




    
![svg](output_32_1.svg)
    



```python
plt.scatter(no_dupes_df['speechiness'], no_dupes_df['streams'])
plt.title('Streams in Relation to Speechiness')
plt.xlabel('speechiness scale of 0-.5')
plt.ylabel('streams in millions')
```




    Text(0, 0.5, 'streams in millions')




    
![svg](output_33_1.svg)
    



```python
plt.scatter(no_dupes_df['valence'],no_dupes_df['streams'])
plt.title('Streams in Relation to Valence')
plt.xlabel('valence scale of 0-1')
plt.ylabel('streams in millions')
```




    Text(0, 0.5, 'streams in millions')




    
![svg](output_34_1.svg)
    


Streams in relation to Tempo


```python
plt.scatter(no_dupes_df['tempo'],no_dupes_df['streams'])
plt.title('Streams in Relation to Tempo')
plt.xlabel('tempo scale of 0-200')
plt.ylabel('streams in millions')
```




    Text(0, 0.5, 'streams in millions')




    
![svg](output_36_1.svg)
    


Observe this correlation matrix compiling on scatter plots above


```python
corr = no_dupes_df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))

f, ax = plt.subplots(figsize=(11, 9))
cmap = sns.diverging_palette(230, 20, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
```




    <AxesSubplot:>




    
![svg](output_38_1.svg)
    


It seems like each individual feature has very little effect on the number of streams, which would support our findings above. After seeing this, we had a couple of ideas. It is possible different features we are currently tracking work together to make a song popular, but it is also possible we are missing other important features. After looking back at the most popular songs over the course of our entire dataframe, we noticed the majority of artists were well known or already accomplished. While it is obvious that an artists "followers" or typical listeners will increase the number of streams a song will get, it would be interesting to know if the number of typical listeners was more important than all these other aspects of the song.


```python

```

### Top 10
Here we observe the traits of specifically the song at the ranks 1-5. This song is likely to change, so there will be different values for the same position at times.


```python
top5s = df.loc[df['position'] <= 10]
#lists for legend to remove redundant code
color_list = ['r', 'orange', 'yellow', 'lime',  'cyan', 'b', 'brown' , 'violet', 'purple', 'black']
top10_legend = ['Rank 1', 'Rank 2', 'Rank 3', 'Rank 4', 'Rank 5', 'Rank 6','Rank 7','Rank 8','Rank 9','Rank 10']

#method to remove redundant code in plotting
def plotTop10(name):
    i = 0
    for index, row in top5s.iterrows():
        plt.scatter(row[name],row['streams'], color=color_list[i])
        i = (i + 1) % 10


top5s.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>position</th>
      <th>track_name</th>
      <th>artist</th>
      <th>streams</th>
      <th>url</th>
      <th>date</th>
      <th>track_id</th>
      <th>duration_ms</th>
      <th>acousticness</th>
      <th>...</th>
      <th>energy</th>
      <th>instrumentalness</th>
      <th>liveness</th>
      <th>loudness</th>
      <th>speechiness</th>
      <th>valence</th>
      <th>tempo</th>
      <th>artist_id</th>
      <th>popularity_index</th>
      <th>follower_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>Starboy</td>
      <td>The Weeknd</td>
      <td>3135625.0</td>
      <td>https://open.spotify.com/track/5aAx2yezTd8zXrk...</td>
      <td>2017-01-01</td>
      <td>7MXVkk9YMctZqd1Srtv4MB</td>
      <td>230453.0</td>
      <td>0.14100</td>
      <td>...</td>
      <td>0.587</td>
      <td>0.000006</td>
      <td>0.137</td>
      <td>-7.015</td>
      <td>0.2760</td>
      <td>0.486</td>
      <td>186.003</td>
      <td>1Xyo4u8uXC1ZmMpatF05PJ</td>
      <td>94.0</td>
      <td>26720759.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2</td>
      <td>Closer</td>
      <td>The Chainsmokers</td>
      <td>3015525.0</td>
      <td>https://open.spotify.com/track/7BKLCZ1jbUBVqRi...</td>
      <td>2017-01-01</td>
      <td>7BKLCZ1jbUBVqRi2FVlTVw</td>
      <td>244960.0</td>
      <td>0.41400</td>
      <td>...</td>
      <td>0.524</td>
      <td>0.000000</td>
      <td>0.111</td>
      <td>-5.599</td>
      <td>0.0338</td>
      <td>0.661</td>
      <td>95.010</td>
      <td>69GGBxA162lTqCwzJG5jLp</td>
      <td>84.0</td>
      <td>17093912.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>3</td>
      <td>Let Me Love You</td>
      <td>DJ Snake</td>
      <td>2545384.0</td>
      <td>https://open.spotify.com/track/4pdPtRcBmOSQDlJ...</td>
      <td>2017-01-01</td>
      <td>3ibKnFDaa3GhpPGlOUj7ff</td>
      <td>256733.0</td>
      <td>0.23500</td>
      <td>...</td>
      <td>0.578</td>
      <td>0.000000</td>
      <td>0.118</td>
      <td>-8.970</td>
      <td>0.0922</td>
      <td>0.556</td>
      <td>94.514</td>
      <td>20s0P9QLxGqKuCsGwFsp7w</td>
      <td>69.0</td>
      <td>2055274.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>4</td>
      <td>Rockabye (feat. Sean Paul &amp; Anne-Marie)</td>
      <td>Clean Bandit</td>
      <td>2356604.0</td>
      <td>https://open.spotify.com/track/5knuzwU65gJK7IF...</td>
      <td>2017-01-01</td>
      <td>5knuzwU65gJK7IF5yJsuaW</td>
      <td>251088.0</td>
      <td>0.40600</td>
      <td>...</td>
      <td>0.763</td>
      <td>0.000000</td>
      <td>0.180</td>
      <td>-4.068</td>
      <td>0.0523</td>
      <td>0.742</td>
      <td>101.965</td>
      <td>6MDME20pz9RveH9rEXvrOM</td>
      <td>80.0</td>
      <td>4092589.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>5</td>
      <td>One Dance</td>
      <td>Drake</td>
      <td>2259887.0</td>
      <td>https://open.spotify.com/track/1xznGGDReH1oQq0...</td>
      <td>2017-01-01</td>
      <td>1zi7xx7UVEFkmKfv06H8x0</td>
      <td>173987.0</td>
      <td>0.00776</td>
      <td>...</td>
      <td>0.625</td>
      <td>0.001800</td>
      <td>0.329</td>
      <td>-5.609</td>
      <td>0.0536</td>
      <td>0.370</td>
      <td>103.967</td>
      <td>3TVXtAsR1Inumwj472S9r4</td>
      <td>96.0</td>
      <td>51374698.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 21 columns</p>
</div>




```python

plotTop10('popularity_index')
plt.title('Top 10 Streams in Relation to Popularity')
plt.xlabel('popularity value')
plt.ylabel('streams in millions')
plt.legend(top10_legend)

```




    <matplotlib.legend.Legend at 0x1a54eee7700>




    
![svg](output_43_1.svg)
    



```python
plotTop10('follower_count')
plt.title('Top 10 Streams in Relation to Follower Count')
plt.xlabel('Follower Count in 10 millions')
plt.ylabel('streams in millions')
plt.legend(top10_legend)
```




    <matplotlib.legend.Legend at 0x1a54f16f520>




    
![svg](output_44_1.svg)
    



```python
plotTop10('duration_ms')
plt.title('Top 10 Streams in Relation to Duration')
plt.xlabel('duration in milliseconds')
plt.ylabel('streams in millions')
plt.legend(top10_legend)
```




    <matplotlib.legend.Legend at 0x1a55c2c0910>




    
![svg](output_45_1.svg)
    


This graph Shows how the duration of a song in milliseconds compares to the number of streams that song received, and we're only using the first 10 pieces of data from our dataframe. This shows us that the songs with the most streams from this set of data are songs which are > 240000 ms, or 4 minutes. This is surprising, because the average song is usually around 3 minutes and 30 seconds or less.


```python
plotTop10('acousticness')
plt.title('Top 10 Streams in Relation to Acousticness')
plt.xlabel('acousticness scale of 0-1')
plt.ylabel('streams in millions')
plt.legend(top10_legend)
```




    <matplotlib.legend.Legend at 0x1a54f79a430>




    
![svg](output_47_1.svg)
    


This graph displays a confidence score for how likely it is that a song is acoustic (with a value of 1 being very likely that the song is acoustic) compared to the number of streams the song has. All of the confidence scores are less than .5, which indicates most of these songs are probably not acoustic


```python

plotTop10('energy')
plt.title('Top 10 Streams in Relation to Energy')
plt.xlabel('energy scale of 0-1')
plt.ylabel('streams in millions')
plt.legend(top10_legend)

```




    <matplotlib.legend.Legend at 0x1a54f9cb7f0>




    
![svg](output_49_1.svg)
    


This graph shows how the "energy" of a song, or generally how noisy and fast the song is, compares to the number of streams for the top 10 songs on the 1st of January. Here, we see that the songs with the most streams are around or above .6 on the energy scale (a higher score means the song is higher energy)


```python
plotTop10('danceability')
plt.title('Top 10 Streams in Relation to Danceability')
plt.xlabel('danceability scale of 0-1')
plt.ylabel('streams in millions')
plt.legend(top10_legend)


```




    <matplotlib.legend.Legend at 0x1a54fc40e20>




    
![svg](output_51_1.svg)
    


This graph shows how "danceable" a song is using a value provided to us by the Spotify API comapred to the number of streams that song got. Danceability is measured as a value from 0 to 1, where 1 is most danceable. This graph appears to be similar to the graph describing, so they may have been determined using similar characteristisc (i.e. both are measuring how upbeat or fast a song is)


```python

plotTop10('loudness')
plt.title('Top 10 Streams in Relation to Loudness')
plt.xlabel('loudness in decibels')
plt.ylabel('streams in millions')
plt.legend(top10_legend)


```




    <matplotlib.legend.Legend at 0x1a55010b8e0>




    
![svg](output_53_1.svg)
    


This graph describes the average volume of each track in our top 5s data set compared to the number of streams each song had. It appears to trend similarly to the last two graphs, indicating that the volume of a track may be correlated with how danceable or energetic a song is.


```python

plotTop10('valence')
plt.xlabel('valence scale of 0-1')
plt.ylabel('streams in millions')
plt.legend(top10_legend)


```




    <matplotlib.legend.Legend at 0x1a54fc7e460>




    
![svg](output_55_1.svg)
    


This graph describes the "valence" of a song compared to the # of streams it got. Valence is described as the "positivity" of a song where "Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry)," according to the Spotify API reference. The reference does not describe how this value is determined, but our data seems to show there may be a correlation between valence and the number of streams a song is getting in the set of number 1 songs. However, this graph does not take into account the other features for the songs. It may be worth trying to consider songs where features except for this one are held to a constant, so that we can consider if there is a correlation between this value and the number of streams.


```python

plotTop10('tempo')
plt.title('Top 10 Streams in Relation to Beats Per Minute (BPM)')
plt.xlabel('tempo scale of 0-200 Beats Per Minute (BPM)')
plt.ylabel('streams in millions')
plt.legend(top10_legend)


```




    <matplotlib.legend.Legend at 0x1a5504a75e0>




    
![svg](output_57_1.svg)
    


This graph describes the tempo of a song comapred to the number of streams that song has. Given our dataset, it is unclear whether there is a correlation between the tempo of a song and the number of streams it gets.

### Correlation of the top 10


```python
corr = top5s.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
f, ax = plt.subplots(figsize=(11, 9))
cmap = sns.diverging_palette(230, 20, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
```




    <AxesSubplot:>




    
![svg](output_60_1.svg)
    


### Unique Relationships

There appeared to be a potential relationship between valence and the number of streams a song was getting, so it might be interesting to look at what the different features are like for songs with a valence of around .4 or higher


```python
highValenceTopTracks = top5s.loc[top5s['valence'] > .4]
highValenceTopTracks.sort_values('streams', ascending=False).head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>position</th>
      <th>track_name</th>
      <th>artist</th>
      <th>streams</th>
      <th>url</th>
      <th>date</th>
      <th>track_id</th>
      <th>duration_ms</th>
      <th>acousticness</th>
      <th>...</th>
      <th>energy</th>
      <th>instrumentalness</th>
      <th>liveness</th>
      <th>loudness</th>
      <th>speechiness</th>
      <th>valence</th>
      <th>tempo</th>
      <th>artist_id</th>
      <th>popularity_index</th>
      <th>follower_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>200</th>
      <td>1</td>
      <td>1</td>
      <td>Shape of You</td>
      <td>Ed Sheeran</td>
      <td>7549041.0</td>
      <td>https://open.spotify.com/track/7qiZfU4dY1lWllz...</td>
      <td>2017-02-01</td>
      <td>7qiZfU4dY1lWllzX7mPBI3</td>
      <td>233713.0</td>
      <td>0.581</td>
      <td>...</td>
      <td>0.652</td>
      <td>0.000000</td>
      <td>0.0931</td>
      <td>-3.183</td>
      <td>0.0802</td>
      <td>0.931</td>
      <td>95.977</td>
      <td>6eUKZXaKkcviH0Ku9w2n3V</td>
      <td>91.0</td>
      <td>73345259.0</td>
    </tr>
    <tr>
      <th>1000</th>
      <td>1</td>
      <td>1</td>
      <td>Despacito - Remix</td>
      <td>Luis Fonsi</td>
      <td>7332260.0</td>
      <td>https://open.spotify.com/track/5CtI0qwDJkDQGwX...</td>
      <td>2017-06-01</td>
      <td>6rPO02ozF3bM7NnOV4h6s2</td>
      <td>228827.0</td>
      <td>0.228</td>
      <td>...</td>
      <td>0.816</td>
      <td>0.000000</td>
      <td>0.0967</td>
      <td>-4.353</td>
      <td>0.1670</td>
      <td>0.816</td>
      <td>178.085</td>
      <td>4V8Sr092TqfHkfAA5fXXqG</td>
      <td>78.0</td>
      <td>9035487.0</td>
    </tr>
    <tr>
      <th>400</th>
      <td>1</td>
      <td>1</td>
      <td>Shape of You</td>
      <td>Ed Sheeran</td>
      <td>7201132.0</td>
      <td>https://open.spotify.com/track/7qiZfU4dY1lWllz...</td>
      <td>2017-03-01</td>
      <td>7qiZfU4dY1lWllzX7mPBI3</td>
      <td>233713.0</td>
      <td>0.581</td>
      <td>...</td>
      <td>0.652</td>
      <td>0.000000</td>
      <td>0.0931</td>
      <td>-3.183</td>
      <td>0.0802</td>
      <td>0.931</td>
      <td>95.977</td>
      <td>6eUKZXaKkcviH0Ku9w2n3V</td>
      <td>91.0</td>
      <td>73345259.0</td>
    </tr>
    <tr>
      <th>600</th>
      <td>1</td>
      <td>1</td>
      <td>Shape of You</td>
      <td>Ed Sheeran</td>
      <td>6815498.0</td>
      <td>https://open.spotify.com/track/7qiZfU4dY1lWllz...</td>
      <td>2017-04-01</td>
      <td>7qiZfU4dY1lWllzX7mPBI3</td>
      <td>233713.0</td>
      <td>0.581</td>
      <td>...</td>
      <td>0.652</td>
      <td>0.000000</td>
      <td>0.0931</td>
      <td>-3.183</td>
      <td>0.0802</td>
      <td>0.931</td>
      <td>95.977</td>
      <td>6eUKZXaKkcviH0Ku9w2n3V</td>
      <td>91.0</td>
      <td>73345259.0</td>
    </tr>
    <tr>
      <th>1200</th>
      <td>1</td>
      <td>1</td>
      <td>Despacito - Remix</td>
      <td>Luis Fonsi</td>
      <td>6398530.0</td>
      <td>https://open.spotify.com/track/5CtI0qwDJkDQGwX...</td>
      <td>2017-07-01</td>
      <td>6rPO02ozF3bM7NnOV4h6s2</td>
      <td>228827.0</td>
      <td>0.228</td>
      <td>...</td>
      <td>0.816</td>
      <td>0.000000</td>
      <td>0.0967</td>
      <td>-4.353</td>
      <td>0.1670</td>
      <td>0.816</td>
      <td>178.085</td>
      <td>4V8Sr092TqfHkfAA5fXXqG</td>
      <td>78.0</td>
      <td>9035487.0</td>
    </tr>
    <tr>
      <th>800</th>
      <td>1</td>
      <td>1</td>
      <td>Despacito - Remix</td>
      <td>Luis Fonsi</td>
      <td>6360737.0</td>
      <td>https://open.spotify.com/track/5CtI0qwDJkDQGwX...</td>
      <td>2017-05-01</td>
      <td>6rPO02ozF3bM7NnOV4h6s2</td>
      <td>228827.0</td>
      <td>0.228</td>
      <td>...</td>
      <td>0.816</td>
      <td>0.000000</td>
      <td>0.0967</td>
      <td>-4.353</td>
      <td>0.1670</td>
      <td>0.816</td>
      <td>178.085</td>
      <td>4V8Sr092TqfHkfAA5fXXqG</td>
      <td>78.0</td>
      <td>9035487.0</td>
    </tr>
    <tr>
      <th>2000</th>
      <td>1</td>
      <td>1</td>
      <td>rockstar</td>
      <td>Post Malone</td>
      <td>5755610.0</td>
      <td>https://open.spotify.com/track/7wGoVu4Dady5GV0...</td>
      <td>2017-11-01</td>
      <td>7ytR5pFWmSjzHJIeQkgog4</td>
      <td>181733.0</td>
      <td>0.247</td>
      <td>...</td>
      <td>0.690</td>
      <td>0.000000</td>
      <td>0.1010</td>
      <td>-7.956</td>
      <td>0.1640</td>
      <td>0.497</td>
      <td>89.977</td>
      <td>4r63FhuTkUYltbVAg5TQnk</td>
      <td>93.0</td>
      <td>5174251.0</td>
    </tr>
    <tr>
      <th>1800</th>
      <td>1</td>
      <td>1</td>
      <td>rockstar</td>
      <td>Post Malone</td>
      <td>5649503.0</td>
      <td>https://open.spotify.com/track/1OmcAT5Y8eg5bUP...</td>
      <td>2017-10-01</td>
      <td>7ytR5pFWmSjzHJIeQkgog4</td>
      <td>181733.0</td>
      <td>0.247</td>
      <td>...</td>
      <td>0.690</td>
      <td>0.000000</td>
      <td>0.1010</td>
      <td>-7.956</td>
      <td>0.1640</td>
      <td>0.497</td>
      <td>89.977</td>
      <td>4r63FhuTkUYltbVAg5TQnk</td>
      <td>93.0</td>
      <td>5174251.0</td>
    </tr>
    <tr>
      <th>1600</th>
      <td>1</td>
      <td>1</td>
      <td>Look What You Made Me Do</td>
      <td>Taylor Swift</td>
      <td>5547962.0</td>
      <td>https://open.spotify.com/track/6uFsE1JgZ20EXyU...</td>
      <td>2017-09-01</td>
      <td>1P17dC1amhFzptugyAO7Il</td>
      <td>211853.0</td>
      <td>0.204</td>
      <td>...</td>
      <td>0.709</td>
      <td>0.000014</td>
      <td>0.1260</td>
      <td>-6.471</td>
      <td>0.1230</td>
      <td>0.506</td>
      <td>128.070</td>
      <td>06HL4z0CvFAxyc27GXpf02</td>
      <td>97.0</td>
      <td>34579892.0</td>
    </tr>
    <tr>
      <th>2200</th>
      <td>1</td>
      <td>1</td>
      <td>rockstar</td>
      <td>Post Malone</td>
      <td>5528701.0</td>
      <td>https://open.spotify.com/track/7wGoVu4Dady5GV0...</td>
      <td>2017-12-01</td>
      <td>7ytR5pFWmSjzHJIeQkgog4</td>
      <td>181733.0</td>
      <td>0.247</td>
      <td>...</td>
      <td>0.690</td>
      <td>0.000000</td>
      <td>0.1010</td>
      <td>-7.956</td>
      <td>0.1640</td>
      <td>0.497</td>
      <td>89.977</td>
      <td>4r63FhuTkUYltbVAg5TQnk</td>
      <td>93.0</td>
      <td>5174251.0</td>
    </tr>
  </tbody>
</table>
<p>10 rows × 21 columns</p>
</div>



We have duplicate pieces of data, so lets remove the duplicates for this test. We're going to try to keep the versions of the song that have the most streams


```python
highValenceTopTracks = highValenceTopTracks.sort_values('streams', ascending=False).drop_duplicates(['artist', 'duration_ms', 'acousticness', 'danceability', 'energy'], keep='first') # Keeping the last seen version of each song, as that will probably hold it's total streams more accurately
highValenceTopTracks.sort_values('streams', ascending=False).head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>position</th>
      <th>track_name</th>
      <th>artist</th>
      <th>streams</th>
      <th>url</th>
      <th>date</th>
      <th>track_id</th>
      <th>duration_ms</th>
      <th>acousticness</th>
      <th>...</th>
      <th>energy</th>
      <th>instrumentalness</th>
      <th>liveness</th>
      <th>loudness</th>
      <th>speechiness</th>
      <th>valence</th>
      <th>tempo</th>
      <th>artist_id</th>
      <th>popularity_index</th>
      <th>follower_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>200</th>
      <td>1</td>
      <td>1</td>
      <td>Shape of You</td>
      <td>Ed Sheeran</td>
      <td>7549041.0</td>
      <td>https://open.spotify.com/track/7qiZfU4dY1lWllz...</td>
      <td>2017-02-01</td>
      <td>7qiZfU4dY1lWllzX7mPBI3</td>
      <td>233713.0</td>
      <td>0.581000</td>
      <td>...</td>
      <td>0.652</td>
      <td>0.000000</td>
      <td>0.0931</td>
      <td>-3.183</td>
      <td>0.0802</td>
      <td>0.931</td>
      <td>95.977</td>
      <td>6eUKZXaKkcviH0Ku9w2n3V</td>
      <td>91.0</td>
      <td>73345259.0</td>
    </tr>
    <tr>
      <th>1000</th>
      <td>1</td>
      <td>1</td>
      <td>Despacito - Remix</td>
      <td>Luis Fonsi</td>
      <td>7332260.0</td>
      <td>https://open.spotify.com/track/5CtI0qwDJkDQGwX...</td>
      <td>2017-06-01</td>
      <td>6rPO02ozF3bM7NnOV4h6s2</td>
      <td>228827.0</td>
      <td>0.228000</td>
      <td>...</td>
      <td>0.816</td>
      <td>0.000000</td>
      <td>0.0967</td>
      <td>-4.353</td>
      <td>0.1670</td>
      <td>0.816</td>
      <td>178.085</td>
      <td>4V8Sr092TqfHkfAA5fXXqG</td>
      <td>78.0</td>
      <td>9035487.0</td>
    </tr>
    <tr>
      <th>2000</th>
      <td>1</td>
      <td>1</td>
      <td>rockstar</td>
      <td>Post Malone</td>
      <td>5755610.0</td>
      <td>https://open.spotify.com/track/7wGoVu4Dady5GV0...</td>
      <td>2017-11-01</td>
      <td>7ytR5pFWmSjzHJIeQkgog4</td>
      <td>181733.0</td>
      <td>0.247000</td>
      <td>...</td>
      <td>0.690</td>
      <td>0.000000</td>
      <td>0.1010</td>
      <td>-7.956</td>
      <td>0.1640</td>
      <td>0.497</td>
      <td>89.977</td>
      <td>4r63FhuTkUYltbVAg5TQnk</td>
      <td>93.0</td>
      <td>5174251.0</td>
    </tr>
    <tr>
      <th>1600</th>
      <td>1</td>
      <td>1</td>
      <td>Look What You Made Me Do</td>
      <td>Taylor Swift</td>
      <td>5547962.0</td>
      <td>https://open.spotify.com/track/6uFsE1JgZ20EXyU...</td>
      <td>2017-09-01</td>
      <td>1P17dC1amhFzptugyAO7Il</td>
      <td>211853.0</td>
      <td>0.204000</td>
      <td>...</td>
      <td>0.709</td>
      <td>0.000014</td>
      <td>0.1260</td>
      <td>-6.471</td>
      <td>0.1230</td>
      <td>0.506</td>
      <td>128.070</td>
      <td>06HL4z0CvFAxyc27GXpf02</td>
      <td>97.0</td>
      <td>34579892.0</td>
    </tr>
    <tr>
      <th>1001</th>
      <td>2</td>
      <td>2</td>
      <td>I'm the One</td>
      <td>DJ Khaled</td>
      <td>5208996.0</td>
      <td>https://open.spotify.com/track/72Q0FQQo32KJloi...</td>
      <td>2017-06-01</td>
      <td>1jYiIOC5d6soxkJP81fxq2</td>
      <td>288877.0</td>
      <td>0.053300</td>
      <td>...</td>
      <td>0.667</td>
      <td>0.000000</td>
      <td>0.1340</td>
      <td>-4.267</td>
      <td>0.0367</td>
      <td>0.817</td>
      <td>80.984</td>
      <td>0QHgL1lAIqAw0HtD7YldmP</td>
      <td>82.0</td>
      <td>5405048.0</td>
    </tr>
    <tr>
      <th>401</th>
      <td>2</td>
      <td>2</td>
      <td>Something Just Like This</td>
      <td>The Chainsmokers</td>
      <td>4581789.0</td>
      <td>https://open.spotify.com/track/6RUKPb4LETWmmr3...</td>
      <td>2017-03-01</td>
      <td>6RUKPb4LETWmmr3iAEQktW</td>
      <td>247160.0</td>
      <td>0.049800</td>
      <td>...</td>
      <td>0.635</td>
      <td>0.000014</td>
      <td>0.1640</td>
      <td>-6.769</td>
      <td>0.0317</td>
      <td>0.446</td>
      <td>103.019</td>
      <td>69GGBxA162lTqCwzJG5jLp</td>
      <td>84.0</td>
      <td>17093912.0</td>
    </tr>
    <tr>
      <th>1201</th>
      <td>2</td>
      <td>2</td>
      <td>Wild Thoughts (feat. Rihanna &amp; Bryson Tiller)</td>
      <td>DJ Khaled</td>
      <td>4558126.0</td>
      <td>https://open.spotify.com/track/1OAh8uOEOvTDqkK...</td>
      <td>2017-07-01</td>
      <td>45XhKYRRkyeqoW3teSOkCM</td>
      <td>204664.0</td>
      <td>0.028700</td>
      <td>...</td>
      <td>0.681</td>
      <td>0.000000</td>
      <td>0.1260</td>
      <td>-3.089</td>
      <td>0.0778</td>
      <td>0.619</td>
      <td>97.621</td>
      <td>0QHgL1lAIqAw0HtD7YldmP</td>
      <td>82.0</td>
      <td>5405048.0</td>
    </tr>
    <tr>
      <th>402</th>
      <td>3</td>
      <td>3</td>
      <td>It Ain't Me (with Selena Gomez)</td>
      <td>Kygo</td>
      <td>4529714.0</td>
      <td>https://open.spotify.com/track/3eR23VReFzcdmS7...</td>
      <td>2017-03-01</td>
      <td>2jRGYG8U5bJzWOH6FLuzvO</td>
      <td>192000.0</td>
      <td>0.016100</td>
      <td>...</td>
      <td>0.658</td>
      <td>0.000138</td>
      <td>0.0607</td>
      <td>-5.362</td>
      <td>0.0748</td>
      <td>0.539</td>
      <td>115.024</td>
      <td>23fqKkggKUBHNkbKtXEls4</td>
      <td>86.0</td>
      <td>6975385.0</td>
    </tr>
    <tr>
      <th>803</th>
      <td>4</td>
      <td>4</td>
      <td>HUMBLE.</td>
      <td>Kendrick Lamar</td>
      <td>4371886.0</td>
      <td>https://open.spotify.com/track/7KXjTSCq5nL1LoY...</td>
      <td>2017-05-01</td>
      <td>7KXjTSCq5nL1LoYtL7XAwS</td>
      <td>177000.0</td>
      <td>0.000282</td>
      <td>...</td>
      <td>0.621</td>
      <td>0.000054</td>
      <td>0.0958</td>
      <td>-6.638</td>
      <td>0.1020</td>
      <td>0.421</td>
      <td>150.011</td>
      <td>2YZyLoL8N0Wb9xBt1NhZWg</td>
      <td>87.0</td>
      <td>16028806.0</td>
    </tr>
    <tr>
      <th>2002</th>
      <td>3</td>
      <td>3</td>
      <td>New Rules</td>
      <td>Dua Lipa</td>
      <td>3758506.0</td>
      <td>https://open.spotify.com/track/2ekn2ttSfGqwhha...</td>
      <td>2017-11-01</td>
      <td>2ekn2ttSfGqwhhate0LSR0</td>
      <td>209320.0</td>
      <td>0.002610</td>
      <td>...</td>
      <td>0.700</td>
      <td>0.000016</td>
      <td>0.1530</td>
      <td>-6.021</td>
      <td>0.0694</td>
      <td>0.608</td>
      <td>116.073</td>
      <td>6M2wZ9GZgrQXHCFfjv46we</td>
      <td>93.0</td>
      <td>21442792.0</td>
    </tr>
  </tbody>
</table>
<p>10 rows × 21 columns</p>
</div>




```python
highValenceTopTracks = highValenceTopTracks.sort_values('valence', ascending=False)
highValenceTopTracks.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>position</th>
      <th>track_name</th>
      <th>artist</th>
      <th>streams</th>
      <th>url</th>
      <th>date</th>
      <th>track_id</th>
      <th>duration_ms</th>
      <th>acousticness</th>
      <th>...</th>
      <th>energy</th>
      <th>instrumentalness</th>
      <th>liveness</th>
      <th>loudness</th>
      <th>speechiness</th>
      <th>valence</th>
      <th>tempo</th>
      <th>artist_id</th>
      <th>popularity_index</th>
      <th>follower_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1006</th>
      <td>7</td>
      <td>7</td>
      <td>There's Nothing Holdin' Me Back</td>
      <td>Shawn Mendes</td>
      <td>3093935.0</td>
      <td>https://open.spotify.com/track/79cuOz3SPQTuFrp...</td>
      <td>2017-06-01</td>
      <td>7JJmb5XwzOO8jgpou264Ml</td>
      <td>199440.0</td>
      <td>0.3800</td>
      <td>...</td>
      <td>0.813</td>
      <td>0.0</td>
      <td>0.0779</td>
      <td>-4.063</td>
      <td>0.0554</td>
      <td>0.969</td>
      <td>121.998</td>
      <td>7n2wHs1TKAczGzO7Dd2rGr</td>
      <td>92.0</td>
      <td>30441601.0</td>
    </tr>
    <tr>
      <th>200</th>
      <td>1</td>
      <td>1</td>
      <td>Shape of You</td>
      <td>Ed Sheeran</td>
      <td>7549041.0</td>
      <td>https://open.spotify.com/track/7qiZfU4dY1lWllz...</td>
      <td>2017-02-01</td>
      <td>7qiZfU4dY1lWllzX7mPBI3</td>
      <td>233713.0</td>
      <td>0.5810</td>
      <td>...</td>
      <td>0.652</td>
      <td>0.0</td>
      <td>0.0931</td>
      <td>-3.183</td>
      <td>0.0802</td>
      <td>0.931</td>
      <td>95.977</td>
      <td>6eUKZXaKkcviH0Ku9w2n3V</td>
      <td>91.0</td>
      <td>73345259.0</td>
    </tr>
    <tr>
      <th>1607</th>
      <td>8</td>
      <td>8</td>
      <td>Sorry Not Sorry</td>
      <td>Demi Lovato</td>
      <td>2952488.0</td>
      <td>https://open.spotify.com/track/25C5CowdsfXld2j...</td>
      <td>2017-09-01</td>
      <td>7gvd8xj4QgPqbQSsn5pV7d</td>
      <td>203760.0</td>
      <td>0.0237</td>
      <td>...</td>
      <td>0.640</td>
      <td>0.0</td>
      <td>0.2620</td>
      <td>-6.928</td>
      <td>0.2250</td>
      <td>0.887</td>
      <td>144.077</td>
      <td>6S2OmqARrzebs0tKUEyXyp</td>
      <td>84.0</td>
      <td>18568349.0</td>
    </tr>
    <tr>
      <th>1604</th>
      <td>5</td>
      <td>5</td>
      <td>Feels (feat. Pharrell Williams, Katy Perry &amp; B...</td>
      <td>Calvin Harris</td>
      <td>3324451.0</td>
      <td>https://open.spotify.com/track/5bcTCxgc7xVfSaM...</td>
      <td>2017-09-01</td>
      <td>5bcTCxgc7xVfSaMV3RuVke</td>
      <td>223413.0</td>
      <td>0.0642</td>
      <td>...</td>
      <td>0.745</td>
      <td>0.0</td>
      <td>0.0943</td>
      <td>-3.105</td>
      <td>0.0571</td>
      <td>0.872</td>
      <td>101.018</td>
      <td>7CajNmpbOovFoOoasH2HaY</td>
      <td>86.0</td>
      <td>20962353.0</td>
    </tr>
    <tr>
      <th>605</th>
      <td>6</td>
      <td>6</td>
      <td>That's What I Like</td>
      <td>Bruno Mars</td>
      <td>3419965.0</td>
      <td>https://open.spotify.com/track/0KKkJNfGyhkQ5aF...</td>
      <td>2017-04-01</td>
      <td>0KKkJNfGyhkQ5aFogxQAPU</td>
      <td>206693.0</td>
      <td>0.0130</td>
      <td>...</td>
      <td>0.560</td>
      <td>0.0</td>
      <td>0.0944</td>
      <td>-4.961</td>
      <td>0.0406</td>
      <td>0.860</td>
      <td>134.066</td>
      <td>0du5cEVh5yTK9QJze8zA0C</td>
      <td>87.0</td>
      <td>27863749.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 21 columns</p>
</div>



We believe no one feature has a strong effect on the number of streams, but it's possible that a combination of values in different features work together to improve stream count.

Using our list of songs with a high valence, we can look at the relationship between featuers like danceability or tempo and stream count to try to see how songs with both a high valence and varying levels of these features affect streams.

Let's get high valence songs from our original dataframe to have a larger sample size


```python
highValenceTracks = df.loc[(df['valence'] > .5) & (df['valence'] < .8)]
veryHighValenceTracks = df.loc[df['valence'] > .8]
lowValenceTracks = df.loc[(df['valence'] < .5) & (df['valence'] > .3)]
veryLowValenceTracks = df.loc[df['valence'] < .3]
#lowValenceTracks.head()
#highValenceTracks.head()
```


```python
# Plotting songs with a high valence and varying levels of danceability against streams to see if these two values work together to impact stream counts
plt.scatter(veryLowValenceTracks['danceability'],veryLowValenceTracks['streams'], color="blue")
plt.scatter(lowValenceTracks['danceability'],lowValenceTracks['streams'], color="turquoise")
plt.scatter(highValenceTracks['danceability'],highValenceTracks['streams'], color="yellow")
plt.scatter(veryHighValenceTracks['danceability'],veryHighValenceTracks['streams'], color="red")
plt.title('Danceability and streams for songs with bounded valences')
plt.xlabel('danceability scale of 0-1')
plt.ylabel('streams in millions')
plt.legend(['Song with valence > .8', 'Song with valence > .5 and < .8', 'Song with valence < .5 and > .3', 'Song with valence < .3'])
```




    <matplotlib.legend.Legend at 0x1a5505e3d90>




    
![svg](output_71_1.svg)
    


This graph displays how the danceability of a song compares to the number of streams it has for songs that have a high valence (>.5). While there is little indication of a linear correlation, it appears that the songs with the most streams all also have a danceability of > .5. 

No longer seeing the relationship we were seeing earlier between valence and number of streams. Maybe the relationship that leads to more streams is a combination of these features together. It might be worth trying to see if there is a relationship between streams and a combination of features like valence AND loudness or tempo AND danceability

Instead of considering high valence songs, let's looks at the top streamed songs for the 1st day of every month in the year of 2017


```python
top500OverYear = df.sort_values('streams', ascending=False).drop_duplicates(['artist', 'duration_ms', 'acousticness', 'danceability', 'energy'], keep='first').head(500)
top500OverYear.head(20)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>position</th>
      <th>track_name</th>
      <th>artist</th>
      <th>streams</th>
      <th>url</th>
      <th>date</th>
      <th>track_id</th>
      <th>duration_ms</th>
      <th>acousticness</th>
      <th>...</th>
      <th>energy</th>
      <th>instrumentalness</th>
      <th>liveness</th>
      <th>loudness</th>
      <th>speechiness</th>
      <th>valence</th>
      <th>tempo</th>
      <th>artist_id</th>
      <th>popularity_index</th>
      <th>follower_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>200</th>
      <td>1</td>
      <td>1</td>
      <td>Shape of You</td>
      <td>Ed Sheeran</td>
      <td>7549041.0</td>
      <td>https://open.spotify.com/track/7qiZfU4dY1lWllz...</td>
      <td>2017-02-01</td>
      <td>7qiZfU4dY1lWllzX7mPBI3</td>
      <td>233713.0</td>
      <td>0.581000</td>
      <td>...</td>
      <td>0.652</td>
      <td>0.000000</td>
      <td>0.0931</td>
      <td>-3.183</td>
      <td>0.0802</td>
      <td>0.931</td>
      <td>95.977</td>
      <td>6eUKZXaKkcviH0Ku9w2n3V</td>
      <td>91.0</td>
      <td>73345259.0</td>
    </tr>
    <tr>
      <th>1000</th>
      <td>1</td>
      <td>1</td>
      <td>Despacito - Remix</td>
      <td>Luis Fonsi</td>
      <td>7332260.0</td>
      <td>https://open.spotify.com/track/5CtI0qwDJkDQGwX...</td>
      <td>2017-06-01</td>
      <td>6rPO02ozF3bM7NnOV4h6s2</td>
      <td>228827.0</td>
      <td>0.228000</td>
      <td>...</td>
      <td>0.816</td>
      <td>0.000000</td>
      <td>0.0967</td>
      <td>-4.353</td>
      <td>0.1670</td>
      <td>0.816</td>
      <td>178.085</td>
      <td>4V8Sr092TqfHkfAA5fXXqG</td>
      <td>78.0</td>
      <td>9035487.0</td>
    </tr>
    <tr>
      <th>2000</th>
      <td>1</td>
      <td>1</td>
      <td>rockstar</td>
      <td>Post Malone</td>
      <td>5755610.0</td>
      <td>https://open.spotify.com/track/7wGoVu4Dady5GV0...</td>
      <td>2017-11-01</td>
      <td>7ytR5pFWmSjzHJIeQkgog4</td>
      <td>181733.0</td>
      <td>0.247000</td>
      <td>...</td>
      <td>0.690</td>
      <td>0.000000</td>
      <td>0.1010</td>
      <td>-7.956</td>
      <td>0.1640</td>
      <td>0.497</td>
      <td>89.977</td>
      <td>4r63FhuTkUYltbVAg5TQnk</td>
      <td>93.0</td>
      <td>5174251.0</td>
    </tr>
    <tr>
      <th>1600</th>
      <td>1</td>
      <td>1</td>
      <td>Look What You Made Me Do</td>
      <td>Taylor Swift</td>
      <td>5547962.0</td>
      <td>https://open.spotify.com/track/6uFsE1JgZ20EXyU...</td>
      <td>2017-09-01</td>
      <td>1P17dC1amhFzptugyAO7Il</td>
      <td>211853.0</td>
      <td>0.204000</td>
      <td>...</td>
      <td>0.709</td>
      <td>0.000014</td>
      <td>0.1260</td>
      <td>-6.471</td>
      <td>0.1230</td>
      <td>0.506</td>
      <td>128.070</td>
      <td>06HL4z0CvFAxyc27GXpf02</td>
      <td>97.0</td>
      <td>34579892.0</td>
    </tr>
    <tr>
      <th>1001</th>
      <td>2</td>
      <td>2</td>
      <td>I'm the One</td>
      <td>DJ Khaled</td>
      <td>5208996.0</td>
      <td>https://open.spotify.com/track/72Q0FQQo32KJloi...</td>
      <td>2017-06-01</td>
      <td>1jYiIOC5d6soxkJP81fxq2</td>
      <td>288877.0</td>
      <td>0.053300</td>
      <td>...</td>
      <td>0.667</td>
      <td>0.000000</td>
      <td>0.1340</td>
      <td>-4.267</td>
      <td>0.0367</td>
      <td>0.817</td>
      <td>80.984</td>
      <td>0QHgL1lAIqAw0HtD7YldmP</td>
      <td>82.0</td>
      <td>5405048.0</td>
    </tr>
    <tr>
      <th>1601</th>
      <td>2</td>
      <td>2</td>
      <td>Mi Gente</td>
      <td>J Balvin</td>
      <td>4756176.0</td>
      <td>https://open.spotify.com/track/2rb5MvYT7ZIxbKW...</td>
      <td>2017-09-01</td>
      <td>4ipnJyDU3Lq15qBAYNqlqK</td>
      <td>189440.0</td>
      <td>0.017900</td>
      <td>...</td>
      <td>0.687</td>
      <td>0.000012</td>
      <td>0.1280</td>
      <td>-4.818</td>
      <td>0.0584</td>
      <td>0.308</td>
      <td>104.959</td>
      <td>1vyhD5VmyZ7KMfW5gqLgo5</td>
      <td>95.0</td>
      <td>24653238.0</td>
    </tr>
    <tr>
      <th>401</th>
      <td>2</td>
      <td>2</td>
      <td>Something Just Like This</td>
      <td>The Chainsmokers</td>
      <td>4581789.0</td>
      <td>https://open.spotify.com/track/6RUKPb4LETWmmr3...</td>
      <td>2017-03-01</td>
      <td>6RUKPb4LETWmmr3iAEQktW</td>
      <td>247160.0</td>
      <td>0.049800</td>
      <td>...</td>
      <td>0.635</td>
      <td>0.000014</td>
      <td>0.1640</td>
      <td>-6.769</td>
      <td>0.0317</td>
      <td>0.446</td>
      <td>103.019</td>
      <td>69GGBxA162lTqCwzJG5jLp</td>
      <td>84.0</td>
      <td>17093912.0</td>
    </tr>
    <tr>
      <th>1201</th>
      <td>2</td>
      <td>2</td>
      <td>Wild Thoughts (feat. Rihanna &amp; Bryson Tiller)</td>
      <td>DJ Khaled</td>
      <td>4558126.0</td>
      <td>https://open.spotify.com/track/1OAh8uOEOvTDqkK...</td>
      <td>2017-07-01</td>
      <td>45XhKYRRkyeqoW3teSOkCM</td>
      <td>204664.0</td>
      <td>0.028700</td>
      <td>...</td>
      <td>0.681</td>
      <td>0.000000</td>
      <td>0.1260</td>
      <td>-3.089</td>
      <td>0.0778</td>
      <td>0.619</td>
      <td>97.621</td>
      <td>0QHgL1lAIqAw0HtD7YldmP</td>
      <td>82.0</td>
      <td>5405048.0</td>
    </tr>
    <tr>
      <th>402</th>
      <td>3</td>
      <td>3</td>
      <td>It Ain't Me (with Selena Gomez)</td>
      <td>Kygo</td>
      <td>4529714.0</td>
      <td>https://open.spotify.com/track/3eR23VReFzcdmS7...</td>
      <td>2017-03-01</td>
      <td>2jRGYG8U5bJzWOH6FLuzvO</td>
      <td>192000.0</td>
      <td>0.016100</td>
      <td>...</td>
      <td>0.658</td>
      <td>0.000138</td>
      <td>0.0607</td>
      <td>-5.362</td>
      <td>0.0748</td>
      <td>0.539</td>
      <td>115.024</td>
      <td>23fqKkggKUBHNkbKtXEls4</td>
      <td>86.0</td>
      <td>6975385.0</td>
    </tr>
    <tr>
      <th>2001</th>
      <td>2</td>
      <td>2</td>
      <td>Havana</td>
      <td>Camila Cabello</td>
      <td>4438592.0</td>
      <td>https://open.spotify.com/track/0ofbQMrRDsUaVKq...</td>
      <td>2017-11-01</td>
      <td>1rfofaqEpACxVEHIZBJe6W</td>
      <td>217307.0</td>
      <td>0.184000</td>
      <td>...</td>
      <td>0.523</td>
      <td>0.000036</td>
      <td>0.1320</td>
      <td>-4.333</td>
      <td>0.0300</td>
      <td>0.394</td>
      <td>104.988</td>
      <td>4nDoRrQiYLoBzwC5BhVJzF</td>
      <td>85.0</td>
      <td>19136575.0</td>
    </tr>
    <tr>
      <th>803</th>
      <td>4</td>
      <td>4</td>
      <td>HUMBLE.</td>
      <td>Kendrick Lamar</td>
      <td>4371886.0</td>
      <td>https://open.spotify.com/track/7KXjTSCq5nL1LoY...</td>
      <td>2017-05-01</td>
      <td>7KXjTSCq5nL1LoYtL7XAwS</td>
      <td>177000.0</td>
      <td>0.000282</td>
      <td>...</td>
      <td>0.621</td>
      <td>0.000054</td>
      <td>0.0958</td>
      <td>-6.638</td>
      <td>0.1020</td>
      <td>0.421</td>
      <td>150.011</td>
      <td>2YZyLoL8N0Wb9xBt1NhZWg</td>
      <td>87.0</td>
      <td>16028806.0</td>
    </tr>
    <tr>
      <th>2202</th>
      <td>3</td>
      <td>3</td>
      <td>Perfect Duet (Ed Sheeran &amp; Beyoncé)</td>
      <td>Ed Sheeran</td>
      <td>4250965.0</td>
      <td>https://open.spotify.com/track/1bhUWB0zJMIKr9y...</td>
      <td>2017-12-01</td>
      <td>1bhUWB0zJMIKr9yVPrkEuI</td>
      <td>259550.0</td>
      <td>0.779000</td>
      <td>...</td>
      <td>0.299</td>
      <td>0.000000</td>
      <td>0.1230</td>
      <td>-7.365</td>
      <td>0.0263</td>
      <td>0.356</td>
      <td>94.992</td>
      <td>6eUKZXaKkcviH0Ku9w2n3V</td>
      <td>91.0</td>
      <td>73345259.0</td>
    </tr>
    <tr>
      <th>601</th>
      <td>2</td>
      <td>2</td>
      <td>Passionfruit</td>
      <td>Drake</td>
      <td>4235699.0</td>
      <td>https://open.spotify.com/track/7hDc8b7IXETo14h...</td>
      <td>2017-04-01</td>
      <td>5mCPDVBb16L4XQwDdbRUpz</td>
      <td>298941.0</td>
      <td>0.256000</td>
      <td>...</td>
      <td>0.463</td>
      <td>0.085000</td>
      <td>0.1090</td>
      <td>-11.377</td>
      <td>0.0396</td>
      <td>0.364</td>
      <td>111.980</td>
      <td>3TVXtAsR1Inumwj472S9r4</td>
      <td>96.0</td>
      <td>51374698.0</td>
    </tr>
    <tr>
      <th>201</th>
      <td>2</td>
      <td>2</td>
      <td>Paris</td>
      <td>The Chainsmokers</td>
      <td>4181293.0</td>
      <td>https://open.spotify.com/track/72jbDTw1piOOj77...</td>
      <td>2017-02-01</td>
      <td>4irYeuAi87yyGHcI4h9s0x</td>
      <td>111020.0</td>
      <td>0.072500</td>
      <td>...</td>
      <td>0.648</td>
      <td>0.005920</td>
      <td>0.0984</td>
      <td>-6.188</td>
      <td>0.0832</td>
      <td>0.196</td>
      <td>106.075</td>
      <td>1VPmR4DJC1PlOtd0IADAO0</td>
      <td>84.0</td>
      <td>2806399.0</td>
    </tr>
    <tr>
      <th>403</th>
      <td>4</td>
      <td>4</td>
      <td>I Don’t Wanna Live Forever (Fifty Shades Darke...</td>
      <td>ZAYN</td>
      <td>3898610.0</td>
      <td>https://open.spotify.com/track/3NdDpSvN911VPGi...</td>
      <td>2017-03-01</td>
      <td>4s1gw3EgOpc9InInSqiMiv</td>
      <td>245653.0</td>
      <td>0.058600</td>
      <td>...</td>
      <td>0.445</td>
      <td>0.000017</td>
      <td>0.2150</td>
      <td>-8.403</td>
      <td>0.0529</td>
      <td>0.106</td>
      <td>117.967</td>
      <td>5ZsFI1h6hIdQRw2ti0hz81</td>
      <td>82.0</td>
      <td>13784895.0</td>
    </tr>
    <tr>
      <th>1203</th>
      <td>4</td>
      <td>4</td>
      <td>2U (feat. Justin Bieber)</td>
      <td>David Guetta</td>
      <td>3853673.0</td>
      <td>https://open.spotify.com/track/3A7qX2QjDlPnazU...</td>
      <td>2017-07-01</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2002</th>
      <td>3</td>
      <td>3</td>
      <td>New Rules</td>
      <td>Dua Lipa</td>
      <td>3758506.0</td>
      <td>https://open.spotify.com/track/2ekn2ttSfGqwhha...</td>
      <td>2017-11-01</td>
      <td>2ekn2ttSfGqwhhate0LSR0</td>
      <td>209320.0</td>
      <td>0.002610</td>
      <td>...</td>
      <td>0.700</td>
      <td>0.000016</td>
      <td>0.1530</td>
      <td>-6.021</td>
      <td>0.0694</td>
      <td>0.608</td>
      <td>116.073</td>
      <td>6M2wZ9GZgrQXHCFfjv46we</td>
      <td>93.0</td>
      <td>21442792.0</td>
    </tr>
    <tr>
      <th>1602</th>
      <td>3</td>
      <td>3</td>
      <td>Friends (with BloodPop®)</td>
      <td>Justin Bieber</td>
      <td>3595450.0</td>
      <td>https://open.spotify.com/track/7nZmah2llfvLDiU...</td>
      <td>2017-09-01</td>
      <td>7iNIg7XDEaYECfWD5dJ9Va</td>
      <td>189467.0</td>
      <td>0.003890</td>
      <td>...</td>
      <td>0.735</td>
      <td>0.000000</td>
      <td>0.3040</td>
      <td>-5.337</td>
      <td>0.0382</td>
      <td>0.631</td>
      <td>104.979</td>
      <td>1uNFoZAHBGtllmzznpCI3s</td>
      <td>96.0</td>
      <td>40403882.0</td>
    </tr>
    <tr>
      <th>2203</th>
      <td>4</td>
      <td>4</td>
      <td>Wolves</td>
      <td>Selena Gomez</td>
      <td>3590643.0</td>
      <td>https://open.spotify.com/track/7EmGUiUaOSGDnUU...</td>
      <td>2017-12-01</td>
      <td>33gwZOGJWEZ7dRWPqPxBEZ</td>
      <td>199758.0</td>
      <td>0.097800</td>
      <td>...</td>
      <td>0.675</td>
      <td>0.000009</td>
      <td>0.3510</td>
      <td>-5.267</td>
      <td>0.0867</td>
      <td>0.325</td>
      <td>160.048</td>
      <td>0c173mlxpT3dSFRgMO8XPh</td>
      <td>85.0</td>
      <td>7952071.0</td>
    </tr>
    <tr>
      <th>405</th>
      <td>6</td>
      <td>6</td>
      <td>Despacito (Featuring Daddy Yankee)</td>
      <td>Luis Fonsi</td>
      <td>3501514.0</td>
      <td>https://open.spotify.com/track/4aWmUDTfIPGksMN...</td>
      <td>2017-03-01</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>20 rows × 21 columns</p>
</div>




```python
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# plt.scatter(top500OverYear['valence'], top500OverYear['tempo'], top500OverYear['streams'])
# plt.xlabel('energy scale of 0-1')
# plt.ylabel('streams in millions')
```

We can start by getting the number of followers each artist has for every track entry in our dataframe. The Spotify API also provides a "popularity" index from 0 to 100, with 100 being the most popular. We will get this information, as well. There will be repetition between duplicate entries for an artist, but we are keeping these in so that we can still build a dataframe.


```python
#Popularity and follower count computed at the beginning
df['popularity_index']
df['follower_count']
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>position</th>
      <th>track_name</th>
      <th>artist</th>
      <th>streams</th>
      <th>url</th>
      <th>date</th>
      <th>track_id</th>
      <th>duration_ms</th>
      <th>acousticness</th>
      <th>...</th>
      <th>energy</th>
      <th>instrumentalness</th>
      <th>liveness</th>
      <th>loudness</th>
      <th>speechiness</th>
      <th>valence</th>
      <th>tempo</th>
      <th>artist_id</th>
      <th>popularity_index</th>
      <th>follower_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>Starboy</td>
      <td>The Weeknd</td>
      <td>3135625.0</td>
      <td>https://open.spotify.com/track/5aAx2yezTd8zXrk...</td>
      <td>2017-01-01</td>
      <td>7MXVkk9YMctZqd1Srtv4MB</td>
      <td>230453.0</td>
      <td>0.14100</td>
      <td>...</td>
      <td>0.587</td>
      <td>0.000006</td>
      <td>0.137</td>
      <td>-7.015</td>
      <td>0.2760</td>
      <td>0.486</td>
      <td>186.003</td>
      <td>1Xyo4u8uXC1ZmMpatF05PJ</td>
      <td>94.0</td>
      <td>26720759.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2</td>
      <td>Closer</td>
      <td>The Chainsmokers</td>
      <td>3015525.0</td>
      <td>https://open.spotify.com/track/7BKLCZ1jbUBVqRi...</td>
      <td>2017-01-01</td>
      <td>7BKLCZ1jbUBVqRi2FVlTVw</td>
      <td>244960.0</td>
      <td>0.41400</td>
      <td>...</td>
      <td>0.524</td>
      <td>0.000000</td>
      <td>0.111</td>
      <td>-5.599</td>
      <td>0.0338</td>
      <td>0.661</td>
      <td>95.010</td>
      <td>69GGBxA162lTqCwzJG5jLp</td>
      <td>84.0</td>
      <td>17093912.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>3</td>
      <td>Let Me Love You</td>
      <td>DJ Snake</td>
      <td>2545384.0</td>
      <td>https://open.spotify.com/track/4pdPtRcBmOSQDlJ...</td>
      <td>2017-01-01</td>
      <td>3ibKnFDaa3GhpPGlOUj7ff</td>
      <td>256733.0</td>
      <td>0.23500</td>
      <td>...</td>
      <td>0.578</td>
      <td>0.000000</td>
      <td>0.118</td>
      <td>-8.970</td>
      <td>0.0922</td>
      <td>0.556</td>
      <td>94.514</td>
      <td>20s0P9QLxGqKuCsGwFsp7w</td>
      <td>69.0</td>
      <td>2055274.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>4</td>
      <td>Rockabye (feat. Sean Paul &amp; Anne-Marie)</td>
      <td>Clean Bandit</td>
      <td>2356604.0</td>
      <td>https://open.spotify.com/track/5knuzwU65gJK7IF...</td>
      <td>2017-01-01</td>
      <td>5knuzwU65gJK7IF5yJsuaW</td>
      <td>251088.0</td>
      <td>0.40600</td>
      <td>...</td>
      <td>0.763</td>
      <td>0.000000</td>
      <td>0.180</td>
      <td>-4.068</td>
      <td>0.0523</td>
      <td>0.742</td>
      <td>101.965</td>
      <td>6MDME20pz9RveH9rEXvrOM</td>
      <td>80.0</td>
      <td>4092589.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>5</td>
      <td>One Dance</td>
      <td>Drake</td>
      <td>2259887.0</td>
      <td>https://open.spotify.com/track/1xznGGDReH1oQq0...</td>
      <td>2017-01-01</td>
      <td>1zi7xx7UVEFkmKfv06H8x0</td>
      <td>173987.0</td>
      <td>0.00776</td>
      <td>...</td>
      <td>0.625</td>
      <td>0.001800</td>
      <td>0.329</td>
      <td>-5.609</td>
      <td>0.0536</td>
      <td>0.370</td>
      <td>103.967</td>
      <td>3TVXtAsR1Inumwj472S9r4</td>
      <td>96.0</td>
      <td>51374698.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 21 columns</p>
</div>



Recall that we have saved a dataframe with no duplicates.


```python
no_dupes_df.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>position</th>
      <th>track_name</th>
      <th>artist</th>
      <th>streams</th>
      <th>url</th>
      <th>date</th>
      <th>track_id</th>
      <th>duration_ms</th>
      <th>acousticness</th>
      <th>...</th>
      <th>energy</th>
      <th>instrumentalness</th>
      <th>liveness</th>
      <th>loudness</th>
      <th>speechiness</th>
      <th>valence</th>
      <th>tempo</th>
      <th>artist_id</th>
      <th>popularity_index</th>
      <th>follower_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>200</th>
      <td>1</td>
      <td>1</td>
      <td>Shape of You</td>
      <td>Ed Sheeran</td>
      <td>7549041.0</td>
      <td>https://open.spotify.com/track/7qiZfU4dY1lWllz...</td>
      <td>2017-02-01</td>
      <td>7qiZfU4dY1lWllzX7mPBI3</td>
      <td>233713.0</td>
      <td>0.5810</td>
      <td>...</td>
      <td>0.652</td>
      <td>0.000000</td>
      <td>0.0931</td>
      <td>-3.183</td>
      <td>0.0802</td>
      <td>0.931</td>
      <td>95.977</td>
      <td>6eUKZXaKkcviH0Ku9w2n3V</td>
      <td>91.0</td>
      <td>73345259.0</td>
    </tr>
    <tr>
      <th>1000</th>
      <td>1</td>
      <td>1</td>
      <td>Despacito - Remix</td>
      <td>Luis Fonsi</td>
      <td>7332260.0</td>
      <td>https://open.spotify.com/track/5CtI0qwDJkDQGwX...</td>
      <td>2017-06-01</td>
      <td>6rPO02ozF3bM7NnOV4h6s2</td>
      <td>228827.0</td>
      <td>0.2280</td>
      <td>...</td>
      <td>0.816</td>
      <td>0.000000</td>
      <td>0.0967</td>
      <td>-4.353</td>
      <td>0.1670</td>
      <td>0.816</td>
      <td>178.085</td>
      <td>4V8Sr092TqfHkfAA5fXXqG</td>
      <td>78.0</td>
      <td>9035487.0</td>
    </tr>
    <tr>
      <th>2000</th>
      <td>1</td>
      <td>1</td>
      <td>rockstar</td>
      <td>Post Malone</td>
      <td>5755610.0</td>
      <td>https://open.spotify.com/track/7wGoVu4Dady5GV0...</td>
      <td>2017-11-01</td>
      <td>7ytR5pFWmSjzHJIeQkgog4</td>
      <td>181733.0</td>
      <td>0.2470</td>
      <td>...</td>
      <td>0.690</td>
      <td>0.000000</td>
      <td>0.1010</td>
      <td>-7.956</td>
      <td>0.1640</td>
      <td>0.497</td>
      <td>89.977</td>
      <td>4r63FhuTkUYltbVAg5TQnk</td>
      <td>93.0</td>
      <td>5174251.0</td>
    </tr>
    <tr>
      <th>1600</th>
      <td>1</td>
      <td>1</td>
      <td>Look What You Made Me Do</td>
      <td>Taylor Swift</td>
      <td>5547962.0</td>
      <td>https://open.spotify.com/track/6uFsE1JgZ20EXyU...</td>
      <td>2017-09-01</td>
      <td>1P17dC1amhFzptugyAO7Il</td>
      <td>211853.0</td>
      <td>0.2040</td>
      <td>...</td>
      <td>0.709</td>
      <td>0.000014</td>
      <td>0.1260</td>
      <td>-6.471</td>
      <td>0.1230</td>
      <td>0.506</td>
      <td>128.070</td>
      <td>06HL4z0CvFAxyc27GXpf02</td>
      <td>97.0</td>
      <td>34579892.0</td>
    </tr>
    <tr>
      <th>1001</th>
      <td>2</td>
      <td>2</td>
      <td>I'm the One</td>
      <td>DJ Khaled</td>
      <td>5208996.0</td>
      <td>https://open.spotify.com/track/72Q0FQQo32KJloi...</td>
      <td>2017-06-01</td>
      <td>1jYiIOC5d6soxkJP81fxq2</td>
      <td>288877.0</td>
      <td>0.0533</td>
      <td>...</td>
      <td>0.667</td>
      <td>0.000000</td>
      <td>0.1340</td>
      <td>-4.267</td>
      <td>0.0367</td>
      <td>0.817</td>
      <td>80.984</td>
      <td>0QHgL1lAIqAw0HtD7YldmP</td>
      <td>82.0</td>
      <td>5405048.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 21 columns</p>
</div>



Let's look at the popularities plotted against the number of streams a song has


```python
plt.scatter(no_dupes_df['popularity_index'], no_dupes_df['streams'])
plt.xlabel("Popularity of artist from 0 to 100")
plt.ylabel("Streams in millions")

```




    Text(0, 0.5, 'Streams in millions')




    
![svg](output_82_1.svg)
    


There are artists in the top 5 positions that have relatively low popularity indices compared to other artists on the top 200 chart. Understanding how these artists got to these high positions given low popularity indices would be valuabe. Let's try to locate all of these top 200 tracks that came from artists with low popularity indices, and see if we can learn from that group.


```python
# lowPopularityArtists = df.loc[df['popularity value'] < ] # Learning about songs on the top 200 chart with low artist popularity might help us understand what is actually important in trying to get a song on the top 200 chart
```

# Insight

In the final step of the data cycle, we draw conclusions based off our analysis to inform decisions made based on the data.

Does popularity/followers make a difference?

From our data visualization conclusions, especially our correlation matrix, it is shown that success (stream count) of a song has a positive and sometimes strong positive correlation with popularity, number of followers, loudness, valence, energy, and accousticness. When obeserving the Top 200, note that the while these correlations are merely postive, when observing the top 10, they are much more strongly positvely correlated. Liveness, tempo, and instrumentalness of have negative to strong negative correlation with success. 


The loudness of songs brings up an interesting reminder of the [Loudness War](https://en.wikipedia.org/wiki/Loudness_war) in the early 1940s. During the loudness war, even though increasing the loudness of a song ultimately reduced its fidelity (fine details), critics preferred the increasing levels. This may be an echo of the impacts of this cultural trend, or perhaps people simply like their music loud, even if at a lower quality.

We can conclude that a song by an artist with at least 200,000 followers, a popularity value of 80, a loudness value of -8, danceability x, valence x, energy x, accousticness x, is likely to enter the top 200 and potentially the top 10.

Observe the next years data (here we show our estimate was right)
