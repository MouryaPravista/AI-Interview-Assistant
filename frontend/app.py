import streamlit as st
import requests

st.set_page_config(page_title="Professional AI Interviewer", layout="centered")
st.title("💼 Professional AI Interview Room")

# Session Management
for key in ['step', 'resume_text', 'roles', 'questions', 'report', 'selected_role', 'selected_level']:
    if key not in st.session_state:
        st.session_state[key] = 1 if key == 'step' else (None if key == 'questions' else "")

# STEP 1: RESUME & ROLE
if st.session_state.step == 1:
    st.header("Step 1: Your Profile")
    file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    if st.button("Analyze & Start") and file:
        with st.spinner("AI is studying your resume..."):
            res = requests.post("http://127.0.0.1:8000/analyze-resume", files={"file": file}).json()
            st.session_state.resume_text, st.session_state.roles, st.session_state.step = res['resume_text'], res['recommended_roles'], 2
            st.rerun()

# STEP 2: SETUP
elif st.session_state.step == 2:
    st.header("Step 2: Interview Settings")
    lvl = st.select_slider("Difficulty", options=["Easy", "Medium", "Hard"])
    
    st.write("Pick a suggested role or type your own:")
    cols = st.columns(3)
    for i, r_name in enumerate(st.session_state.roles[:3]):
        if cols[i].button(f"Target: {r_name}"):
            with st.spinner("Preparing 5-round interview..."):
                d = {"role": r_name, "resume_text": st.session_state.resume_text, "level": lvl}
                qs = requests.post("http://127.0.0.1:8000/get-questions", data=d).json()
                st.session_state.questions, st.session_state.selected_role, st.session_state.selected_level, st.session_state.step = qs['questions'], r_name, lvl, 3
                st.rerun()

# STEP 3: INTERVIEW ROOM
elif st.session_state.step == 3:
    st.header(f"Interviewing for {st.session_state.selected_role}")
    st.caption(f"Difficulty: {st.session_state.selected_level} | 5 Rounds")
    st.progress(0.6) # Visual progress
    
    u_ans = []
    for i, q in enumerate(st.session_state.questions):
        q_txt = q.get('question') if isinstance(q, dict) else q
        st.markdown(f"**Q{i+1}:** {q_txt}")
        ans = st.text_area("Your Response", key=f"ans_{i}", help="Be detailed for a better score.")
        u_ans.append({"question": q_txt, "answer": ans})
        st.divider()

    if st.button("Submit Full Interview"):
        with st.spinner("Hiring Manager is evaluating..."):
            rep = requests.post("http://127.0.0.1:8000/evaluate", json=u_ans).json()
            st.session_state.report, st.session_state.step = rep, 4
            st.rerun()

# STEP 4: RESULT
elif st.session_state.step == 4:
    st.header("Interview Performance Report")
    r = st.session_state.report
    st.metric("Final Score", r.get('overall_score', '0/10'))
    st.info(f"**Summary:** {r.get('feedback', '')}")
    
    for item in r.get('details', []):
        with st.expander(f"Q: {item.get('question', '')[:60]}..."):
            st.write(f"**Grade:** {item.get('score', 0)}/10")
            st.write(f"**Feedback:** {item.get('feedback', '')}")
            
    if st.button("Restart New Session"):
        st.session_state.step = 1
        st.rerun()