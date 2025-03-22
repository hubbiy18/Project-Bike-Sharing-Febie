import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi tampilan Streamlit
st.set_page_config(page_title="Dashboard Bike Sharing", layout="wide")

# Load dataset
df_day = pd.read_csv("processed_bike_data.csv")


df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_day['month'] = df_day['dteday'].dt.month
df_day['day_type'] = df_day['weekday'].apply(lambda x: 'Weekend' if x in [0, 6] else 'Weekday')

# Sidebar untuk navigasi
st.sidebar.title("Silahkan Pilih Analisis")
page = st.sidebar.radio("Navigasi", ["Tren Bulanan", "Hari Kerja vs Akhir Pekan"])

# Fitur interaktif: Pilih bulan tertentu
selected_month = st.sidebar.selectbox("Pilih Bulan", ["Semua"] + list(range(1, 13)))

# Visualisasi Tren Peminjaman Bulanan
if page == "Tren Bulanan":
    st.title("Tren Peminjaman Sepeda per Bulan")

    # Agregasi data bulanan
    monthly_data = df_day.groupby('month')[['cnt', 'casual', 'registered']].sum().reset_index()

    # Filter data berdasarkan pilihan bulan
    if selected_month != "Semua":
        monthly_data = monthly_data[monthly_data['month'] == selected_month]

    # Plot line chart tren penggunaan sepeda berdasarkan bulan
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='month', y='cnt', data=monthly_data, label='Total Peminjaman', marker='o', color='blue', ax=ax)
    sns.lineplot(x='month', y='registered', data=monthly_data, label='Registered Users', marker='o', color='green', ax=ax)
    sns.lineplot(x='month', y='casual', data=monthly_data, label='Casual Users', marker='o', color='orange', ax=ax)

    # Atur tampilan
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Peminjaman")
    ax.set_title("Tren Penggunaan Sepeda Berdasarkan Bulan")
    ax.legend()
    ax.grid(True)

    # Tampilkan plot di Streamlit
    st.pyplot(fig)

    # Insight
    st.markdown("""
    **Insight:**
    - Peminjaman sepeda meningkat dari awal tahun hingga puncaknya pada bulan Mei-September (musim panas).  
    - Pengguna terdaftar mendominasi peminjaman sepanjang tahun.  
    - Peminjaman menurun drastis di akhir tahun (November-Desember) akibat musim dingin.  
    """)

# Visualisasi Perbedaan Hari Kerja vs Akhir Pekan
elif page == "Hari Kerja vs Akhir Pekan":
    st.title("Peminjaman Sepeda: Hari Kerja vs Akhir Pekan")

    # Agregasi data berdasarkan tipe hari
    df_grouped = df_day.groupby("day_type")[["casual", "registered", "cnt"]].sum().reset_index()

    # Visualisasi Bar Chart
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="day_type", y="cnt", hue="day_type", data=df_grouped, palette={"Weekday": "blue", "Weekend": "orange"}, ax=ax)

    # Tambahkan label
    ax.set_xlabel("Tipe Hari")
    ax.set_ylabel("Total Peminjaman")
    ax.set_title("Perbandingan Peminjaman Sepeda: Hari Kerja vs Akhir Pekan")
    ax.legend().set_title("Tipe Hari")

    # Menampilkan angka di atas batang
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height()):,}",
                    (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha="center", va="bottom", fontsize=12, fontweight="bold", color="black")

    # Tampilkan plot di Streamlit
    st.pyplot(fig)

    # Insight
    st.markdown("""
    **Insight:**
    - Peminjaman lebih tinggi pada **hari kerja** dibanding akhir pekan.  
    - Hal ini menunjukkan bahwa sepeda lebih sering digunakan untuk **keperluan komuter** (perjalanan ke kantor/sekolah) daripada rekreasi.  
    """)

# Footer
st.sidebar.info("Dashboard ini dibuat untuk menampilkan hasil analisis dataset Bike Sharing. Project By Febie Elfaladonna")

