import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def seed(table, filepath):
    df = pd.read_csv(filepath)

    # Replace NaN values
    df = df.fillna("")

    records = df.to_dict(orient="records")

    # Insert records in batches
    for i in range(0, len(records), 50):
        batch = records[i:i+50]
        supabase.table(table).upsert(batch).execute()

    print(f"✅ Seeded {table} with {len(records)} rows")


if __name__ == "__main__":

    seed("skills", "data/skills.csv")
    seed("skill_topics", "data/skill_topics.csv")
    seed("job_roles", "data/job_roles.csv")
    seed("students", "data/students.csv")

    print("\n🎉 All data uploaded successfully!")