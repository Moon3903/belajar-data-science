import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

st.set_page_config(page_title="pesanan perbulan")

st.markdown("# Visualisasi pesanan perbulan")
st.sidebar.header("Visualisasi pesanan")
st.write(
    """Visualisasi pesanan perbulan dari dataset [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)"""
)

df_orders = pd.read_csv('data/olist_orders_dataset.csv')
df_orders.dropna(axis=0, inplace=True)

columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
           "order_delivered_customer_date", "order_estimated_delivery_date"]
for column in columns:
    df_orders[column] = pd.to_datetime(df_orders[column])

df_orders.sort_values(by="order_purchase_timestamp", inplace=True)
df_orders.reset_index(inplace=True)

min_date = df_orders["order_purchase_timestamp"].min().to_pydatetime().date()
max_date = df_orders["order_purchase_timestamp"].max().to_pydatetime().date()

dates_selection = st.slider(
    'Pilih range bulan',
    min_value=min_date,
    max_value=max_date,
    format="YYYY/MM",
    value=(min_date, max_date)
)

df_orders = df_orders[(df_orders["order_purchase_timestamp"] >= str(dates_selection[0])) &
                      (df_orders["order_purchase_timestamp"] <= str(dates_selection[1]))]

group_param = df_orders['order_purchase_timestamp'].dt.to_period("M")
monthly_order = df_orders.groupby(group_param).order_id.nunique().reset_index()

# dates_selection = st.slider(
#     'Pilih range bulan',
#     min_value=datetime(2023,1,1),
#     max_value=datetime(2024,1,1),
#     format="YY/MM",
#     value=(datetime(2023,1,1), datetime(2024,1,1))
# )

fig, ax = plt.subplots(figsize=(10, 7))

sns.set(style="ticks", context="talk")
plt.style.use("dark_background")

sns.barplot(
    y="order_purchase_timestamp",
    x="order_id",
    data=monthly_order,
    palette="pastel",
)
ax.set_ylabel(None)
ax.set_xlabel("Number of Orders", fontsize=30)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)
