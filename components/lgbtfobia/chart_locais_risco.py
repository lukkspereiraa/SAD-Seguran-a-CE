import streamlit as st
import plotly.express as px

def render(df):
    if df.empty or 'Local' not in df.columns or 'Natureza' not in df.columns: return
    
    st.markdown("#### :material/location_on: Modus Operandi (Local vs. Tipificação)")
    st.info("Este gráfico de barras empilhadas revela se a Transfobia possui um palco de violência diferente da Homofobia. Isto dita onde o policiamento deve focar a sua atenção.")
    
    df_locais = df.groupby(['Local', 'Natureza']).size().reset_index(name='Casos')
    
    # Encontrar os 10 locais com mais casos globais
    top_locais = df['Local'].value_counts().head(10).index
    df_locais_top = df_locais[df_locais['Local'].isin(top_locais)]
    
    fig_loc = px.bar(
        df_locais_top,
        y='Local',
        x='Casos',
        color='Natureza',
        orientation='h',
        title="Top 10 Locais de Ocorrência por Tipo de Preconceito",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_loc.update_layout(yaxis={'categoryorder':'total ascending'}, barmode='stack', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_loc, use_container_width=True)