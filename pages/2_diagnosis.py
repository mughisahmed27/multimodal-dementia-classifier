import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.markdown(
    """
    <style>
    .stApp {
        background-color: #d9f2f2;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.set_page_config(page_title="Diagnosis Summary", layout="wide")

# ---------------------------------
# Ensure Prediction Exists
# ---------------------------------
if "prediction" not in st.session_state:
    st.warning("No prediction available. Please return to the main page.")
    st.stop()

prediction = st.session_state.prediction
probabilities = st.session_state.probabilities
inputs = st.session_state.get("last_inputs", None)

diagnosis_map = {
    1: "Cognitively Normal",
    2: "Mild Cognitive Impairment (MCI)",
    3: "Dementia"
}

diagnosis_text = diagnosis_map[prediction]

# ---------------------------------
# Centered Title
# ---------------------------------
st.markdown("<h1 style='text-align:center;'>Diagnosis Summary</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------
# Diagnosis Colour Box
# ---------------------------------
color_map = {
    1: "#2ecc71",   # green
    2: "#f1c40f",   # yellow
    3: "#e74c3c"    # red
}

box_color = color_map[prediction]

st.markdown(
    f"""
    <div style="
        background-color: {box_color};
        padding: 40px;
        border-radius: 12px;
        text-align: center;
        color: white;
        font-size: 32px;
        font-weight: bold;
    ">
        {diagnosis_text}
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)

# ---------------------------------
# Three Column Layout
# ---------------------------------
col1, col2, col3 = st.columns(3)

labels = ["Cognitively Normal", "MCI", "Dementia"]
percent_probs = [round(p * 100, 1) for p in probabilities]

# =================================
# COLUMN 1 — Probability Breakdown
# =================================
with col1:
    st.subheader("Probability Breakdown")

    max_prob = max(percent_probs)

    for label, prob in zip(labels, percent_probs):
        if prob == max_prob:
            st.markdown(f"**{label}: {prob}%**")
        else:
            st.markdown(f"{label}: {prob}%")


# =================================
# COLUMN 2 — Custom Bar Chart
# =================================
with col2:
    st.subheader("Probability Distribution")

    colors = ["#2ecc71", "#f1c40f", "#e74c3c"]  # green, yellow, red

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=labels,
        y=percent_probs,
        text=[f"{p}%" for p in percent_probs],
        textposition="outside",
        marker_color=colors,
        width=0.4 
    ))

    fig.update_layout(
        yaxis=dict(title="Probability (%)", range=[0, 100]),
        xaxis=dict(title=""),
        height=400,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

# =================================
# COLUMN 3 — Key Indicators
# =================================
with col3:
    st.subheader("Key Indicators")

    indicators = []

    if inputs:
        if inputs["MMSCORE"] < 24:
            indicators.append("Low MMSE score (<24)")

        if inputs["MOCA"] < 26:
            indicators.append("Low MOCA score (<26)")

        if inputs["hippocampus_norm_vol"] < 0.003:
            indicators.append("Reduced hippocampal volume")

        if inputs["precentral_thick"] < 2.3:
            indicators.append("Reduced cortical thickness")

    if indicators:
        for item in indicators:
            st.markdown(f"- {item}")
    else:
        st.markdown("No significant abnormal indicators detected.")


# ---------------------------------
# Disclaimer
# ---------------------------------
st.markdown("---")
st.markdown("### Clinical Disclaimer")
st.markdown("""
This tool is intended for research and educational purposes only.  
It does not constitute a medical diagnosis.  

Clinical decisions must be made by qualified healthcare professionals 
based on comprehensive clinical assessment.
""")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #0077b6;
        color: white;
        font-size: 20px;
        padding: 12px 20px;
        border-radius: 8px;
        border: none;
        width: 100%;
        margin-left: 200px;
    }
    div.stButton > button:hover {
        background-color: #023e8a;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

left, center, right = st.columns([1, 2, 1])

with center:
    return_clicked = st.button("Return to Main Page")

if return_clicked:
    st.switch_page("app.py")
