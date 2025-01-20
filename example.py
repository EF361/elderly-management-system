import streamlit as st


# Load the CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Apply the CSS
local_css("styles.css")

# Example of using the CSS classes
st.markdown(
    '<div class="big-font">Welcome to AI Elderly Care Management System</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="highlight">This text is highlighted!</div>', unsafe_allow_html=True
)
