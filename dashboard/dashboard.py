import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set title in the navbar
st.set_page_config(page_title="Analisis Udara", layout="wide")

# Navbar with title
st.markdown("<h1 style='text-align: center;'>Analisis Udara</h1>", unsafe_allow_html=True)

# Sidebar with menu
st.sidebar.title("Filter Tanggal")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime('2013-03-01').date())
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime('2017-03-01').date())

# Convert to pandas datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Load data
data = pd.read_csv('data_bersih.csv')

# Convert month names to numeric values if needed
month_mapping = {
    'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4, 'Mei': 5,
    'Juni': 6, 'Juli': 7, 'Agustus': 8, 'September': 9, 'Oktober': 10,
    'November': 11, 'Desember': 12
}
if data['month'].dtype == 'object':  # Check if month column is not numeric
    data['month'] = data['month'].map(month_mapping)

# Create a new datetime column
data['date'] = pd.to_datetime(data[['year', 'month', 'day']])

# Filter data based on date range
filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

# Filter data where Kualitas_Udara == 1
data_baik = filtered_data[filtered_data['Kualitas_Udara'] == 1]

# Define the ordered list of months
ordered_months = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 
                  'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

# Add month names to the data_baik DataFrame
data_baik['month_name'] = pd.Categorical(data_baik['date'].dt.month_name(locale='id_ID'), 
                                         categories=ordered_months, 
                                         ordered=True)

# Count the number of observations per month, ensuring all months are included
monthly_counts = data_baik['month_name'].value_counts().reindex(ordered_months, fill_value=0)

# Plot the line chart based on months

data_baik = data[data['Kualitas_Udara'] == 1]
temperatur_counts = data_baik['TEMP_Category'].value_counts()

plt.figure(figsize=(10, 6))
temperatur_counts.plot(kind='bar', color='skyblue')
plt.title('Jumlah Observasi untuk Setiap Kategori Temperatur dengan Kualitas Data Baik')
plt.xlabel('Kategori Temperatur')
plt.ylabel('Jumlah Observasi')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Display the plot in Streamlit
st.pyplot(plt)





plt.figure(figsize=(12, 6))
plt.plot(monthly_counts.index, monthly_counts.values, marker='o', color='skyblue', linestyle='-')
plt.title('Jumlah Observasi per Bulan dengan Kualitas Data Baik')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Observasi')
plt.grid(True, linestyle='--', alpha=0.7)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Display the plot in Streamlit
st.pyplot(plt)


corr_matrix = data.corr(numeric_only=True)

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix[['Kualitas_Udara']], annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1)
plt.title('Heatmap Korelasi Kualitas Udara dengan Variabel Lainnya')
st.pyplot(plt)