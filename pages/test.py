import streamlit as st

st.set_page_config(
    page_title="Test Page",
    layout="wide"
)

# Centered Big Title
st.markdown(
    """
    <h1 style='text-align: center; font-size: 60px;'>
        You've got dementia bro helpppp!!
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)

# Center the image
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("assets/test.jpg", use_container_width=True)