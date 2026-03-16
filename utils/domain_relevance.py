DOMAIN_RELEVANCE = {
    "Python":                {"Data Scientist":1.0,"ML Engineer":1.0,"Software Developer":0.7,"Web Developer":0.5,"DevOps Engineer":0.6,"default":0.3},
    "Machine Learning":      {"Data Scientist":1.0,"ML Engineer":1.0,"Software Developer":0.4,"default":0.2},
    "Web Development":       {"Web Developer":1.0,"Software Developer":0.6,"Product Manager":0.4,"default":0.2},
    "Data Analysis":         {"Data Scientist":0.9,"ML Engineer":0.7,"Product Manager":0.5,"default":0.3},
    "Embedded Systems":      {"Embedded Systems Engineer":1.0,"IoT Developer":0.9,"Hardware Design Engineer":0.7,"VLSI Design Engineer":0.5,"default":0.2},
    "VLSI / Chip Design":    {"VLSI Design Engineer":1.0,"Hardware Design Engineer":0.7,"Embedded Systems Engineer":0.4,"default":0.1},
    "IoT / Wireless":        {"IoT Developer":1.0,"Embedded Systems Engineer":0.7,"Telecom Engineer":0.6,"default":0.2},
    "Structural / Civil":    {"Structural Engineer":1.0,"Site Engineer":0.8,"Construction Manager":0.7,"default":0.2},
    "AutoCAD / CAD":         {"Structural Engineer":0.8,"Site Engineer":0.9,"Mechanical Design Engineer":0.9,"Automobile Engineer":0.7,"default":0.3},
    "Mechanical Design":     {"Mechanical Design Engineer":1.0,"Automobile Engineer":0.8,"Manufacturing Engineer":0.6,"Robotics Engineer":0.5,"default":0.2},
    "Chemical Process":      {"Process Engineer":1.0,"Petrochemical Engineer":0.9,"R&D Chemist":0.5,"default":0.2},
    "Pharma / Bio":          {"Pharmaceutical Engineer":1.0,"Quality Assurance Engineer":0.7,"R&D Chemist":0.6,"default":0.2},
    "DevOps / Cloud":        {"DevOps Engineer":1.0,"ML Engineer":0.6,"Software Developer":0.5,"default":0.2},
    "Networking / Security": {"Cybersecurity Analyst":1.0,"DevOps Engineer":0.6,"Telecom Engineer":0.5,"default":0.2},
    "Research & Development":{"R&D Chemist":1.0,"Data Scientist":0.6,"ML Engineer":0.5,"default":0.3},
    "General / Other":       {"default":0.3},
}

ALL_DOMAINS = list(DOMAIN_RELEVANCE.keys())

def get_relevance(domain: str, role_name: str) -> float:
    dr = DOMAIN_RELEVANCE.get(domain, {"default": 0.3})
    return dr.get(role_name, dr.get("default", 0.3))
