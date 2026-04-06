import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Multimodal ADNI Classifier", layout="wide")


# css styling

st.markdown("""
<style>

.stApp {
    background-color: #d9f2f2;
}


div[data-testid="stMarkdownContainer"] p {
    font-size: 18px !important;
    font-weight: 500 !important;
}


input {
    font-size: 18px !important;
}


div[data-baseweb="select"] {
    font-size: 18px !important;
}


h3 {
    font-size: 30px !important;
}


.section-desc {
    font-size: 15px;
    color: #444444;
    height: 120px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


#load ML random forest model

model = joblib.load("multimodal_random_forest_pipeline.pkl")

# Title

st.title("Multimodal Alzheimer's Disease Classifier")
st.markdown("Enter patient data below.")

error_placeholder = st.empty()

col1, col2, col3 = st.columns(3)

# Demographics + Cognitive scores

with col1:

    st.subheader("Demographics")

    st.markdown("""
<div class="section-desc">
Enter the patient's demographic information. Age and education level are known
to influence cognitive performance and dementia risk.
</div>
""", unsafe_allow_html=True)

    age = st.number_input("Age (years)", min_value=0, max_value=100, value=0)

    education = st.number_input(
        "Education (years)",
        min_value=0,
        max_value=30,
        value=0
    )

    gender = st.selectbox("Gender", ["Male", "Female"])

    st.markdown("---")

    st.subheader("Cognitive Tests")

    st.markdown("""
<div class="section-desc">
Enter the patient's cognitive scores.  
MMSE and MoCA are widely used clinical assessments that evaluate memory,
attention, language ability, and other cognitive functions.
</div>
""", unsafe_allow_html=True)

    mmse = st.number_input("MMSE Score (0–30)", min_value=0, max_value=30, value=0)

    moca = st.number_input("MOCA Score (0–30)", min_value=0, max_value=30, value=0)


# MRI Volumes

with col2:

    st.subheader("MRI Normalised Volumes")

    st.markdown("""
<div class="section-desc">
Enter the normalised brain structure volumes derived from MRI analysis.
These values represent the size of each brain structure relative to total
intracranial volume (ICV). Typical values range between <b>0.001 – 0.01</b>.
Do <b>not</b> enter raw mm3 measurements.
</div>
""", unsafe_allow_html=True)

    hippocampus = st.number_input("Hippocampus", value=0.0, step=0.000001, format="%.10f")
    amygdala = st.number_input("Amygdala", value=0.0, step=0.000001, format="%.10f")
    temporal_pole = st.number_input("Temporal Pole", value=0.0, step=0.000001, format="%.10f")
    brainstem = st.number_input("Brainstem", value=0.0, step=0.000001, format="%.10f")

# Cortical Thickness

with col3:

    st.subheader("Cortical Thickness")

    st.markdown("""
<div class="section-desc">
Enter cortical thickness measurements obtained from MRI analysis.
Values should be entered in <b>millimetres (mm)</b>. Typical cortical thickness
ranges between <b>2.0 – 3.5 mm</b>. Reduced thickness may indicate cortical
atrophy associated with neurodegenerative conditions.
</div>
""", unsafe_allow_html=True)

    precentral = st.number_input("Precentral (mm)", value=0.0, step=0.0001, format="%.4f")
    superior_frontal = st.number_input("Superior Frontal (mm)", value=0.0, step=0.0001, format="%.4f")
    insula = st.number_input("Insula (mm)", value=0.0, step=0.0001, format="%.4f")


#button styling

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
    predict_clicked = st.button("Predict Diagnosis")

# diagnosis prediction
if predict_clicked:

    input_data = pd.DataFrame({
        "MMSCORE":[mmse],
        "MOCA":[moca],
        "AGE":[age],
        "EDUCATION_YEARS":[education],
        "hippocampus_norm_vol":[hippocampus],
        "amygdala_norm_vol":[amygdala],
        "temporal_pole_norm_vol":[temporal_pole],
        "brainstem_norm_vol":[brainstem],
        "precentral_thick":[precentral],
        "superior_frontal_thick":[superior_frontal],
        "insula_thick":[insula],
        "GENDER":[gender]
    })

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    st.session_state.last_inputs = {
        "MMSCORE":mmse,
        "MOCA":moca,
        "hippocampus_norm_vol":hippocampus,
        "precentral_thick":precentral
    }

    st.session_state.prediction = prediction
    st.session_state.probabilities = probabilities

    st.switch_page("pages/2_diagnosis.py")