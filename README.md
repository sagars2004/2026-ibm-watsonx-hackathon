# Silent Bottleneck Detector 
### *IBM watsonx Hackathon 2026 Submission*

> **"We don't just find bottlenecks. We fix them."**

The **Silent Bottleneck Detector** is an AI-powered system that autonomously identifies, analyzes, and resolves hidden inefficiencies in engineering teams. Unlike traditional dashboards that simply display metrics, our solution uses **IBM Granite 4.0** to reason about data and **Langflow Agents** to take corrective action in real-time.

---

## Key Features

*   **Cognitive Analysis:** Powered by **IBM watsonx.ai (Granite 4.0)** to detect subtle patterns like "Knowledge Silos" or "Meeting Overload" that regular metrics miss.
*   **Autonomous Agent:** A custom **Langflow** agent that can rebalance workloads and unblock tickets via chat command.
*   **Real-Timestamp Self-Healing:** Actions taken by the agent (e.g., "Resolve Blockers") are reflected on the dashboard in < 2 seconds.
*   **Enterprise Orchestration:** Integrated with **IBM watsonx Orchestrate** to enforce company policies and automate recurring health checks.
*   **Premium Operations Center:** A modern UI design that brings a futuristic feel to engineering management.

---

## Architecture

Our "Dual-Brain" architecture combines local responsiveness with cloud power:

1.  **Frontend:** React + Vite (Frosted Glass UI) with an embedded **Langflow Widget**.
2.  **Backend:** Python Flask API acting as the central nervous system.
3.  **AI Layer:** 
    *   **IBM watsonx.ai:** Generates insights and health scores.
    *   **Langflow:** Manages agent reasoning and tool execution.
4.  **Data Layer:** IBM Cloudant (with robust mock data generation for demo stability).

---

## Quick Start

### Prerequisites
*   Node.js v16+
*   Python 3.10+
*   (Optional) Docker

### 1. Backend Setup
The backend serves the API and manages the "Data Story" (Mock Data).
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start the API (Runs on port 5001)
python app.py
```

### 2. Frontend Setup
The dashboard allows you to visualize the health score and interact with the Agent.
```bash
cd frontend
npm install
npm run dev
```
Access the dashboard at `http://localhost:5173`.

### 3. Agent Setup (Langflow)
Our agent logic is defined in `docs/advanced_langflow_tools.py`.
1.  Run Langflow (locally or via Docker).
2.  Import the custom tools provided in the `docs/` folder.
3.  Connect the Agent to the Backend API (`http://host.docker.internal:5001`).

---

## Project Structure

*   `/backend` - Flask API, Watsonx Client, and Self-Healing Logic.
*   `/frontend` - React App with Frosted UI and Langflow Widget integration.
*   `/docs` - Architecture diagrams, Agent Tool code, and "Engineering Handbook" RAG source.

---

## Technologies Used

*   **IBM watsonx Orchestrate agent**
*   **IBM watsonx.ai**
*   **Langflow**
*   **IBM Cloudant database**
*   **React / Vite**
*   **Python / Flask**
*   **ngrok**

---

*Built with ❤️ (and a lot of caffeine) by Sagar Sahu for the IBM 2026 AI Demystified Hackathon.*
