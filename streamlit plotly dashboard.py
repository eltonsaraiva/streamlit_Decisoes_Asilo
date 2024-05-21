import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    layout='wide'
)

file_path = 'asylum-decisions.csv'
df = pd.read_csv(file_path)

years = sorted(df['Year'].unique())
countries = sorted(set(df['Country of origin']).union(set(df['Country of asylum'])))

# Streamlit interface
st.subheader("Dashboard - Decisões de Asilo")

# Year/country seleção com slider e dropdown
selected_year = st.slider("Selecione o ano", min_value=int(years[0]), max_value=int(years[-1]), step=1, key="year_slider")
selected_country = st.selectbox("Selecione o País", countries, key="country_select")

# Filtro do dataset com base no Year e Country selecionados
filtered_df_origin = df[(df['Year'] == selected_year) & (df['Country of origin'] == selected_country)]
filtered_df_asylum = df[(df['Year'] == selected_year) & (df['Country of asylum'] == selected_country)]

# Dados para Countries de origen incluindo '0 values' para o mapa ser preenchido
origin_data = filtered_df_asylum.groupby('Country of origin')['Recognized decisions'].sum().reset_index()
all_countries_origin = pd.DataFrame(countries, columns=['Country of origin'])
origin_data = all_countries_origin.merge(origin_data, on='Country of origin', how='left').fillna(0)

# Dados para Countries de asilo incluindo '0 values'
asylum_data = filtered_df_origin.groupby('Country of asylum')['Recognized decisions'].sum().reset_index()
all_countries_asylum = pd.DataFrame(countries, columns=['Country of asylum'])
asylum_data = all_countries_asylum.merge(asylum_data, on='Country of asylum', how='left').fillna(0)


# Create the maps
fig_origin = px.choropleth(origin_data, locations="Country of origin", locationmode="country names",
                           color="Recognized decisions", hover_name="Country of origin",
                           projection="natural earth", color_continuous_scale="YlOrRd",
                           title="País de Origem", template="plotly_dark")

fig_asylum = px.choropleth(asylum_data, locations="Country of asylum", locationmode="country names",
                           color="Recognized decisions", hover_name="Country of asylum",
                           projection="natural earth", color_continuous_scale="YlOrRd",
                           title="Países de Asilo", template='plotly_dark', )


# Crie gráficos de barras para os 10 principais países
top_origin_data = origin_data.nlargest(10, 'Recognized decisions')  # Top 10 Países de Origem
top_asylum_data = asylum_data.nlargest(10, 'Recognized decisions')  # Top 10 Países de Asilo

fig_bar_origin = px.bar(top_origin_data, x='Recognized decisions', y='Country of origin',
                        orientation='h', color='Recognized decisions', color_continuous_scale='YlOrRd',
                        title='Top 10 Países de Origem')

fig_bar_asylum = px.bar(top_asylum_data, x='Recognized decisions', y='Country of asylum',
                        orientation='h', color='Recognized decisions', color_continuous_scale='YlOrRd',
                        title='Top 10 Países de Asilo')

# Inverte a ordem das barras
fig_bar_origin.update_layout(yaxis=dict(categoryorder='total ascending'))
fig_bar_asylum.update_layout(yaxis=dict(categoryorder='total ascending'))


# Exibir os mapas e gráficos de barras lado a lado
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_origin, use_container_width=True)
    st.plotly_chart(fig_bar_origin, use_container_width=True)

with col2:
    st.plotly_chart(fig_asylum, use_container_width=True)
    st.plotly_chart(fig_bar_asylum, use_container_width=True)