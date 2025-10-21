"""
AI summarization module using OpenAI with FitBUX brand voice
"""
import openai
from typing import List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import *
import json
import os

class AISummarizer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Load brand guidelines
        self.brand_guidelines = self._load_brand_guidelines()
    
    def _load_brand_guidelines(self) -> str:
        """Load brand guidelines from file"""
        try:
            brand_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'brand_guidelines.md')
            with open(brand_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "Use FitBUX's Innocent Everyman voice: calm, trustworthy, educational, and empowering."
    
    def summarize_content(self, content: Dict) -> str:
        """
        Summarize a single piece of content using FitBUX's brand voice
        
        Args:
            content: Dictionary containing title, description, url, source, etc.
            
        Returns:
            Summary string in FitBUX voice
        """
        # Prepare content for summarization
        content_text = f"""
        Title: {content.get('title', '')}
        Description: {content.get('description', '')}
        Source: {content.get('source', '')}
        URL: {content.get('url', '')}
        """
        
        if content.get('content'):
            content_text += f"\nContent: {content['content']}"
        
        prompt = f"""
        You are FitBUX's financial content summarizer. Follow the brand voice guidelines below:

        {self.brand_guidelines}

        Summarize the following financial content in 2-3 sentences for young professionals (20-40 years old).
        Use FitBUX's Innocent Everyman voice: calm, trustworthy, educational, and empowering.
        Focus on what this means for their personal finances and why it matters.
        Always end with either a lesson, next step, or feeling of progress.

        Content to summarize:
        {content_text}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are FitBUX's financial content summarizer. Always use the Innocent Everyman voice: calm, trustworthy, educational, and empowering."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.6
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error summarizing content: {e}")
            return f"Important financial update from {content.get('source', 'Unknown')}: {content.get('title', 'No title available')}"
    
    def create_fitbux_perspective(self, all_content: List[Dict]) -> str:
        """
        Create the FitBUX Perspective section based on all content
        
        Args:
            all_content: List of all content items
            
        Returns:
            FitBUX perspective summary
        """
        # Extract key themes from content
        themes = []
        for content in all_content:
            title = content.get('title', '').lower()
            description = content.get('description', '').lower()
            
            if any(keyword in title or keyword in description for keyword in ['student loan', 'pslf', 'forgiveness']):
                themes.append('student loans')
            elif any(keyword in title or keyword in description for keyword in ['inflation', 'cost', 'price']):
                themes.append('inflation')
            elif any(keyword in title or keyword in description for keyword in ['housing', 'home', 'mortgage']):
                themes.append('housing')
            elif any(keyword in title or keyword in description for keyword in ['credit', 'debt', 'payment']):
                themes.append('credit and debt')
        
        # Create perspective prompt
        themes_text = ', '.join(set(themes)) if themes else 'general financial topics'
        
        prompt = f"""
        You are FitBUX's financial perspective writer. Follow the brand voice guidelines:

        {self.brand_guidelines}

        Write a 3-5 sentence summary of today's financial landscape for young professionals (20-40).
        The main themes today are: {themes_text}
        
        Use FitBUX's Innocent Everyman voice: calm, trustworthy, educational, and empowering.
        Acknowledge any concerns but provide reassurance and direction.
        End with a sense of progress or next steps.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are FitBUX's financial perspective writer. Always use the Innocent Everyman voice."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error creating FitBUX perspective: {e}")
            return "Today's financial landscape continues to evolve, and staying informed helps you make confident decisions about your money. Remember, you're not alone in navigating these changes - thousands of professionals like you are building their financial future one step at a time."
    
    def process_all_content(self, news_articles: List[Dict], reddit_posts: List[Dict], youtube_videos: List[Dict]) -> Dict:
        """
        Process all content and create summaries
        
        Args:
            news_articles: List of news articles
            reddit_posts: List of Reddit posts
            youtube_videos: List of YouTube videos
            
        Returns:
            Dictionary with processed content and summaries
        """
        all_content = news_articles + reddit_posts + youtube_videos
        
        # Summarize each piece of content
        summarized_content = []
        for content in all_content:
            summary = self.summarize_content(content)
            content['fitbux_summary'] = summary
            summarized_content.append(content)
        
        # Create FitBUX perspective
        fitbux_perspective = self.create_fitbux_perspective(all_content)
        
        return {
            'content': summarized_content,
            'fitbux_perspective': fitbux_perspective,
            'total_items': len(all_content)
        }
