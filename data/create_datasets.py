import pandas as pd
import os

os.makedirs("data", exist_ok=True)

skills = [
    # CSE
    {"skill_id":"SK001","skill_name":"Data Structures","department":"CSE","category":"Core CS"},
    {"skill_id":"SK002","skill_name":"Algorithms","department":"CSE","category":"Core CS"},
    {"skill_id":"SK003","skill_name":"OOP Concepts","department":"CSE","category":"Core CS"},
    {"skill_id":"SK004","skill_name":"DBMS","department":"CSE","category":"Core CS"},
    {"skill_id":"SK005","skill_name":"OS Concepts","department":"CSE","category":"Core CS"},
    {"skill_id":"SK006","skill_name":"Computer Networks","department":"CSE","category":"Core CS"},
    {"skill_id":"SK007","skill_name":"Python","department":"CSE","category":"Programming"},
    {"skill_id":"SK008","skill_name":"Machine Learning","department":"CSE","category":"AI/ML"},
    {"skill_id":"SK009","skill_name":"Deep Learning","department":"CSE","category":"AI/ML"},
    {"skill_id":"SK010","skill_name":"SQL","department":"CSE","category":"Database"},
    {"skill_id":"SK011","skill_name":"HTML/CSS","department":"CSE","category":"Web"},
    {"skill_id":"SK012","skill_name":"JavaScript","department":"CSE","category":"Web"},
    {"skill_id":"SK013","skill_name":"React/Vue","department":"CSE","category":"Web"},
    {"skill_id":"SK014","skill_name":"Docker","department":"CSE","category":"DevOps"},
    {"skill_id":"SK015","skill_name":"Linux/Unix","department":"CSE","category":"DevOps"},
    {"skill_id":"SK016","skill_name":"System Design","department":"CSE","category":"Architecture"},
    # ECE
    {"skill_id":"SK017","skill_name":"C/C++ Programming","department":"ECE","category":"Programming"},
    {"skill_id":"SK018","skill_name":"Microcontrollers","department":"ECE","category":"Embedded"},
    {"skill_id":"SK019","skill_name":"VLSI Design","department":"ECE","category":"VLSI"},
    {"skill_id":"SK020","skill_name":"Verilog/VHDL","department":"ECE","category":"VLSI"},
    {"skill_id":"SK021","skill_name":"Circuit Design","department":"ECE","category":"Electronics"},
    {"skill_id":"SK022","skill_name":"Signal Processing","department":"ECE","category":"DSP"},
    {"skill_id":"SK023","skill_name":"MATLAB","department":"ECE","category":"Tools"},
    {"skill_id":"SK024","skill_name":"PCB Design","department":"ECE","category":"Hardware"},
    # MECH
    {"skill_id":"SK025","skill_name":"CAD (SolidWorks/AutoCAD)","department":"MECH","category":"Design"},
    {"skill_id":"SK026","skill_name":"FEA (ANSYS)","department":"MECH","category":"Simulation"},
    {"skill_id":"SK027","skill_name":"Thermodynamics","department":"MECH","category":"Core"},
    {"skill_id":"SK028","skill_name":"Fluid Mechanics","department":"MECH","category":"Core"},
    {"skill_id":"SK029","skill_name":"Strength of Materials","department":"MECH","category":"Core"},
    {"skill_id":"SK030","skill_name":"Manufacturing Processes","department":"MECH","category":"Manufacturing"},
    # CIVIL
    {"skill_id":"SK031","skill_name":"Structural Analysis","department":"CIVIL","category":"Core"},
    {"skill_id":"SK032","skill_name":"RCC Design","department":"CIVIL","category":"Design"},
    {"skill_id":"SK033","skill_name":"AutoCAD/STAAD Pro","department":"CIVIL","category":"Tools"},
    {"skill_id":"SK034","skill_name":"Soil Mechanics","department":"CIVIL","category":"Geotechnical"},
    {"skill_id":"SK035","skill_name":"Surveying","department":"CIVIL","category":"Field"},
    # CHEM
    {"skill_id":"SK036","skill_name":"Chemical Process Design","department":"CHEM","category":"Core"},
    {"skill_id":"SK037","skill_name":"Process Simulation (Aspen)","department":"CHEM","category":"Tools"},
    {"skill_id":"SK038","skill_name":"Safety & HAZOP","department":"CHEM","category":"Safety"},
    {"skill_id":"SK039","skill_name":"Organic Chemistry","department":"CHEM","category":"Core"},
    {"skill_id":"SK040","skill_name":"Quality Control","department":"CHEM","category":"QA"},
]
pd.DataFrame(skills).to_csv("data/skills.csv", index=False)

topics = [
    # Data Structures (SK001)
    {"topic_id":"TP001","skill_id":"SK001","topic_name":"Arrays & Strings","difficulty_weight":1},
    {"topic_id":"TP002","skill_id":"SK001","topic_name":"Linked Lists","difficulty_weight":1},
    {"topic_id":"TP003","skill_id":"SK001","topic_name":"Stacks & Queues","difficulty_weight":1},
    {"topic_id":"TP004","skill_id":"SK001","topic_name":"Trees & Graphs","difficulty_weight":2},
    {"topic_id":"TP005","skill_id":"SK001","topic_name":"Dynamic Programming","difficulty_weight":3},
    # Python (SK007)
    {"topic_id":"TP006","skill_id":"SK007","topic_name":"Syntax & Basics","difficulty_weight":1},
    {"topic_id":"TP007","skill_id":"SK007","topic_name":"OOP in Python","difficulty_weight":2},
    {"topic_id":"TP008","skill_id":"SK007","topic_name":"File Handling","difficulty_weight":1},
    {"topic_id":"TP009","skill_id":"SK007","topic_name":"Pandas & NumPy","difficulty_weight":2},
    {"topic_id":"TP010","skill_id":"SK007","topic_name":"Decorators & Generators","difficulty_weight":3},
    # Machine Learning (SK008)
    {"topic_id":"TP011","skill_id":"SK008","topic_name":"Linear Regression","difficulty_weight":1},
    {"topic_id":"TP012","skill_id":"SK008","topic_name":"Classification Algorithms","difficulty_weight":2},
    {"topic_id":"TP013","skill_id":"SK008","topic_name":"Model Evaluation","difficulty_weight":2},
    {"topic_id":"TP014","skill_id":"SK008","topic_name":"Feature Engineering","difficulty_weight":2},
    {"topic_id":"TP015","skill_id":"SK008","topic_name":"Ensemble Methods","difficulty_weight":3},
    # Microcontrollers (SK018)
    {"topic_id":"TP016","skill_id":"SK018","topic_name":"GPIO & Interrupts","difficulty_weight":1},
    {"topic_id":"TP017","skill_id":"SK018","topic_name":"UART/SPI/I2C","difficulty_weight":2},
    {"topic_id":"TP018","skill_id":"SK018","topic_name":"PWM & Timers","difficulty_weight":2},
    {"topic_id":"TP019","skill_id":"SK018","topic_name":"RTOS Basics","difficulty_weight":3},
    # CAD (SK025)
    {"topic_id":"TP020","skill_id":"SK025","topic_name":"2D Drafting","difficulty_weight":1},
    {"topic_id":"TP021","skill_id":"SK025","topic_name":"3D Part Modelling","difficulty_weight":2},
    {"topic_id":"TP022","skill_id":"SK025","topic_name":"Assembly Design","difficulty_weight":2},
    {"topic_id":"TP023","skill_id":"SK025","topic_name":"GD&T","difficulty_weight":3},
    # Structural Analysis (SK031)
    {"topic_id":"TP024","skill_id":"SK031","topic_name":"Truss Analysis","difficulty_weight":1},
    {"topic_id":"TP025","skill_id":"SK031","topic_name":"Beam Design","difficulty_weight":2},
    {"topic_id":"TP026","skill_id":"SK031","topic_name":"Column Design","difficulty_weight":2},
    {"topic_id":"TP027","skill_id":"SK031","topic_name":"Seismic Analysis","difficulty_weight":3},
    # Chemical Process (SK036)
    {"topic_id":"TP028","skill_id":"SK036","topic_name":"Mass & Energy Balance","difficulty_weight":1},
    {"topic_id":"TP029","skill_id":"SK036","topic_name":"Heat Exchangers","difficulty_weight":2},
    {"topic_id":"TP030","skill_id":"SK036","topic_name":"Distillation","difficulty_weight":2},
    {"topic_id":"TP031","skill_id":"SK036","topic_name":"Reactor Design","difficulty_weight":3},
    # Add these to your topics list in create_datasets.py
# Algorithms (SK002)
{"topic_id":"TP032","skill_id":"SK002","topic_name":"Sorting Algorithms","difficulty_weight":1},
{"topic_id":"TP033","skill_id":"SK002","topic_name":"Searching Algorithms","difficulty_weight":1},
{"topic_id":"TP034","skill_id":"SK002","topic_name":"Graph Algorithms","difficulty_weight":2},
{"topic_id":"TP035","skill_id":"SK002","topic_name":"Greedy Algorithms","difficulty_weight":2},
{"topic_id":"TP036","skill_id":"SK002","topic_name":"Divide & Conquer","difficulty_weight":3},
# OOP Concepts (SK003)
{"topic_id":"TP037","skill_id":"SK003","topic_name":"Classes & Objects","difficulty_weight":1},
{"topic_id":"TP038","skill_id":"SK003","topic_name":"Inheritance","difficulty_weight":1},
{"topic_id":"TP039","skill_id":"SK003","topic_name":"Polymorphism","difficulty_weight":2},
{"topic_id":"TP040","skill_id":"SK003","topic_name":"Abstraction","difficulty_weight":2},
{"topic_id":"TP041","skill_id":"SK003","topic_name":"Design Patterns","difficulty_weight":3},
# DBMS (SK004)
{"topic_id":"TP042","skill_id":"SK004","topic_name":"ER Diagrams","difficulty_weight":1},
{"topic_id":"TP043","skill_id":"SK004","topic_name":"Normalization","difficulty_weight":2},
{"topic_id":"TP044","skill_id":"SK004","topic_name":"SQL Queries","difficulty_weight":1},
{"topic_id":"TP045","skill_id":"SK004","topic_name":"Transactions & ACID","difficulty_weight":2},
{"topic_id":"TP046","skill_id":"SK004","topic_name":"Indexing & Query Optimization","difficulty_weight":3},
# Deep Learning (SK009)
{"topic_id":"TP047","skill_id":"SK009","topic_name":"Neural Networks Basics","difficulty_weight":1},
{"topic_id":"TP048","skill_id":"SK009","topic_name":"CNNs","difficulty_weight":2},
{"topic_id":"TP049","skill_id":"SK009","topic_name":"RNNs & LSTMs","difficulty_weight":2},
{"topic_id":"TP050","skill_id":"SK009","topic_name":"Transfer Learning","difficulty_weight":3},
{"topic_id":"TP051","skill_id":"SK009","topic_name":"Transformers","difficulty_weight":3},
]   
pd.DataFrame(topics).to_csv("data/skill_topics.csv", index=False)

roles = [
    {"role_id":"JR001","role_name":"Software Developer","department":"CSE","required_skill_ids":"SK001,SK002,SK003,SK004,SK007","benchmark_scores":"8,7,7,6,7"},
    {"role_id":"JR002","role_name":"Data Scientist","department":"CSE","required_skill_ids":"SK007,SK008,SK009,SK010,SK004","benchmark_scores":"8,8,7,7,6"},
    {"role_id":"JR003","role_name":"Web Developer","department":"CSE","required_skill_ids":"SK011,SK012,SK013,SK007,SK004","benchmark_scores":"8,8,7,6,5"},
    {"role_id":"JR004","role_name":"DevOps Engineer","department":"CSE","required_skill_ids":"SK014,SK015,SK006,SK007,SK016","benchmark_scores":"8,7,7,6,7"},
    {"role_id":"JR005","role_name":"ML Engineer","department":"CSE","required_skill_ids":"SK007,SK008,SK009,SK001,SK002","benchmark_scores":"9,8,7,7,7"},
    {"role_id":"JR006","role_name":"Cybersecurity Analyst","department":"CSE","required_skill_ids":"SK006,SK015,SK005,SK004,SK016","benchmark_scores":"8,7,7,6,6"},
    {"role_id":"JR007","role_name":"Embedded Systems Engineer","department":"ECE","required_skill_ids":"SK017,SK018,SK021,SK022,SK015","benchmark_scores":"8,8,7,6,5"},
    {"role_id":"JR008","role_name":"VLSI Design Engineer","department":"ECE","required_skill_ids":"SK019,SK020,SK021,SK017,SK023","benchmark_scores":"8,8,7,6,6"},
    {"role_id":"JR009","role_name":"IoT Developer","department":"ECE","required_skill_ids":"SK018,SK017,SK021,SK007,SK024","benchmark_scores":"8,7,6,6,5"},
    {"role_id":"JR010","role_name":"Signal Processing Engineer","department":"ECE","required_skill_ids":"SK022,SK023,SK021,SK017,SK020","benchmark_scores":"8,7,6,6,5"},
    {"role_id":"JR011","role_name":"Mechanical Design Engineer","department":"MECH","required_skill_ids":"SK025,SK026,SK029,SK027,SK028","benchmark_scores":"8,7,7,6,6"},
    {"role_id":"JR012","role_name":"Manufacturing Engineer","department":"MECH","required_skill_ids":"SK030,SK025,SK029,SK026,SK027","benchmark_scores":"8,7,6,6,5"},
    {"role_id":"JR013","role_name":"Thermal Engineer","department":"MECH","required_skill_ids":"SK027,SK028,SK026,SK025,SK029","benchmark_scores":"8,7,7,6,6"},
    {"role_id":"JR014","role_name":"Structural Engineer","department":"CIVIL","required_skill_ids":"SK031,SK032,SK033,SK034,SK035","benchmark_scores":"8,8,7,6,5"},
    {"role_id":"JR015","role_name":"Site Engineer","department":"CIVIL","required_skill_ids":"SK033,SK031,SK034,SK035,SK032","benchmark_scores":"8,7,7,6,5"},
    {"role_id":"JR016","role_name":"Process Engineer","department":"CHEM","required_skill_ids":"SK036,SK037,SK038,SK039,SK040","benchmark_scores":"8,7,7,6,6"},
    {"role_id":"JR017","role_name":"Quality Assurance Engineer","department":"CHEM","required_skill_ids":"SK040,SK038,SK036,SK039,SK037","benchmark_scores":"8,7,6,6,5"},
    {"role_id":"JR018","role_name":"R&D Chemist","department":"CHEM","required_skill_ids":"SK039,SK036,SK040,SK037,SK038","benchmark_scores":"8,7,6,5,5"},
]
pd.DataFrame(roles).to_csv("data/job_roles.csv", index=False)

import random
random.seed(42)

depts      = ["CSE","CSE","CSE","ECE","ECE","MECH","MECH","CIVIL","CIVIL","CHEM"]
role_map   = {"CSE":["JR001","JR002","JR003"],"ECE":["JR007","JR008"],"MECH":["JR011","JR012"],"CIVIL":["JR014","JR015"],"CHEM":["JR016","JR017"]}
tier_map   = {"CSE":[2,3,3,4,4],"ECE":[3,3,4,4,5],"MECH":[3,4,4,5,5],"CIVIL":[3,4,4,5,5],"CHEM":[3,4,4,5,5]}
colleges   = {"CSE":["NIT Trichy","Osmania University","JNTU Hyderabad","VIT Vellore","SRM Chennai"],
              "ECE":["NIT Warangal","Osmania University","JNTU Kakinada","Amrita Coimbatore","KL University"],
              "MECH":["NIT Surathkal","JNTU Anantapur","Andhra University","GRIET Hyderabad","Vignan University"],
              "CIVIL":["NIT Calicut","Osmania University","JNTU Hyderabad","Vasavi College","MVSR College"],
              "CHEM":["NIT Trichy","Andhra University","JNTU Hyderabad","BITS Pilani","Osmania University"]}

students = []
for i in range(50):
    dept  = depts[i % 10]
    tier  = tier_map[dept][i % 5]
    cgpa  = round(random.uniform(5.5, 9.8), 2)
    sid   = f"STU{i+1:03d}"
    students.append({
        "student_id":         sid,
        "name":               f"Student {i+1}",
        "roll_no":            f"{dept[:2]}{21+i%4}{i+1:03d}",
        "department":         dept,
        "year":               random.choice(["3rd Year","4th Year"]),
        "college":            colleges[dept][i % 5],
        "college_tier":       tier,
        "cgpa":               cgpa,
        "target_role_id":     random.choice(role_map[dept]),
        "num_projects":       random.randint(0, 4),
        "num_certifications": random.randint(0, 3),
        "num_internships":    random.randint(0, 2),
        "num_backlogs":       random.randint(0, 3),
    })
pd.DataFrame(students).to_csv("data/students.csv", index=False)

score_rows = []
skill_dept = {"CSE":["SK001","SK002","SK007","SK008","SK010"],
              "ECE":["SK017","SK018","SK019","SK021","SK022"],
              "MECH":["SK025","SK026","SK027","SK028","SK029"],
              "CIVIL":["SK031","SK032","SK033","SK034","SK035"],
              "CHEM":["SK036","SK037","SK038","SK039","SK040"]}
for stu in students:
    for sk in skill_dept[stu["department"]]:
        score_rows.append({
            "student_id":         stu["student_id"],
            "skill_id":           sk,
            "skill_score":        round(random.uniform(2.0, 9.5), 1),
            "topics_known_count": random.randint(1, 4),
        })
pd.DataFrame(score_rows).to_csv("data/student_skill_scores.csv", index=False)

apps = []
for stu in students:
    cgpa      = stu["cgpa"]
    tier      = stu["college_tier"]
    tier_w    = {1:1.0,2:0.85,3:0.70,4:0.60,5:0.45}[tier]
    skills    = skill_dept[stu["department"]]
    scores    = {sk: round(random.uniform(2.0,9.5),1) for sk in skills}
    bench     = 7
    sm        = round(sum(min(1.0,s/bench) for s in scores.values())/len(scores), 3)
    cos       = round(sm * random.uniform(0.85,1.0), 3)
    proj_rel  = round(random.uniform(0.2, 0.9), 2)
    cert_rel  = round(random.uniform(0.1, 0.8), 2)
    int_rel   = round(random.uniform(0.0, 0.9), 2)
    back_pen  = round(random.uniform(0.0, 0.5) if stu["num_backlogs"]>0 else 0.0, 2)
    num_gaps  = sum(1 for s in scores.values() if s < bench)
    readiness = round(
        sm*0.45*100 + (cgpa/10)*0.12*100 + tier_w*0.10*100 +
        cert_rel*0.08*100 + proj_rel*0.10*100 + int_rel*0.10*100 - back_pen*0.05*100, 2)
    placed = 1 if (readiness >= 55 and cgpa >= 6.5 and random.random() > 0.25) else 0
    apps.append({
        "student_id":                  stu["student_id"],
        "role_id":                     stu["target_role_id"],
        "department":                  stu["department"],
        "college_tier":                tier,
        "cgpa":                        cgpa,
        "cosine_similarity":           cos,
        "skill_match_score":           sm,
        "readiness_score":             readiness,
        "num_projects":                stu["num_projects"],
        "num_certifications":          stu["num_certifications"],
        "num_internships":             stu["num_internships"],
        "num_backlogs":                stu["num_backlogs"],
        "project_relevance_score":     proj_rel,
        "cert_relevance_score":        cert_rel,
        "internship_relevance_score":  int_rel,
        "backlog_penalty_score":       back_pen,
        "num_skill_gaps":              num_gaps,
        "placed":                      placed,
    })
pd.DataFrame(apps).to_csv("data/student_applications.csv", index=False)

import os
for f in os.listdir("data"):
    size = os.path.getsize(f"data/{f}")
