# Langflow Demo Setup Guide

## 1. Start Langflow
Open a new terminal window/tab:

```bash
cd backend
source venv/bin/activate  # Activate your python virtual environment
pip install langflow      # Ensure it's installed in this venv
python -m langflow run    # Start the server
```

Access the UI at: **http://127.0.0.1:7860**

## 2. Create the "Silent Detector" Flow
1. Click **"New Flow"**.
2. From the sidebar, drag a **Custom Component** node onto the canvas.
3. **Double-click** the code area in the node (or click the "Edit" icon).
4. **Copy & Paste** the content of `docs/langflow_tool_script.py` into it.
5. Click **"Check & Save"** (or Build).
6. Set the **API URL** input to: `http://localhost:5001/api/analyze/quick`

## 3. Connect the Brain
To simulate the "Agent" reasoning:
1. Add a **Chat Input** node.
2. Add a **Prompt** node. 
   - Template: "Analyze the following engineering data and identify the top bottleneck: {data}"
   - Connect **Chat Input** -> **Prompt**.
   - Connect **Custom Tool (Output)** -> **Prompt (data)**.
3. Add a **LiteLLM Model** (or Watsonx) node.
   - Connect **Prompt** -> **Model**.
4. Add a **Chat Output** node.
   - Connect **Model** -> **Chat Output**.

## 4. Run It
- Click the **Lightning Bolt** (Play) icon on the Chat Output.
- Type: "What is the team status?"
- Watch it fetch data from your running backend and summarize it!
