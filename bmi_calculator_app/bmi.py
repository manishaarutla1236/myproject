import streamlit as st
st.title("BMI Calculator")
weight=st.slider("Enter your weight(in kg)",min_value=0.00,max_value=150.00)
height=st.slider("Enter your height(in cm)",min_value=1.00,max_value=300.00)
height_m=height/100
if height_m <= 0:
    st.write("Height must be greater than zero to calculate BMI.")
bmi = weight / (height_m ** 2)


if bmi < 18.5:
    status,color="Underweight","blue"
    st.info("Tip:Eat nutrient-rich food and consult a dietician")
elif 18.5<=bmi<25:
    status,color="Normal weight","green"
    st.success("Great job!Maintain your healthy lifestyle")
elif 25<=bmi<30:
    status,color="Overweight","red"
    st.warning("Tip:Regular exercise and portion control helps")
else:
    status,color="Obese","orange"
    st.error("Consider a professional health plan for weight management.")
st.markdown(f"Your BMI is{bmi:.2f}")
st.markdown(f"Status:{status}")
