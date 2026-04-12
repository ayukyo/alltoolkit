"""
AllToolkit - Cron Utils Advanced Examples

Advanced usage patterns and real-world scenarios.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import create_scheduler, CronParser, CronMatcher, validate, next_run
from datetime import datetime, timedelta
import time


class TaskLogger:
    """Simple logger for task executions."""
    
    def __init__(self, filename="cron_task_log.txt"):
        self.filename = filename
    
    def log(self, task_name: str, message: str):
        """Log a message with timestamp."""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {task_name}: {message}\n"
        
        with open(self.filename, 'a') as f:
            f.write(log_entry)
        
        print(log_entry.strip())


class EmailNotifier:
    """Mock email notifier for demonstrations."""
    
    def __init__(self, recipients: list):
        self.recipients = recipients
        self.sent_count = 0
    
    def send(self, subject: str, body: str):
        """Send an email (mock implementation)."""
        self.sent_count += 1
        print(f"  📧 Email sent to {len(self.recipients)} recipients")
        print(f"     Subject: {subject}")
        print(f"     Body preview: {body[:50]}...")


class DatabaseCleaner:
    """Mock database cleaner for demonstrations."""
    
    def __init__(self):
        self.cleaned_count = 0
    
    def clean_old_records(self, days: int = 30):
        """Clean records older than specified days."""
        self.cleaned_count += 1
        print(f"  🗑️  Cleaned records older than {days} days")
        print(f"     Total cleanups performed: {self.cleaned_count}")


class ReportGenerator:
    """Mock report generator for demonstrations."""
    
    def __init__(self):
        self.reports_generated = 0
    
    def generate_daily_report(self):
        """Generate a daily report."""
        self.reports_generated += 1
        print(f"  📊 Daily report generated")
        print(f"     Total reports: {self.reports_generated}")
    
    def generate_weekly_report(self):
        """Generate a weekly report."""
        self.reports_generated += 1
        print(f"  📈 Weekly report generated")
        print(f"     Total reports: {self.reports_generated}")
    
    def generate_monthly_report(self):
        """Generate a monthly report."""
        self.reports_generated += 1
        print(f"  📉 Monthly report generated")
        print(f"     Total reports: {self.reports_generated}")


def example_1_production_scheduler():
    """Example 1: Production-like scheduler with logging."""
    print("=" * 60)
    print("Example 1: Production Scheduler with Logging")
    print("=" * 60)
    
    scheduler = create_scheduler()
    logger = TaskLogger()
    
    # Create tasks with logging
    def logged_task(name, callback):
        def wrapper():
            try:
                logger.log(name, "Starting task")
                callback()
                logger.log(name, "Task completed successfully")
            except Exception as e:
                logger.log(name, f"Task failed: {str(e)}")
                raise
        
        return wrapper
    
    # Add tasks with logging
    scheduler.add_task(
        "backup",
        "Database Backup",
        "0 2 * * *",  # Daily at 2 AM
        logged_task("backup", lambda: print("  💾 Backup completed"))
    )
    
    scheduler.add_task(
        "cleanup",
        "Temp File Cleanup",
        "0 3 * * *",  # Daily at 3 AM
        logged_task("cleanup", lambda: print("  🧹 Cleanup completed"))
    )
    
    print("Tasks configured with logging")
    for task in scheduler.list_tasks():
        print(f"  - {task.name}: {task.cron_expr}")
    print()
    
    scheduler.stop()


def example_2_task_dependencies():
    """Example 2: Tasks with dependencies."""
    print("=" * 60)
    print("Example 2: Tasks with Dependencies")
    print("=" * 60)
    
    scheduler = create_scheduler()
    task_status = {}
    
    def create_dependent_task(task_id, name, dependencies, callback):
        """Create a task that only runs if dependencies succeeded."""
        def wrapper():
            # Check dependencies
            for dep_id in dependencies:
                dep_task = scheduler.get_task(dep_id)
                if dep_task and dep_task.last_error:
                    print(f"  ⚠️  Skipping {name}: dependency {dep_id} failed")
                    return
            
            # Run the task
            print(f"  ✓ Dependencies met, running {name}")
            callback()
            task_status[task_id] = "success"
        
        return wrapper
    
    # Task 1: Extract data
    scheduler.add_task(
        "extract",
        "Extract Data",
        "0 1 * * *",
        create_dependent_task("extract", "Extract Data", [], 
                             lambda: print("  📥 Data extracted"))
    )
    
    # Task 2: Transform data (depends on extract)
    scheduler.add_task(
        "transform",
        "Transform Data",
        "0 2 * * *",
        create_dependent_task("transform", "Transform Data", ["extract"],
                             lambda: print("  🔄 Data transformed"))
    )
    
    # Task 3: Load data (depends on transform)
    scheduler.add_task(
        "load",
        "Load Data",
        "0 3 * * *",
        create_dependent_task("load", "Load Data", ["transform"],
                             lambda: print("  📤 Data loaded"))
    )
    
    print("ETL pipeline configured:")
    for task in scheduler.list_tasks():
        print(f"  - {task.name} at {task.cron_expr}")
    print()
    
    # Simulate running the pipeline
    print("Simulating ETL pipeline execution...")
    for task in scheduler.list_tasks():
        task.schedule.next_execution = datetime.now() - timedelta(minutes=1)
    
    scheduler.run_due_tasks()
    print()
    
    scheduler.stop()


def example_3_notification_system():
    """Example 3: Automated notification system."""
    print("=" * 60)
    print("Example 3: Automated Notification System")
    print("=" * 60)
    
    scheduler = create_scheduler()
    notifier = EmailNotifier(["admin@example.com", "team@example.com"])
    
    # Morning digest
    def send_morning_digest():
        notifier.send(
            "Morning Digest",
            "Good morning! Here's your daily summary..."
        )
    
    scheduler.add_task(
        "morning_digest",
        "Morning Digest Email",
        "0 8 * * mon-fri",  # Weekdays at 8 AM
        send_morning_digest
    )
    
    # Weekly report
    def send_weekly_report():
        notifier.send(
            "Weekly Report",
            "Here's your weekly performance report..."
        )
    
    scheduler.add_task(
        "weekly_report",
        "Weekly Report Email",
        "0 9 * * mon",  # Monday at 9 AM
        send_weekly_report
    )
    
    # Monthly summary
    def send_monthly_summary():
        notifier.send(
            "Monthly Summary",
            "Here's your monthly activity summary..."
        )
    
    scheduler.add_task(
        "monthly_summary",
        "Monthly Summary Email",
        "0 10 1 * *",  # First of month at 10 AM
        send_monthly_summary
    )
    
    print("Notification schedule:")
    for task in scheduler.list_tasks():
        print(f"  - {task.name}: {task.cron_expr}")
        print(f"    Next: {task.schedule.next_execution}")
    print()
    
    # Show upcoming notifications
    print("Upcoming notifications:")
    matcher = CronMatcher()
    now = datetime.now()
    
    notifications = [
        ("Morning Digest", "0 8 * * mon-fri"),
        ("Weekly Report", "0 9 * * mon"),
        ("Monthly Summary", "0 10 1 * *"),
    ]
    
    for name, expr in notifications:
        next_dt = matcher.next_run(expr, after=now)
        print(f"  {name}: {next_dt}")
    print()
    
    scheduler.stop()


def example_4_maintenance_window():
    """Example 4: Maintenance window scheduling."""
    print("=" * 60)
    print("Example 4: Maintenance Window Scheduling")
    print("=" * 60)
    
    scheduler = create_scheduler()
    cleaner = DatabaseCleaner()
    
    # Daily maintenance (lightweight)
    scheduler.add_task(
        "daily_maintenance",
        "Daily Maintenance",
        "30 3 * * *",  # 3:30 AM daily
        lambda: print("  🔧 Daily maintenance completed")
    )
    
    # Weekly deep clean
    scheduler.add_task(
        "weekly_cleanup",
        "Weekly Deep Clean",
        "0 2 * * sun",  # Sunday 2 AM
        lambda: cleaner.clean_old_records(30)
    )
    
    # Monthly archive
    scheduler.add_task(
        "monthly_archive",
        "Monthly Archive",
        "0 1 1 * *",  # First of month 1 AM
        lambda: cleaner.clean_old_records(90)
    )
    
    # Quarterly audit
    scheduler.add_task(
        "quarterly_audit",
        "Quarterly Audit",
        "0 0 1 jan,apr,jul,oct *",  # First of quarter months
        lambda: print("  📋 Quarterly audit completed")
    )
    
    print("Maintenance schedule:")
    for task in scheduler.list_tasks():
        print(f"  - {task.name}")
        print(f"    Schedule: {task.cron_expr}")
        print(f"    Next: {task.schedule.next_execution}")
    print()
    
    scheduler.stop()


def example_5_health_check():
    """Example 5: Health check monitoring."""
    print("=" * 60)
    print("Example 5: Health Check Monitoring")
    print("=" * 60)
    
    scheduler = create_scheduler()
    health_status = {"api": True, "database": True, "cache": True}
    
    def check_api_health():
        print("  ❤️  Checking API health...")
        # Simulate health check
        health_status["api"] = True
        print("     API: OK")
    
    def check_database_health():
        print("  ❤️  Checking database health...")
        health_status["database"] = True
        print("     Database: OK")
    
    def check_cache_health():
        print("  ❤️  Checking cache health...")
        health_status["cache"] = True
        print("     Cache: OK")
    
    def generate_health_report():
        print("  📊 Generating health report...")
        all_healthy = all(health_status.values())
        status = "All systems operational" if all_healthy else "Issues detected"
        print(f"     Status: {status}")
    
    # Health checks every 5 minutes
    scheduler.add_task(
        "health_api",
        "API Health Check",
        "*/5 * * * *",
        check_api_health
    )
    
    scheduler.add_task(
        "health_db",
        "Database Health Check",
        "*/5 * * * *",
        check_database_health
    )
    
    scheduler.add_task(
        "health_cache",
        "Cache Health Check",
        "*/5 * * * *",
        check_cache_health
    )
    
    # Hourly health report
    scheduler.add_task(
        "health_report",
        "Hourly Health Report",
        "0 * * * *",
        generate_health_report
    )
    
    print("Health monitoring configured:")
    for task in scheduler.list_tasks():
        print(f"  - {task.name}: {task.cron_expr}")
    print()
    
    # Run a quick check
    print("Running health checks...")
    for task in scheduler.list_tasks()[:3]:
        task.schedule.next_execution = datetime.now() - timedelta(minutes=1)
    scheduler.run_due_tasks()
    print()
    
    scheduler.stop()


def example_6_reporting_pipeline():
    """Example 6: Automated reporting pipeline."""
    print("=" * 60)
    print("Example 6: Automated Reporting Pipeline")
    print("=" * 60)
    
    scheduler = create_scheduler()
    reporter = ReportGenerator()
    notifier = EmailNotifier(["reports@example.com"])
    
    def daily_report_with_notification():
        reporter.generate_daily_report()
        notifier.send("Daily Report", "Your daily report is ready...")
    
    def weekly_report_with_notification():
        reporter.generate_weekly_report()
        notifier.send("Weekly Report", "Your weekly report is ready...")
    
    def monthly_report_with_notification():
        reporter.generate_monthly_report()
        notifier.send("Monthly Report", "Your monthly report is ready...")
    
    # Daily report at 7 AM
    scheduler.add_task(
        "daily_report",
        "Daily Report",
        "0 7 * * *",
        daily_report_with_notification
    )
    
    # Weekly report on Monday 8 AM
    scheduler.add_task(
        "weekly_report",
        "Weekly Report",
        "0 8 * * mon",
        weekly_report_with_notification
    )
    
    # Monthly report on 1st at 9 AM
    scheduler.add_task(
        "monthly_report",
        "Monthly Report",
        "0 9 1 * *",
        monthly_report_with_notification
    )
    
    print("Reporting pipeline configured:")
    for task in scheduler.list_tasks():
        print(f"  - {task.name}")
        print(f"    Schedule: {task.cron_expr}")
        print(f"    Next: {task.schedule.next_execution}")
    print()
    
    print(f"Total reports generated: {reporter.reports_generated}")
    print(f"Total emails sent: {notifier.sent_count}")
    print()
    
    scheduler.stop()


def example_7_rate_limiting():
    """Example 7: Rate limiting with cron."""
    print("=" * 60)
    print("Example 7: Rate Limiting Simulation")
    print("=" * 60)
    
    from mod import CronParser
    
    parser = CronParser()
    
    # Simulate rate limiting windows
    rate_limits = {
        "api_calls": "*/1 * * * *",  # Reset every minute
        "daily_quota": "0 0 * * *",  # Reset daily
        "weekly_quota": "0 0 * * mon",  # Reset weekly
    }
    
    print("Rate limit reset schedules:")
    for name, expr in rate_limits.items():
        if validate(expr):
            next_reset = next_run(expr)
            print(f"  {name}:")
            print(f"    Expression: {expr}")
            print(f"    Next reset: {next_reset}")
    print()
    
    # Calculate how many times something runs in a period
    matcher = CronMatcher()
    now = datetime.now()
    
    # Count executions in next 24 hours
    expr = "*/15 * * * *"  # Every 15 minutes
    runs = matcher.next_runs(expr, count=96, after=now)  # 24 hours * 4 per hour
    
    print(f"Expression: {expr}")
    print(f"Executions in next 24 hours: {len(runs)}")
    print(f"First: {runs[0]}")
    print(f"Last: {runs[-1]}")
    print()


def example_8_business_hours():
    """Example 8: Business hours scheduling."""
    print("=" * 60)
    print("Example 8: Business Hours Scheduling")
    print("=" * 60)
    
    # Business hours: 9 AM - 6 PM, Monday to Friday
    business_hours_expr = "0 9-18 * * mon-fri"
    
    print(f"Business hours expression: {business_hours_expr}")
    print(f"Valid: {validate(business_hours_expr)}")
    print()
    
    matcher = CronMatcher()
    now = datetime.now()
    
    # Show next week's business hour starts
    print("Next business hour starts:")
    runs = matcher.next_runs("0 9 * * mon-fri", count=5, after=now)
    for i, run in enumerate(runs, 1):
        print(f"  Day {i}: {run.strftime('%A, %Y-%m-%d %H:%M')}")
    print()
    
    # Show business hour ends
    print("Business hour ends (6 PM):")
    runs = matcher.next_runs("0 18 * * mon-fri", count=5, after=now)
    for i, run in enumerate(runs, 1):
        print(f"  Day {i}: {run.strftime('%A, %Y-%m-%d %H:%M')}")
    print()
    
    # Lunch reminder at noon
    lunch_expr = "0 12 * * mon-fri"
    print(f"Lunch reminder: {lunch_expr}")
    next_lunch = matcher.next_run(lunch_expr, after=now)
    print(f"Next lunch reminder: {next_lunch}")
    print()


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("AllToolkit - Cron Utils Advanced Examples")
    print("=" * 60 + "\n")
    
    example_1_production_scheduler()
    example_2_task_dependencies()
    example_3_notification_system()
    example_4_maintenance_window()
    example_5_health_check()
    example_6_reporting_pipeline()
    example_7_rate_limiting()
    example_8_business_hours()
    
    print("=" * 60)
    print("All advanced examples completed!")
    print("=" * 60)
