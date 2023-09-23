import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

st.set_page_config(layout='wide')

st.title(':blue[Chicago Crime] Database :cop:')
st.caption('streamlit experiments')
st.divider()
progress_text = "Operation in progress. Please wait."
my_bar = st.progress(40, text=progress_text)



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
    df_calculate = df_supports.groupby(['Question','Departmant', 'S Month'], as_index= False).size()
    df_calculate['Supporters'] = df_calculate['size']

    df_notr= df[(df['Answer'] >6) & (df['Answer'] <9)] #find notr
    df_notr = df_notr.groupby(['Question','Departmant', 'S Month'], as_index= False).size()
    df_calculate['Notur'] = df_notr['size']

    df_detractors =df[df['Answer'] < 7] #find detractors
    df_detractors = df_detractors.groupby(['Question','Departmant', 'S Month'], as_index= False).size()
    df_calculate['Detractors'] = df_detractors ['size']

    df_total_count = df.groupby(['Question','Departmant', 'S Month'], as_index = False).size() #sum partisipated employee of survey 
    df_calculate['SUM'] = df_total_count['size']

    suports_yuzdesi = df_calculate['Supporters'] / (df_calculate['SUM'] / 100)
    df_calculate['Supporters %'] = round(suports_yuzdesi,2)

    notr_yuzdesi = df_calculate['Notur'] / (df_calculate['SUM'] / 100)
    df_calculate['Notur %'] = round(notr_yuzdesi, 2)

    detractors_yuzdesi = df_calculate['Detractors'] / (df_calculate['SUM'] / 100)
    df_calculate['Detractors %'] = round(detractors_yuzdesi,2)
    df_calculate.sort_values (by='Departmant')

    return df_calculate


def calculate_data3 (df):
    df_supports = df[df['Answer'] > 8] #fin
    #df_supports = df_supports.groupby(['Departmant','Question']).size().unstack(fill_value=0).stack()
    #df_supports = df_supports.groupby([pd.Categorical(df_supports.Departmant), 'Question']).size().fillna(0)
    df_supports = df_supports.groupby(['Question', 'Departmant']).Answer.count().reindex(df_supports['Departmant'].unique()).fillna(0).astype(int).rename('a_count').reset_index()
    st.data_editor(df_supports)





def analysis_data (df):
    df_analysis = df.groupby(by=['Question','Departmant'])[['Answer']].sum()
    return df_analysis  


df = survey_data_load() #first data load 
df = create_sidebar (df) # creating sidebar objects and data
#df = analysis_data (df)
df_calc = calculate_data2(df)
#calculate_data3(df)


#my_bar = st.progress(supporter_count, text=progress_text)

     
df_calc = df_calc.sort_values(['Departmant'], ascending=True)
st.data_editor(df_calc) 

investment_by_business_type= df_calc

fig_investment=px.bar(
    investment_by_business_type,
    x="Detractors %",
    y="Question",
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
left.plotly_chart(fig_investment,use_container_width=True)







with st.container():
   #st.plotly_chart(fig_investment,use_container_width=True)
   st.write("This is inside the container")
