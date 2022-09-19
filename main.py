from pytube import Channel
from pytube import Playlist

class FindVideoByKeywords:
    def __init__(self,link:str):
        try:
            self.videos_container = Channel(link)
        except:
            self.videos_container = Playlist(link)
        self.keywords = []
        self.captions = []
        self.last_analizys = []
        

    def set_keywords(self, keywords):
        if type(keywords) == list: 
            self.keywords = {x:1 for x in keywords}
        else:
            self.keywords = keywords
    
    def get_captions(self, lang):
        """Get transcript of all videos"""
        for video in self.videos_container.videos:
            try:
                caption = video.captions[lang].generate_list_captions()
                self.captions.append({"title":video.title, "caption":caption}) 
            except Exception as e:
                print(f"ERROR --->: {video.title}")
        
        return self.captions
    
    def analyze(self):
        rated_videos = []
        for v in self.captions:
            v_rate = {"title" : v["title"], "points" : 0, "ocurrences" : []}
            for track in v["caption"]:
                for word in self.keywords.keys():
                    if word in track["text"]:
                        v_rate["points"] += self.keywords[word]
                        v_rate["ocurrences"].append(
                            f"{track['start']} --> {track['end']} {track['text']}"
                        )
            rated_videos.append(v_rate)
        rated_videos.sort(key=lambda x:x["points"],reverse=True)
        self.last_analizys.append(rated_videos) 
        return rated_videos
    
    @staticmethod 
    def visualize(rated_videos:list):
        for video in rated_videos:
            print(f"\n{video['title']} --> pontos : {video['points']}")
            for ocurrence in video["ocurrences"]:
                print("\t",ocurrence)

if __name__ == "__main__":
    #testar se ta tudo ok
    channel = FindVideoByKeywords("https://www.youtube.com/c/Dunossauro")
    captions = channel.get_captions("a.pt")
    channel.set_keywords({"sexo": 10, "amor":5, "tesão":10})
    result = channel.analyze()
    channel.visualize(result)
