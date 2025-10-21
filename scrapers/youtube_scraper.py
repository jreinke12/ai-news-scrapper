"""
YouTube scraping module for financial channels
"""
from googleapiclient.discovery import build
from typing import List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import *
from datetime import datetime, timedelta

class YouTubeScraper:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    
    def get_channel_videos(self, channel_id: str, max_results: int = 5) -> List[Dict]:
        """
        Get recent videos from a YouTube channel
        
        Args:
            channel_id: YouTube channel ID
            max_results: Maximum number of videos to fetch
            
        Returns:
            List of video dictionaries
        """
        try:
            # Get channel's uploads playlist
            channel_response = self.youtube.channels().list(
                part='contentDetails',
                id=channel_id
            ).execute()
            
            if not channel_response['items']:
                print(f"Channel {channel_id} not found")
                return []
            
            uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from uploads playlist
            playlist_response = self.youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=max_results
            ).execute()
            
            videos = []
            for item in playlist_response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                snippet = item['snippet']
                
                # Get additional video details
                video_response = self.youtube.videos().list(
                    part='snippet,statistics',
                    id=video_id
                ).execute()
                
                if video_response['items']:
                    video_details = video_response['items'][0]
                    video_snippet = video_details['snippet']
                    video_stats = video_details.get('statistics', {})
                    
                    videos.append({
                        'title': video_snippet['title'],
                        'description': video_snippet['description'][:500],  # First 500 chars
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'source': snippet['channelTitle'],
                        'published_at': video_snippet['publishedAt'],
                        'view_count': int(video_stats.get('viewCount', 0)),
                        'like_count': int(video_stats.get('likeCount', 0)),
                        'content_type': 'youtube_video'
                    })
            
            return videos
            
        except Exception as e:
            print(f"Error fetching videos from channel {channel_id}: {e}")
            return []
    
    def search_financial_videos(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search for financial videos on YouTube
        
        Args:
            query: Search query
            max_results: Maximum number of videos to return
            
        Returns:
            List of video dictionaries
        """
        try:
            # Search for videos
            search_response = self.youtube.search().list(
                part='snippet',
                q=query,
                type='video',
                order='relevance',
                publishedAfter=(datetime.now() - timedelta(days=7)).isoformat() + 'Z',
                maxResults=max_results
            ).execute()
            
            videos = []
            for item in search_response['items']:
                video_id = item['id']['videoId']
                
                # Get video details
                video_response = self.youtube.videos().list(
                    part='snippet,statistics',
                    id=video_id
                ).execute()
                
                if video_response['items']:
                    video_details = video_response['items'][0]
                    video_snippet = video_details['snippet']
                    video_stats = video_details.get('statistics', {})
                    
                    videos.append({
                        'title': video_snippet['title'],
                        'description': video_snippet['description'][:500],
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'source': video_snippet['channelTitle'],
                        'published_at': video_snippet['publishedAt'],
                        'view_count': int(video_stats.get('viewCount', 0)),
                        'like_count': int(video_stats.get('likeCount', 0)),
                        'content_type': 'youtube_search'
                    })
            
            return videos
            
        except Exception as e:
            print(f"Error searching YouTube for '{query}': {e}")
            return []
    
    def get_all_youtube_content(self) -> List[Dict]:
        """
        Get all YouTube content from channels and searches
        """
        all_videos = []
        
        # Get videos from specific channels
        for channel_id in YOUTUBE_CHANNELS:
            channel_videos = self.get_channel_videos(channel_id, max_results=3)
            all_videos.extend(channel_videos)
        
        # Search for trending financial topics and expert content
        search_queries = YOUTUBE_EXPERT_SEARCHES + [
            "student loan forgiveness 2025",
            "PSLF public service loan forgiveness", 
            "personal finance tips 2025",
            "inflation impact young adults"
        ]
        
        for query in search_queries:
            search_videos = self.search_financial_videos(query, max_results=2)
            all_videos.extend(search_videos)
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_videos = []
        
        for video in all_videos:
            if video['url'] not in seen_urls:
                seen_urls.add(video['url'])
                unique_videos.append(video)
        
        # Sort by view count (most popular first)
        unique_videos.sort(key=lambda x: x['view_count'], reverse=True)
        
        return unique_videos[:MAX_YOUTUBE_VIDEOS]
