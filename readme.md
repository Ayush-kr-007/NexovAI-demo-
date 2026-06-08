# NexovAI Demo Setup

## Prerequisites

* Python 3.13
* MongoDB Atlas connection string
* Groq API Key
* Sarvam API Key

## Clone Repository

```bash
git clone <repo-url>
cd ai-calling-agent
```

## Create Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Create .env

```env
GROQ_API_KEY=YOUR_KEY
SARVAM_API_KEY=YOUR_KEY
MONGO_URI=YOUR_MONGO_URI
```

## Run AI Caller

```bash
python run.py
```

The AI caller will start on:

```text
http://localhost:7860/client/
```

## Run Dashboard

Open a second terminal:

```bash
streamlit run app.py
```

Dashboard:

```text
http://localhost:8501
```
