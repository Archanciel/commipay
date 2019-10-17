# from streamlit tutu https://towardsdatascience.com/how-to-write-web-apps-using-simple-python-for-data-scientists-a227a1a01582

import streamlit as st
x = st.slider('x')
st.write(x, 'squared is', x * x)