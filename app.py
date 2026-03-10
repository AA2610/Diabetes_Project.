import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# ---------------- PAGE SETTINGS ---------------- #
st.set_page_config(
    page_title="Diabetes Health Dashboard",
    page_icon="🩺",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #E0F7FA; }
.main-title { font-family: 'Times New Roman', Times, serif !important; font-weight: bold !important; color: black !important; font-size: 48px !important; text-align:center; }
.section-title { font-family: 'Times New Roman', Times, serif !important; font-weight: bold !important; color: black !important; font-size:32px !important; }
.card-heading { font-family: 'Times New Roman', Times, serif !important; font-weight: bold !important; color: black !important; font-size:24px !important; margin-bottom:5px; }
.card-value { font-family: 'Times New Roman', Times, serif !important; font-weight: normal !important; color: black !important; font-size:18px !important; margin-bottom:10px; }
label { font-family: 'Times New Roman', Times, serif !important; font-weight: bold !important; color: black !important; font-size:18px !important; }
input, textarea { color: black !important; background-color: #FFFFFF !important; border-radius: 8px !important; }
.card { background-color: #FFFFFF; padding: 20px; border-radius: 15px; box-shadow: 3px 3px 15px rgba(0,0,0,0.1); margin-bottom:20px; }
.stButton>button { background-color:#0288D1; color:white; height:3em; width:100%; border-radius:10px; font-size:16px; font-weight:bold; }
.faq-btn { background-color:#B3E5FC; color:black; padding:5px 10px; margin:3px; border-radius:8px; cursor:pointer; font-size:14px; display:inline-block; }
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ---------------- #
model = joblib.load("diabetes_model.pkl")
scaler = joblib.load("scaler.pkl")

# ---------------- PAGE TITLE ---------------- #
st.markdown('<h1 class="main-title">Diabetes Health Dashboard</h1>', unsafe_allow_html=True)
st.write("")

# ---------------- LAYOUT ---------------- #
col_left, col_right = st.columns([2,1])

# ---------------- LEFT COLUMN ---------------- #
with col_left:
    st.markdown('<h2 class="section-title">Health Report & Prediction</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    preg = st.number_input("Pregnancies", min_value=0)
    glucose = st.number_input("Glucose Level", min_value=0)
    bp = st.number_input("Blood Pressure", min_value=0)
    skin = st.number_input("Skin Thickness", min_value=0)
    insulin = st.number_input("Insulin Level", min_value=0)
    bmi = st.number_input("BMI", min_value=0.0)
    dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0)
    age = st.number_input("Age", min_value=1)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Generate Health Report"):
        input_data = pd.DataFrame({
            'Pregnancies':[preg],
            'Glucose':[glucose],
            'BloodPressure':[bp],
            'SkinThickness':[skin],
            'Insulin':[insulin],
            'BMI':[bmi],
            'DiabetesPedigreeFunction':[dpf],
            'Age':[age]
        })
        scaled = scaler.transform(input_data)
        prediction = model.predict(scaled)
        probability = model.predict_proba(scaled)[0][1]

        if probability < 0.30:
            risk = "LOW"
            risk_color = "#4CAF50"
        elif probability < 0.70:
            risk = "MEDIUM"
            risk_color = "#FFC107"
        else:
            risk = "HIGH"
            risk_color = "#F44336"

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown('<p class="card-heading">Prediction Result</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="card-value">{"DIABETIC" if prediction[0]==1 else "NON-DIABETIC"}</p>', unsafe_allow_html=True)

        st.markdown('<p class="card-heading">Probability</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="card-value">{round(probability*100,2)}%</p>', unsafe_allow_html=True)

        st.markdown('<p class="card-heading">Risk Level</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background-color:{risk_color}; color:white; padding:10px; border-radius:10px; font-size:20px; text-align:center;'>
        {risk}
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="card-heading">Health Parameters</p>', unsafe_allow_html=True)
        fig = go.Figure(data=[go.Bar(
            x=input_data.columns,
            y=input_data.iloc[0].values,
            marker_color='black'
        )])
        fig.update_layout(
            plot_bgcolor='#E0F7FA',
            paper_bgcolor='#E0F7FA',
            xaxis=dict(color='black'),
            yaxis=dict(color='black'),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<p class="card-heading">Health Suggestions</p>', unsafe_allow_html=True)
        if risk=="LOW":
            st.markdown('<p class="card-value">• Maintain balanced diet <br>• Exercise regularly </p>', unsafe_allow_html=True)
        elif risk=="MEDIUM":
            st.markdown('<p class="card-value">• Reduce sugar intake <br>• Daily walking recommended </p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="card-value">• Consult doctor immediately <br>• Follow strict diabetic diet </p>', unsafe_allow_html=True)

        st.markdown('<p class="card-heading">Medical Alerts</p>', unsafe_allow_html=True)
        if glucose>=200: st.markdown('<p class="card-value">Critical glucose level</p>', unsafe_allow_html=True)
        elif glucose>=140: st.markdown('<p class="card-value">High glucose detected</p>', unsafe_allow_html=True)
        if bmi>=30: st.markdown('<p class="card-value">Obesity risk</p>', unsafe_allow_html=True)
        if bp>=140: st.markdown('<p class="card-value">High blood pressure risk</p>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RIGHT COLUMN: CHATBOT WITH FAQ ---------------- #
faq_answers = {
    "What is diabetes?": "Diabetes is a condition where your blood sugar levels are too high.",
    "Types of diabetes": "The main types are Type 1, Type 2, and Gestational diabetes.",
    "Symptoms of diabetes": "Common symptoms include increased thirst, frequent urination, fatigue, and blurred vision.",
    "Prevent diabetes": "Maintain a healthy diet, exercise regularly, and monitor blood sugar levels.",
    "Diet for diabetes": "Focus on balanced meals with vegetables, proteins, and low sugar intake.",
    "Exercise for diabetes": "Walking, jogging, cycling, and other regular physical activity help manage diabetes."
}

with col_right:
    st.markdown('<h2 class="section-title">AI Diabetes Chatbot</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # FAQ Buttons
    st.markdown('<p class="card-heading">Quick FAQs</p>', unsafe_allow_html=True)
    for faq in faq_answers.keys():
        if st.button(faq, key=faq):
            st.session_state['user_question'] = faq

    # Long rectangular input box
    user_question = st.text_area("Type your question here...", height=100, key="user_question")

    # Chatbot response
    if st.button("Ask Chatbot"):
        answer = "Sorry, I don't have an answer for that."
        question_lower = user_question.lower()
        for key in faq_answers:
            if key.lower() in question_lower:
                answer = faq_answers[key]
                break
        st.markdown('<p style="color:black; font-weight:bold; font-size:18px;">Chatbot Response:</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:black; font-size:16px;">{answer}</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)