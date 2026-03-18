# 🎓 Student Skill Gap Analyzer & Upskill Tracker
### Engineering Edition — CSE · ECE · MECH · CIVIL · CHEM

An ML-based web application that analyzes student skill gaps against industry role benchmarks and generates personalized upskilling roadmaps.

---

## Features
- **Topic-wise Skill Assessment** — Tick topics you know, score auto-calculated
- **College Tier Weighting** — Tier 1–5 affects readiness formula
- **Domain-aware Credentials** — Projects, certs, internships scored by domain relevance
- **Gap Analysis** — Radar chart, gauge, skill breakdown table
- **Personalized Roadmap** — Priority-ranked courses with links
- **Upskill Tracker** — Daily task logger with progress tracking
- **Progress Page** — Before vs after skill comparison

---

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend ML | Python, Scikit-learn, NumPy, Pandas |
| Database | Supabase (PostgreSQL) |
| Charts | Plotly |

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-team/student-skill-gap-analyzer.git
cd student-skill-gap-analyzer
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

### 5. Set up database
Run the schema in Supabase SQL Editor:
```bash
# Copy contents of database/schema.sql and run in Supabase dashboard
```



### 6. Generate datasets
```bash
python data/create_datasets.py
```

### 6. Seed the data
```bash
python database/seed_data.py
```

### 7. Train the ML model
```bash
python -m ml.placement_model
```

### 8. Run the app
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

