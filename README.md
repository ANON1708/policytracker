# PolicyTracker

**Agentic Monitoring System for AI Regulation**

PolicyTracker is a lightweight system for **monitoring, summarising, and tracking changes in AI policy and regulation sources**.

The system ingests regulatory documents, generates structured summaries using a local language model, and detects changes in the underlying source over time.

Designed as a **research and policy analysis tool**, PolicyTracker demonstrates how agent-like systems can support monitoring of rapidly evolving governance frameworks.

---

# Core Functions

### Source Monitoring

* Track regulatory webpages and policy PDFs
* Maintain a persistent **watchlist of policy sources**
* Store extracted document text and metadata

### Automated Policy Summaries

For each source the system generates:

* **Research Summary**

  * Five concise analytical bullet points

* **Medium-style Draft**

  * ~400–500 word readable explanation

* **Relevant Excerpts**

  * Key sentences extracted from the source

### Update Detection

* Re-fetch source content
* Compare against stored text
* Identify document changes
* Generate updated summaries
* Present **old vs new summary comparison**

### Source History

Each source maintains a structured event log:

* Source added
* Summary generated
* Summary regenerated
* Update detected
* Update accepted

This enables **basic temporal tracking of policy changes.**

---

# System Architecture

```text
User
  ↓
Flask Web Interface
  ↓
Source Extraction Layer
  • Webpage Extractor
  • PDF Extractor
  ↓
Text Processing
  • Cleaning
  • Chunking
  ↓
Local LLM Inference
  • Ollama
  • llama3.2:3b
  ↓
AI Output Generation
  • Research Summary
  • Medium Draft
  • Relevant Excerpts
  ↓
Persistence Layer
  • JSON storage
  • Source history
  ↓
Update Monitoring
  • Text comparison
  • Change detection
```

---

# Technology Stack

| Layer         | Technology            |
| ------------- | --------------------- |
| Backend       | Python, Flask         |
| Extraction    | Requests, Trafilatura |
| Summarisation | Ollama (local LLM)    |
| Model         | `llama3.2:3b`         |
| Storage       | JSON files            |
| Frontend      | HTML + Tailwind CSS   |

---

# Agentic Behaviour

PolicyTracker implements a simple **observe → analyse → update** cycle.

1. Observe

   * ingest policy source

2. Analyse

   * generate structured summary via LLM

3. Monitor

   * periodically re-check source

4. Update

   * detect changes and generate updated analysis

This creates a **lightweight monitoring agent for policy documents**.

---

# Repository Structure

```
policytracker/
│
app.py
requirements.txt
.env.example
README.md
│
services/
  extractor.py
  extractor_web.py
  extractor_pdf.py
  summarizer.py
  storage.py
  update_checker.py
  chunker.py
│
templates/
  dashboard.html
  source.html
  history.html
│
data/
  sources/
```

---

# Running Locally

Install dependencies

```
pip install -r requirements.txt
```

Install and run Ollama

```
ollama pull llama3.2:3b
ollama serve
```

Start the application

```
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

# Next Development Steps

PolicyTracker currently tracks **single-document changes**.
Future improvements aim to transform it into a **true regulatory intelligence tracker.**

### 1. Temporal Policy Tracking

Store **versioned summaries over time**

```
policy source
  ↓
summary v1
summary v2
summary v3
```

This enables:

* policy evolution tracking
* change timelines

---

### 2. Historical Change Reports

Automatically generate reports such as:

```
"How the EU AI Act guidance evolved over 6 months"
```

This would require:

* summary version storage
* semantic diff between summaries
* timeline generation

---

### 3. Semantic Change Detection

Move from raw text comparison to:

* embedding similarity
* policy concept detection
* structural change detection

---

### 4. Multi-Source Regulatory Analysis

Track multiple sources simultaneously:

```
EU AI Act
US Executive Orders
UK AI Regulation
OECD Framework
```

Then generate:

* cross-jurisdiction summaries
* comparative policy analysis

---

### 5. Autonomous Monitoring Agent

Introduce scheduled monitoring:

```
daily source checks
automatic update alerts
policy change notifications
```

---

# Research Applications

PolicyTracker can support research in:

* AI governance
* regulatory technology (RegTech)
* policy monitoring systems
* AI-assisted policy analysis
* document change detection

---

