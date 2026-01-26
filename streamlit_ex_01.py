import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('広告費と売り上げ')
data = pd.read_csv('zmy2020a.csv')
df = pd.DataFrame(data)

