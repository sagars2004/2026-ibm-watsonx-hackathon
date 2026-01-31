"""
Silent Bottleneck Detector - Mock Data Generators

Generates realistic mock data that demonstrates bottleneck patterns:
- Single points of failure (one person doing 78% of reviews)
- Hidden delays (18-hour deploy queues)
- Flaky processes (CI/CD failures)
- Knowledge silos (only 2 people touching critical code)
- Meeting overload (34% of time in meetings)
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import uuid


# Team members for realistic data
TEAM_MEMBERS = [
    {"id": "sarah", "name": "Sarah Chen", "role": "Senior Engineer", "avatar": "👩‍💻"},
    {"id": "mike", "name": "Mike Johnson", "role": "DevOps Lead", "avatar": "👨‍💻"},
    {"id": "alex", "name": "Alex Rivera", "role": "Backend Developer", "avatar": "🧑‍💻"},
    {"id": "emma", "name": "Emma Wilson", "role": "Frontend Developer", "avatar": "👩‍💻"},
    {"id": "james", "name": "James Park", "role": "Full Stack Developer", "avatar": "👨‍💻"},
    {"id": "lisa", "name": "Lisa Thompson", "role": "QA Engineer", "avatar": "👩‍💻"},
]

# Code areas for knowledge silo detection
CODE_AREAS = [
    "auth",
    "payments",
    "api-gateway",
    "user-management",
    "notifications",
    "analytics",
    "database",
    "frontend-core",
]


def generate_github_data(days: int = 30) -> Dict[str, Any]:
    """
    Generate GitHub PR data with intentional bottleneck patterns:
    - Sarah reviews 78% of all PRs (single point of failure)
    - Long review times averaging 18+ hours
    - Knowledge silos in auth and payments
    """
    pull_requests = []
    now = datetime.now()
    
    # Generate PRs for the past N days
    for i in range(days * 2):  # ~2 PRs per day
        created_at = now - timedelta(days=random.randint(1, days), hours=random.randint(0, 23))
        
        # Author distribution (somewhat even)
        author = random.choice(TEAM_MEMBERS)
        
        # Reviewer distribution - INTENTIONALLY SKEWED to Sarah (bottleneck!)
        reviewer_roll = random.random()
        if reviewer_roll < 0.78:  # 78% go to Sarah
            reviewer = next(m for m in TEAM_MEMBERS if m["id"] == "sarah")
        elif reviewer_roll < 0.93:  # 15% go to Mike
            reviewer = next(m for m in TEAM_MEMBERS if m["id"] == "mike")
        else:  # 7% distributed to others
            reviewer = random.choice([m for m in TEAM_MEMBERS if m["id"] not in ["sarah", "mike", author["id"]]])
        
        # Review time - INTENTIONALLY LONG (hidden delay bottleneck!)
        if random.random() < 0.3:  # 30% take extra long
            review_hours = random.randint(24, 72)
        else:
            review_hours = random.randint(4, 24)
        
        reviewed_at = created_at + timedelta(hours=review_hours)
        
        # Time from reviewed to merged (deploy delay bottleneck!)
        if random.random() < 0.6:  # 60% wait overnight
            merge_delay = random.randint(8, 20)
        else:
            merge_delay = random.randint(1, 4)
        
        merged_at = reviewed_at + timedelta(hours=merge_delay) if reviewed_at < now else None
        
        # Code areas touched
        area = random.choice(CODE_AREAS)
        
        # Knowledge silo: auth and payments only touched by Sarah and Mike
        if area in ["auth", "payments"]:
            author = random.choice([m for m in TEAM_MEMBERS if m["id"] in ["sarah", "mike"]])
        
        pr = {
            "id": f"PR-{1000 + i}",
            "title": f"[{area.upper()}] {random.choice(['Fix', 'Add', 'Update', 'Refactor'])} {area} {random.choice(['module', 'service', 'handler', 'component'])}",
            "author": author,
            "reviewer": reviewer,
            "area": area,
            "created_at": created_at.isoformat(),
            "reviewed_at": reviewed_at.isoformat() if reviewed_at < now else None,
            "merged_at": merged_at.isoformat() if merged_at and merged_at < now else None,
            "review_time_hours": review_hours,
            "merge_delay_hours": merge_delay if merged_at else None,
            "files_changed": random.randint(2, 25),
            "lines_added": random.randint(10, 500),
            "lines_deleted": random.randint(5, 200),
            "status": "merged" if merged_at and merged_at < now else ("reviewed" if reviewed_at < now else "pending"),
            "comments": random.randint(0, 15),
        }
        pull_requests.append(pr)
    
    # Sort by created date
    pull_requests.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Calculate reviewer statistics
    reviewer_counts = {}
    for pr in pull_requests:
        reviewer_id = pr["reviewer"]["id"]
        reviewer_counts[reviewer_id] = reviewer_counts.get(reviewer_id, 0) + 1
    
    total_reviews = sum(reviewer_counts.values())
    reviewer_stats = {
        reviewer_id: {
            "reviews": count,
            "percentage": round(count / total_reviews * 100, 1),
            "member": next(m for m in TEAM_MEMBERS if m["id"] == reviewer_id)
        }
        for reviewer_id, count in sorted(reviewer_counts.items(), key=lambda x: -x[1])
    }
    
    # Calculate knowledge silo stats
    area_authors = {}
    for pr in pull_requests:
        area = pr["area"]
        author_id = pr["author"]["id"]
        if area not in area_authors:
            area_authors[area] = set()
        area_authors[area].add(author_id)
    
    knowledge_silos = [
        {
            "area": area,
            "contributors": list(authors),
            "contributor_count": len(authors),
            "is_silo": len(authors) <= 2
        }
        for area, authors in area_authors.items()
    ]
    
    return {
        "pull_requests": pull_requests,
        "reviewer_stats": reviewer_stats,
        "knowledge_silos": knowledge_silos,
        "summary": {
            "total_prs": len(pull_requests),
            "avg_review_time_hours": round(sum(pr["review_time_hours"] for pr in pull_requests) / len(pull_requests), 1),
            "avg_merge_delay_hours": round(sum(pr["merge_delay_hours"] for pr in pull_requests if pr["merge_delay_hours"]) / len([pr for pr in pull_requests if pr["merge_delay_hours"]]), 1),
            "pending_reviews": len([pr for pr in pull_requests if pr["status"] == "pending"]),
        }
    }


def generate_jira_data(days: int = 30) -> Dict[str, Any]:
    """Generate Jira ticket data."""
    statuses = ["To Do", "In Progress", "In Review", "Done"]
    priorities = ["Critical", "High", "Medium", "Low"]
    ticket_types = ["Bug", "Feature", "Task", "Improvement"]
    
    tickets = []
    now = datetime.now()
    
    for i in range(days * 3):
        created_at = now - timedelta(days=random.randint(1, days))
        assignee = random.choice(TEAM_MEMBERS)
        
        if random.random() < 0.25:
            status = "In Review"
            days_in_status = random.randint(3, 10)
        else:
            status = random.choice(statuses)
            days_in_status = random.randint(0, 3)
        
        ticket = {
            "id": f"PROJ-{2000 + i}",
            "title": f"{random.choice(['Implement', 'Fix', 'Update', 'Investigate'])} {random.choice(CODE_AREAS)} {random.choice(['issue', 'feature', 'enhancement'])}",
            "type": random.choice(ticket_types),
            "priority": random.choice(priorities),
            "status": status,
            "assignee": assignee,
            "created_at": created_at.isoformat(),
            "days_in_current_status": days_in_status,
            "story_points": random.choice([1, 2, 3, 5, 8]),
            "labels": random.sample(CODE_AREAS, k=random.randint(1, 2)),
            "blocked": status == "In Review" and days_in_status > 5,
            "blocker_reason": "Waiting for code review" if status == "In Review" and days_in_status > 5 else None,
        }
        tickets.append(ticket)
    
    status_counts = {}
    for ticket in tickets:
        status = ticket["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    blocked_tickets = [t for t in tickets if t["blocked"]]
    
    return {
        "tickets": tickets,
        "status_distribution": status_counts,
        "blocked_tickets": blocked_tickets,
        "summary": {
            "total_tickets": len(tickets),
            "blocked_count": len(blocked_tickets),
            "avg_days_in_review": round(sum(t["days_in_current_status"] for t in tickets if t["status"] == "In Review") / max(len([t for t in tickets if t["status"] == "In Review"]), 1), 1),
            "velocity": sum(t["story_points"] for t in tickets if t["status"] == "Done"),
        }
    }


def generate_slack_data(days: int = 30) -> Dict[str, Any]:
    """Generate Slack activity data with high meeting time."""
    now = datetime.now()
    daily_activity = []
    
    for day_offset in range(days):
        date = now - timedelta(days=day_offset)
        
        for member in TEAM_MEMBERS:
            if random.random() < 0.4:
                meeting_hours = random.uniform(4, 7)
            else:
                meeting_hours = random.uniform(1, 3)
            
            messages_sent = random.randint(10, 80)
            after_hours_messages = random.randint(0, 15) if random.random() < 0.3 else 0
            
            daily_activity.append({
                "date": date.strftime("%Y-%m-%d"),
                "member": member,
                "meeting_hours": round(meeting_hours, 1),
                "messages_sent": messages_sent,
                "after_hours_messages": after_hours_messages,
                "channels_active": random.randint(3, 12),
            })
    
    total_meeting_hours = sum(a["meeting_hours"] for a in daily_activity)
    total_work_hours = days * len(TEAM_MEMBERS) * 8
    meeting_percentage = round(total_meeting_hours / total_work_hours * 100, 1)
    
    member_stats = {}
    for member in TEAM_MEMBERS:
        member_activity = [a for a in daily_activity if a["member"]["id"] == member["id"]]
        member_stats[member["id"]] = {
            "member": member,
            "avg_meeting_hours": round(sum(a["meeting_hours"] for a in member_activity) / len(member_activity), 1),
            "total_messages": sum(a["messages_sent"] for a in member_activity),
            "after_hours_messages": sum(a["after_hours_messages"] for a in member_activity),
        }
    
    # Calculate Sentiment (Burnout detection)
    # Base: 85
    # Penalty: 0.5 per % of meeting time over 20%
    # Penalty: 1.0 per % of after hours activity
    
    base_sentiment = 85.0
    meeting_penalty = max(0, (meeting_percentage - 20) * 0.5)
    after_hours_penalty = round(len([a for a in daily_activity if a["after_hours_messages"] > 0]) / len(daily_activity) * 100, 1) * 0.5
    
    sentiment_score = max(10, round(base_sentiment - meeting_penalty - after_hours_penalty, 1))
    
    return {
        "daily_activity": daily_activity[:30],
        "member_stats": member_stats,
        "summary": {
            "meeting_percentage": meeting_percentage,
            "total_meeting_hours_week": round(total_meeting_hours / (days / 7), 1),
            "avg_messages_per_day": round(sum(a["messages_sent"] for a in daily_activity) / days, 1),
            "after_hours_activity_rate": round(len([a for a in daily_activity if a["after_hours_messages"] > 0]) / len(daily_activity) * 100, 1),
            "sentiment_score": sentiment_score, # New Field
        }
    }


def generate_cicd_data(days: int = 30) -> Dict[str, Any]:
    """Generate CI/CD pipeline data with 40% failure rate."""
    pipelines = []
    now = datetime.now()
    stages = ["checkout", "install", "lint", "unit-test", "integration-test", "build", "deploy"]
    
    for i in range(days * 4):
        started_at = now - timedelta(days=random.randint(0, days), hours=random.randint(0, 23))
        
        failed_stage = None
        if random.random() < 0.4:
            if random.random() < 0.8:
                failed_stage = "integration-test"
            else:
                failed_stage = random.choice(["unit-test", "build", "deploy"])
        
        stage_durations = {}
        for stage in stages:
            if failed_stage and stage == failed_stage:
                duration = random.randint(60, 300)
                stage_durations[stage] = {"duration_seconds": duration, "status": "failed"}
                break
            else:
                duration = random.randint(30, 180)
                stage_durations[stage] = {"duration_seconds": duration, "status": "success"}
        
        total_duration = sum(s["duration_seconds"] for s in stage_durations.values())
        triggered_by = random.choice(TEAM_MEMBERS)
        
        pipeline = {
            "id": f"pipeline-{uuid.uuid4().hex[:8]}",
            "branch": random.choice(["main", "develop", "feature/auth", "feature/payments", "bugfix/login"]),
            "commit": uuid.uuid4().hex[:7],
            "triggered_by": triggered_by,
            "started_at": started_at.isoformat(),
            "finished_at": (started_at + timedelta(seconds=total_duration)).isoformat(),
            "duration_seconds": total_duration,
            "status": "failed" if failed_stage else "success",
            "failed_stage": failed_stage,
            "stages": stage_durations,
        }
        pipelines.append(pipeline)
    
    pipelines.sort(key=lambda x: x["started_at"], reverse=True)
    
    total_runs = len(pipelines)
    failed_runs = len([p for p in pipelines if p["status"] == "failed"])
    
    stage_failures = {}
    for p in pipelines:
        if p["failed_stage"]:
            stage = p["failed_stage"]
            stage_failures[stage] = stage_failures.get(stage, 0) + 1
    
    return {
        "pipelines": pipelines,
        "stage_failures": stage_failures,
        "summary": {
            "total_runs": total_runs,
            "success_rate": round((total_runs - failed_runs) / total_runs * 100, 1),
            "failure_rate": round(failed_runs / total_runs * 100, 1),
            "avg_duration_minutes": round(sum(p["duration_seconds"] for p in pipelines) / total_runs / 60, 1),
            "flaky_stage": max(stage_failures.items(), key=lambda x: x[1])[0] if stage_failures else None,
            "flaky_stage_failures": max(stage_failures.values()) if stage_failures else 0,
        }
    }


def generate_all_mock_data(days: int = 30) -> Dict[str, Any]:
    """Generate all mock data in one call."""
    return {
        "github": generate_github_data(days),
        "jira": generate_jira_data(days),
        "slack": generate_slack_data(days),
        "cicd": generate_cicd_data(days),
        "generated_at": datetime.now().isoformat(),
        "period_days": days,
    }
