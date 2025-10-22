"""
Scheduling system for the FitBUX Financial News Curator Agent
"""
import schedule
import time
import pytz
from datetime import datetime
from config.config import *
from main_agent import run_news_curator

class NewsScheduler:
    def __init__(self):
        self.central_tz = pytz.timezone('US/Central')
        self.setup_schedule()
    
    def setup_schedule(self):
        """Set up the scheduling based on configuration"""
        
        # Weekday schedule (Monday-Friday): 6am, 9am, 12pm, 3pm, 5pm CST
        for time_str in SCHEDULE_CONFIG['weekdays']['times']:
            schedule.every().monday.at(time_str).do(self.run_curator_job)
            schedule.every().tuesday.at(time_str).do(self.run_curator_job)
            schedule.every().wednesday.at(time_str).do(self.run_curator_job)
            schedule.every().thursday.at(time_str).do(self.run_curator_job)
            schedule.every().friday.at(time_str).do(self.run_curator_job)
        
        # Weekend schedule (Saturday-Sunday): 6pm CST
        for time_str in SCHEDULE_CONFIG['weekends']['times']:
            schedule.every().saturday.at(time_str).do(self.run_curator_job)
            schedule.every().sunday.at(time_str).do(self.run_curator_job)
        
        print("Schedule configured:")
        print("Weekdays (Mon-Fri): 6:00 AM, 9:00 AM, 12:00 PM, 3:00 PM, 5:00 PM CST")
        print("Weekends (Sat-Sun): 6:00 PM CST")
    
    def run_curator_job(self):
        """Run the news curator job"""
        try:
            current_time = datetime.now(self.central_tz).strftime("%Y-%m-%d %H:%M:%S %Z")
            print(f"\n{'='*50}")
            print(f"Running FitBUX News Curator at {current_time}")
            print(f"{'='*50}")
            
            # Run the main curator function
            success = run_news_curator()
            
            if success:
                print(f"SUCCESS: News curator completed successfully at {current_time}")
            else:
                print(f"ERROR: News curator failed at {current_time}")
                
        except Exception as e:
            print(f"ERROR: Error running news curator: {e}")
    
    def run_scheduler(self):
        """Run the scheduler (blocking)"""
        print("FitBUX News Curator Scheduler started")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\nScheduler stopped by user")
    
    def run_once(self):
        """Run the curator once immediately (for testing)"""
        print("Running FitBUX News Curator once (test mode)")
        self.run_curator_job()
    
    def get_next_run_times(self):
        """Get the next scheduled run times"""
        next_runs = []
        
        for job in schedule.jobs:
            next_run = job.next_run
            if next_run:
                next_runs.append({
                    'job': str(job.job_func),
                    'next_run': next_run.strftime("%Y-%m-%d %H:%M:%S %Z")
                })
        
        return sorted(next_runs, key=lambda x: x['next_run'])
    
    def print_schedule_status(self):
        """Print current schedule status"""
        print("\nCurrent Schedule Status:")
        print("-" * 40)
        
        next_runs = self.get_next_run_times()
        for run_info in next_runs[:5]:  # Show next 5 runs
            print(f"Next: {run_info['next_run']}")
        
        print(f"\nTotal scheduled jobs: {len(schedule.jobs)}")

def main():
    """Main function to run the scheduler"""
    scheduler = NewsScheduler()
    
    # Print initial status
    scheduler.print_schedule_status()
    
    # Check if running in test mode
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        scheduler.run_once()
    else:
        scheduler.run_scheduler()

if __name__ == "__main__":
    main()
