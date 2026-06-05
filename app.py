import streamlit as st
import requests
import pandas as pd

# Page config
st.set_page_config(
    page_title="Student Performance Tracker",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .stButton>button:hover { background-color: #45a049; }
    .metric-card {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin: 5px;
    }
    .metric-number { font-size: 2rem; font-weight: bold; }
    .metric-label { font-size: 0.9rem; opacity: 0.8; }
    .success-box {
        background: #1a472a;
        border-left: 4px solid #4CAF50;
        padding: 15px;
        border-radius: 8px;
        color: #90EE90;
    }
    .error-box {
        background: #4a1515;
        border-left: 4px solid #f44336;
        padding: 15px;
        border-radius: 8px;
        color: #ffcdd2;
    }
    .topper-card {
        background: linear-gradient(135deg, #f6d365, #fda085);
        padding: 20px;
        border-radius: 12px;
        color: #1a1a1a;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

BASE_URL = "http://localhost:8000"

# Header
st.markdown("""
<div style='text-align:center; padding: 20px 0'>
    <h1 style='color:#4CAF50; font-size:2.5rem'>🎓 Student Performance Tracker</h1>
    <p style='color:#888; font-size:1rem'>Manage students · Track grades · Find toppers</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Stats bar at top
stats_resp = requests.get(f"{BASE_URL}/stats")
stats = stats_resp.json()

if "total_students" in stats:
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"""<div class='metric-card'>
        <div class='metric-number'>{stats['total_students']}</div>
        <div class='metric-label'>Total Students</div></div>""",
        unsafe_allow_html=True)
    c2.markdown(f"""<div class='metric-card'>
        <div class='metric-number'>{stats['average_marks']}</div>
        <div class='metric-label'>Average Marks</div></div>""",
        unsafe_allow_html=True)
    c3.markdown(f"""<div class='metric-card'>
        <div class='metric-number'>{stats['highest_marks']}</div>
        <div class='metric-label'>Highest Marks</div></div>""",
        unsafe_allow_html=True)
    c4.markdown(f"""<div class='metric-card'>
        <div class='metric-number'>{stats['lowest_marks']}</div>
        <div class='metric-label'>Lowest Marks</div></div>""",
        unsafe_allow_html=True)
    st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Student", "🔍 Search", "🏆 Topper", "📋 All Students"])

with tab1:
    st.subheader("Add New Student")
    col1, col2 = st.columns(2)
    with col1:
        roll_no = st.number_input("Roll Number", min_value=1, step=1)
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=15, max_value=30, step=1, value=20)
    with col2:
        subject = st.text_input("Subject")
        marks = st.slider("Marks (out of 100)", 0, 100, 75)
        
        # Grade preview
        if marks >= 90: grade_preview = "A 🌟"
        elif marks >= 75: grade_preview = "B ✅"
        elif marks >= 60: grade_preview = "C ⚠️"
        else: grade_preview = "F ❌"
        st.metric("Grade Preview", grade_preview)

    if st.button("Add Student "):
        if name and subject:
            response = requests.post(
                f"{BASE_URL}/add-student",
                params={"roll_no": int(roll_no)},
                json={"name": name, "age": int(age),
                      "marks": float(marks), "subject": subject}
            )
            result = response.json()
            if "error" in result:
                st.markdown(f"<div class='error-box'>❌ {result['error']}</div>",
                    unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='success-box'>✅ {result['message']} — Grade: {result['grade']}</div>",
                    unsafe_allow_html=True)
                st.rerun()
        else:
            st.warning("Please fill in all fields")

with tab2:
    st.subheader("Search Student by Roll Number")
    search_roll = st.number_input("Roll Number", min_value=1, step=1, key="search")
    if st.button("Search 🔍"):
        response = requests.get(f"{BASE_URL}/student/{int(search_roll)}")
        result = response.json()
        if "error" in result:
            st.markdown(f"<div class='error-box'>❌ {result['error']}</div>",
                unsafe_allow_html=True)
        else:
            col1, col2, col3 = st.columns(3)
            col1.metric("Name", result["name"])
            col2.metric("Marks", result["marks"])
            col3.metric("Grade", result["grade"])
            st.info(f"Subject: {result['subject']} | Age: {result['age']}")

with tab3:
    st.subheader("🏆 Class Topper(s)")
    if st.button("Find Topper 🏆"):
        response = requests.get(f"{BASE_URL}/topper")
        result = response.json()
        if "message" in result:
            st.info(result["message"])
        else:
            st.success(f"Highest Marks: {result['highest_marks']} — {result['total_toppers']} topper(s)")
            for roll, data in result["toppers"].items():
                st.markdown(f"""<div class='topper-card'>
                    🥇 {data['name']} | Roll: {roll} | 
                    Marks: {data['marks']} | Grade: {data['grade']}
                </div><br>""", unsafe_allow_html=True)

with tab4:
    st.subheader("All Students")
    if st.button("Load All Students 📋"):
        response = requests.get(f"{BASE_URL}/all-students")
        result = response.json()
        if "message" in result:
            st.info(result["message"])
        else:
            # Convert to table format
            table_data = []
            for roll, data in result.items():
                table_data.append({
                    "Roll No": roll,
                    "Name": data["name"],
                    "Age": data["age"],
                    "Subject": data["subject"],
                    "Marks": data["marks"],
                    "Grade": data["grade"]
                })
            st.dataframe(table_data, use_container_width=True)
            # Add after the dataframe display
            if table_data:
                st.subheader("📊 Marks Distribution")
                df = pd.DataFrame(table_data)
                st.bar_chart(df.set_index("Name")["Marks"])