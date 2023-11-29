import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

st.set_page_config(
    page_title="Kategori Produk",
)

st.sidebar.header("Visualisasi Kategori Produk")

st.write("# Kategori produk yang paling sering dipesan")

st.markdown(
    """
    Kategori produk yang paling sering dipesan dari dataset [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
"""
)

df_products = pd.read_csv('data/olist_products_dataset.csv')
df_order_item = pd.read_csv('data/olist_order_items_dataset.csv')

df_products.dropna(axis=0, inplace=True, subset=['product_category_name'])

df_products_order_item = pd.merge(
    left=df_products,
    right=df_order_item,
    how="inner",
    left_on="product_id",
    right_on="product_id"
)

data_top = st.slider('Banyak kategori: ', 1,
                     df_products['product_category_name'].nunique(), 5)

top_product_category = df_products_order_item.groupby(by="product_category_name").order_id.nunique().sort_values(ascending=False).reset_index().head(data_top)


fig, ax = plt.subplots(figsize=(10, 5))

sns.set(style="ticks", context="talk")
plt.style.use("dark_background")

sns.barplot(
    y="product_category_name",
    x="order_id",
    data=top_product_category, palette="pastel",
)
ax.set_ylabel(None)
ax.set_xlabel("Number of Orders", fontsize=30)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)
