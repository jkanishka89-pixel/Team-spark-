import streamlit as st
import pandas as pd
from datetime import datetime

# ------------------------------------------------------------
# TeamSpark | Hackathon 5.0 Round 2 prototype
# Demo-only app: all student/event records are illustrative.
# No API key or external AI service is required.
# ------------------------------------------------------------

st.set_page_config(
    page_title="TeamSpark | Find your people",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --ink:#17233f; --muted:#68758e; --violet:#7657f6; --cyan:#25c6d9; --pink:#ff6da8; --paper:#f6f7fc; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background: radial-gradient(circle at 90% 0%, #e9e6ff 0, transparent 28%), linear-gradient(180deg,#f8f9ff 0%,#f5f7fc 100%); color:var(--ink); }
h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; color:var(--ink); }
.block-container { padding-top:1.6rem; padding-bottom:3rem; max-width:1450px; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#171d3b 0%,#242653 100%); }
[data-testid="stSidebar"] * { color:#f6f7ff !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { padding:8px 10px; border-radius:10px; }
.hero { padding:28px 30px; border-radius:24px; color:white; background:linear-gradient(115deg,#27245d 0%,#654de0 54%,#24b9d0 100%); box-shadow:0 16px 38px rgba(65,67,150,.18); margin-bottom:22px; }
.hero h1 { color:white !important; font-size:2.5rem; margin:0 0 8px 0; }
.hero p { color:#edf1ff; margin:0; font-size:1.05rem; }
.eyebrow { text-transform:uppercase; letter-spacing:2px; font-size:.72rem; font-weight:700; color:#c9d5ff; margin-bottom:8px; }
.metric-card { background:white; border:1px solid #e8eaf4; border-radius:18px; padding:18px 20px; box-shadow:0 8px 24px rgba(35,45,90,.05); min-height:112px; }
.metric-label { color:#77819a; font-size:.82rem; font-weight:600; }
.metric-value { color:#20294a; font-family:'Space Grotesk'; font-size:1.8rem; font-weight:700; margin-top:4px; }
.metric-note { color:#8b94a8; font-size:.75rem; margin-top:2px; }
.panel { background:white; border:1px solid #e8eaf4; border-radius:18px; padding:20px; box-shadow:0 8px 24px rgba(35,45,90,.045); }
.profile-card { background:white; border:1px solid #e8eaf4; border-radius:18px; padding:18px; height:100%; box-shadow:0 8px 22px rgba(35,45,90,.04); }
.tag { display:inline-block; padding:5px 9px; margin:3px 4px 3px 0; border-radius:999px; background:#f0edff; color:#5d49c8; font-size:.74rem; font-weight:700; }
.tag-cyan { background:#e5fbfd; color:#12899a; }
.small-muted { color:#7d879e; font-size:.83rem; }
.score { font-family:'Space Grotesk'; font-size:1.7rem; font-weight:700; color:#624ce0; }
.step { border-left:3px solid #8b79ff; padding:4px 0 10px 14px; margin:4px 0; }
div.stButton > button { border:0; border-radius:12px; background:linear-gradient(100deg,#7057ed,#25b9cf); color:white; font-weight:700; padding:.62rem 1rem; }
div.stButton > button:hover { color:white; border:0; filter:brightness(1.06); }
.stTabs [data-baseweb="tab"] { font-weight:700; }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- Illustrative demo data ----------
STUDENTS = [
    {"name":"Aarav Menon","branch":"CSE","year":"2nd year","skills":["Python","Machine Learning","Data Analysis"],"interests":["AI","Healthcare","Social Impact"],"level":"Intermediate","availability":"Weekends","beginner":False,"reliability":4.8,"bio":"Enjoys turning datasets into useful ideas.","avatar":"🧠"},
    {"name":"Meera Krishnan","branch":"ECE","year":"1st year","skills":["IoT","Arduino","Embedded C"],"interests":["Smart Cities","Agriculture","Hardware"],"level":"Beginner","availability":"Evenings","beginner":True,"reliability":4.7,"bio":"Curious about sensors and real-world prototypes.","avatar":"🔌"},
    {"name":"Ishaan Rao","branch":"IT","year":"3rd year","skills":["React","UI/UX","Figma"],"interests":["EdTech","Accessibility","Design"],"level":"Advanced","availability":"Weekends","beginner":False,"reliability":4.6,"bio":"Builds friendly interfaces and clear user journeys.","avatar":"🎨"},
    {"name":"Nila Suresh","branch":"EEE","year":"2nd year","skills":["Python","IoT","Circuit Design"],"interests":["Agriculture","Clean Energy","Hardware"],"level":"Intermediate","availability":"Evenings","beginner":False,"reliability":4.9,"bio":"Interested in practical electronics and sustainability.","avatar":"⚡"},
    {"name":"Kabir Shah","branch":"CSE","year":"1st year","skills":["HTML","CSS","JavaScript"],"interests":["Web","EdTech","Accessibility"],"level":"Beginner","availability":"Flexible","beginner":True,"reliability":4.5,"bio":"Learning full-stack development through projects.","avatar":"💻"},
    {"name":"Diya Thomas","branch":"Biotech","year":"3rd year","skills":["Research","Data Analysis","Biology"],"interests":["Healthcare","AI","Social Impact"],"level":"Intermediate","availability":"Weekends","beginner":False,"reliability":4.8,"bio":"Brings a domain-research perspective to teams.","avatar":"🧬"},
    {"name":"Rohan Das","branch":"CSE","year":"2nd year","skills":["Python","Backend","SQL"],"interests":["FinTech","AI","Web"],"level":"Intermediate","availability":"Evenings","beginner":False,"reliability":4.4,"bio":"Likes APIs, databases and building reliable systems.","avatar":"🛠️"},
    {"name":"Ananya Iyer","branch":"Design","year":"2nd year","skills":["UI/UX","Figma","Presentation"],"interests":["Smart Cities","EdTech","Design"],"level":"Intermediate","availability":"Flexible","beginner":False,"reliability":4.9,"bio":"Focuses on user research, storytelling and visual design.","avatar":"🌈"},
]

EVENTS = {
    "HackFest 2026": {
        "theme":"Build inclusive, useful technology for everyday challenges.",
        "roles":["AI / ML","Frontend","Backend","Hardware / IoT","UI / UX","Domain Research"],
        "skills":["Python","Machine Learning","React","Backend","IoT","UI/UX","Research"],
        "team_size":4, "deadline":"In 2 days", "icon":"🚀"
    },
    "GreenTech Challenge": {
        "theme":"Create practical solutions for sustainability and agriculture.",
        "roles":["Hardware / IoT","Data / AI","Frontend","Domain Research"],
        "skills":["IoT","Arduino","Python","Data Analysis","Circuit Design","Research"],
        "team_size":4, "deadline":"In 5 days", "icon":"🌱"
    },
    "Campus EdTech Sprint": {
        "theme":"Make learning more accessible, engaging and inclusive.",
        "roles":["UI / UX","Frontend","Backend","Learning Research"],
        "skills":["UI/UX","Figma","React","HTML","Backend","Research"],
        "team_size":4, "deadline":"In 1 week", "icon":"📚"
    },
}

SKILL_OPTIONS = sorted({s for person in STUDENTS for s in person["skills"]} | {
    "Machine Learning","Python","React","UI/UX","IoT","Arduino","Embedded C",
    "Backend","SQL","Figma","Data Analysis","Research","Presentation","HTML","CSS"
})
INTEREST_OPTIONS = ["AI","Healthcare","Social Impact","Smart Cities","Agriculture","Hardware","EdTech","Accessibility","Design","Clean Energy","Web","FinTech"]

# ---------- Helpers ----------
def metric(label, value, note):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)

def score_candidate(person, event, user_skills, user_interests, availability):
    required = set(event["skills"])
    candidate_skills = set(person["skills"])
    user_skills = set(user_skills)
    # Candidate relevance to event and complementary skills to the current profile.
    event_fit = len(candidate_skills & required) / max(1, len(required))
    complement_pool = required - user_skills
    complement = len(candidate_skills & complement_pool) / max(1, len(complement_pool))
    interest_fit = len(set(person["interests"]) & set(user_interests)) / max(1, len(user_interests))
    avail_fit = 1.0 if availability == "Any" or person["availability"] in [availability, "Flexible"] else 0.55
    level_fit = 1.0 if person["level"] != "Beginner" else 0.85
    score = 100 * (0.40*event_fit + 0.30*complement + 0.15*interest_fit + 0.10*avail_fit + 0.05*level_fit)
    reasons = []
    matched = sorted(candidate_skills & required)
    gaps = sorted(candidate_skills & complement_pool)
    if matched: reasons.append("Event skills: " + ", ".join(matched[:3]))
    if gaps: reasons.append("Can fill your gap in: " + ", ".join(gaps[:3]))
    shared = sorted(set(person["interests"]) & set(user_interests))
    if shared: reasons.append("Shared interests: " + ", ".join(shared[:2]))
    if not reasons: reasons.append("Potential contributor; review their profile before inviting.")
    return round(score, 1), reasons

def render_student(person, score=None, reasons=None):
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    st.markdown(f"### {person['avatar']} {person['name']}")
    st.markdown(f"<span class='small-muted'>{person['branch']} • {person['year']} • {person['level']}</span>", unsafe_allow_html=True)
    if score is not None:
        st.markdown(f"<div class='score'>{score}% <span class='small-muted'>match estimate</span></div>", unsafe_allow_html=True)
    tags = "".join([f"<span class='tag'>{s}</span>" for s in person["skills"]])
    st.markdown(tags, unsafe_allow_html=True)
    st.caption(person["bio"])
    st.markdown(f"**Interests:** {', '.join(person['interests'])}")
    st.markdown(f"**Availability:** {person['availability']}  ·  **Commitment signal:** {person['reliability']}/5")
    if reasons:
        st.markdown("**Why this match?**")
        for reason in reasons:
            st.markdown(f"- {reason}")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Sidebar navigation ----------
with st.sidebar:
    st.markdown("# ✨ TeamSpark")
    st.caption("Find your people. Build better teams.")
    page = st.radio("WORKSPACE", ["Overview","My Profile","AI Match Lab","Student Explorer","Team Builder","Deadline Rescue"], label_visibility="visible")
    st.markdown("---")
    st.markdown("**Solo Spark@2026**")
    st.caption("International Hackathon 5.0 · Round 2")
    st.caption("Demo prototype · Sample records")

# ---------- Header ----------
st.markdown('<div class="hero"><div class="eyebrow">INTERNATIONAL HACKATHON 5.0 · DOMAIN 1</div><h1>Better teams begin with better connections.</h1><p>Discover people beyond your circle. Find complementary skills. Create a team that fits the challenge.</p></div>', unsafe_allow_html=True)

if page == "Overview":
    st.subheader("Your collaboration command centre")
    c1,c2,c3,c4 = st.columns(4)
    with c1: metric("DEMO STUDENT PROFILES", "08", "Illustrative sample records")
    with c2: metric("DEMO EVENTS", "03", "Example challenge briefs")
    with c3: metric("MATCH DIMENSIONS", "05", "Skills · gaps · interests · time · level")
    with c4: metric("TEAM SIZE", "04", "Example event team size")
    st.write("")
    left,right = st.columns([1.35,1])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### 🧭 From discovery to collaboration")
        for title, desc in [
            ("01 · Create your profile","Add skills, interests, experience and availability."),
            ("02 · Choose an event","Understand its theme, team size and required roles."),
            ("03 · Find your fit","Review ranked matches with clear explanations."),
            ("04 · Build a balanced team","Spot missing capabilities and invite collaborators."),
        ]:
            st.markdown(f"<div class='step'><b>{title}</b><br><span class='small-muted'>{desc}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### 💡 TeamSpark difference")
        st.markdown("**Not just similar people. Complementary people.**")
        st.write("TeamSpark considers event requirements, skill gaps, shared interests and availability, then explains why a person may fit.")
        st.info("All names, profiles, metrics and match scores in this prototype are illustrative demo data—not real student records or validated AI results.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.write("")
    st.markdown("### Explore the workspace")
    tiles = st.columns(3)
    for col, icon, title, desc in zip(tiles, ["🪪","🧠","🧩"], ["My Profile","AI Match Lab","Team Builder"], ["Build a skill-aware profile.","Understand every match score.","See which roles your team still needs."]):
        with col:
            st.markdown(f"<div class='profile-card'><h2>{icon}</h2><h3>{title}</h3><p class='small-muted'>{desc}</p></div>", unsafe_allow_html=True)

elif page == "My Profile":
    st.subheader("🪪 Create your collaboration profile")
    st.write("A clear profile helps the matching demo identify relevant and complementary teammates.")
    with st.form("profile_form"):
        a,b = st.columns(2)
        with a:
            name = st.text_input("Your name", value=st.session_state.get("my_name",""))
            branch = st.selectbox("Department / branch", ["ECE","CSE","IT","EEE","Mechanical","Civil","Biotech","Other"])
            year = st.selectbox("Study year", ["1st year","2nd year","3rd year","4th year","Other"])
            level = st.selectbox("Experience level", ["Beginner","Intermediate","Advanced"])
        with b:
            skills = st.multiselect("Your skills", SKILL_OPTIONS, default=st.session_state.get("my_skills",["Python"]))
            interests = st.multiselect("Your interests", INTEREST_OPTIONS, default=st.session_state.get("my_interests",["AI","Social Impact"]))
            availability = st.selectbox("Availability", ["Evenings","Weekends","Flexible"])
            looking = st.checkbox("I am open to joining a team", value=True)
        submitted = st.form_submit_button("Save demo profile ✨", use_container_width=True)
    if submitted:
        st.session_state.my_name = name.strip() or "You"
        st.session_state.my_branch = branch
        st.session_state.my_year = year
        st.session_state.my_level = level
        st.session_state.my_skills = skills
        st.session_state.my_interests = interests
        st.session_state.my_availability = availability
        st.session_state.my_open = looking
        st.success("Your profile is saved for this session.")
    if "my_name" in st.session_state:
        st.markdown("### Profile preview")
        st.markdown(f"**{st.session_state.my_name}** · {st.session_state.my_branch} · {st.session_state.my_year}")
        st.write("Skills:", ", ".join(st.session_state.my_skills) or "Not added yet")
        st.write("Interests:", ", ".join(st.session_state.my_interests) or "Not added yet")
        st.caption("This demo profile is stored only in the current browser session; it is not uploaded to a database.")

elif page == "AI Match Lab":
    st.subheader("🧠 AI Match Lab")
    st.write("Choose an event and see how the prototype ranks potential teammates.")
    event_name = st.selectbox("Select an event", list(EVENTS.keys()))
    event = EVENTS[event_name]
    st.markdown(f"<div class='panel'><h3>{event['icon']} {event_name}</h3><p>{event['theme']}</p><b>Roles needed:</b> {', '.join(event['roles'])}<br><span class='small-muted'>Team size: {event['team_size']} · Deadline: {event['deadline']}</span></div>", unsafe_allow_html=True)
    st.write("")
    d1,d2 = st.columns(2)
    with d1:
        your_skills = st.multiselect("Your current skills", SKILL_OPTIONS, default=st.session_state.get("my_skills",["Python","IoT"]))
        your_interests = st.multiselect("Your interests", INTEREST_OPTIONS, default=st.session_state.get("my_interests",["AI","Hardware"]))
    with d2:
        your_time = st.selectbox("Your availability", ["Any","Evenings","Weekends","Flexible"])
        beginner_mode = st.toggle("Beginner-friendly mode", value=False, help="Prioritise welcoming profiles that are also suitable for beginners.")
    if st.button("✨ Find my best-fit teammates", use_container_width=True):
        results = []
        for p in STUDENTS:
            score, reasons = score_candidate(p,event,your_skills,your_interests,your_time)
            if beginner_mode and p["beginner"]:
                score = min(100, score + 5)
                reasons.append("Beginner-friendly discovery preference applied.")
            results.append((score,p,reasons))
        results.sort(key=lambda x:x[0], reverse=True)
        st.session_state.match_results = results
        st.session_state.match_event = event_name
    if st.session_state.get("match_results"):
        st.markdown(f"### Ranked recommendations · {st.session_state.get('match_event','')}")
        for rank,(score,p,reasons) in enumerate(st.session_state.match_results[:5],1):
            with st.expander(f"#{rank}  {p['avatar']} {p['name']}  ·  {score}% estimated fit", expanded=(rank==1)):
                x,y = st.columns([1,2])
                with x:
                    st.metric("Match estimate", f"{score}%")
                    st.progress(min(1.0,score/100))
                    st.caption(f"Commitment signal: {p['reliability']}/5")
                with y:
                    st.write("**Why this person may fit**")
                    for reason in reasons: st.write("•",reason)
                    st.write("**Skills:**",", ".join(p["skills"]))
        st.caption("Prototype scoring is transparent, rule-based and illustrative. It is not a trained or externally validated AI model.")

elif page == "Student Explorer":
    st.subheader("🔎 Student Explorer")
    st.write("Browse illustrative profiles and discover capabilities beyond your immediate network.")
    q = st.text_input("Search by name, branch or skill", placeholder="Try Python, ECE, UI/UX...")
    branch_filter = st.multiselect("Filter by branch", sorted({p["branch"] for p in STUDENTS}))
    level_filter = st.multiselect("Experience level", ["Beginner","Intermediate","Advanced"])
    filtered = []
    for p in STUDENTS:
        blob = " ".join([p["name"],p["branch"],p["bio"],*p["skills"],*p["interests"]]).lower()
        if q.lower() in blob and (not branch_filter or p["branch"] in branch_filter) and (not level_filter or p["level"] in level_filter):
            filtered.append(p)
    st.caption(f"{len(filtered)} illustrative profiles found")
    for start in range(0,len(filtered),2):
        cols = st.columns(2)
        for col,p in zip(cols,filtered[start:start+2]):
            with col: render_student(p)

elif page == "Team Builder":
    st.subheader("🧩 Gap-Filling Team Builder")
    event_name = st.selectbox("Choose your challenge", list(EVENTS.keys()), key="builder_event")
    event = EVENTS[event_name]
    st.write(f"**Challenge:** {event['theme']}")
    team_names = st.multiselect("Select people already in your team", [p["name"] for p in STUDENTS], default=["Aarav Menon","Meera Krishnan"])
    selected = [p for p in STUDENTS if p["name"] in team_names]
    covered = set()
    for p in selected: covered.update(p["skills"])
    required = set(event["skills"])
    missing = sorted(required-covered)
    st.markdown("### Current capability coverage")
    if required:
        st.progress(min(1.0,len(required & covered)/len(required)))
        st.caption(f"{len(required & covered)} of {len(required)} example skill requirements currently represented.")
    if missing:
        st.warning("Potential gaps: " + ", ".join(missing))
    else:
        st.success("The selected team covers the example skill list.")
    suggestions=[]
    for p in STUDENTS:
        if p in selected: continue
        adds = sorted(set(p["skills"]) & set(missing))
        if adds: suggestions.append((len(adds),p,adds))
    suggestions.sort(key=lambda x:(x[0],x[1]["reliability"]),reverse=True)
    st.markdown("### Suggested gap-fillers")
    if suggestions:
        for _,p,adds in suggestions[:4]:
            with st.container(border=True):
                a,b = st.columns([3,1])
                with a:
                    st.markdown(f"**{p['avatar']} {p['name']}** · {p['branch']} · {p['level']}")
                    st.write("Can add:",", ".join(adds))
                    st.caption(p["bio"])
                with b:
                    st.metric("Commitment signal",f"{p['reliability']}/5")
    else:
        st.info("No additional gap-filler found in this small illustrative dataset. Try another event or team combination.")
    st.caption("Team recommendations are suggestions only. Real members must review and accept invitations.")

elif page == "Deadline Rescue":
    st.subheader("⏳ Deadline Rescue")
    st.write("A last-minute discovery view that highlights useful complementary skills when an event deadline is close.")
    event_name = st.selectbox("Event approaching its deadline", list(EVENTS.keys()), key="rescue_event")
    event = EVENTS[event_name]
    st.markdown(f"<div class='panel'><h3>⚡ {event_name}</h3><b>Deadline:</b> {event['deadline']}<br><b>Roles to cover:</b> {', '.join(event['roles'])}</div>", unsafe_allow_html=True)
    needed = st.multiselect("Which roles are still missing?", event["roles"], default=event["roles"][:2])
    if st.button("Find quick team options",use_container_width=True):
        role_skill_map = {
            "AI / ML":["Python","Machine Learning","Data Analysis"],
            "Frontend":["React","HTML","CSS","UI/UX"],
            "Backend":["Backend","SQL","Python"],
            "Hardware / IoT":["IoT","Arduino","Circuit Design","Embedded C"],
            "UI / UX":["UI/UX","Figma","Presentation"],
            "Domain Research":["Research","Biology","Data Analysis"],
            "Learning Research":["Research","Accessibility","Presentation"],
            "Data / AI":["Python","Data Analysis","Machine Learning"],
        }
        role_skills=set()
        for role in needed: role_skills.update(role_skill_map.get(role,[]))
        ranked=[]
        for p in STUDENTS:
            overlap=sorted(set(p["skills"]) & role_skills)
            if overlap: ranked.append((len(overlap),p,overlap))
        ranked.sort(key=lambda x:(x[0],x[1]["reliability"]),reverse=True)
        st.session_state.rescue_results=ranked
    if st.session_state.get("rescue_results") is not None:
        if st.session_state.rescue_results:
            for count,p,overlap in st.session_state.rescue_results[:5]:
                with st.container(border=True):
                    st.markdown(f"**{p['avatar']} {p['name']}** · {p['branch']} · {p['availability']}")
                    st.write("Useful capabilities:",", ".join(overlap))
                    st.caption("Review availability and contact the person directly; no invitation is sent by this demo.")
        else:
            st.info("No matching profile in this illustrative dataset.")
    st.info("Deadline Rescue is a concept demonstration. It does not contact students or guarantee availability.")

st.markdown("---")
st.markdown("<div style='text-align:center;color:#8791a8;font-size:.82rem'>✨ TeamSpark · Solo Spark@2026 · International Hackathon 5.0 · Round 2<br>Prototype demonstration only · Sample data is illustrative · No real student data is collected</div>", unsafe_allow_html=True)
