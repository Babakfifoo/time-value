import streamlit as st
import streamlit_vertical_slider as svs
import numpy as np
import pandas as pd


COLOR_SECONDARY = "#005757"
COLOR_PRIMARY = "#86e5d4"
st.set_page_config(layout="wide")

st.title("Setting Parameters")
left_period, right_period = st.columns([1, 6])
with left_period:
    period = st.radio(
        "Period type:", options=["Year", "Half-year", "Quarter"], horizontal=True
    )
with right_period:
    step_count = st.slider(
        label="Count of periods",
        min_value=1,
        max_value=20,
        step=1,
    )


with st.expander("Interest Rates (%)", expanded=True):
    bottom_cols = st.columns(step_count)
    values = list(range(step_count))

    for i, col in enumerate(bottom_cols):
        with col:
            st.markdown(
                body="<p style='text-align: right;'>",
                unsafe_allow_html=True,
            )

            values[i] = svs.vertical_slider(
                label=str(i + 1),
                key=f"{i + 1}",
                default_value=0,
                step=0.05,
                min_value=0,
                max_value=10,
                height=100,
                value_always_visible=True,
                slider_color=COLOR_PRIMARY,
                thumb_color=COLOR_SECONDARY,
            )
            st.markdown(
                body="</p>",
                unsafe_allow_html=True,
            )
    sep_exp = st.toggle("Separate rates for expences:")

if sep_exp:
    with st.expander("Expence Growth (%)", expanded=True):
        expense_cols = st.columns(spec=step_count)
        expense_rate = list(range(step_count))

        for i, col in enumerate(expense_cols):
            with col:
                st.markdown(
                    body="<p style='text-align: right;'>",
                    unsafe_allow_html=True,
                )

                expense_rate[i] = svs.vertical_slider(
                    label=str(i + 1),
                    key=f"exp{i + 1}",
                    default_value=0,
                    step=0.05,
                    min_value=0,
                    max_value=10,
                    height=100,
                    value_always_visible=True,
                    slider_color=COLOR_PRIMARY,
                    thumb_color=COLOR_SECONDARY,
                )
                st.markdown(
                    body="</p>",
                    unsafe_allow_html=True,
                )
else:
    expense_rate = values

interest_mat = np.prod(
    np.triu(((np.array(values) / 100) * np.ones((step_count, step_count))).T) + 1,
    axis=0,
)
expense_mat = np.prod(
    np.triu(((np.array(expense_rate) / 100) * np.ones((step_count, step_count))).T) + 1,
    axis=0,
)

with st.expander("Values (€)", expanded=True):
    value_cols = st.columns([1, 1])
    with value_cols[0]:
        st.markdown("### Income (€)")
        selling_price = st.number_input("Selling Price (Exit value €)", min_value=1)
        GRR = st.number_input("Gross rental revenue (€):", min_value=1)
        OI = st.number_input("Other income (€):", min_value=1)

    with value_cols[1]:
        st.markdown("### Expense (€)")
        today_val = st.number_input("Market Value (Today €)", min_value=1)
        expense_all = st.number_input("Current year expences (All)", min_value=1)


st.markdown("# Results")

st.markdown(f"#### Calculations are done for *{step_count}* periods.")

avg_interest_rate = round(
    number=(
        np.float_power(np.prod(a=np.array(object=values) / 100 + 1), 1 / step_count) - 1
    )
    * 100,
    ndigits=2,
)
st.markdown(body=f"#### Average interest rate is: %{avg_interest_rate}")
if sep_exp:
    avg_expense_rate = round(
        number=(
            np.float_power(np.prod(a=np.array(object=expense_rate) / 100 + 1), 1 / step_count) - 1
        )
        * 100,
        ndigits=2,
    )
    st.markdown(body=f"#### Average interest rate is: %{avg_expense_rate}")
future_value = round(
    number=today_val * np.prod(a=np.array(object=values) / 100 + 1), ndigits=2
)

"## Cashflow:"

NOI = (interest_mat * GRR) + (interest_mat * OI) - (expense_mat * expense_all)
NOI[0] = NOI[0] - today_val
NOI[-1] = NOI[-1] + selling_price

df = pd.DataFrame(
    data=[
        [f"{i:2.2f}%" for i in (values)],
        [f"{i:2.2f}%" for i in (expense_rate)],
        [f"-{today_val:,.2f}€"] + [""] * (step_count - 1),
        [f"{i:,.2f}€" for i in (interest_mat * GRR)],
        [f"{i:,.2f}€" for i in (interest_mat * OI)],
        [f"{i:,.2f}€" for i in (expense_mat * expense_all)],
        [""] * (step_count - 1) + [f"{selling_price:,.2f}€"],
        [f"{i:,.2f}€" for i in NOI],
    ],
    index=[
        "Interest %",
        "Expence Growth %",
        "Outflow",
        "Gross rental revenue",
        "Other Income",
        "Total expences",
        "Sell Price",
        "Total",
    ],
    columns=[period[0] + str(i + 1) for i in range(step_count)],
)
st.table(df)

