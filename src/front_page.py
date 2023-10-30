import requests
import pandas as pd
import streamlit as st
import cfbd
import os
import sys
from PIL import Image
from pathlib import Path
from io import BytesIO

# Create the filepath

#sys.path.insert(0, os.path.join(Path(__file__).parents[1]))
df = pd.read_csv(r'src\data\team_records.csv')

#st.title("Welcome to Your Favorite College Football Team's Homepage!")

#answer = st.text_input("What is your favorite college football team: ")
#if answer:
 #   st.write(list())



