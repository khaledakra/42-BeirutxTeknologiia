# 🛡️ AI Security Council

**Multi-AI Threat Analysis System with True Positive / False Positive Detection**

Built for 42Beirut x Teknologiia Hackathon

---

## 📋 Overview

The AI Security Council uses **three specialized AI agents** working together to analyze cybersecurity threats, reduce SOC alert fatigue, and provide executive-level strategic recommendations.

### Key Features

- 🤖 **Three-Tier AI Analysis**: DeepSeek, ChatGPT (GPT-4), and Gemini working in consensus
- ✅ **True Positive / False Positive Detection**: Reduces alert fatigue with AI-powered classification
- 🌍 **Real-time Threat Intelligence**: Integration with IPInfo, AlienVault OTX, and IP-API
- 📊 **Executive Dashboard**: Beautiful real-time visualization with auto-refresh
- 🔄 **Fully Automated**: N8N workflow orchestration with Docker deployment
- 🎯 **Geopolitical Analysis**: Strategic context for threat assessment

---

## 🏗️ Architecture

```
┌─────────────────┐
│   CSV Input     │
│ (10 threats)    │
└────────┬────────┘
         │
    ┌────▼────┐
    │ Agent 1 │ ← DeepSeek AI
    │ TRIAGE  │   Risk Scoring & Prioritization
    └────┬────┘
         │
    ┌────▼────┐
    │ Agent 2 │ ← ChatGPT GPT-4
    │ HUNTER  │   Deep Intel + TP/FP Classification
    └────┬────┘   (IPInfo, AlienVault, IP-API)
         │
    ┌────▼────┐
    │ Agent 3 │ ← Gemini 2.5 Flash
    │ ORACLE  │   Strategic Pattern Analysis
    └────┬────┘   Geopolitical Context
         │
    ┌────▼────────────┐
    │  Aggregation    │
    │  Dashboard API  │
    └────┬────────────┘
         │
    ┌────▼────────────┐
    │   Dashboard     │
    │  (Port 8080)    │
    └─────────────────┘
```

### Agent Roles

| Agent | AI Model | Role | Output |
|-------|----------|------|--------|
| **Agent 1: TRIAGE** | DeepSeek | Initial risk scoring based on port analysis, attack types, malware indicators | URGENT / INVESTIGATE / ROUTINE |
| **Agent 2: HUNTER** | ChatGPT GPT-4 | Deep threat intelligence analysis with TP/FP classification | THREAT / SUSPICIOUS / BENIGN |
| **Agent 3: ORACLE** | Gemini 2.5 Flash | Strategic pattern analysis with geopolitical context | ESCALATE_TO_SOC / BLOCK / MONITOR / ALLOW |

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- API Keys (you'll add these directly in N8N workflows):
  - [DeepSeek API Key](https://platform.deepseek.com/)
  - [OpenAI API Key](https://platform.openai.com/)
  - [Google Gemini API Key](https://makersuite.google.com/app/apikey)
  - [IPInfo API Key](https://ipinfo.io/) (free tier)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-security-council.git
cd ai-security-council
```

### 2. Start the System

```bash
docker-compose up -d
```

This starts:
- **N8N**: `http://localhost:5678` (Workflow orchestration)
- **Dashboard**: `http://localhost:8080` (Visualization)
- **Dashboard API**: `http://localhost:3000` (Data endpoint)

### 3. Import Workflows into N8N

1. Open N8N at `http://localhost:5678`
2. Go to **Workflows** → **Import from File**
3. Import these workflows in order:
   - `workflows/Agent-1.json` (TRIAGE - DeepSeek)
   - `workflows/Agent-2.json` (HUNTER - ChatGPT)
   - `workflows/Agent-3.json` (ORACLE - Gemini)
   - `workflows/Main.json` (Orchestrator)

### 4. Configure API Keys in N8N Workflows

**For Agent-1 (DeepSeek):**
1. Open `Agent-1` workflow in N8N
2. Find the **"DeepSeek API"** HTTP Request node
3. Click on the node → Headers section
4. Update `Authorization` header value to: `Bearer YOUR_DEEPSEEK_API_KEY`
5. Save the workflow

**For Agent-2 (ChatGPT):**
1. Open `AAAAAf` workflow in N8N
2. Find the **"OpenAI API"** HTTP Request node
3. Update `Authorization` header to: `Bearer YOUR_OPENAI_API_KEY`
4. Find the **"IPInfo"** HTTP Request node
5. Update URL to include your token: `https://ipinfo.io/{{ $json.ip }}/json?token=YOUR_IPINFO_TOKEN`
6. Save the workflow

**For Agent-3 (Gemini):**
1. Open `Agent0-3` workflow in N8N
2. Find the **"Gemini API"** HTTP Request node
3. Update URL to include your key: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=YOUR_GEMINI_KEY`
4. Save the workflow

### 5. Run the Analysis

1. In N8N, open the **"AI Security Council - Main Workflow"**
2. Click **"Execute Workflow"** button (top right)
3. Watch the agents analyze 10 threats (takes ~30-60 seconds)
4. Open `http://localhost:8080` in your browser to view the dashboard

---

## 📊 Dashboard Features

The dashboard **auto-refreshes every 5 seconds** and displays:

### 📈 Executive Summary
- Overall threat level (CRITICAL / HIGH / MEDIUM / LOW)
- Total threats analyzed
- AI confidence score
- Campaign type assessment

### 🤖 AI Agent Consensus
- **Agent 1 (TRIAGE)**: Urgent/Investigate/Routine verdicts with counts
- **Agent 2 (HUNTER)**: Threat/Suspicious/Benign classification with counts
- **Agent 3 (ORACLE)**: Strategic analysis and executive summary

### 🎯 True Positive / False Positive Analysis
- True Positive count
- False Positive count
- False Positive Rate percentage
- Detection Accuracy percentage
- Analysis summary explaining TP/FP breakdown

### 🌍 Geographic Threat Distribution
- Top 5 countries by threat count
- Visual bar charts showing threat distribution

### 🚨 Top Priority Threats
- Critical threats requiring immediate action
- Full geopolitical context and reasoning
- IP addresses with strategic analysis

### 💡 Strategic Recommendations
- **Immediate Actions**: BLOCK/ESCALATE decisions with counts
- **Short-term Priorities**: 24-48h monitoring recommendations
- **Long-term Strategy**: Overall security posture improvements

### 📋 All Threat Assessments
- Complete threat list with IP, port, attack type
- Location data from threat intelligence APIs
- Oracle strategic verdict and reasoning
- TP/FP badge for each threat (color-coded)

---

## 🗂️ Project Structure

```
ai-security-council/
├── docker-compose.yml          # Docker orchestration
├── README.md                   # This file
├── SETUP.md                    # Detailed setup guide
│
├── workflows/                  # N8N workflow definitions
│   ├── Agent-1.json           # TRIAGE (DeepSeek)
│   ├── Agent-2.json           # HUNTER (ChatGPT + Threat Intel)
│   ├── Agent-3.json           # ORACLE (Gemini)
│   └── Main.json              # Orchestrator workflow
│
├── dashboard/                  # Dashboard web interface
│   ├── index.html             # Main dashboard UI
│   └── api.py                 # Python API server
│
└── data/                       # Shared data directory
    ├── latest_data.json       # Generated threat analysis (auto-created)
    └── latest_data.csv        # CSV input (10 sample threats)
```

---

## 🔧 How It Works

### Workflow Execution Flow

1. **Main Workflow** triggers and reads `data/latest_data.csv` (10 threats)
2. **Agent 1 (TRIAGE)** analyzes each threat with DeepSeek AI
   - Risk scoring (0-100)
   - Priority classification (URGENT/INVESTIGATE/ROUTINE)
   - Initial verdict
3. **Agent 2 (HUNTER)** performs deep analysis with ChatGPT + Threat Intel APIs
   - Queries IPInfo, AlienVault OTX, IP-API
   - TP/FP classification (TRUE_POSITIVE/FALSE_POSITIVE)
   - Threat verdict (THREAT/SUSPICIOUS/BENIGN)
4. **Agent 3 (ORACLE)** provides strategic analysis with Gemini
   - Geopolitical context assessment
   - Attack pattern analysis
   - Final recommendation (BLOCK/ESCALATE_TO_SOC/MONITOR/ALLOW)
5. **Aggregation Node** combines all results
   - Calculates statistics
   - Builds geographic distribution
   - Generates priority threats list
   - Creates strategic recommendations
6. **Dashboard API** serves the data via HTTP
7. **Dashboard** displays results with auto-refresh every 5 seconds

---

## 🔑 API Configuration

### AI Models Used

| Agent | Model | Temperature | Max Tokens | Purpose |
|-------|-------|-------------|------------|---------|
| TRIAGE | deepseek-chat | 0.7 | 2048 | Fast risk assessment |
| HUNTER | gpt-4 | 0.7 | 2048 | Deep analysis with TP/FP |
| ORACLE | gemini-2.5-flash | 0.7 | 4096 | Strategic reasoning |

### Threat Intelligence APIs

- **IPInfo**: IP geolocation and organization data (requires free API token)
- **AlienVault OTX**: Threat intelligence pulse data (no auth required)
- **IP-API**: Additional geolocation data (no auth required)

---

## 📝 Input Data Format

The system reads threat data from `data/latest_data.csv`:

```csv
ip,port,priority,attack_type,risk_score,risk_reasons
103.216.15.12,22,high,brute_force,75,"High-frequency login attempts, Known attack port"
11.48.99.245,80,urgent,intrusion,85,"DoD infrastructure, Unauthorized access"
49.32.208.167,3389,critical,rdp_brute_force,90,"Multiple failed RDP attempts"
```

**CSV Columns:**
- `ip`: IP address to analyze
- `port`: Target port number
- `priority`: Initial priority (urgent/high/medium/low)
- `attack_type`: Type of attack detected
- `risk_score`: Initial risk score (0-100)
- `risk_reasons`: Comma-separated reasons for flagging

---

## 🐛 Troubleshooting

### Dashboard shows "Waiting for data"
1. Check if N8N workflow executed successfully (no red error nodes)
2. Verify `data/latest_data.json` file was created
3. Check browser console (F12) for API errors
4. Ensure Dashboard API is running: `docker ps | grep dashboard_api`

### N8N Workflow Errors
1. **"Unauthorized" errors**: Check API keys in HTTP Request nodes
2. **"Cannot find module"**: Restart N8N container: `docker-compose restart n8n`
3. **Workflow won't execute**: Check N8N logs: `docker-compose logs n8n`

### API Rate Limits
- **DeepSeek**: 10 requests/minute (free tier)
- **OpenAI**: Varies by plan (check your quota)
- **Gemini**: 60 requests/minute (free tier)
- **IPInfo**: 50,000 requests/month (free tier)

### Service Management

**Restart all services:**
```bash
docker-compose restart
```

**View logs:**
```bash
docker-compose logs -f n8n
docker-compose logs -f dashboard_api
```

**Stop services:**
```bash
docker-compose down
```

**Full reset (deletes all N8N data):**
```bash
docker-compose down -v
docker-compose up -d
```

---

## 🎯 Hackathon Features

✅ **Multi-AI Agent Architecture** - 3 specialized AI agents with distinct roles
✅ **Real-time Threat Intelligence** - Integration with IPInfo, AlienVault, IP-API
✅ **Executive Dashboard** - Auto-refreshing visualization with beautiful UI
✅ **TP/FP Classification** - Reduces SOC alert fatigue with AI-powered analysis
✅ **Geopolitical Context** - Strategic assessment of threat origins
✅ **Consensus Analysis** - All 3 agents collaborate for robust decisions

---

## 📜 License

MIT License - Built for educational purposes

---

## 👥 Team

Built at 42Beirut x Teknologiia Hackathon

---

## 🙏 Acknowledgments

- **42Beirut** and **Teknologiia** for organizing the hackathon
- **N8N** for the amazing workflow automation platform
- **DeepSeek**, **OpenAI**, and **Google** for AI API access
- **IPInfo** and **AlienVault** for threat intelligence data
