import streamlit as st
import requests

# Local API endpoint for patient parameters processing
LOCAL_API_ENDPOINT = "http://127.0.0.1:8000/diabetes/recommendation" 

# Streamlit app
st.set_page_config(
    page_title="MediScan",
    page_icon="💊",
    layout="wide"
)

# Title and description
st.title("MediScan - Diabetic Patient Description Analyzer")
st.subheader(
    "Welcome to MediScan! Enter patient descriptions or refer from our samples to analyze and generate recommendations."
)

# Sidebar with sample descriptions and symptoms
st.sidebar.title("Reference Information")

# Fixed sample descriptions
st.sidebar.subheader("Sample Descriptions:")
st.sidebar.text("1. A 55-year-old patient with a BMI of 28 presents with post-meal blood sugar spikes and weight gain. The patient has a moderately active lifestyle with irregular eating patterns and is a non-smoker and does not consume alcohol.")
st.sidebar.text("2. A 38-year-old individual with a BMI of 27 presents with elevated fasting blood sugar levels and increased thirst and frequent urination. The patient follows a sedentary lifestyle with irregular meal timings. They are a non-smoker but consume alcohol occasionally.")
st.sidebar.text("3. A 60-year-old patient with a BMI of 32 presents with poorly controlled blood sugar and insulin resistance. The patient leads a sedentary lifestyle with irregular meal timings.")

# Fixed diabetes symptoms
st.sidebar.subheader("Possible Diabetes Symptoms:")
st.sidebar.text("- Frequent urination")
st.sidebar.text("- Increased thirst")
st.sidebar.text("- Weight loss")
st.sidebar.text("- Fatigue")
st.sidebar.text("- Blurred vision")

def process_parameters(input_description):
    # Call your local API to process patient parameters
    response = requests.get(f"{LOCAL_API_ENDPOINT}/{input_description}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error processing parameters. Status Code: {response.status_code}"}

def main():
    # Streamlit app title and description
    # st.title("Patient Parameters Processing App")
    st.write("Enter the patient parameters and click the button to process.")

    # Input elements for patient parameters
    description = st.text_area("Enter the description:")

    # age = st.number_input("Enter Age:", min_value=0, max_value=150, value=55)
    # bmi = st.number_input("Enter BMI:", min_value=0, max_value=100, value=28)
    # symptoms = st.text_input("Enter Symptoms:")
    # activity_level = st.selectbox("Select Activity Level:", ["Low", "Moderate", "High"], index=1)
    # eating_pattern = st.selectbox("Select Eating pattern style:", ["Regular", "Non-regular"], index=1)
    # smoker_flag = st.checkbox("Smoker")
    # alcohol_flag = st.checkbox("Alcohol Consumer")

    # Process button
    if st.button("Process Parameters"):
        # Prepare parameters string
        # smoker = "non" if not smoker_flag else ""
        # alcohol= "not" if not alcohol_flag else ""
        # parameters_str = f"A {age}-year-old patient with a BMI of {bmi} presents with {symptoms}.The patient has a {activity_level} active lifestyle with {eating_pattern} eating patterns, is a {smoker} smoker and does {alcohol} consume alcohol."
        # st.write(parameters_str)
        
        # Call local API and get results
        results = process_parameters(description)
        
        # Display results
        st.write("Processed Results:")
        st.json(results)

if __name__ == "__main__":
    main()