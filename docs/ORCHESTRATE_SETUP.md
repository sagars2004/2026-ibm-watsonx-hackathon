# watsonx Orchestrate Setup Guide

This guide walks you through setting up watsonx Orchestrate to automate workflows based on detected bottlenecks.

## Prerequisites

1. ✅ Backend API running (`python app.py` in `/backend`)
2. ✅ OpenAPI spec ready (`backend/openapi.yaml`)
3. 🔲 Access to watsonx Orchestrate workspace
4. 🔲 Backend deployed to a public URL (for production)

---

## Step 1: Access watsonx Orchestrate

### Option A: IBM Cloud Trial (Recommended for Hackathon)

1. Go to [IBM Cloud Catalog](https://cloud.ibm.com/catalog)
2. Search for **"watsonx Orchestrate"**
3. Click **"Create"** (Lite plan is free)
4. Once provisioned, click **"Launch watsonx Orchestrate"**

### Option B: Existing Workspace

If you have access to an existing Orchestrate workspace, go to:
- [watsonx Orchestrate](https://www.ibm.com/products/watsonx-orchestrate)

---

## Step 2: Expose Your API (For Testing)

For Orchestrate to reach your local API during development, you have two options:

### Option A: Use ngrok (Quick for Testing)

```bash
# Install ngrok if you don't have it
brew install ngrok

# Expose your local backend
ngrok http 5001
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`) - you'll need this!

### Option B: Deploy to IBM Code Engine (Production)

```bash
# Login to IBM Cloud
ibmcloud login

# Create Code Engine project
ibmcloud ce project create --name bottleneck-detector

# Deploy (from backend directory)
ibmcloud ce application create \
  --name bottleneck-api \
  --source . \
  --build-source . \
  --port 5001
```

---

## Step 3: Update OpenAPI Spec with Your URL

Before importing, update the server URL in `backend/openapi.yaml`:

```yaml
servers:
  - url: https://YOUR-NGROK-URL.ngrok.io  # or your deployed URL
    description: Production server
```

---

## Step 4: Import Skills into Orchestrate

### In watsonx Orchestrate:

1. Click **"Skill studio"** (left sidebar)
2. Click **"Create"** → **"Import API"**
3. Upload the `openapi.yaml` file from your backend folder
4. Click **"Next"**

### Configure Each Skill:

The import will create these skills from your API:

| Skill Name | API Endpoint | Purpose |
|------------|--------------|---------|
| **Analyze Team Bottlenecks** | POST /api/analyze | Run full AI analysis |
| **Get Team Health Score** | GET /api/metrics/health-score | Quick health check |
| **Get AI Recommendations** | GET /api/recommendations | Fetch action items |
| **Trigger Orchestration** | POST /api/orchestrate/trigger | Execute automated actions |
| **Get GitHub Data** | GET /api/data/github | Fetch PR metrics |
| **Get Jira Data** | GET /api/data/jira | Fetch ticket data |
| **Get Slack Data** | GET /api/data/slack | Fetch communication data |
| **Get CI/CD Data** | GET /api/data/cicd | Fetch pipeline data |

5. For each skill, click **"Enhance"** to:
   - Add a friendly display name
   - Write a natural language description
   - Set input/output labels

6. Click **"Publish"** to make skills available

---

## Step 5: Create Automated Workflows

### Workflow 1: Weekly Bottleneck Report

**Purpose:** Every Monday, analyze bottlenecks and post summary to Slack

1. Go to **"Automations"** → **"Create automation"**
2. Name it: `Weekly Bottleneck Report`
3. Set trigger: **Schedule** → Every Monday at 9:00 AM

4. Add steps:
   ```
   Step 1: Analyze Team Bottlenecks
           └─ days: 7
   
   Step 2: If health_score < 60
           └─ Post to Slack
              Channel: #engineering
              Message: "⚠️ Team Health Alert! Score: {health_score}/100
                       {bottleneck_count} bottlenecks detected.
                       Top issue: {bottlenecks[0].title}"
   
   Step 3: Else
           └─ Post to Slack
              Channel: #engineering  
              Message: "✅ Weekly Health Check: {health_score}/100 - Looking good!"
   ```

5. Click **"Save and Enable"**

---

### Workflow 2: Real-time Workload Balancer

**Purpose:** When a bottleneck is detected, automatically take action

1. Create new automation: `Auto-Balance Workload`
2. Set trigger: **Webhook** (copy the webhook URL)

3. Add steps:
   ```
   Step 1: Parse incoming bottleneck data
   
   Step 2: If bottleneck.type == "single_point_of_failure"
           └─ Create Jira Ticket
              Title: "Redistribute code review load"
              Assignee: Engineering Manager
              Priority: High
   
   Step 3: If bottleneck.type == "meeting_overload"
           └─ Send Slack DM
              To: Team Lead
              Message: "Team meeting time at {metric_value}. 
                       Consider implementing 'No Meeting Wednesday'"
   
   Step 4: Trigger Orchestration
           └─ action: "balance_workload"
   ```

4. Save and copy the webhook URL

5. Update your backend to call this webhook when bottlenecks are detected

---

## Step 6: Connect External Apps

### Connect Slack:

1. Go to **"Connections"** (left sidebar)
2. Find **"Slack"** → Click **"Connect"**
3. Authorize with your Slack workspace
4. Select channels the bot can post to

### Connect Jira:

1. Find **"Jira"** → Click **"Connect"**
2. Enter your Jira instance URL
3. Authorize with API token
4. Select projects to integrate

---

## Step 7: Test Your Setup

### Test via Chat Interface:

1. Go to the main Orchestrate chat
2. Try natural language commands:
   - *"Analyze my team's bottlenecks"*
   - *"What's our current health score?"*
   - *"Show me recommendations"*

### Test via API:

```bash
curl -X POST https://YOUR-URL/api/orchestrate/trigger \
  -H "Content-Type: application/json" \
  -d '{"action": "weekly_analysis"}'
```

---

## Step 8: Create the Automation Workflow (The "Wow" Factor)

This is the key demo piece where the system works proactively!

1. **Go to "Automations"** (Icon usually looks like a lightning bolt or flow chart)
2. Click **"Create automation"** (or "New automation")
3. **Choose "Scheduled"** (or "Time-based") trigger
4. **Configure Schedule:**
   - **Frequency:** Weekly
   - **Day:** Monday
   - **Time:** 9:00 AM

5. **Add Actions (The Flow):**

   **Action 1: Check Team Health**
   - Search for your custom skill: **"Get Health Score"**
   - Add it to the flow.

   **Action 2: Decision Logic (If/Else)**
   - Add a **"Condition"** or **"Decision"** block.
   - **Rule:** `If [Get Health Score.health_score] < 60`

   **Action 3: True Path (Critical Health)**
   - **Action:** Send a notification (e.g., Slack or Email).
   - **Message:** "⚠️ **Critical Alert:** Team Health Score is **[health_score]**. Immediate attention required."
   - **Action:** Create Ticket (Jira).
   - **Summary:** "Investigate Critical Team Health (Score: [health_score])"

   **Action 4: False Path (Healthy)**
   - **Action:** Send a notification.
   - **Message:** "✅ **Monday Update:** Team is healthy! Score: **[health_score]**. Keep it up!"

6. **Activate:** Give it a name like "Weekly Health Check" and turn it **ON**.

---

## Demo Flow for Hackathon

1. **Open Dashboard** → Show current health score (31/100 - Critical!)

2. **Click "Run Analysis"** → Watch bottlenecks appear

3. **Show Orchestrate Chat** → Say "Analyze team bottlenecks"

4. **Demo Automation** → Show the Slack message posted automatically

5. **Show Jira** → Point out the auto-created tickets

6. **Explain the Value:**
   > "Instead of a manager manually reviewing metrics every week, 
   > watsonx Orchestrate automatically detects problems and takes action.
   > This saves 5+ hours per week and catches issues before they escalate."

---

## Troubleshooting

### "Cannot reach API"
- Ensure ngrok or deployed URL is accessible
- Check CORS settings in Flask
- Verify the URL in openapi.yaml matches your actual endpoint

### "Skill import failed"
- Validate openapi.yaml at [editor.swagger.io](https://editor.swagger.io)
- Ensure all operationIds are unique
- Check that all $ref schemas are defined

### "Slack/Jira not working"
- Verify OAuth permissions
- Check that the connected account has access to the channels/projects
- Look at Orchestrate logs for detailed errors

---

## Next Steps

After setup:
1. **Deploy to production** for the live demo
2. **Practice the demo flow** multiple times
3. **Prepare backup** (recording/screenshots) in case of network issues
4. **Highlight AI value** - watsonx.ai analyzes patterns, Orchestrate automates responses

---

## Quick Reference

| Component | URL |
|-----------|-----|
| Backend API | http://localhost:5001 |
| Frontend Dashboard | http://localhost:5173 |
| OpenAPI Spec | `backend/openapi.yaml` |
| Orchestrate Console | https://www.ibm.com/products/watsonx-orchestrate |

**Good luck with the hackathon! 🚀**
