import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Diagnosis Summary", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color:#d9f2f2;
}

p, li {
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)


#ensure prediction exists

if "prediction" not in st.session_state:
    st.warning("No prediction available. Please return to the main page and enter valid data.")
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


st.markdown("<h1 style='text-align:center;'>Diagnosis Summary</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Diagnosis colour box

color_map = {
    1: "#2ecc71",
    2: "#f1c40f",
    3: "#e74c3c"
}

st.markdown(
f"""
<div style="
background-color:{color_map[prediction]};
padding:40px;
border-radius:12px;
text-align:center;
color:white;
font-size:36px;
font-weight:bold;">
{diagnosis_text}
</div>
""",
unsafe_allow_html=True
)


# Diagnosis explanation

diagnosis_explanations = {

    1: """
**The model did not detect patterns associated with cognitive impairment in the provided data.
Cognitive test scores and neuroimaging indicators appear consistent with normal cognitive function.**
""",

    2: """
**The model identified patterns that may indicate mild cognitive impairment (MCI).
MCI is an intermediate stage between normal cognitive ageing and dementia, where some cognitive decline is present but daily functioning is largely preserved.**
""",

    3: """
**The model detected patterns consistent with significant cognitive decline.
This may include lower cognitive test scores and neuroimaging markers associated with dementia.**
"""
}

st.markdown(
f"""
<div style="
text-align:center;
font-size:18px;
max-width:900px;
margin:auto;
margin-top:10px;">
{diagnosis_explanations[prediction]}
</div>
""",
unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)

labels = ["Cognitively Normal", "MCI", "Dementia"]
percent_probs = [round(p * 100, 1) for p in probabilities]

col1, col2, col3 = st.columns(3)


# Probability Breakdown
with col1:

    st.subheader("Probability Breakdown")

    st.markdown("""
This section shows the **model's confidence** in each possible diagnosis.
For example, if the model reports **70% Dementia**, this means the model is **70% confident that Dementia is the most likely classification**, based on the input data.
**It does not mean the patient has a 70% chance of having dementia.**
""")

    max_prob = max(percent_probs)

    for label, prob in zip(labels, percent_probs):

        if prob == max_prob:
            st.markdown(f"**{label}: {prob}%**")
        else:
            st.markdown(f"{label}: {prob}%")

# Probability Chart
with col2:

    st.subheader("Probability Distribution")

    st.markdown("""
This chart visualises the probability assigned by the model to each cognitive stage.
""")

    colors = ["#2ecc71", "#f1c40f", "#e74c3c"]

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
        yaxis=dict(title="Model Probability (%)", range=[0, 100]),
        xaxis=dict(title="Cognitive Stage"),
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)


# Key indicators

with col3:

    st.subheader("Key Indicators")

    if inputs:

        if inputs["MMSCORE"] < 24:
            st.markdown("""
**Low MMSE score (<24)**  
A Mini Mental State Examination score below 24 may indicate significant cognitive impairment and is commonly used as a clinical screening threshold for dementia.
""")

        if inputs["MOCA"] < 26:
            st.markdown("""
**Low MOCA score (<26)**  
A Montreal Cognitive Assessment score below 26 suggests potential mild cognitive impairment or early dementia.
""")

        if inputs["hippocampus_norm_vol"] < 0.003:
            st.markdown("""
**Reduced hippocampal volume**  
The hippocampus plays a key role in memory formation. Reduced volume is a well established biomarker associated with Alzheimer's disease and neurodegeneration.
""")

        if inputs["precentral_thick"] < 2.3:
            st.markdown("""
**Reduced cortical thickness**  
Cortical thinning can occur as a result of neuronal loss and is frequently observed in neurodegenerative disorders such as Alzheimer's disease.
""")

    else:
        st.markdown("No significant abnormal indicators detected.")

#Disclaimer
st.markdown("---")

st.markdown("### Clinical Disclaimer")

st.markdown("""
This tool is intended for research and educational purposes only.
It does not constitute a medical diagnosis and should not be used as a substitute for professional clinical evaluation.
Clinical decisions must be made by qualified healthcare professionals based on comprehensive neurological and cognitive assessment.
""")

# Return button

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