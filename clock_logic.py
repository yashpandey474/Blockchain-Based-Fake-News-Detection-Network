import time
from datetime import datetime
import streamlit as st

t = st.empty()

while True:
    t.markdown("%s" % str(int(time.time())))
    time.sleep(1)