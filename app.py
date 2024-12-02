
import streamlit as st
import joblib
import pandas as pd
import json

# Load the trained model pipeline
pipeline = joblib.load('model.pkl')  # Replace with the actual path to your saved model

# Input dictionary with feature names and possible values
with open('selected_features.json', 'r') as f:
    feature_dict = json.load(f)

# Generate categorical and numerical feature names
cat_features = []
num_features = []
for k, v in feature_dict.items():
    if len(v) != 0:  # If non-empty list, create one-hot encoded feature names
        for t in v:
            cat_features.append(f'{k}_{t}')
    else:  # If empty list, treat as numerical feature
        num_features.append(f'{k}')

# Combine all features
all_features = cat_features + num_features

# Streamlit app title
st.title("Car Price Prediction App")

# Description
st.write("Provide values for the following features to predict the car price:")

# Create a zero-filled DataFrame with all features
input_df = pd.DataFrame(columns=all_features)
input_df.loc[0] = 0  # Fill with zeros initially

# User inputs
for feature, options in feature_dict.items():
    if len(options) != 0:  # Categorical features
        user_input = st.selectbox(
            f"Select value for {feature}:",
            options + ['Other']
        )
        if user_input == 'Other':  # Allow custom input
            custom_value = st.text_input(f"Enter custom value for {feature}:", value="")
            if custom_value:
                input_df[f"{feature}_{custom_value}"] = 1
        else:  # Update the selected one-hot encoded feature
            input_df[f"{feature}_{user_input}"] = 1
    else:  # Numerical features
        user_input = st.number_input(
            f"Enter numerical value for {feature}:",
            min_value=0.0, step=1.0
        )
        input_df[feature] = user_input

st.write(input_df)

# Display user inputs and predict when the button is clicked
if st.button("Predict"):
    try:
        # Predict using the pipeline
        prediction = pipeline.predict(input_df)[0]
        st.success(f"The predicted price of the car is: ${prediction:,.2f}")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
