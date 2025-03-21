import streamlit as st
import streamlit_vertical_slider as svs
import numpy as np


st.set_page_config(layout="wide")

st.title("Interest Rate")
step_count = st.slider("Count of periods", min_value=2, max_value=30, step=1)
bottom_cols = st.columns(step_count)
values = list(range(step_count))

with st.container():
    for i, col in enumerate(bottom_cols):
        with col:
            st.markdown(
                body="<p style='text-align: center; color: orange;'>",
                unsafe_allow_html=True,
            )

            values[i] = svs.vertical_slider(
                key=f"{i}",
                default_value=0,
                step=0.05,
                min_value=0,
                max_value=5,
                height=200,
            )
            st.markdown(
                body="</p>",
                unsafe_allow_html=True,
            )

begin_number = st.number_input("Insert today's value:")

st.markdown(
    body=f"#### Average interest rate is: %{
        round(number=(np.float_power(
            np.prod(a=np.array(object=values) / 100 + 1), 1 / step_count
        ) - 1) * 100, ndigits=2)
    }"
)
future_value = round(
    number=begin_number * np.prod(a=np.array(object=values) / 100 + 1),
    ndigits=2
)
st.markdown(
    body=f"#### The Future value is: {future_value}"
)
st.markdown(
    body=f"#### Difference is: {round(number=future_value - begin_number, ndigits=2)}"
)
pct_change = round(number=(future_value - begin_number) * 100 / begin_number, ndigits=2)
st.markdown(
    body=f"#### Difference in Percentage: %{pct_change}"
)
