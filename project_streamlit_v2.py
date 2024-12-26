import streamlit as st
import pickle
import numpy as np
from sklearn.ensemble import AdaBoostClassifier

def label_to_input(category, text):
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    if (category == "weekday_purchase"):
        label = st.selectbox(text, days_of_week)
    elif (category == "month_purchase"):
        label = st.selectbox(text, months)
    else :
        label = st.selectbox(text, encoders[category].classes_)
    return encoders[category].transform([label])[0]


# model
with open("project_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)
# encoder
with open("source_encoder.pkl", "rb") as encoder_file:
    encoders = pickle.load(encoder_file)

# ui
st.title("Fraudeulent Order Detection")
st.write("Enter the details below to make a prediction:")

# input
IP_country = label_to_input('IP_country', 'IP Country')
month_purchase = label_to_input('month_purchase', 'Month purchased')
weekday_purchase = label_to_input('weekday_purchase', 'Weekday purchased')

device_freq = st.number_input("Device Frequency", min_value=0)
hour_purchased = st.number_input("Hour of Purchase (0-23)", min_value=0, max_value=23)
time_since_signup = st.number_input("Time Since Signup (in seconds)", min_value=0)


# predict
if st.button("Predict"):
    features = np.array([[IP_country, device_freq, month_purchase, weekday_purchase, hour_purchased, time_since_signup]])
    
    prediction = model.predict(features)
    
    if prediction[0] == 0:
        st.success("The order is safe.")
    else:
        st.error("The order may be fradulent!")
