"""
Email system for sending daily digest with markdown attachments
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import pytz
from typing import List, Dict
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import *

class EmailSystem:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_user = EMAIL_USER
        self.email_pass = EMAIL_PASS
        self.email_from = EMAIL_FROM
        self.email_to = EMAIL_TO
    
    def create_digest_content(self, processed_content: Dict) -> str:
        """
        Create the main digest content in markdown format
        
        Args:
            processed_content: Dictionary with content and FitBUX perspective
            
        Returns:
            Markdown formatted digest content
        """
        now = datetime.now(pytz.timezone('US/Central'))
        date_str = now.strftime("%B %d, %Y")
        time_str = now.strftime("%I:%M %p %Z")
        
        # Start building the digest
        digest = f"""Date: {date_str}
Compiled automatically at {time_str}

===============================================

TOP FINANCIAL STORIES FOR YOUNG PROFESSIONALS
===============================================

"""
        
        # Add each content item
        for i, content in enumerate(processed_content['content'][:10], 1):
            title = content.get('title', 'No Title')
            source = content.get('source', 'Unknown Source')
            url = content.get('url', '#')
            summary = content.get('fitbux_summary', 'Summary not available')
            content_type = content.get('content_type', '')
            
            # Add type indicator based on content type
            type_indicator = {
                'news': '[NEWS]',
                'reddit_post': '[REDDIT]',
                'reddit_discussion': '[DISCUSSION]',
                'youtube_video': '[VIDEO]',
                'youtube_search': '[YOUTUBE]',
                'expert_article': '[EXPERT]'
            }.get(content_type, '[ARTICLE]')
            
            digest += f"""{i}. {type_indicator} {title}
   Source: {source}
   Link: {url}
   
   Summary: {summary}
   
   {'-' * 60}
   
"""
        
        # Add FitBUX Perspective
        digest += f"""
===============================================

FITBUX PERSPECTIVE
===============================================

{processed_content['fitbux_perspective']}

===============================================

This digest was automatically compiled by the FitBUX Financial News Curator Agent.
For questions or feedback, contact jreinke@fitbux.com
"""
        
        return digest
    
    def create_markdown_file(self, digest_content: str) -> str:
        """
        Create a markdown file with the digest content
        
        Args:
            digest_content: The digest content in markdown format
            
        Returns:
            Path to the created markdown file
        """
        now = datetime.now(pytz.timezone('US/Central'))
        filename = f"fitbux_digest_{now.strftime('%Y%m%d_%H%M')}.md"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(digest_content)
            return filename
        except Exception as e:
            print(f"Error creating markdown file: {e}")
            return None
    
    def send_email(self, digest_content: str, markdown_file_path: str = None) -> bool:
        """
        Send the digest email with optional markdown attachment
        
        Args:
            digest_content: The digest content
            markdown_file_path: Path to markdown file to attach
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_from
            msg['To'] = self.email_to
            msg['Subject'] = f"FitBUX Financial News Digest – {datetime.now(pytz.timezone('US/Central')).strftime('%B %d, %Y')}"
            
            # Add body
            msg.attach(MIMEText(digest_content, 'html'))
            
            # Add markdown file as attachment if provided
            if markdown_file_path and os.path.exists(markdown_file_path):
                with open(markdown_file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(markdown_file_path)}'
                )
                msg.attach(part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_pass)
                text = msg.as_string()
                server.sendmail(self.email_from, self.email_to, text)
            
            print(f"Email sent successfully to {self.email_to}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_digest(self, processed_content: Dict) -> bool:
        """
        Send the complete digest with markdown attachment
        
        Args:
            processed_content: Dictionary with processed content
            
        Returns:
            True if sent successfully
        """
        # Create digest content
        digest_content = self.create_digest_content(processed_content)
        
        # Create markdown file
        markdown_file = self.create_markdown_file(digest_content)
        
        # Send email
        success = self.send_email(digest_content, markdown_file)
        
        # Clean up markdown file after sending
        if markdown_file and os.path.exists(markdown_file):
            try:
                os.remove(markdown_file)
            except Exception as e:
                print(f"Error cleaning up markdown file: {e}")
        
        return success
