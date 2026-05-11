import streamlit as st
import requests

st.set_page_config(page_title="AI Interview Pro", layout="wide")
st.title("🚀 AI Interview Pro: Easy, Medium, Hard")

# Initialize Session States (The app's memory)
if 'step' not in st.session_state: st.session_state.step = 1
if 'resume_text' not in st.session_state: st.session_state.resume_text = ""
if 'roles' not in st.session_state: st.session_state.roles = []
if 'questions' not in st.session_state: st.session_state.questions = None

# --- STEP 1: UPLOAD ---
if st.session_state.step == 1:
    st.header("Step 1: Upload your Profile")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    if st.button("Analyze Resume"):
        if uploaded_file:
            with st.spinner("AI is reading your resume..."):
                res = requests.post("http://127.0.0.1:8000/analyze-resume", files={"file": uploaded_file}).json()
                st.session_state.resume_text = res['resume_text']
                st.session_state.roles = res['recommended_roles']
                st.session_state.step = 2
                st.rerun()
# --- STEP 2: ROLE SELECTION ---
elif st.session_state.step == 2:
    st.header("Step 2: Select your Target Role")
    st.write("Based on your resume, AI suggests:")
    
    # 1. Suggested Role Buttons
    cols = st.columns(3)
    for i, role in enumerate(st.session_state.roles):
        if cols[i].button(f"Target: {role}"):
            with st.spinner(f"Generating 9 questions for {role}..."):
                data = {"role": role, "resume_text": st.session_state.resume_text}
                res = requests.post("http://127.0.0.1:8000/get-questions", data=data).json()
                st.session_state.questions = res['questions']
                st.session_state.selected_role = role
                st.session_state.step = 3
                st.rerun()
    
    st.write("---")
    
    # 2. Custom Role Input
    custom_role = st.text_input("Or type a custom role (e.g., Agentic AI Engineer):")
    
    if st.button("Use Custom Role"):
        if custom_role:
            with st.spinner(f"Generating 9 leveled questions for {custom_role}..."):
                # We send the custom role to the same backend endpoint
                data = {"role": custom_role, "resume_text": st.session_state.resume_text}
                res = requests.post("http://127.0.0.1:8000/get-questions", data=data).json()
                
                # Save the results and move to the next step
                st.session_state.questions = res['questions']
                st.session_state.selected_role = custom_role
                st.session_state.step = 3
                st.rerun()
        else:
            st.warning("Please type a role first!")

# --- STEP 3: THE INTERVIEW ---
elif st.session_state.step == 3:
    st.header(f"Interview for {st.session_state.selected_role}")
    
    user_answers = []
    
    # Section: Easy
    with st.expander("🟢 EASY LEVEL (Fundamentals)", expanded=True):
        for i, q in enumerate(st.session_state.questions['easy']):
            st.write(f"**Q:** {q['question']}")
            ans = st.text_area("Your Answer", key=f"e_{i}")
            user_answers.append({"question": q['question'], "answer": ans, "level": "easy"})

    # Section: Medium
    with st.expander("🟡 MEDIUM LEVEL (Problem Solving)"):
        for i, q in enumerate(st.session_state.questions['medium']):
            st.write(f"**Q:** {q['question']}")
            ans = st.text_area("Your Answer", key=f"m_{i}")
            user_answers.append({"question": q['question'], "answer": ans, "level": "medium"})

    # Section: Hard
    with st.expander("🔴 HARD LEVEL (Advanced/System Design)"):
        for i, q in enumerate(st.session_state.questions['hard']):
            st.write(f"**Q:** {q['question']}")
            ans = st.text_area("Your Answer", key=f"h_{i}")
            user_answers.append({"question": q['question'], "answer": ans, "level": "hard"})

    if st.button("Finish & Evaluate"):
        with st.spinner("AI is grading 9 answers..."):
            report = requests.post("http://127.0.0.1:8000/evaluate", json=user_answers).json()
            st.session_state.report = report
            st.session_state.step = 4
            st.rerun()

# --- STEP 4: FINAL REPORT ---
elif st.session_state.step == 4:
    st.header("Final Interview Report")
    
    # We use .get() so it never crashes if a key is missing
    report = st.session_state.report
    score = report.get('overall_score', report.get('score', 'N/A'))
    feedback = report.get('feedback', 'No summary provided.')
    details = report.get('details', report.get('evaluations', []))

    st.metric("Overall Score", score)
    st.write(f"**AI Feedback:** {feedback}")
    
    if details:
        for item in details:
            # Again, use .get() for safety inside the loop
            q_text = item.get('question', 'Question')
            q_score = item.get('score', '0')
            q_feed = item.get('feedback', 'No feedback provided.')
            
            with st.expander(f"Q: {q_text[:50]}..."):
                st.write(f"**Score:** {q_score}/10")
                st.write(f"**Feedback:** {q_feed}")
    else:
        st.warning("Individual question details were not returned by the AI.")
            
    if st.button("Restart New Interview"):
        st.session_state.clear()
        st.rerun()