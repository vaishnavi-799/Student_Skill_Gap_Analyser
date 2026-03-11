-- Students table
CREATE TABLE students (
    student_id TEXT PRIMARY KEY,
    name TEXT,
    roll_no TEXT,
    department TEXT,
    year TEXT,
    college TEXT,
    college_tier INT,
    cgpa FLOAT,
    target_role_id TEXT,
    num_projects INT DEFAULT 0,
    project_domains TEXT,
    num_certifications INT DEFAULT 0,
    cert_domains TEXT,
    num_internships INT DEFAULT 0,
    internship_domains TEXT,
    internship_months TEXT,
    num_backlogs INT DEFAULT 0,
    backlog_domains TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Skills master table
CREATE TABLE skills (
    skill_id TEXT PRIMARY KEY,
    skill_name TEXT,
    department TEXT,
    category TEXT
);

-- Skill topics table
CREATE TABLE skill_topics (
    topic_id TEXT PRIMARY KEY,
    skill_id TEXT REFERENCES skills(skill_id),
    topic_name TEXT,
    difficulty_weight INT
);

-- Job roles table
CREATE TABLE job_roles (
    role_id TEXT PRIMARY KEY,
    role_name TEXT,
    department TEXT,
    required_skill_ids TEXT,
    benchmark_scores TEXT
);

-- Student skill scores table
CREATE TABLE student_skill_scores (
    id SERIAL PRIMARY KEY,
    student_id TEXT REFERENCES students(student_id),
    skill_id TEXT REFERENCES skills(skill_id),
    skill_score FLOAT,
    topics_known_count INT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Analysis results table
CREATE TABLE student_analysis (
    id SERIAL PRIMARY KEY,
    student_id TEXT REFERENCES students(student_id),
    role_id TEXT,
    readiness_score FLOAT,
    cosine_similarity FLOAT,
    placement_probability FLOAT,
    num_skill_gaps INT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Upskill tasks table
CREATE TABLE student_tasks (
    id SERIAL PRIMARY KEY,
    student_id TEXT REFERENCES students(student_id),
    title TEXT,
    skill_tag TEXT,
    priority TEXT,
    is_done BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);