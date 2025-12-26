from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import pandas as pd
import json
import plotly
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime
from i18n_english import TEXTS, get_text

app = Flask(__name__)
app.secret_key = 'cmd-ba-cnc-secret-key-2025'

# Study data structure (English only)
STUDIES_DATA = {
    'HRS': {
        'name': 'Health and Retirement Study',
        'country': 'United States',
        'years': '1992-ongoing',
        'biomarker_years': '2006, 2008, 2010, 2012, 2014, 2016',
        'biomarkers': ['HbA1c', 'CRP', 'Total Cholesterol', 'HDL', 'SBP/DBP', 'BMI'],
        'sample_size': '~20,000',
        'access_status': 'Obtained',
        'cmd_ba_status': 'Complete 6-biomarker model',
        'description': 'US longitudinal study of adults aged 50+ since 1992. DBS biomarker collection with alternating half-sample design. 2016 was final DBS wave with venous blood beginning.'
    },
    'ELSA': {
        'name': 'English Longitudinal Study of Ageing',
        'country': 'England',
        'years': '2002-ongoing',
        'biomarker_years': '2004, 2008, 2012, 2016, 2018',
        'biomarkers': ['HbA1c', 'CRP', 'Total Cholesterol', 'HDL', 'SBP/DBP', 'BMI'],
        'sample_size': '~11,000',
        'access_status': 'Obtained',
        'cmd_ba_status': 'Complete 6-biomarker model',
        'description': 'England longitudinal study of adults aged 50+ since 2002. Nurse visits collect blood biomarkers and physical measures.'
    },
    'SHARE': {
        'name': 'Survey of Health, Ageing and Retirement in Europe',
        'country': '12 European countries',
        'years': '2004-ongoing',
        'biomarker_years': 'DBS 2015 only',
        'biomarkers': ['HbA1c', 'CRP', 'Total Cholesterol', 'HDL', 'BMI (self-reported)'],
        'sample_size': '~27,200 DBS samples',
        'access_status': 'Obtained',
        'cmd_ba_status': 'Partial 4-biomarker model (missing measured BP)',
        'major_limitation': 'Missing measured blood pressure data',
        'description': 'Multi-country European study. Wave 6 (2015) collected DBS samples, but blood pressure measurements were NOT included in protocol.'
    },
    'CHARLS': {
        'name': 'China Health and Retirement Longitudinal Study',
        'country': 'China',
        'years': '2011-ongoing',
        'biomarker_years': '2011, 2015',
        'biomarkers': ['HbA1c', 'CRP', 'Total Cholesterol', 'HDL', 'SBP/DBP', 'BMI'],
        'sample_size': '~21,000',
        'access_status': 'Obtained',
        'cmd_ba_status': 'Complete 6-biomarker model',
        'description': 'China national study of adults aged 45+ since 2011. Blood biomarkers collected in waves 1(2011) and 3(2015).'
    },
    'LASI-DAD': {
        'name': 'Longitudinal Aging Study in India',
        'country': 'India',
        'years': '2017-ongoing',
        'biomarker_years': '2017-2019, 2022-2024',
        'biomarkers': ['HbA1c', 'CRP', 'Total Cholesterol', 'HDL', 'SBP/DBP', 'BMI'],
        'sample_size': '~6,000',
        'access_status': 'Obtained',
        'cmd_ba_status': 'Complete 6-biomarker model',
        'description': 'India national dementia study of adults aged 60+ since 2017. Venous blood collection across 18 states and 4 metropolitan cities.'
    },
    'MHAS': {
        'name': 'Mexican Health and Aging Study',
        'country': 'Mexico',
        'years': '2001-ongoing',
        'biomarker_years': '2012, 2016',
        'biomarkers': ['HbA1c', 'CRP', 'Total Cholesterol', 'HDL', 'SBP/DBP', 'BMI'],
        'sample_size': '~4,000',
        'access_status': 'Obtained',
        'cmd_ba_status': 'Complete 6-biomarker model',
        'description': 'Mexico national panel study of adults aged 50+ since 2001, harmonized with HRS.'
    },
    'HAALSI': {
        'name': 'Health and Aging in Africa',
        'country': 'South Africa',
        'years': '2014-ongoing',
        'biomarker_years': 'CRP: Wave 1 only; Cholesterol: Waves 1&3',
        'biomarkers': ['Glucose (not HbA1c)', 'CRP (Wave 1 only)', 'Total Cholesterol', 'HDL', 'SBP/DBP', 'BMI'],
        'sample_size': '~5,100',
        'access_status': 'Obtained',
        'cmd_ba_status': 'Partial 5-biomarker model (missing HbA1c)',
        'hba1c_limitation': 'NO HbA1c - capillary glucose only',
        'description': 'South Africa rural community study. Point-of-care biomarkers: NO HbA1c (capillary glucose only), CRP Wave 1 only.'
    },
    'IFLS': {
        'name': 'Indonesian Family Life Survey',
        'country': 'Indonesia',
        'years': '1993-ongoing',
        'biomarker_years': 'HbA1c: Wave 5 (2014-15); CRP: Waves 4&5',
        'biomarkers': ['HbA1c (Wave 5 only)', 'CRP (Waves 4&5)'],
        'sample_size': '~50,000',
        'access_status': 'Partial obtained',
        'cmd_ba_status': 'Severely limited 2-biomarker model',
        'severe_limitation': 'NO cholesterol, blood pressure, or BMI data obtained',
        'description': 'Indonesian national survey. Limited to DBS biomarkers only - only 2 out of 6 core indicators available.'
    },
    'TILDA': {
        'name': 'The Irish Longitudinal Study on Ageing',
        'country': 'Ireland',
        'years': 'TBD',
        'biomarker_years': 'TBD',
        'biomarkers': ['TBD'],
        'sample_size': 'TBD',
        'access_status': 'To obtain',
        'cmd_ba_status': 'TBD',
        'description': 'Irish longitudinal study - data access application pending'
    },
    'NICOLA': {
        'name': 'Northern Ireland Cohort for Longitudinal Study of Ageing',
        'country': 'Northern Ireland',
        'years': 'TBD',
        'biomarker_years': 'TBD',
        'biomarkers': ['TBD'],
        'sample_size': 'TBD',
        'access_status': 'To obtain',
        'cmd_ba_status': 'TBD',
        'description': 'Northern Ireland aging study - data access application pending'
    },
    'SLHAS': {
        'name': 'Sri Lanka Health and Ageing Study',
        'country': 'Sri Lanka',
        'years': 'TBD',
        'biomarker_years': 'TBD',
        'biomarkers': ['TBD'],
        'sample_size': 'TBD',
        'access_status': 'To obtain',
        'cmd_ba_status': 'TBD',
        'description': 'Sri Lanka health and aging study - data access application pending'
    }
}

# Routes
@app.before_request
def before_request():
    # Set default language to English
    if 'language' not in session:
        session['language'] = 'en'

@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html', get_text=get_text, studies=STUDIES_DATA)

@app.route('/datasets')
def datasets():
    """Dataset details page"""
    return render_template('datasets.html', get_text=get_text)

@app.route('/studies')
def studies():
    """Studies page"""
    return render_template('studies.html', 
                         studies=STUDIES_DATA,
                         current_language='en',
                         get_text=get_text)

@app.route('/biomarkers')
def biomarkers():
    """Biomarkers page"""
    return render_template('biomarkers.html', get_text=get_text)

@app.route('/visualization')
def visualization():
    """Data visualization page"""
    return render_template('visualization.html', get_text=get_text)

# API Routes
@app.route('/api/studies_data')
def api_studies_data():
    """API endpoint - Studies data"""
    return jsonify(STUDIES_DATA)

@app.route('/api/coverage_chart')
def api_coverage_chart():
    """API endpoint - Generate coverage chart"""
    complete_6 = []
    partial = []
    limited = []
    pending = []
    
    for study, data in STUDIES_DATA.items():
        status = data.get('cmd_ba_status', '').lower()
        if 'complete' in status:
            complete_6.append(study)
        elif 'partial' in status:
            partial.append(study)
        elif 'limited' in status:
            limited.append(study)
        else:
            pending.append(study)
    
    fig = go.Figure(data=[
        go.Bar(name='Complete 6-biomarker', x=['Complete'], y=[len(complete_6)], 
               marker_color='#28a745', text=[len(complete_6)], textposition='auto'),
        go.Bar(name='Partial coverage', x=['Partial'], y=[len(partial)], 
               marker_color='#ffc107', text=[len(partial)], textposition='auto'),
        go.Bar(name='Limited coverage', x=['Limited'], y=[len(limited)], 
               marker_color='#dc3545', text=[len(limited)], textposition='auto'),
        go.Bar(name='Pending access', x=['Pending'], y=[len(pending)], 
               marker_color='#6c757d', text=[len(pending)], textposition='auto')
    ])
    
    fig.update_layout(
        title='CMD-BA-CNC Study Biomarker Coverage',
        xaxis_title='Coverage Type',
        yaxis_title='Number of Studies',
        showlegend=True,
        height=400
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/api/geographic_distribution')
def api_geographic_distribution():
    """API endpoint - Geographic distribution chart"""
    regions = {}
    for study, data in STUDIES_DATA.items():
        country = data.get('country', 'Unknown')
        
        if 'United States' in country:
            region = 'North America'
        elif 'England' in country or 'Ireland' in country or 'European' in country:
            region = 'Europe'
        elif 'China' in country:
            region = 'East Asia'
        elif 'India' in country:
            region = 'South Asia'
        elif 'Mexico' in country:
            region = 'Latin America'
        elif 'South Africa' in country:
            region = 'Africa'
        elif 'Indonesia' in country:
            region = 'Southeast Asia'
        elif 'Sri Lanka' in country:
            region = 'South Asia'
        else:
            region = 'Other'
        
        if region not in regions:
            regions[region] = []
        regions[region].append(study)
    
    fig = go.Figure(data=[
        go.Pie(labels=list(regions.keys()), 
               values=[len(studies) for studies in regions.values()],
               hole=0.3,
               textinfo='label+percent+value')
    ])
    
    fig.update_layout(
        title='Geographic Distribution of Participating Studies',
        height=400
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/api/sample_size_chart')
def api_sample_size_chart():
    """API endpoint - Sample size comparison chart"""
    studies = []
    sample_sizes = []
    colors = []
    
    for study, data in STUDIES_DATA.items():
        if data.get('sample_size', 'TBD') != 'TBD':
            studies.append(study)
            # Extract numeric value from sample size string
            size_str = str(data['sample_size'])
            size_num = 0
            if '~' in size_str:
                size_str = size_str.replace('~', '').replace(',', '')
                try:
                    size_num = int(size_str.split()[0])
                except:
                    size_num = 0
            sample_sizes.append(size_num)
            
            # Color based on CMD-BA status
            status = data.get('cmd_ba_status', '').lower()
            if 'complete' in status:
                colors.append('#28a745')
            elif 'partial' in status:
                colors.append('#ffc107')
            elif 'limited' in status:
                colors.append('#dc3545')
            else:
                colors.append('#6c757d')
    
    fig = go.Figure(data=[
        go.Bar(x=studies, y=sample_sizes, marker_color=colors,
               text=[f'{size:,}' if size > 0 else 'N/A' for size in sample_sizes], 
               textposition='auto')
    ])
    
    fig.update_layout(
        title='Sample Size Comparison Across Studies',
        xaxis_title='Study',
        yaxis_title='Sample Size',
        xaxis_tickangle=45,
        height=400
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/api/timeline_chart')
def api_timeline_chart():
    """API endpoint - Data collection timeline chart"""
    studies = []
    start_years = []
    end_years = []
    colors = []
    
    for study, data in STUDIES_DATA.items():
        years_str = data.get('years', '')
        if years_str and years_str != 'TBD':
            try:
                if '-ongoing' in years_str:
                    start_year = int(years_str.split('-')[0])
                    end_year = 2024  # Current year
                elif '-' in years_str:
                    parts = years_str.split('-')
                    start_year = int(parts[0])
                    end_year = int(parts[1]) if parts[1].isdigit() else 2024
                else:
                    start_year = int(years_str)
                    end_year = start_year
                
                studies.append(study)
                start_years.append(start_year)
                end_years.append(end_year)
                
                # Color based on CMD-BA status
                status = data.get('cmd_ba_status', '').lower()
                if 'complete' in status:
                    colors.append('#28a745')
                elif 'partial' in status:
                    colors.append('#ffc107')
                elif 'limited' in status:
                    colors.append('#dc3545')
                else:
                    colors.append('#6c757d')
            except:
                continue
    
    fig = go.Figure()
    
    for i, study in enumerate(studies):
        fig.add_trace(go.Scatter(
            x=[start_years[i], end_years[i]],
            y=[study, study],
            mode='lines+markers',
            line=dict(color=colors[i], width=6),
            marker=dict(size=8),
            name=study,
            showlegend=False
        ))
    
    fig.update_layout(
        title='Data Collection Timeline Across Studies',
        xaxis_title='Year',
        yaxis_title='Study',
        height=400,
        xaxis=dict(range=[1990, 2025])
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
