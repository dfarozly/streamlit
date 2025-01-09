import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import altair as alt

#insert file
file_path = "tryout_grades_results.csv"
df = pd.read_csv(file_path)

#layout
st.set_page_config(
    page_title="TO SNBT AY 2024/2025",
    page_icon=":coffee:",
    layout="wide",
    initial_sidebar_state="expanded"
)
alt.themes.enable("dark")

#logo
st.sidebar.image("logo_smartstudent1.png", use_container_width=True)

#judul
st.sidebar.title("TO SNBT AY 2024/2025")

#sidebar filter
filter_column = st.sidebar.selectbox("Pilih kolom", df.columns)

#apply filter
if pd.api.types.is_numeric_dtype(df[filter_column]):
    # Numeric filter
    min_val, max_val = st.sidebar.slider(
        f"Select range for {filter_column}",
        float(df[filter_column].min()),
        float(df[filter_column].max()),
        (float(df[filter_column].min()), float(df[filter_column].max()))
    )

elif pd.api.types.is_object_dtype(df[filter_column]) or pd.api.types.is_categorical_dtype(df[filter_column]):
    # Categorical filter
    unique_values = df[filter_column].unique()
    selected_values = st.sidebar.selectbox(f"Pilih {filter_column}", unique_values)

filtered_data = df.loc[:,["Tryout Name" , "PNU" , "PBM" , "PPU" , "PKT" , "LBI" , "LBE" , "PNM" , "Skor Rata-Rata"]][df[filter_column] == selected_values]

#create donut
filtered_data_mean = round(filtered_data.loc[:,["PNU" , "PBM" , "PPU" , "PKT" , "LBI" , "LBE" , "PNM" , "Skor Rata-Rata"]].mean())
colors = ["#008000", "#00FFFF", "#d35400", "#0000FF", "#3498db", "#FF00FF", "#CCCCFF"]

def make_donut(filtered_data_mean):
    source = pd.DataFrame({
        "category": ["A", "B"],
        "value": [1000-filtered_data_mean, filtered_data_mean]
    })

    donut_chart = alt.Chart(source).mark_arc(innerRadius=40, outerRadius=60).encode(
        theta=alt.Theta(field="value", type="quantitative", stack=True),  
        color=alt.Color(field="category", type="nominal",scale=alt.Scale(domain= ["A", "B"], range= ['#f2f4f4','#E74C3C']) , legend=None)
    ).properties(width=130, height=200)

    text = donut_chart.mark_text(align='center', font="Lato", fontSize=20, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{filtered_data_mean}'))
    
    return donut_chart + text

def make_donut2(filtered_data_mean, input_text, input_color):
    if input_color == "PNU":
        chart_color = ['#008000', '#f2f4f4']
    if input_color == "PBM":
        chart_color = ['#00FFFF', '#f2f4f4']
    if input_color == "PPU":
        chart_color = ['#d35400', '#f2f4f4']
    if input_color == "PKT":
        chart_color = ['#0000FF', '#f2f4f4']
    if input_color == "LBI":
        chart_color = ['#3498db', '#f2f4f4']
    if input_color == "LBE":
        chart_color = ['#FF00FF', '#f2f4f4']
    if input_color == "PNM":
        chart_color = ['#CCCCFF', '#f2f4f4']

    source = pd.DataFrame({
        "category": ["", input_text],
        "value": [1000-filtered_data_mean, filtered_data_mean]
    })

    donut_chart2 = alt.Chart(source).mark_arc(innerRadius=20, outerRadius=30).encode(
        theta=alt.Theta(field="value", type="quantitative", stack=True), 
        color=alt.Color(field="category", type="nominal", scale=alt.Scale(domain=[input_text, ""], range=chart_color), legend=None)
    ).properties(width=60, height=120)

    text = donut_chart2.mark_text(align='center', font="Lato", fontSize=15, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{filtered_data_mean}'))
    
    return donut_chart2 + text

#tampilkan filter di container 1
with st.container():
    col1, col2, col3 = st.columns((1.5, 4.5, 2), border=True)
    with col1:
        st.altair_chart(make_donut(filtered_data_mean["Skor Rata-Rata"]))
#tampilkan grafik nilai rata-rata
    with col2:
        st.subheader("Nilai Rata-Rata")
        st.bar_chart(filtered_data.loc[:,["Skor Rata-Rata"]], stack=False, height=200, color='#E74C3C')
#tampilkan tabel nilai rata-rata
    with col3:
        st.dataframe(filtered_data.loc[:,["Tryout Name" , "Skor Rata-Rata"]],
        height=250,
        column_order=("Tryout Name" , "Skor Rata-Rata"),
        hide_index="True",
        column_config={
            "Tryout Name":st.column_config.TextColumn("Tryout Name"),
            "Skor Rata-Rata":st.column_config.ProgressColumn("Skor Rata-Rata", format="%f", min_value=0, max_value=1000)},
        )

#tampilkan grafik nilai per subtes di container 2
with st.container(border=True):
    col4, col5 = st.columns((3, 5), border=False)
    with col4:
        with st.container(border=False):
            col = st.columns((0.75, 0.75, 0.75, 0.75))
            with col[0]: 
                st.altair_chart(make_donut2(filtered_data_mean["PNU"], "PNU", "PNU"))
            with col[1]: 
                st.altair_chart(make_donut2(filtered_data_mean["PKT"], "PKT", "PKT"))
            with col[2]: 
                st.altair_chart(make_donut2(filtered_data_mean["PBM"], "PBM", "PBM"))
            with col[3]: 
                st.altair_chart(make_donut2(filtered_data_mean["PPU"], "PPU", "PPU"))
        with st.container(border=False):
            col = st.columns((1, 1, 1))
            with col[0]: 
                st.altair_chart(make_donut2(filtered_data_mean["LBI"], "LBI", "LBI"))
            with col[1]: 
                st.altair_chart(make_donut2(filtered_data_mean["LBE"], "LBE", "LBE"))
            with col[2]: 
                st.altair_chart(make_donut2(filtered_data_mean["PNM"], "PNM", "PNM"))
    with col5:
        st.subheader("Nilai Subtes")
        st.bar_chart(filtered_data.loc[:,["PNU" , "PBM" , "PPU" , "PKT" , "LBI" , "LBE" , "PNM"]], color=colors, stack=False, height=250)
