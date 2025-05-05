import spacy 
import re 

nlp = spacy.load("en_core_web_sm") #load nlp english model


def extract_keywords(text):
    text = re.sub(r'[^\w\s]', '', text)
    doc = nlp(text.lower())
    keywords = set()

    temp_tokens = [token.lemma_ for token in doc if token.pos_ in {"NOUN", "PROPN"} and not token.is_stop] #lemma gives u base form of the word (non plural)


    combos = [
    ("power", "bi", "power bi"),
    ("data", "governance", "data governance"),
    ("machine", "learning", "machine learning"),
    ]   

    for w1, w2, phrase in combos: 
        if w1 in temp_tokens and w2 in temp_tokens:
            keywords.add(phrase)
            temp_tokens = [t for t in temp_tokens if t not in {w1,w2}]

    synonym_map = {
    "creation": "development",
    "visualization": "dashboard",
    "intern": "student",
    "excel": "spreadsheets",
    "experience": "background",
    }

    temp_tokens = [synonym_map.get(t, t) for t in temp_tokens]
        

    keywords.update(temp_tokens) #bulk version of add
    return keywords


print("Paste the job posting text (press Enter twice when done):")
job_lines = []
while True:
    line = input()
    if line.strip() == "": #is line empty 
        break
    job_lines.append(line)
job_text = "\n".join(job_lines)

print("✅ Job post loaded!\n")

education_keywords = {
    "bachelor", "master", "phd", "degree", "engineering", "science", 
    "university", "college", "major", "field of study"
}

education_lines = []
skill_lines = []

for line in job_lines:
    lower_line = line.lower()
    if any(word in lower_line for word in education_keywords):
        education_lines.append(line)
    else:
        skill_lines.append(line)


job_education = extract_keywords("\n".join(education_lines))
job_skills = extract_keywords("\n".join(skill_lines))

  

with open('resume.txt', 'r') as f:
    resume_text = f.read()
    resume_phrases = extract_keywords(resume_text)  

matched_edu = job_education & resume_phrases
missing_edu = job_education - resume_phrases

matched_skills = job_skills & resume_phrases
missing_skills = job_skills - resume_phrases



with open("match_report.txt", "w") as f:
    f.write("📚 Education Match:\n")
    for word in sorted(matched_edu):
        print(f"✔ {word}\n")
    for word in sorted(missing_edu):
        f.write(f"✘ {word}\n")

    f.write("\n🛠️ Skills Match:\n")
    for word in sorted(matched_skills):
        f.write(f"✔ {word}\n")
    for word in sorted(missing_skills):
        f.write(f"✘ {word}\n")

    total = len(job_education | job_skills ) #union
    match_total = len(matched_edu) + len(matched_skills)
    match_percent = round((match_total / total) * 100) if total else 0 

    f.write(f"\n💯 Total Match Score: {match_percent}%\n")

