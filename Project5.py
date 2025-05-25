import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Title of the Dashboard
st.title("Data Analysis Dashboard for Sales Data")

# Load Dataset
st.header("Dataset Overview")
df = pd.read_csv(r"C:\Users\KIIT0001\Downloads\archive\SalesForCourse_quizz_table.csv")
st.write("First few rows of the dataset:")
st.dataframe(df)

# Data Description
st.subheader("Basic Statistics")
st.write(df.describe())

# Checking null values
st.subheader("Missing Values Count")
st.write(df.isnull().sum())

# Cleaning Data
st.subheader("Data Cleaning")
df.drop(['Column1', 'Year', 'Month'], axis=1, inplace=True)
st.write("After dropping irrelevant columns:")
st.dataframe(df.head())

# Convert object type columns to datetime
for col in df.columns:
    if df[col].dtype == 'object':
        try:
            df[col] = pd.to_datetime(df[col])
        except:
            pass  # Ignore if conversion fails

# Correlation Matrix Visualization
st.subheader("Correlation Heatmap")
numeric_df = df.select_dtypes(include=['number'])
correlation_matrix = numeric_df.corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
ax.set_title("Correlation Heatmap")
st.pyplot(fig)

# Removing highly correlated columns
df.drop(['Unit Price', 'Revenue'], axis=1, inplace=True)

# Boolean Encoding
df = pd.get_dummies(df, columns=['Customer Gender'], drop_first=True)

# Visualizing Gender Distribution
st.subheader("Customer Gender Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(x='Customer Gender_M', data=df, palette=['Pink', 'skyblue'], ax=ax)
ax.set_title("Distribution of Customer Gender")
st.pyplot(fig)

# Pie Charts for Product Category per Country
st.subheader("Category Distribution per Country")
grouped = df.groupby(['Country', 'Product Category']).size().reset_index(name='Count')

selected_country = st.selectbox("Select a Country:", grouped['Country'].unique())
country_data = grouped[grouped['Country'] == selected_country]

fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(country_data['Count'], labels=country_data['Product Category'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
ax.set_title(f'Category Distribution in {selected_country}')
st.pyplot(fig)

# Customer Age Distribution
st.subheader("Customer Age Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df['Customer Age'], bins=30, kde=True, color='skyblue', ax=ax)
ax.set_title("Distribution of Customer Age")
st.pyplot(fig)

# Customer Gender & Popularity of Sub Categories
st.subheader("Popularity of Sub Categories Across Customer Genders")
grouped = df.groupby(['Customer Gender_M', 'Sub Category']).size().reset_index(name='Count')
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='Customer Gender_M', y='Count', hue='Sub Category', data=grouped, palette='tab10', ax=ax)
ax.set_title("Popularity of Sub Categories Across Customer Genders")
st.pyplot(fig)

# Total Quantity Sold Per Country
st.subheader("Total Quantity Sold in Each Country")
country_quantity = df.groupby('Country')['Quantity'].sum().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='Country', y='Quantity', data=country_quantity, palette='tab10', ax=ax)
ax.set_title("Total Quantity Sold in Each Country Comparison")
st.pyplot(fig)

# Trends Over Time
st.subheader("Quantity Trends Over Time")
df['Date'] = pd.to_datetime(df['Date'])
date_quantity = df.groupby('Date')['Quantity'].sum().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='Date', y='Quantity', data=date_quantity, linestyle='solid', color='skyblue', ax=ax)
ax.set_title("Quantity Trends Over Time")
st.pyplot(fig)

st.write("Dashboard Successfully Loaded 🚀")
