import streamlit as st
import pandas as pd
import joblib

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Multimodal ADNI Classifier",
    layout="wide"
)

# ----------------------------
# Background Colour
# ----------------------------
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

# ----------------------------
# Load Model
# ----------------------------
model = joblib.load("multimodal_random_forest_pipeline.pkl")

# ----------------------------
# Title
# ----------------------------
st.title("Multimodal Alzheimer's Disease Classifier")
st.markdown("Enter patient data below.")

error_placeholder = st.empty()

# Track whether validation failed
validation_failed = False

# ----------------------------
# 3 Column Layout
# ----------------------------
col1, col2, col3 = st.columns(3)

# ============================
# COLUMN 1 — DEMOGRAPHICS + COGNITION
# ============================
with col1:
    st.subheader("Demographics")

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

    mmse = st.number_input(
        "MMSE Score (0–30)",
        min_value=0,
        max_value=30,
        value=0
    )

    moca = st.number_input(
        "MOCA Score (0–30)",
        min_value=0,
        max_value=30,
        value=0
    )

# ============================
# COLUMN 2 — MRI VOLUMES
# ============================
with col2:
    title_col, help_col = st.columns([0.9, 0.1])

    with title_col:
        st.subheader("MRI Normalised Volumes")

    with help_col:
        with st.popover("ℹ️"):
            st.markdown("""
            **Normalised Volumes**

            Enter values as proportions of intracranial volume (ICV).
            Do NOT enter raw mm³ values.
            """)

    hippocampus = st.number_input("Hippocampus", value=0.0, step=0.000001, format="%.10f")
    amygdala = st.number_input("Amygdala", value=0.0, step=0.000001, format="%.10f")
    temporal_pole = st.number_input("Temporal Pole", value=0.0, step=0.000001, format="%.10f")
    brainstem = st.number_input("Brainstem", value=0.0, step=0.000001, format="%.10f")

# ============================
# COLUMN 3 — CORTICAL THICKNESS
# ============================
with col3:
    title_col, help_col = st.columns([0.9, 0.1])

    with title_col:
        st.subheader("Cortical Thickness")

    with help_col:
        with st.popover("ℹ️"):
            st.markdown("""
            **Cortical Thickness**

            Enter thickness values in millimetres (mm).
            Typical range: 2.0 – 3.5 mm.
            """)

    precentral = st.number_input("Precentral (mm)", value=0.0, step=0.0001, format="%.4f")
    superior_frontal = st.number_input("Superior Frontal (mm)", value=0.0, step=0.0001, format="%.4f")
    insula = st.number_input("Insula (mm)", value=0.0, step=0.0001, format="%.4f")

# ----------------------------
# Styled Predict Button
# ----------------------------
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

# ----------------------------
# Validation + Prediction
# ----------------------------
if predict_clicked:

    invalid_fields = []

    field_values = {
        "Age": age,
        "Education Years": education,
        "MMSE Score": mmse,
        "MOCA Score": moca,
        "Hippocampus Volume": hippocampus,
        "Amygdala Volume": amygdala,
        "Temporal Pole Volume": temporal_pole,
        "Brainstem Volume": brainstem,
        "Precentral Thickness": precentral,
        "Superior Frontal Thickness": superior_frontal,
        "Insula Thickness": insula,
    }

    for field, value in field_values.items():
        if value == 0:
            invalid_fields.append(field)

    # if invalid_fields:

    #     error_placeholder.markdown(
    #         f"""
    #         <div style="
    #             background-color: #ffcccc;
    #             padding: 15px;
    #             border-radius: 8px;
    #             border: 1px solid #ff4d4d;
    #             color: #990000;
    #             font-weight: bold;
    #             text-align: center;
    #         ">
    #             ⚠ All fields must be completed before prediction.<br>
    #             Missing: {", ".join(invalid_fields)}
    #         </div>
    #         """,
    #         unsafe_allow_html=True
    #     )

        st.stop()

    # ----------------------------
    # Prepare Input Data
    # ----------------------------
    input_data = pd.DataFrame({
        "MMSCORE": [mmse],
        "MOCA": [moca],
        "AGE": [age],
        "EDUCATION_YEARS": [education],
        "hippocampus_norm_vol": [hippocampus],
        "amygdala_norm_vol": [amygdala],
        "temporal_pole_norm_vol": [temporal_pole],
        "brainstem_norm_vol": [brainstem],
        "precentral_thick": [precentral],
        "superior_frontal_thick": [superior_frontal],
        "insula_thick": [insula],
        "GENDER": [gender]
    })

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    st.session_state.last_inputs = {
        "MMSCORE": mmse,
        "MOCA": moca,
        "hippocampus_norm_vol": hippocampus,
        "precentral_thick": precentral
    }

    st.session_state.prediction = prediction
    st.session_state.probabilities = probabilities

    st.switch_page("pages/test.py")
