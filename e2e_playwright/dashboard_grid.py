# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2025)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import streamlit as st


@st.cache_data(show_spinner=False)
def generate_mock_data(
    days: int = 90, seed: int = 7
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate mock time-series and categorical data for the dashboard.

    Parameters
    ----------
    days:
        Number of days of data to generate.
    seed:
        Random seed for reproducibility.

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame]
        time_series_df: Columns [date, users, sales, revenue, conversion_rate]
        category_df: Columns [category, revenue]
    """

    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=dt.date.today(), periods=days, freq="D")

    base_users = rng.normal(loc=1200, scale=120, size=days).clip(min=300)
    trend_users = np.linspace(0, 150, days)
    users = (base_users + trend_users).round().astype(int)

    # Sales roughly proportional to users with noise
    sales_rate = rng.normal(loc=0.08, scale=0.01, size=days).clip(0.03, 0.15)
    sales = (
        np.floor(users * sales_rate + rng.normal(0, 10, size=days))
        .clip(min=0)
        .astype(int)
    )

    # Revenue per sale varies slightly day-to-day
    revenue_per_sale = rng.normal(loc=42.0, scale=4.5, size=days).clip(20, 80)
    revenue = (sales * revenue_per_sale).round(2)

    conversion_rate = (sales / np.maximum(users, 1) * 100).round(2)

    time_series_df = pd.DataFrame(
        {
            "date": dates,
            "users": users,
            "sales": sales,
            "revenue": revenue,
            "conversion_rate": conversion_rate,
        }
    )

    categories = ["Alpha", "Beta", "Gamma", "Delta", "Omega"]
    cat_weights = rng.uniform(0.8, 1.2, size=len(categories))
    cat_revenue = (cat_weights / cat_weights.sum()) * revenue[-7:].sum()
    category_df = pd.DataFrame(
        {"category": categories, "revenue": cat_revenue.round(2)}
    )

    return time_series_df, category_df


def percentage_delta(current: float, previous: float) -> float:
    if previous == 0:
        return 0.0
    return (current - previous) / previous * 100.0


st.set_page_config(page_title="Dashboard Grid (Mock)", layout="wide")

use_container_shadow = st.sidebar.toggle("Use container shadow", value=True)
use_container_background = st.sidebar.toggle("Use container background", value=True)
use_container_border = st.sidebar.toggle("Use container border", value=False)

# Header / meta
with st.container():
    st.title(":material/bar_chart: Demo Dashboard Grid")
    st.caption(
        "Mock data showcasing containers, columns, metrics, a dataframe, and charts."
    )
    st.write(f"Last updated: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

ts_df, cat_df = generate_mock_data(days=120)

# KPI row
kpi_cols = st.columns(4)
latest = ts_df.iloc[-1]
prev = ts_df.iloc[-2]

with kpi_cols[0]:
    st.container(
        shadow=use_container_shadow,
        background=use_container_background,
        border=use_container_border,
    ).metric(
        label="Active Users",
        value=f"{latest.users:,}",
        delta=f"{abs(percentage_delta(latest.users, prev.users)):+.1f}%",
    )
with kpi_cols[1]:
    st.container(
        shadow=use_container_shadow,
        background=use_container_background,
        border=use_container_border,
    ).metric(
        label="Sales",
        value=f"{latest.sales:,}",
        delta=f"{abs(percentage_delta(latest.sales, prev.sales)):+.1f}%",
    )
with kpi_cols[2]:
    st.container(
        shadow=use_container_shadow,
        background=use_container_background,
        border=use_container_border,
    ).metric(
        label="Revenue",
        value=f"${latest.revenue:,.0f}",
        delta=f"{abs(percentage_delta(latest.revenue, prev.revenue)):+.1f}%",
    )
with kpi_cols[3]:
    st.container(
        shadow=use_container_shadow,
        background=use_container_background,
        border=use_container_border,
    ).metric(
        label="Conversion Rate",
        value=f"{latest.conversion_rate:.2f}%",
        delta=f"{abs(latest.conversion_rate - prev.conversion_rate):+.2f} pp",
    )


# Main grid
left_col, right_col = st.columns([3, 2], gap="small")

with left_col:
    with st.container(
        shadow=use_container_shadow,
        background=use_container_background,
        border=use_container_border,
        height=350,
    ):
        st.subheader("Recent Activity")
        st.dataframe(
            ts_df.tail(25).sort_values("date", ascending=False).reset_index(drop=True),
            use_container_width=True,
            hide_index=True,
            height=240,
        )

with right_col:
    with st.container(
        shadow=use_container_shadow,
        background=use_container_background,
        border=use_container_border,
        height=350,
    ):
        st.subheader("Trends (Last 60 Days)")
        recent = ts_df.set_index("date").tail(60)[["users", "sales"]]
        st.line_chart(recent, height=220)
        st.caption("Users and Sales over time")


# Secondary grid
c1, c2, c3 = st.columns([2, 2, 2])

with c1:
    with st.container(
        shadow=use_container_shadow,
        background=use_container_background,
        border=use_container_border,
    ):
        st.subheader("Category Revenue (7d)")
        st.dataframe(
            cat_df.sort_values("revenue", ascending=False),
            use_container_width=True,
            height=240,
        )

with c2:
    with st.container(
        shadow=use_container_shadow,
        background=use_container_background,
        border=use_container_border,
    ):
        st.subheader("Sales (14d)")
        sales_14 = ts_df.set_index("date").tail(14)[["sales"]]
        st.bar_chart(sales_14, height=240)

with c3:
    with st.container(
        shadow=use_container_shadow,
        background=use_container_background,
        border=use_container_border,
    ):
        st.subheader("Revenue vs. Conversion (30d)")
        rev_conv = ts_df.set_index("date").tail(30)[["revenue", "conversion_rate"]]
        st.area_chart(rev_conv, height=240)
