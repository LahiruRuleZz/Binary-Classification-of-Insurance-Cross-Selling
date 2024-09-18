import streamlit as st
import pickle

# Load the model
model = pickle.load(open(r'C:\Users\Lahiru Anuradha\Desktop\CI SUBMISION\Binary_Classification\model_clf_RF_Insuarance.pkl', 'rb'))

st.title('Insurance Cross-Selling Prediction')

# Input fields with default values for resetting
def get_default_values():
    return {
        'age': 30,
        'gender': 'Male',
        'driving_license': 'Yes',
        'region_code': 0,
        'previously_insured': 'No',
        'vehicle_age': '1-2 Year',
        'vehicle_damage': 'No',
        'annual_premium': 5000.0,
        'policy_sales_channel': 1,
        'vintage': 0
    }

# Initialize session state
if 'inputs' not in st.session_state:
    st.session_state.inputs = get_default_values()

def reset_fields():
    st.session_state.inputs = get_default_values()

# Input fields
age = st.number_input('Age', min_value=18, max_value=92, value=st.session_state.inputs['age'])
gender = st.radio('Gender', ['Male', 'Female'], index=['Male', 'Female'].index(st.session_state.inputs['gender']))
driving_license = st.selectbox('Driving License', ['Yes', 'No'], index=['Yes', 'No'].index(st.session_state.inputs['driving_license']))
region_code = st.number_input('Region Code', min_value=0, value=st.session_state.inputs['region_code'])
previously_insured = st.selectbox('Previously Insured', ['Yes', 'No'], index=['Yes', 'No'].index(st.session_state.inputs['previously_insured']))
vehicle_age = st.selectbox('Vehicle Age', ['1-2 Year', '< 1 Year', '> 2 Years'], index=['1-2 Year', '< 1 Year', '> 2 Years'].index(st.session_state.inputs['vehicle_age']))
vehicle_damage = st.selectbox('Vehicle Damage', ['Yes', 'No'], index=['Yes', 'No'].index(st.session_state.inputs['vehicle_damage']))
annual_premium = st.number_input('Annual Premium', min_value=0.0, max_value=250898.0, step=1000.0, value=st.session_state.inputs['annual_premium'])
policy_sales_channel = st.number_input('Policy Sales Channel', min_value=1, value=st.session_state.inputs['policy_sales_channel'])
vintage = st.number_input('Vintage', min_value=0, value=st.session_state.inputs['vintage'])

# Prediction logic
def predict(age, gender, driving_license, region_code, previously_insured, vehicle_age,
            vehicle_damage, annual_premium, policy_sales_channel, vintage):
    
    # Convert categorical features to numerical values
    gender = 1 if gender == 'Male' else 0
    driving_license = 1 if driving_license == 'Yes' else 0
    previously_insured = 1 if previously_insured == 'Yes' else 0
    vehicle_damage = 1 if vehicle_damage == 'Yes' else 0

    # Map vehicle_age to numerical values
    if vehicle_age == '1-2 Year':
        vehicle_age = 1
    elif vehicle_age == '< 1 Year':
        vehicle_age = 2
    else:  # '> 2 Years'
        vehicle_age = 3

    # Create a feature vector for prediction
    features = [age, gender, driving_license, region_code, previously_insured, vehicle_age,
                vehicle_damage, annual_premium, policy_sales_channel, vintage]

    # Make prediction
    prediction = model.predict([features])
    
    if prediction[0] == 1:
        return 'The customer is likely to respond!'
    else:
        return 'The customer is unlikely to respond.'

# Display result
if st.button('Predict'):
    result = predict(age, gender, driving_license, region_code, previously_insured, vehicle_age,
                     vehicle_damage, annual_premium, policy_sales_channel, vintage)
    st.write('Prediction:', result)

# Clear button to reset input fields
if st.button('Clear'):
    reset_fields()
    # Optionally, you can use `st.experimental_rerun()` to refresh the app and reflect changes immediately.
    st.experimental_rerun()
