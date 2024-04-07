import googleapiclient.discovery
import googleapiclient.errors

from KeyTopicsGenerator import RetrieveTopics

if __name__ == '__main__':
    topic_retriever = RetrieveTopics()
    key_topics = topic_retriever.RetrieveTopics() 


def GetVideos(key_topics):
    # Parameters
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "***"  

    # Get service
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    # Define search parameters
    for topic in key_topics:
        search_keyword = topic
        max_results = 2  

        request = youtube.search().list(
            part="snippet",
            maxResults=max_results,
            q=search_keyword,
            order="relevance", 
            type="video",  
        )

        # Execute the request and get the response
        response = request.execute()

        # Print video titles and IDs
        for item in response.get("items", []):
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            print(f"{topic}: {title} - https://www.youtube.com/watch?v={video_id}")


GetVideos(key_topics)