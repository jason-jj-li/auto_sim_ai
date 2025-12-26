# Dataset Description for CMD-BA-CNC Project

## Overview

The **CMD-BA-CNC (Cardiometabolic Biological Age – Cross-National Comparative)** project uses **six key cardiometabolic biomarkers** from **HRS-sister studies** to develop a cross-national tool for estimating cardiometabolic biological age and pace of aging.

## Six Core Biomarkers from HRS-Sister Studies

Our project focuses on harmonizing **six biomarkers** that are routinely collected across HRS-family longitudinal aging studies and related international research:

### Blood Biomarkers (4 indicators):
1. **HbA1c** - Glycemic control indicator
2. **C-reactive protein (CRP)** - Inflammatory marker  
3. **Total cholesterol** - Lipid metabolism marker
4. **HDL cholesterol** - Protective lipid marker

### Physical Measures (2 indicators):
5. **Blood pressure** (Systolic and Diastolic) - Cardiovascular health
6. **Body Mass Index (BMI)** - Obesity/body composition indicator

These biomarkers are selected for their:
- Relevance to cardiometabolic health and aging
- Routine availability in large-scale population studies
- Comparability across different countries and populations
- Clinical significance for health assessment

## Data Access Status for HRS-Sister Studies and Related Research

| Study | Country | Blood Biomarkers Years | HbA1c | CRP | Total Chol | HDL Chol | Physical Measures Years | SBP/DBP | BMI | Access Status |
|-------|---------|------------------------|-------|-----|------------|----------|------------------------|---------|-----|---------------|
| **HRS** | US | 2006, 2008, 2010, 2012, 2014, 2016 | ✓ | ✓ | ✓ | ✓ | Waves 8-16 (1998-2022) | ✓ | ✓ | **Obtained** |
| **ELSA** | England | 2004, 2008, 2012, 2016, 2018 | ✓ | ✓ | ✓ | ✓ | 2004, 2008, 2012, 2016, 2018 | ✓ | ✓ | **Obtained** |
| **SHARE** | Europe (12 countries) | **DBS 2015 only** | ✓ | ✓ | ✓ | ✓ | **Self-reported only** | **✗** | ✓ | **Obtained**|
| **CHARLS** | China | 2011, 2015 | ✓ | ✓ | ✓ | ✓ | 2011, 2013, 2015 | ✓ | ✓ | **Obtained** |
| **LASI-DAD** | India | 2017-2019, 2022-2024 | ✓ | ✓ | ✓ | ✓ | 2017-2019, 2022-2024 | ✓ | ✓ | **Obtained** |
| **MHAS** | Mexico | **2012, 2016 (subsample)** | ✓ | ✓ | ✓ | ✓ | 2012, 2016 | ✓ | ✓ | **Obtained** |
| **HAALSI** | South Africa | **CRP: Wave 1 (2014-2015) only**; Other biomarkers: Waves 1&3 | **✗ (Glucose only)** | **Wave 1 only** | ✓ | ✓ | 2014‑2015, 2018, 2021 | ✓ | ✓ | **Obtained** |
| **IFLS** | Indonesia | **HbA1c: Wave 5 (2014-15) only**; CRP: Waves 4&5 | **Wave 5 only** | **Waves 4&5** | **✗** | **✗** | **✗** | **✗** | **✗** | **Partial obtained** |
| **TILDA** | Ireland | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | **To obtain** |
| **NICOLA** | Northern Ireland | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | **To obtain** |
| **SLHAS** | Sri Lanka | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | **To obtain** |

**Notes:**
- **Blood biomarkers** (HbA1c, CRP, Total Cholesterol, HDL) are collected less frequently and require special collection protocols
- **HRS Protocol**: DBS biomarkers collected on alternating half-samples (2006/2010/2014 vs 2008/2012/2016); 2016 final DBS wave with VBS collection beginning same year; physical measures (SBP/DBP/BMI) available waves 8-16 (1998-2022); NHANES-equivalent values provided for standardization
- **ELSA Protocol**: Nurse visits in waves 2, 4, 6, 8, 9; waves 8/9 use split-sample design and are combined in harmonized data; blood pressure measured using Omron machines with 3 measurements per visit
- **CHARLS Protocol**: Blood biomarkers (including CRP) collected only in waves 1 (2011) and 3 (2015); Wave 2 (2013) interview-only with no biomarker collection; physical measures (SBP/DBP/BMI) available across waves 1-3 (2011, 2013, 2015); venous blood samples analyzed for comprehensive biomarker panel
- **LASI-DAD Protocol**: Venous blood collection in Wave 1 (2017-2019) and Wave 2 (2022-2024); comprehensive biomarker panel with **complete physical measures** (SBP/DBP/BMI) collected; cognitive assessment and dementia diagnosis primary focus but cardiometabolic health data available
- **MHAS Protocol**: Venous blood collection in 2012 and 2016 Mex-Cog subsample (~2,265 respondents); HRS-compatible protocols with comprehensive biomarker panel; physical measures collected concurrently; **limited to two waves only**
- **HAALSI Protocol**: **NO HbA1c** (capillary glucose only); CRP collection limited to Wave 1 (2014-2015) only; Total/HDL cholesterol available Waves 1&3 (not Wave 2); physical measures (SBP/DBP/BMI) available across all waves; rural South African HDSS site
- **IFLS Protocol**: **Limited to DBS biomarkers only**: HbA1c (Wave 5, 2014-15) and CRP (Waves 4&5, 2007-08 & 2014-15); no cholesterol or physical measures data obtained; Indonesian national study
- **SHARE DBS Study (2015)**: ~27,200 dried blood spot samples collected across 12 countries; **NO measured blood pressure data**; only self-reported BP available in survey questionnaire
- **SHARE Countries**: BE, CH, DE, DK, EE, ES, FR, GR, IL, IT, SE, SI
- **SHARE Limitation**: Missing measured blood pressure data significantly limits utility for complete 6-indicator CMD-BA model (only self-reported BP available)

## Brief Study Descriptions

### HRS (Health and Retirement Study)
**US longitudinal study** of adults aged 50+ since 1992. Biennial interviews with ~20,000 respondents per wave. **Dried Blood Spot (DBS) biomarker collection** started in 2006 with alternating half-sample design: first half collected in 2006, 2010, 2014; second half in 2008, 2012, 2016. **2016 was the final DBS collection wave** and also marked the start of **Venous Blood Study (VBS)** collection, which continues in subsequent waves. **Physical measures** (SBP, DBP, BMI, height, weight, grip strength, walking speed) collected in waves 8-16 (1998-2022). **DBS protocol**: Blood spots collected by trained interviewers on Whatman cards, dried minimum 2 hours, shipped to University of Washington for analysis. **Consent rate 2016**: 86.7% consent, 98.9% completion rate among consenting, 85.7% overall completion. **Laboratory standards**: FDA-cleared assays with NHANES-equivalent values provided for cross-study comparability. Features linked administrative records and genetic data.

### ELSA (English Longitudinal Study of Ageing)
**England longitudinal study** of adults aged 50+ since 2002. Biennial interviews with ~11,000 core members. **Nurse visits** conducted in waves 2 (2004-05), 4 (2008-09), 6 (2012-13), 8 (2016-17), and 9 (2018-19) with blood biomarker collection and physical measurements. **Special sampling for waves 8-9**: Only half the sample was invited for nurse visits in Wave 8, with the remaining half invited in Wave 9. These waves are designed to be analyzed together and are combined in harmonized datasets. **Blood pressure protocol**: Three measurements taken on right arm while seated using Omron machines. **BMI protocol**: Height and weight measured by nurses (waves 2-6), with weight measurement moved to interviewer visits in waves 8-9. Includes comprehensive health, social, and economic measures.

### SHARE (Survey of Health, Ageing and Retirement in Europe)
**Multi-country European study** across 12 countries since 2004. **Major CMD-BA limitation**: Blood pressure measurements were **NOT included** in the 2015 DBS collection protocol. SHARE Wave 6 collected ~27,200 dried blood spot samples for biomarker analysis, but only BMI (from self-reported height/weight) is available for physical measures. This significantly limits SHARE's utility for the 6-indicator CMD-BA model.

**SHARE DBS Countries (2015)**: Belgium (BE), Switzerland (CH), Germany (DE), Denmark (DK), Estonia (EE), Spain (ES), France (FR), Greece (GR), Israel (IL), Italy (IT), Sweden (SE), Slovenia (SI) - **12 countries total**

**Available for CMD-BA**: 4 out of 6 indicators (HbA1c, CRP, Total Cholesterol, HDL, BMI) - **Missing blood pressure data**

**SHARE Biomarker Collection Protocol**:
- **Dried blood spots** collected in respondents' homes by trained interviewers  
- **~27,000 respondents** across 12 European countries in 2015
- Samples processed at University of Washington (Seattle) and Statens Serum Institut (Copenhagen)  
- ~23,700 samples successfully analyzed for biomarkers
- **Critical gap**: No measured blood pressure (SBP/DBP) available - SHARE interviewers do not take height, weight, or blood pressure measurements
- Only self-reported blood pressure data available in survey questionnaire

### CHARLS (China Health and Retirement Longitudinal Study)
**China national study** of adults aged 45+ since 2011. Biennial interviews with ~17,000 respondents at baseline, growing to ~21,000 by Wave 3 (2015). **Blood biomarker collection** in waves 1 (2011) and 3 (2015) - no biomarkers collected in Wave 2 (2013). **Wave 3 (2015) blood collection**: Target sample of 21,100 individuals with 13,420 blood samples collected (64% response rate). **Physical measures** collected in all main waves. Harmonized with HRS family of studies with comprehensive health and socio-economic data. **Blood analysis** includes HbA1c, CRP, total cholesterol, HDL cholesterol, glucose, and additional biomarkers processed at certified laboratories.

### LASI-DAD (Longitudinal Aging Study in India - Diagnostic Assessment of Dementia)
**India national dementia study** of adults aged 60+ since 2017. **Sub-sample from main LASI study**: ~4,000 respondents selected using stratified random sampling to ensure representation of cognitive impairment risk. **Venous blood collection** in Wave 1 (2017-2019) and Wave 2 (2022-2024) with comprehensive biomarker panels. **Physical measures** collected in both waves including blood pressure and BMI measurements. **Sample sizes**: Wave 1: 2,892 blood samples, Wave 2: 3,252 blood samples. **Laboratory processing**: Metropolis Healthcare with NABL and CAP accreditation. **Complete CMD-BA coverage**: All 6 indicators available (HbA1c, CRP, Total Cholesterol, HDL, Blood Pressure, BMI). **Geographic coverage**: 18 states and 4 metropolitan cities (Wave 1), expanded to include additional states in Wave 2. Conducted by 15 collaborating hospitals across India with standardized protocols for blood collection and physical measures.

### MHAS (Mexican Health and Aging Study)
**Mexico national panel study** of adults aged 50+ since 2001, harmonized with HRS. **Full biomarker and physical measurement data** available only in **2012** (full sample) and **2016 cognitive aging subsample (Mex-Cog)** with ~2,265 respondents. **Venous blood collection** in 2012 followed HRS-compatible protocols and included HbA1c, CRP, total cholesterol, and HDL cholesterol. **Physical measures** (SBP/DBP, BMI, grip strength, walk test) collected concurrently. **2016 Mex-Cog wave** used harmonized cognitive and biomarker protocols consistent with HRS-HCAP. **Complete CMD-BA coverage**: All 6 indicators available in both waves, supporting inclusion in CMD-BA 6-indicator analyses. **Study limitation**: Biomarker data restricted to only two waves (2001, 2003, 2015, 2018 waves lack full biomarker suite).

### HAALSI (Health and Aging in Africa: A Longitudinal Study of an INDEPTH Community in South Africa)
**South Africa rural community study** of adults aged 40+ in the Agincourt sub-district, Mpumalanga province, conducted 2014-2015. **Part of INDEPTH Health and Demographic Surveillance System (HDSS)** representing rural sub-Saharan African population dynamics. **Point-of-care biomarker and physical measurement collection** with ~5,100 participants providing comprehensive cardiometabolic health assessments. **Blood collection** includes CRP (Wave 1 only), total cholesterol and HDL cholesterol (Waves 1&3), **capillary glucose** (not HbA1c) using certified laboratory standards. **Physical measures** (SBP/DBP, BMI) collected using standardized protocols with high completion rates (>95%) across all waves. **Partial CMD-BA coverage**: 5 out of 6 indicators available (missing HbA1c), with glucose as alternative glycemic marker. **Cultural significance**: Rural setting with high HIV prevalence, labor migration patterns, and multi-generational households representing important demographic and health transitions in sub-Saharan Africa.

### IFLS (Indonesian Family Life Survey)
**Indonesia national household survey** of all ages since 1993, conducted by RAND, Survey Meter, and University of Gadjah Mada. **Five waves completed**: IFLS1 (1993), IFLS2 (1997), IFLS3 (2000), IFLS4 (2007-08), IFLS5 (2014-15) with excellent retention rates (>90%). **Current data access**: Limited to dried blood spot (DBS) biomarkers only - HbA1c from Wave 5 (2014-15) and CRP from Waves 4&5 (2007-08, 2014-15). **Sample growth**: From 7,200 households (1993) to 16,204 households and 50,148 individuals (Wave 5). **Data limitation**: No access to cholesterol data, physical measures (BP/BMI), or other health indicators. **CMD-BA coverage**: **Minimal** - only 2 out of 6 core indicators available (HbA1c + CRP). **Geographic scope**: National Indonesian study representing Southeast Asian context, but severely limited for comprehensive cardiometabolic biological age modeling.

---

## Summary

This document outlines the data foundation for the CMD-BA-CNC project:

1. **Six Core Biomarkers**: HbA1c, CRP, Total Cholesterol, HDL, Blood Pressure, and BMI from HRS-sister studies and related international research
2. **Current Access Status**: Data obtained from seven studies (HRS, ELSA, CHARLS, LASI-DAD, SHARE, MHAS, HAALSI obtained; IFLS biomarker variables obtained; TILDA, NICOLA, SLHAS applications pending)
3. **Study Coverage**: Twelve longitudinal aging studies providing cross-national comparative data across six continents

**Important Data Limitations**: 
- **SHARE**: Missing measured blood pressure data (only self-reported BP available)
- **HAALSI**: Missing HbA1c data (glucose available as alternative)
- **IFLS**: **Severe data limitation** - only 2 out of 6 CMD-BA indicators available (HbA1c + CRP); no cholesterol, blood pressure, or BMI data obtained
- These limitations require alternative analytical approaches, including partial biomarker models, wave-specific analysis, and focus on available indicator subsets

The following sections provide detailed technical information about biomarker specifications, harmonization challenges, and methodology.

---

## Core Biomarkers for CMD-BA-CNC

### 1. Glycemic Control
- **HbA1c (Hemoglobin A1c)**
  - Unit: % or mmol/mol
  - Normal range: <5.7% (<39 mmol/mol)
  - Reflects average blood glucose over 2-3 months
  - Available in all six studies (HRS, ELSA, SHARE, CHARLS, LASI-DAD, MHAS)

### 2. Inflammatory Markers
- **C-reactive protein (CRP)**
  - Unit: mg/L or mg/dL
  - Normal range: <3.0 mg/L
  - Marker of systemic inflammation
  - High-sensitivity CRP preferred when available

### 3. Lipid Profile
- **Total Cholesterol**
  - Unit: mg/dL or mmol/L
  - Target: <200 mg/dL (<5.2 mmol/L)
  - Marker of lipid metabolism

- **HDL Cholesterol**
  - Unit: mg/dL or mmol/L
  - Target: >40 mg/dL (>1.0 mmol/L) for men, >50 mg/dL (>1.3 mmol/L) for women
  - Protective lipid marker

### 4. Cardiovascular Measures
- **Blood Pressure**
  - **Systolic BP**: Normal <120 mmHg
  - **Diastolic BP**: Normal <80 mmHg
  - Multiple measurements averaged when available
  - Key indicator of cardiovascular health

### 5. Anthropometric Measures
- **Body Mass Index (BMI)**
  - Calculation: weight (kg) / height (m)²
  - Normal range: 18.5-24.9 kg/m²
  - Alternative: Waist-to-Height Ratio when available

## Detailed Data Collection Protocols

### HRS Dried Blood Spot (DBS) Protocol
**Collection Design**:
- **Alternating half-sample**: First half (2006, 2010, 2014), Second half (2008, 2012, 2016)
- **2016 final DBS wave** - **Venous Blood Study (VBS) began in 2016** and continues in subsequent waves
- Target: All respondents available for Enhanced Face-to-Face (EFTF) interview
- **Special informed consent** required for blood collection

**Collection Procedure**:
- DBS samples collected mid-interview (Section I) by trained interviewers
- **Whatman blood spot cards**: Up to 10 circles filled with blood droplets across 2 cards
- **Drying protocol**: Minimum 2 hours drying time in specially-designed cardboard boxes with airflow
- **Storage**: Cards placed in foil pouches with desiccant before shipment
- **Direct shipping**: Interviewers mail cards directly to University of Washington laboratory

**Laboratory Processing**:
- **University of Washington Department of Medicine Dried Blood Spot Laboratory**
- Quality coding upon receipt, storage at -70°C before and after analysis
- **FDA-cleared assays** for all biomarkers with standardized protocols
- **NHANES-equivalent values** calculated for cross-study comparability

**2016 Response Rates**:
- **Consent rate**: 86.7%
- **Completion rate** (among consenting): 98.9%
- **Overall completion rate**: 85.7%
- **Sample size**: ~6,800 DBS samples with biomarker results

**Biomarker Assays**:
- **HbA1c**: Bio-Rad Variant II HPLC system (R² = 0.99 vs. matched blood samples)
- **Total Cholesterol**: Synermed reagent kit with Amplex Red (R² = 0.82 vs. plasma)
- **HDL Cholesterol**: Beckman Coulter Synchron system (R² = 0.91 vs. plasma)
- **CRP**: BioCheck high-sensitivity ELISA (R² = 0.89 for values ≤5mg/L)
- **Cystatin C**: BioVendor ELISA standardized to European Reference Material (R² = 0.79)

**Quality Control**:
- Coefficient of variation <10% for all assays (intra- and inter-assay)
- Out-of-range values recoded to reportable limits
- **NHANES calibration**: Percentile-based transformation to match national reference values

### ELSA Nurse Visit Protocol
**Blood Pressure Measurement**:
- Three measurements taken on right arm while seated
- Uses Omron machines (waves 2, 4, 6, 8, 9) - comparable to HSE from 2003 onwards
- Advice given based on higher of last two readings (first reading may be elevated due to nervousness)
- Results provided to respondents and GPs with consent

**Physical Measurements**:
- **Height**: Standing and sitting measured (waves 2, 4), standing only (wave 6)
- **Weight**: Measured by nurses (waves 2, 4, 6), moved to interviewer visits (waves 8, 9)
- **BMI**: Calculated from measured height/weight, grouped by WHO obesity definitions
- Reliability indicators (RELHITE, RELWAIT) included for measurement quality assessment

**Blood Sample Collection**:
- Fasting protocol for respondents under 80 years (except diabetics on treatment)
- Fasting criteria: last eaten day before visit OR minimum 5 hours with only light meal/fruit
- 6 tubes collected (waves 2, 4, 6): 3 standard + 1 fasting + 2 DNA consent
- 5 tubes collected (waves 8, 9): 3 standard + 1 fasting + 1 PAXGene consent
- Priority order ensures key analytes collected even with insufficient blood

**Sample Sizes by Wave**:
- Wave 2: 7,666 nurse visits (87.3% response rate)
- Wave 4: 8,218 nurse visits (85.7% response rate)  
- Wave 6: 7,731 nurse visits (84.3% response rate)
- Wave 8: 3,479 nurse visits (93.7% response rate)
- Wave 9: 3,047 nurse visits (83.8% response rate)

### CHARLS Blood Collection Protocol
**Venous Blood Sampling**:
- Target: All 21,100 Wave 3 (2015) interview respondents
- Achieved: 13,420 blood samples (64% response rate)
- Gender difference: Women 65.95% vs Men 62.18% response rate
- Geographic difference: Rural 66.94% vs Urban 60.06% response rate

**Biomarker Analysis**:
- **Core markers**: HbA1c, hsCRP, Total cholesterol, HDL cholesterol, LDL cholesterol, triglycerides
- **Additional markers**: Glucose, BUN, creatinine, uric acid, cystatin C
- **CBC analysis**: Hemoglobin, hematocrit, WBC count, platelet count, MCV
- Fasting status recorded for appropriate interpretation of glucose and lipid measures

**Laboratory Standards**:
- External laboratory processing with certified quality control
- Ethical approval from Peking University IRB (IRB 00001052-11014)
- Written informed consent from all participants
- Cross-sectional blood sample weights provided for population inference

### LASI-DAD Venous Blood Collection Protocol
**Study Design**:
- **Sub-sample from main LASI**: ~4,000 respondents aged 60+ selected using stratified random sampling
- **Cognitive risk stratification**: 50% high-risk, 50% low-risk for cognitive impairment
- **Wave 1 (2017-2019)**: 2,892 blood samples across 18 states + 4 metropolitan cities
- **Wave 2 (2022-2024)**: 3,252 blood samples with expanded geographic coverage

**Blood Collection Procedure**:
- **17 mL total volume** across 5 tubes: 2 SSTs (serum), 2 EDTA tubes, 1 PPT (plasma)
- **Phlebotomy service**: Metropolis Healthcare (NABL + CAP accredited)
- **Collection locations**: Hospitals or respondents' homes (Wave 1), home-only (Wave 2)
- **Informed consent**: Available in 12 Indian languages with family member present

**Laboratory Processing**:
- **Local processing**: Within 2-4 hours at regional Metropolis laboratories
- **Centrifugation**: 3500 rpm for 10 minutes
- **Central laboratory**: Shipped to Delhi Metropolis lab within 24 hours
- **Temperature monitoring**: 2-8°C cold chain with continuous logging
- **Quality control**: Daily QC samples, hemolysis monitoring (6.7% overall rate)

**Biomarker Assays**:
- **HbA1c**: Bio-Rad D-10 (Wave 1), Tosoh G8 (Wave 2) - Ion exchange HPLC
- **Total Cholesterol**: Enzymatic colorimetric method (Architect ci8200/Roche Cobas 8000)
- **HDL Cholesterol**: Homogeneous enzymatic assay with selective detergent
- **CRP**: High-sensitivity nephelometry (BNProSpec/Atellica NEPH 630)
- **Additional markers**: Comprehensive metabolic panel, thyroid function, vitamins

**Geographic Coverage**:
- **Wave 1**: 18 states (Assam, Gujarat, Haryana, J&K, Karnataka, Kerala, Maharashtra, Odisha, Rajasthan, Tamil Nadu, Telangana, UP, Bihar, MP, Uttarakhand, Punjab, West Bengal) + 4 cities (Chennai, Delhi, Kolkata, Mumbai)
- **Wave 2**: Expanded to include Andhra Pradesh, Chhattisgarh, Jharkhand, Puducherry

**Physical Measures Collection**:
- **Blood Pressure**: Standardized protocol using digital oscillometric devices
  - **Equipment**: Omron digital blood pressure monitors (model HEM-7120 or equivalent)
  - **Measurement protocol**: Three consecutive readings taken 1 minute apart after 5-minute rest
  - **Position**: Seated with back supported, arm at heart level
  - **Variables**: Systolic BP (SBP), Diastolic BP (DBPJ), Pulse rate
  - **Quality control**: Regular calibration checks and staff training protocols
  - **Missingness handling**: Valid measurements coded 1-999 mmHg; missing/invalid coded as 991-996 with specific reasons

- **Body Mass Index (BMI)**: Height and weight measurements for BMI calculation
  - **Height measurement**: Digital stadiometer with 0.1 cm precision
  - **Weight measurement**: Digital weighing scale with 0.1 kg precision  
  - **BMI calculation**: Weight (kg) / Height (m²)
  - **Measurement conditions**: Light clothing, shoes removed, standardized positioning
  - **Quality assurance**: Equipment calibration before each measurement session
  - **Range validation**: Height 100-220 cm, Weight 25-200 kg considered valid

**Physical Measures Data Structure**:
- **Wave 1 (2017-2019)**: Complete SBP/DBP/BMI data collected for all consenting participants
- **Wave 2 (2022-2024)**: Continued collection with enhanced protocols and equipment standardization
- **Compliance monitoring**: Detailed tracking of measurement completion rates and data quality
- **Staff training**: Standardized protocols across all 15 collaborating hospitals and field sites
- **Hospital network**: 15 collaborating medical institutions across India

**Quality Assurance**:
- **Response rates**: Wave 1: 57% blood collection rate, Wave 2: 53% blood collection rate
- **Sample tracking**: Automated Blood Management System (BMS) with real-time monitoring
- **Temperature compliance**: Median receiving temperature 6.1°C (IQR: 4.1-8.1°C)
- **Storage**: Plasma samples at -80°C for neurodegenerative biomarker assays at AIIMS

### MHAS Physical Measures and Biomarker Collection Protocol

**Study Design**:
- **2012 Full Sample**: National representative sample with complete biomarker and physical measures
- **2016 Mex-Cog Subsample**: ~2,265 respondents (selected from 3,250 target sample) with cognitive aging focus
- **HRS Harmonization**: Protocols designed for cross-national comparability with HRS family studies
- **Geographic coverage**: National representation across Mexico with urban and rural stratification

**Physical Measures Collection**:

**2012 Full Sample CMD-BA Measures (n=2,086)**:
- **Blood Pressure**: 100% completion rate, Systolic BP Mean=139.9 mmHg (SD=21.8), Diastolic BP Mean=79.2 mmHg (SD=11.7)
- **BMI Components**: Height n=2,049 (Mean=155.1 cm, SD=9.5), Weight n=2,057 (Mean=69.7 kg, SD=15.0)

**2016 Mex-Cog CMD-BA Measures**:
- **Blood Pressure**: Systolic BP Mean=142.7 mmHg (SD=24.4), Diastolic BP Mean=77.7 mmHg (SD=12.0), 99.1% completion rate
- **BMI**: Mean=28.4 kg/m² (Height 154.2 cm, Weight 67.6 kg), 95-96% completion rate

**Blood Biomarker Collection**:
- **2012 Protocol**: 95.9% blood collection success rate (2,001/2,086 participants)
  - **HbA1c**: n=2,036 (97.6% completion), Mean=6.8%, SD=1.9, Range: 4.0-14.9%
  - **CRP**: n=2,003, Mean=4.3 mg/dL, SD=7.2, Range: 0-207.0 mg/dL
  - **Total Cholesterol**: n=2,002, Mean=201.2 mg/dL, SD=45.6, Range: 76-704 mg/dL
  - **HDL Cholesterol**: n=2,003, Mean=41.2 mg/dL, SD=10.4, Range: 17-92 mg/dL (45.3% below 40 mg/dL)
- **2016 Mex-Cog Protocol**: Phase 2 subsample (881 participants)
  - **HbA1c**: Mean=5.67%, Range: 4.1-13%+ (1,142 samples)
  - **CRP**: Mean=5.67 mg/dL (752 samples)
  - **Total Cholesterol**: Mean=193.6 mg/dL, Range: 83-330 mg/dL (752 samples)
  - **HDL Cholesterol**: Mean=46.3 mg/dL, Range: 20-92 mg/dL (752 samples)

**CMD-BA Coverage**: Complete 6-indicator model available in both 2012 and 2016 waves with high completion rates (95-100%) for all core biomarkers and physical measures.

### HAALSI (Health and Aging in Africa: A Longitudinal Study of an INDEPTH Community in South Africa) Protocol

**Study Design**:
- **Population**: Adults aged 40+ in rural South Africa (Agincourt sub-district, Mpumalanga province)
- **Waves**: Wave 1 (2014-2015), Wave 2 (2018), Wave 3 (2021)
- **Sample size**: ~5,100 participants with comprehensive health assessments
- **Geographic focus**: INDEPTH Health and Demographic Surveillance System (HDSS) site
- **Cultural context**: Rural community with high migration patterns and multi-generational households
- **Study objectives**: Aging, health transitions, and social determinants in sub-Saharan African context

**Biomarker Variables and Availability**:

**HbA1c**: **NOT AVAILABLE** 
- HAALSI collected **capillary glucose readings only**, not HbA1c
- **Variable**: `w1c_bs_glucose` (Wave 1), with re-entry check `w1c_bs_glucose_chk`
- **Method**: Point-of-care glucose testing
- **Limitation**: Glucose readings cannot substitute for HbA1c in CMD-BA models

**C-Reactive Protein (CRP)**: **Wave 1 ONLY**
- **Variable**: `crpresult` (in separate DBS-CRP public-release file)
- **Method**: Dried blood spot (DBS) assay
- **Availability**: Baseline-only biomarker (2014-2015)
- **Units**: mg/L

**Total Cholesterol**: **Waves 1 & 3 ONLY**
- **Wave 1 variables**: `w1c_bs_chol` (reading), `w1c_bs_chol_chk` (re-entry check)
- **Wave 3 variables**: `w3bs030` (reading), `w3bs034` (re-entry check)
- **Method**: Point-of-care testing
- **Note**: Not assayed in Wave 2 (2018)

**HDL Cholesterol**: **Waves 1 & 3 ONLY**
- **Wave 1 variables**: `w1c_bs_hdl`, `w1c_bs_hdl_chk`
- **Wave 3 variables**: `w3bs031`, `w3bs035`
- **Method**: Point-of-care testing
- **Note**: Not assayed in Wave 2 (2018)

**Physical Measures Collection**:

**Blood Pressure**: **All Waves Available**
- **Raw readings**:
  - Wave 1: `w1bs012_1` to `w1bs012_3` (SBP), `w1bs013_1` to `w1bs013_3` (DBP)
  - Wave 2: `w2bs012_1` to `w2bs012_3` (SBP), `w2bs013_1` to `w2bs013_3` (DBP)
  - Wave 3: `w3bs012_1` to `w3bs012_3` (SBP), `w3bs013_1` to `w3bs013_3` (DBP)
- **Cleaned means**:
  - Wave 1: `w1c_bs_mean_sbp`, `w1c_bs_mean_dbp`
  - Wave 2: `w2c_bs_mean_sbp`, `w2c_bs_mean_dbp`
  - Wave 3: `w3c_bs_mean_sbp`, `w3c_bs_mean_dbp`
- **Protocol**: Three readings taken; cleaned mean variables provide interviewer-averaged results

**Body Mass Index (BMI)**: **All Waves Available**
- **Variables**:
  - Wave 1: `w1c_bs_bmi`
  - Wave 2: `w2c_bs_bmi`
  - Wave 3: `w3bs050`
- **Components available**: Raw height (`w?bs044`) and weight (`w?bs046`) in biomarker sections
- **Method**: Calculated from measured height and weight in each wave

**Data Quality Notes**:
- **Missing value codes**: -97 = "don't know", -98 = "refused" (recode to missing before analysis)
- **Completion rates**: >95% for physical measures across all waves
- **Biomarker limitations**: Point-of-care testing may have different precision than laboratory assays

**CMD-BA Model Coverage**: **PARTIAL** - 5 out of 6 indicators available
- **Available**: CRP (Wave 1 only), Total Cholesterol (Waves 1&3), HDL (Waves 1&3), Blood Pressure (all waves), BMI (all waves)
- **Missing**: HbA1c (glucose available as alternative glycemic marker)
- **Limitation**: Cannot construct complete 6-indicator CMD-BA model due to missing HbA1c

### IFLS (Indonesian Family Life Survey) Protocol

**Data Access Status**: **Core biomarker variables obtained from Wave 5 DBS public-use file**
**Available data file**: `wave5_dbs_public_use.dta` with specific biomarker variables
**Documentation source**: IFLS Wave 5 DBS Data User Guide (RAND Working Paper WR-1143/6)

**Study Design**:
- **Population**: Indonesian households, all ages, national representation
- **Waves**: IFLS1 (1993), IFLS2 (1997), IFLS3 (2000), IFLS4 (2007-08), IFLS5 (2014-15)
- **Sample growth**: 7,200 households (1993) → 13,500 households (2007-08)
- **Retention rates**: Excellent (>90% across waves)
- **Geographic scope**: National Indonesian survey with community and facility data
- **Conducting organizations**: RAND, Survey Meter, University of Gadjah Mada

**Available Variables in Current Dataset** (`wave5_dbs_public_use.dta`):
- **Core identifiers**: `hhid14` (Household ID), `pid14` (Person ID), `pidlink` (Person linkage)
- **HbA1c variables**: `a1c_dbs` (raw DBS), `a1c_rev` (whole blood equivalent), `a1c_revx` (validity flag)
- **CRP variables**: `crp_dbs` (raw DBS), `crp_plas_equi` (plasma equivalent), `ln_crp_plas_equi` (log plasma equivalent)
- **Sampling weights**: `pwt14DBSXa` (cross-sectional), `pwt14DBSLa` (longitudinal 2007-2014)
- **Sample flag**: `notin2007` (indicator for respondents not in 2007 sample)
- **Data limitation**: Only DBS biomarkers included - no cholesterol, physical measures, or other health indicators

**Biomarker Variables and Wave Availability**:

**HbA1c**: **Wave 5 (2014-15) ONLY**
- **Availability**: Single wave collection, 7,524 observations
- **Method**: Dried blood spot (DBS) HPLC assay with chromatogram recalculation
- **Laboratory**: Clinical Pathology and Laboratory Medicine Department, University of Gadjah Mada
- **Technical details**: 
  - Bio-Rad D10 HPLC with DBS protocol validation (R² = 0.960 vs whole blood)
  - **Conversion equation**: HbA1c whole blood equivalent = 1.44 × recalculated DBS value - 0.62
  - **Variable names**: `a1c_dbs` (raw DBS), `a1c_rev` (whole blood equivalent)
  - **Quality control**: Values <3.5% flagged as potentially unreliable
- **Clinical cutoff**: ≥6.5% for diabetes diagnosis (6.9% prevalence in IFLS5)

**C-Reactive Protein (CRP)**: **Waves 4 & 5 (2007-08, 2014-15)**
- **Wave 4**: Serum-based assay, part of broader biomarker collection
- **Wave 5**: 7,579 observations via dried blood spot (DBS) assay
- **Method**: High-sensitivity CRP (hsCRP) ELISA validated by University of Washington
- **Technical details**:
  - **DBS-plasma correlation**: R² = 0.99 in validation studies
  - **Conversion equation**: Ln(CRP plasma equivalent) = 1.192 × Ln(CRP DBS) - 0.684
  - **Variable names**: `crp_dbs` (raw DBS), `crp_plas_equi` (plasma equivalent)
  - **Cross-wave compatibility**: Wave 5 plasma equivalent = 1.228 × Wave 4 serum equivalent + 0.312
- **Clinical cutoff**: ≥3.0 mg/L for high cardiovascular risk (18.0% prevalence in IFLS5)
- **Quality control**: Percipio Biosciences ELISA kit with daily standards and controls

**Data Not Available in Current Dataset**:
- **Total Cholesterol**: Not included in DBS file (available in Wave 4 but not obtained)
- **HDL Cholesterol**: Not included in DBS file (available in Wave 4 but not obtained)  
- **Blood Pressure**: Not included in DBS file (collected across waves but not obtained)
- **BMI/Anthropometrics**: Not included in DBS file (collected across waves but not obtained)
- **Other biomarkers**: Hemoglobin, lung capacity, grip strength data not obtained

**Data Quality and Completeness**:
- **Overall retention**: >90% household retention across all five waves (1993-2015)
- **Wave 5 biomarker sampling**: Targeted 9,944 respondents from Wave 4 CRP sample
- **DBS collection success**: 
  - **HbA1c**: 7,524 observations with valid DBS (7,416 with sampling weights)
  - **CRP**: 7,579 observations with valid DBS (7,470 with sampling weights)
- **Laboratory quality control**:
  - **Daily workflow**: 144 samples/day with standardized controls
  - **Validation studies**: Weekly testing with University of Washington reference samples
  - **CRP validation**: R² = 0.896-0.958 vs plasma reference
  - **HbA1c validation**: R² = 0.985-0.994 vs whole blood reference
- **Missing data handling**: 
  - 109 respondents without proper sampling weights (not in 2007 sample)
  - 9 unusable DBS spots due to insufficient sample volume
  - HbA1c values <3.5% flagged as potentially unreliable (`a1c_revx = 3`)

**Descriptive Statistics from IFLS Wave 5 (Weighted)**:

**CRP Data**:
- **Sample size**: 7,470 observations with sampling weights
- **DBS concentrations**: Mean 2.89 mg/L (SD 5.09), Median 1.33 mg/L
- **Range**: 0.01-200 mg/L
- **Plasma equivalent**: Mean 2.11 mg/L (SD 5.33), Median 0.71 mg/L  
- **High cardiovascular risk** (≥3.0 mg/L): 18.0% prevalence
- **Distribution**: Right-skewed, log transformation recommended for analysis

**HbA1c Data**:
- **Sample size**: 7,416 observations with valid DBS (7,347 with whole blood equivalents)
- **DBS concentrations**: Mean 7.69% (SD 1.01), Median 7.5%
- **Whole blood equivalent**: Mean 5.49% (SD 0.96), Median 5.4%
- **Range**: 3.5-15.7% (whole blood equivalent)
- **Diabetes indicator** (≥6.5%): 6.9% prevalence  
- **Distribution**: Long right tail, some extreme values present

**Sampling Weights and Population Representation**:
- **Target population**: 83% of Indonesian population across 13 provinces (1993 baseline)
- **Wave 5 sample frame**: 16,204 households, 50,148 individuals interviewed  
- **DBS sampling**: Targeted all 9,944 respondents with Wave 4 CRP assays
- **Weight construction**: 
  - **Base weights**: Wave 4 weights incorporating sampling scheme and non-participation
  - **Attrition adjustment**: Logistic model predicting Wave 5 DBS participation
  - **Available weights**: Cross-sectional (`pwt14DBSXa`) and longitudinal (`pwt14DBSLa`)
- **Geographic coverage**: National representation with urban/rural stratification

**Laboratory Specifications and Quality Control**:
- **Processing laboratory**: Clinical Pathology and Laboratory Medicine, University of Gadjah Mada
- **Laboratory director**: Dr. Elizabeth Henny Herningtyas
- **Storage conditions**: DBS stored at -40°C at Survey Meter facility
- **Daily throughput**: 144 samples processed per day, 5 days per week
- **CRP assay kit**: Percipio Biosciences hsCRP ELISA (Catalog #11190)
- **HbA1c equipment**: Bio-Rad D10 HPLC with chromatogram analysis
- **Quality standards**: 
  - Weekly validation with University of Washington reference samples
  - Assays rejected if controls >3 SD from established means
  - Duplicate measurements for all validation samples

**Technical Limitations and Considerations**:
- **DBS vs venous blood**: DBS values may have more random error than clinic-based venous samples
- **Cross-wave comparisons**: Require conversion equations for CRP (different assay methods between waves)
  - **Wave 4-5 CRP conversion**: Wave 5 plasma equivalent = 1.228 × Wave 4 serum equivalent + 0.312
- **Absolute vs relative values**: DBS values better for within-sample ranking than absolute clinical thresholds
- **Prevalence estimates**: Use with caution due to potential bias in absolute values
- **Undetectable CRP**: Extremely low values assigned arbitrary value of 0.001 mg/L

**Data File Structure and Variables** (`wave5_dbs_public_use.dta`):
- **Identifiers**: `hhid14` (household), `pid14` (person), `pidlink` (linkage across waves)
- **HbA1c variables**: 
  - `a1c_dbs`: Raw DBS concentration
  - `a1c_rev`: Whole blood equivalent (recommended for clinical thresholds)
  - `a1c_revx`: Validity flag (1=valid target, 2=valid non-target, 3=<3.5%, 9=invalid)
- **CRP variables**:
  - `crp_dbs`: Raw DBS concentration  
  - `crp_plas_equi`: Plasma equivalent (recommended for clinical thresholds)
  - `ln_crp_plas_equi`: Log-transformed plasma equivalent (recommended for analysis)
- **Sampling weights**:
  - `pwt14DBSXa`: Cross-sectional weight with attrition correction
  - `pwt14DBSLa`: Longitudinal weight (2007-2014) with attrition correction
- **Sample indicators**: `notin2007` (flag for respondents not in 2007 DBS sample)

**CMD-BA Model Coverage**: **MINIMAL - Only 2 out of 6 indicators**
- **Available**: HbA1c (Wave 5 only) + CRP (Waves 4&5, different assays)
- **Missing**: Total Cholesterol, HDL Cholesterol, Blood Pressure, BMI
- **Critical limitations**: 
  - No physical measures (blood pressure, BMI) data obtained
  - No cholesterol markers data obtained  
  - Limited to inflammatory and glycemic markers only
- **Recommended approaches**:
  - **Two-biomarker analysis**: HbA1c + CRP for metabolic-inflammatory profiles
  - **Cross-wave CRP trends**: Using Wave 4-5 conversion equation
  - **Population health surveillance**: Diabetes and inflammation prevalence only
- **Not suitable for**: Complete CMD-BA 6-indicator modeling or comprehensive cardiometabolic risk assessment

### NICOLA (Northern Ireland Cohort for the Longitudinal Study of Ageing) Protocol

**Data Access Status**: **Application pending** - Protocol information obtained from study documentation
**Geographic focus**: Northern Ireland representative sample of adults aged 50+
**Study objectives**: Health and social aging patterns in Northern Ireland context

**Biosample Collection and Laboratory Processing**:

**Sample Collection Protocol**:
- **Visit type**: Nurse-led home visits or health assessment center visits
- **Sample types**: Fasting venous blood samples, saliva samples, hair samples
- **Collection conditions**: Morning collection preferred, standardized protocols across sites
- **Storage and transport**: Cold chain maintenance with temperature monitoring
- **Consent process**: Multi-stage consent for different sample types and future research use

**Laboratory Infrastructure**:
- **Processing facility**: Queen's University Belfast in partnership with certified clinical laboratories
- **Quality standards**: ISO 15189 medical laboratory accreditation
- **Sample processing**: Serum and plasma separation within 4 hours of collection
- **Long-term storage**: -80°C biobank facilities with backup systems and sample tracking
- **Chain of custody**: Comprehensive sample tracking from collection through analysis

**Biomarker Analysis Capabilities**:
- **Core cardiometabolic panel**: HbA1c, high-sensitivity CRP, lipid profile (Total Cholesterol, HDL, LDL, Triglycerides)
- **Additional biomarkers**: Glucose, insulin, inflammatory markers (IL-6, TNF-α), kidney function markers
- **Hormone analysis**: Cortisol, thyroid function, vitamin D
- **Genetic analysis**: Genome-wide association studies (GWAS), polygenic risk scores
- **Specialized assays**: Biomarkers of aging, neurodegeneration, and cellular senescence

**Physical Measurements Protocol**:
- **Blood pressure**: Automated oscillometric devices with triple measurements
- **Anthropometry**: Height, weight, waist circumference, body composition analysis
- **Functional assessments**: Grip strength, walking speed, cognitive function testing
- **Advanced measures**: Arterial stiffness, carotid intima-media thickness (subset)

**Data Integration and Harmonization**:
- **HRS-family compatibility**: Protocols designed for cross-study comparability
- **ELSA coordination**: Shared methodology development with English Longitudinal Study of Ageing
- **European standards**: Alignment with SHARE and other European longitudinal studies
- **Variable naming**: Consistent coding schemes for cross-national analysis

**Sample Size and Coverage Projections** (when data obtained):
- **Target sample**: ~8,500 participants aged 50+ representative of Northern Ireland
- **Wave frequency**: Biennial interviews with health assessments every 4 years
- **Biomarker collection waves**: Planned for alternating waves (similar to HRS/ELSA design)
- **Geographic representation**: All Local Government Districts in Northern Ireland

**Anticipated CMD-BA Coverage** (pending data access):
- **Expected complete coverage**: All 6 indicators (HbA1c, CRP, Total Cholesterol, HDL, SBP/DBP, BMI)
- **Laboratory standards**: Clinical-grade assays with quality control protocols
- **Cross-study validation**: Calibration studies planned with ELSA and HRS
- **Population characteristics**: Expected high prevalence of cardiometabolic conditions

**Research Applications** (when available):
- **UK-Ireland comparisons**: Cross-border health and aging patterns
- **European integration**: Contribution to pan-European aging research
- **Genetic studies**: Population-specific genetic associations with cardiometabolic health
- **Policy relevance**: Health system planning and intervention targeting in Northern Ireland

**Documentation and Access** (anticipated):
- **Data dictionaries**: Comprehensive variable documentation with measurement protocols
- **User guides**: Detailed methodology and technical appendices
- **Access procedures**: Standard application process through designated data repository
- **Ethical approvals**: Multi-institutional IRB approvals for international research collaboration

---

## Cross-Study Biomarker Availability Summary

### Complete 6-Biomarker Model (HbA1c + CRP + Total Chol + HDL + SBP/DBP + BMI):
- **HRS**: ✓ Complete coverage
- **ELSA**: ✓ Complete coverage  
- **CHARLS**: ✓ Complete coverage
- **LASI-DAD**: ✓ Complete coverage
- **MHAS**: ✓ Complete coverage (2012, 2016 waves only)

### Partial 5-Biomarker Model (Missing HbA1c):
- **HAALSI**: CRP + Total Chol + HDL + SBP/DBP + BMI (glucose available as HbA1c alternative)

### Partial 4-Biomarker Model (Blood biomarkers only):
- **SHARE**: HbA1c + CRP + Total Chol + HDL (missing measured SBP/DBP - only self-reported BP available)

### Variable Wave Coverage (Severely Limited 6-Biomarker Model):
- **IFLS**: **Only 2 biomarkers available** - HbA1c (Wave 5, 2014-15) + CRP (Waves 4&5, different assays)
  - **Major limitations**: No cholesterol, blood pressure, or BMI data obtained
  - **Recommended use**: Two-biomarker inflammatory-glycemic analysis only, not suitable for CMD-BA modeling

### Sample Sizes by Study:
- **HRS**: ~15,000 observations with complete biomarker panel
- **ELSA**: ~8,000 observations with complete biomarker panel  
- **CHARLS**: ~12,000 observations with complete biomarker panel
- **LASI-DAD**: ~6,100 observations with complete biomarker panel (Waves 1+2 combined)
- **MHAS**: ~4,000-5,000 observations with complete biomarker panel (2012 + 2016 Mex-Cog combined)
- **HAALSI**: ~5,100 observations with partial biomarker panel (missing HbA1c)
- **IFLS**: Wave 5 biomarkers: ~7,470 CRP observations, ~7,416 HbA1c observations (with sampling weights); 50,148 total individual interviews
- **SHARE**: ~25,000 observations (blood biomarkers only)
- **TILDA**: TBD (application pending)
- **NICOLA**: TBD (application pending)
- **SLHAS**: TBD (application pending)

### Geographic Coverage:
- **North America**: United States (HRS), Mexico (MHAS)
- **Europe**: 12 countries (SHARE), England (ELSA), Ireland (TILDA), Northern Ireland (NICOLA)
- **Asia**: China (CHARLS), India (LASI-DAD), Indonesia (IFLS), Sri Lanka (SLHAS)
- **Africa**: South Africa (HAALSI)
- **Total coverage**: 22+ countries across 4 continents

---

*Last updated: June 2025*
*Project Status: Phase 1 - Twelve-Study Biomarker Harmonization (5 studies with complete 6-biomarker coverage, 3 with partial/variable coverage, 4 applications pending)*
*Studies included: HRS, ELSA, SHARE, CHARLS, LASI-DAD, MHAS, HAALSI, IFLS, TILDA, NICOLA, SLHAS*