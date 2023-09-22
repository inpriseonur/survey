import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


def survey_data_load():
    df = pd.read_csv('Survey.csv')
    df.columns = ['Survey ID', 'Survey Date', 'Survey Name', 'Question', 'Answer', 'Departmant', 'Job Title', 'Team', 'Start Date', 'Is Manager']
    df['Survey Date'] = pd.to_datetime(df['Survey Date'],format='%d.%m.%Y')
    df['Start Date'] = pd.to_datetime(df['Start Date'],format='%d.%m.%Y')
    df['S Year'] = df['Survey Date'].dt.year
    df['S Month'] = df['Survey Date'].dt.strftime('%B') #surver month converting month name
    df['E Year'] = df['Start Date'].dt.year
    df['E Month'] = df['Start Date'].dt.month
    return df

def create_sidebar(df):
    sb_survey_year = st.sidebar.selectbox('Select Survey Year', df['S Year'].unique().tolist())
    df = df[df['S Year'] == sb_survey_year] #Filtiring selected year all data.
    sb_survey = st.sidebar.selectbox('Select a Survey', df['Survey Name'].unique().tolist()) 
    df = df[df['Survey Name'] == sb_survey]
    sb_month = st.sidebar.multiselect('Select A Mount', df['S Month'].unique(), df['S Month'].unique().tolist())
    df = df[df['S Month'].isin(sb_month)]
    return df

def calculate_data (df):
    df_supports =df[df['Answer'] > 8] #find supports
    df_calculate = df_supports.groupby(by=['Question','Departmant']).count()[['Answer']]
    df_calculate['Supporters'] = df_calculate['Answer']

    df_notr= df[(df['Answer'] >6) & (df['Answer'] <9)] #find notr
    df_notr = df_notr.groupby(by=['Question','Departmant']).count()[['Answer']] 
    df_calculate['Notur'] = df_notr['Answer']

    df_detractors =df[df['Answer'] < 7] #find detractors
    df_detractors = df_detractors.groupby(by=['Question','Departmant']).count()[['Answer']]
    df_calculate['Detractors'] = df_detractors ['Answer']

    df_total_count = df.groupby(by=['Question','Departmant']).count()[['Answer']] #sum partisipated employee of survey 
    df_calculate['SUM'] = df_total_count['Answer']

    suports_yuzdesi = df_calculate['Supporters'] / (df_calculate['SUM'] / 100)
    df_calculate['Supporters %'] = round(suports_yuzdesi,2)

    notr_yuzdesi = df_calculate['Notur'] / (df_calculate['SUM'] / 100)
    df_calculate['Notur %'] = round(notr_yuzdesi, 2)

    detractors_yuzdesi = df_calculate['Detractors'] / (df_calculate['SUM'] / 100)
    df_calculate['Detractors %'] = round(detractors_yuzdesi,2)

    return df_calculate

def calculate_data2 (df):
    df_supports =df[df['Answer'] > 8] #find supports
    df_calculate = df_supports.groupby(['Question','Departmant'], as_index = False).size()
    df_calculate['Supporters'] = df_calculate['size']

    df_notr= df[(df['Answer'] >6) & (df['Answer'] <9)] #find notr
    df_notr = df_notr.groupby(['Question','Departmant'], as_index= False).size() 
    df_calculate['Notur'] = df_notr['size']

    df_detractors =df[df['Answer'] < 7] #find detractors
    df_detractors = df_detractors.groupby(['Question','Departmant'], as_index= False).size()
    df_calculate['Detractors'] = df_detractors ['size']

    df_total_count = df.groupby(['Question','Departmant'], as_index = False).size() #sum partisipated employee of survey 
    df_calculate['SUM'] = df_total_count['size']

    suports_yuzdesi = df_calculate['Supporters'] / (df_calculate['SUM'] / 100)
    df_calculate['Supporters %'] = round(suports_yuzdesi,2)

    notr_yuzdesi = df_calculate['Notur'] / (df_calculate['SUM'] / 100)
    df_calculate['Notur %'] = round(notr_yuzdesi, 2)

    detractors_yuzdesi = df_calculate['Detractors'] / (df_calculate['SUM'] / 100)
    df_calculate['Detractors %'] = round(detractors_yuzdesi,2)

    return df_calculate


def analysis_data (df):
    df_analysis = df.groupby(by=['Question','Departmant'])[['Answer']].sum()
    return df_analysis  


df = survey_data_load() #first data load 
df = create_sidebar (df) # creating sidebar objects and data
#df = analysis_data (df)
df_calc = calculate_data2(df)
st.data_editor(df_calc) 

investment_by_business_type= df_calc
st.write (investment_by_business_type)

fig_investment=px.bar(
    investment_by_business_type,
    x="Detractors %",
    y="Departmant",
    orientation="h",
    title="<b> Investment by Business Type </b>",
    color_discrete_sequence=["#0083B8"]*len(investment_by_business_type),
    template="plotly_white",
)


fig_investment.update_layout(
plot_bgcolor="rgba(0,0,0,0)",
xaxis=(dict(showgrid=False))
    )

left,right,center=st.columns(3)
right.plotly_chart(fig_investment,use_container_width=True)
