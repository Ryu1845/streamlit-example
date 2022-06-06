import streamlit as st
from twspace_dl import Twspace, TwspaceDL

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

st.set_page_config(page_title="twspace-dl online", page_icon="🌟", layout="wide")
params = st.experimental_get_query_params()
url = st.text_input(label="Space URL")
space = Twspace.from_space_url(url)

with st.sidebar:
    st.write("## Twitter Space Downloader")
