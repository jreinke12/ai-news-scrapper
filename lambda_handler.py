"""
AWS Lambda handler for the FitBUX Financial News Curator Agent
"""
import json
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_agent import run_news_curator

def lambda_handler(event, context):
    """
    AWS Lambda handler function
    
    Args:
        event: Lambda event data
        context: Lambda context
        
    Returns:
        Response dictionary
    """
    try:
        print("🚀 Lambda function started")
        print(f"Event: {json.dumps(event)}")
        
        # Run the news curator
        success = run_news_curator()
        
        if success:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'FitBUX News Curator completed successfully',
                    'timestamp': context.aws_request_id
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'message': 'FitBUX News Curator failed',
                    'timestamp': context.aws_request_id
                })
            }
            
    except Exception as e:
        print(f"❌ Lambda function error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Lambda function error: {str(e)}',
                'timestamp': context.aws_request_id
            })
        }
