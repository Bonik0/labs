from googleapiclient.discovery import build
from config import db_config
from mysqlclass import my_sql_serv

api_key = "AIzaSyAuTwKIkOUI0IouVtugq9KcAFE9fF5elrg"
api_key2 = "AIzaSyDMF4m4WpzbWI9q6fjLoZAO1CeH48YIaFU"
channel_name = "ersssdi"

class Video:
    def __init__(self, api_key, videos_id) -> None: #( min(videoCount, 250) / 50) quota 
        print("v0!!")
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey = self.api_key)
        self.videos = Video.__get_deteils_of_all_videos(self, videos_id)

    def __get_deteils_of_all_videos(self, videos_id) -> list: #( min(videoCount, 250) / 50) quota 
        print("v1!!\n")
        dist_of_video_dateils = []
        videos_count = len(videos_id)
        while (videos_count > 0):
            request_ids = ",".join(videos_id[len(videos_id) - videos_count: len(videos_id) - videos_count + 50])
            request = self.youtube.videos().list(
                part = "snippet, statistics, liveStreamingDetails",
                maxResults = 50,
                id = request_ids
            )
            response = request.execute()
            for item in response["items"]:
               dist_of_video_dateils.append({
                        "id": item["id"],
                        "publishedAt": item["snippet"]["publishedAt"],
                        "channelId" :  item["snippet"]["channelId"], 
                        "title" : item["snippet"]["title"], 
                        "viewCount" : int(item["statistics"]["viewCount"]),
                        "likeCount" :  int(item["statistics"]["likeCount"]),
                        "commentCount" : int(item["statistics"]["commentCount"])
                })
            videos_count -= 50
        return dist_of_video_dateils
    
    def get_main_information(self) -> list: #0 quota
        return self.videos

    def sort_videos_by_counter(self, parametr) -> list: #0 quota
        videos = [[self.videos[i][f"{parametr}Count"], i] for i in range(len(self.videos))]
        videos.sort()
        videos_sort = []
        for i in videos:
            videos_sort.append(self.videos[i[1]])
        return videos_sort




class channel:
    def __init__(self, api_key, channel_name, db_config) -> None: #1 or 101 quota
        print("c0!!")
        self.api_key = api_key
        self.server = my_sql_serv(db_config)
        self.youtube = build("youtube", "v3", developerKey = self.api_key)
        self.channel_name = channel_name
        self.channel_id = self.server.find_channel_id(self.channel_name)
        if self.channel_id == "":
            self.channel_id = channel.__find_id_for_channel(self)
            self.server.update_channels(self.channel_name,self.channel_id)
        self.channel_main_details = channel.__get_channel_main_details(self)

    def __find_id_for_channel(self) -> str: # 100 quota
        print("c1!!")
        request = self.youtube.search().list(
            part = "snippet",
            q = self.channel_name,
            maxResults = 5,
            order = "relevance",
            type = "channel"
        )
        response = request.execute()
        for item in response["items"]:
            if item["snippet"]["channelTitle"] == self.channel_name:
                return item["id"]["channelId"]
        print("ERROR IN 1")
        return ""

    def __get_channel_main_details(self) -> dict: #1 quota 
        print("c3!!\n")
        request = self.youtube.channels().list(
            part = "snippet, statistics, contentDetails", 
            maxResults = 1,
            id = self.channel_id)
        response = request.execute()
        return {"relatedPlaylists": response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"], 
                "viewCount": response["items"][0]["statistics"]["viewCount"],
                "subscriberCount" : response["items"][0]["statistics"]["subscriberCount"], 
                "videoCount" : response["items"][0]["statistics"][ "videoCount"]}
    
    def get_all_videos_id_for_channel(self) -> list: # ( min(videoCount, 250) / 50) quota
        print("c7!!")
        videos_id = []
        nextPageToken = ""
        videos_count = min(int(self.channel_main_details["videoCount"]), 250)
        while(videos_count > 0):
            request = self.youtube.playlistItems().list(
                part = "snippet",
                maxResults = 50,
                pageToken = nextPageToken, 
                playlistId = self.channel_main_details["relatedPlaylists"]
            )
            response = request.execute()
            if videos_count - 50 > 0:
                nextPageToken = response["nextPageToken"]
            for item in response["items"]:
                videos_id.append(item["snippet"]["resourceId"]["videoId"])
            videos_count -= 50 
        return videos_id

    def get_channel_main_details(self) -> dict: #0 quota
        print("c6!!")
        return self.channel_main_details
    
    def get_channel_all_details(self) -> dict: #1 quota
        print("c4!!\n")
        request = self.youtube.channels().list(
            part = "snippet, statistics, contentDetails", 
            maxResults = 1,
            id = self.channel_id)
        response = request.execute()
        return response 


    
new_chanel = channel(api_key, channel_name, db_config)
print(new_chanel.channel_id, new_chanel.channel_name)
videos_list = Video(api_key, new_chanel.get_all_videos_id_for_channel())
print(videos_list.sort_videos_by_counter("view"))