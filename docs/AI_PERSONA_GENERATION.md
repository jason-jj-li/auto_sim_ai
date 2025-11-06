# AI-Powered Persona Generation Tutorial

## Overview
This feature allows you to generate synthetic personas by simply describing your target population in natural language. The AI automatically extracts demographic information and creates realistic personas that match your description.

## How It Works

### 1. AI Demographic Extraction
- Paste free-form text describing your target population
- The LLM analyzes the text using a specialized prompt
- Extracts structured demographic data in JSON format
- Intelligently parses complex demographic descriptions

### 2. Intelligent Distribution Parsing
The system includes advanced parsers that understand natural language demographics:
- **Percentage extraction**: "Male 51.24%, Female 48.76%" → exact distribution
- **Range detection**: "Middle school to bachelor's degree, covering illiterate to doctorate" → all 7 education levels
- **Keyword analysis**: "Predominantly Han ethnicity" → weighted ethnic distribution
- **Pattern recognition**: "Urban residents 63.89%" → urban/rural split

### 3. Persona Generation
- Extracted demographics are converted into statistical distributions
- PersonaGenerator creates realistic personas with coherent backgrounds
- Each persona includes: name, age, gender, occupation, education, location, marital status, ethnicity, political affiliation, religion, personality traits, values, and a natural language background

### 4. Key Demographics Extracted

**Core Demographics** (always extracted):
- **Age**: Single age, range (25-35), or description (young adults)
- **Gender**: Distribution with percentages (Male 51.24%, Female 48.76%)
- **Occupation**: Profession types (nurses, tech workers, students)
- **Education**: Levels from illiterate to doctorate, with distribution weights

**Extended Demographics** (parsed from text):
- **Location**: Urban/rural mix, specific regions, cities
- **Marital Status**: Single, married, divorced, widowed with percentages
- **Ethnicity**: Han Chinese, ethnic minorities distributions
- **Political Affiliation**: Mass, party member, youth league, democratic parties
- **Religion**: No religion, Buddhism, Taoism, Christianity, Islam

**Additional Context** (enhances background generation):
- **Income**: Range or category (low income, middle income, high income)
- **Family**: Household size, children, family structure
- **Health**: Status, concerns, chronic conditions
- **Technology**: Usage patterns, digital literacy
- **Interests**: Hobbies, activities, preferences
- **Values**: Core beliefs, priorities, worldview

## Usage Instructions

### Step 1: Connect to LLM

**Before using AI extraction, you MUST connect to an LLM:**

1. Go to the **Home** page
2. Choose your LLM provider:
   - **LM Studio** (local, free, recommended for Chinese)
   - **DeepSeek** (API, affordable, excellent Chinese support)
   - **OpenAI** (API, expensive, good quality)
3. Enter API details:
   - Base URL (e.g., `http://localhost:1234/v1` for LM Studio)
   - API Key (if required)
   - Model name
4. Click "Test Connection"
5. ✅ Verify "Connection successful" message appears

**💡 Recommendation**: For Chinese population generation, use LM Studio with Qwen2.5 or DeepSeek-V3 models for best results.

---

### Step 2: Navigate to AI Extraction

1. Click **Setup** page in the sidebar
2. Click **Generate Personas** tab
3. Click **AI-Powered Extraction** sub-tab

You should see:
- Large text area for population description
- Number of personas slider (no limit, warning at 1000+)
- "Extract Demographics & Generate Personas" button

---

### Step 3: Write Your Prompt

**Use the comprehensive examples above as templates!**

**Minimum required information:**
- Age range or distribution
- Gender breakdown
- Basic occupation or context

**Recommended information (for better results):**
- Education levels with distribution
- Location (urban/rural, regions)
- Marital status, ethnicity, political affiliation, religion
- Income levels
- Values and interests
- Health and technology usage

**Example Quick Start:**
```text
Chinese urban residents, age 25-45, Male (51.24%), Female (48.76%).
Education: Mainly middle school to bachelor's degree, covering illiterate to doctorate.
Urban residents 63.89%, rural residents 36.11%.
```

---

### Step 4: Extract & Generate

1. **Paste your population description** in the text area
2. **Set number of personas** (e.g., 100, 500, 1000)
   - No upper limit (but 1000+ will show warning)
   - Larger numbers = more representative distributions
3. **Click "Extract Demographics & Generate Personas"**
4. **Wait for processing** (typically 5-30 seconds)
   - LLM extraction: 2-5 seconds
   - Persona generation: 3-25 seconds depending on quantity

---

### Step 5: Review Extracted Demographics

After extraction, you'll see a **blue info box** showing:

```
```text
Age: 18-65, average 42 years
Gender: Male (51.24%), Female (48.76%)
Education: Mainly middle school to bachelor's, covering illiterate to doctorate
Occupation: Enterprise employees, self-employed, civil servants, ...
Location: Urban residents 63.89%, rural residents 36.11%
Marital Status: Married 68%, Single 22%, Divorced 8%, Widowed 2%
Ethnicity: Han Chinese 91%, Ethnic minorities 9%
Political Affiliation: Mass 70%, Party member 25%, Youth League 4%, Democratic parties 1%
Religion: No religion 85%, Buddhism 8%, Taoism 3%, ...
```
```

**Verify this matches your expectations!** If not, adjust your prompt and try again.

---

### Step 6: Review Generated Personas

Scroll down to see **individual personas** in expandable cards:

Each card shows:
- 👤 Name, Age, Gender
- 💼 Occupation
- 🎓 Education
- 📍 Location
- 💍 Marital Status
- 🧬 Ethnicity
- 🏛️ Political Affiliation
- ⛪ Religion
- 🎨 Personality Traits (5 traits)
- 💎 Core Values (5 values)
- 📖 Background (coherent Chinese narrative)

**💡 Click "Show Details" to expand and verify personas are realistic!**

---

### Step 7: Review Demographics Summary

After generation, scroll to **Population Demographics Summary**:

#### **📊 Basic Demographics** (3-column layout)

**Column 1 - Age Statistics:**
- Mean Age: 42.3 years
- Age Range: 18-65 years
- Age Groups:
  - 18-25: 150 (15.0%)
  - 26-35: 250 (25.0%)
  - 36-45: 280 (28.0%)
  - 46-55: 200 (20.0%)
  - 56-65: 120 (12.0%)

**Column 2 - Gender & Education:**
- Gender: Male 512 (51.2%), Female 488 (48.8%)
- Education: Bachelor 350 (35.0%), Middle school 200 (20.0%), High school 180 (18.0%)

**Column 3 - Occupations & Locations:**
- Top Occupations: Enterprise employees (35%), Self-employed (15%), ...
- Top Locations: Urban (63.9%), Rural (36.1%)

#### **📊 Additional Demographics** (4-column layout)

Shows distributions for:
- **Marital Status**: Married, Single, Divorced, Widowed
- **Ethnicity**: Han Chinese, Hui, Manchu, Mongol, ...
- **Political Affiliation**: Mass, Party member, Youth League, Democratic parties
- **Religion**: No religion, Buddhism, Taoism, Christianity, ...

**✅ This summary validates that your generated population matches the target demographics!**

---

### Step 8: Use or Save Personas

**Option A: Use Immediately for Simulation**
1. Click **"Continue to Simulation"** button (top right)
2. Redirects to Simulation page with personas loaded
3. Start running surveys immediately

**Option B: Save Permanently**
1. Click **"Save Permanently"** button
2. Personas saved to `data/personas/` directory
3. Can load later from "Load Existing Personas" tab
4. Persists across sessions and browser refreshes

**Option C: Export**
1. Go to Simulation page after continuing
2. Click "Export Personas" to download CSV
3. Share or archive your generated population

---

### Step 9: Iterate and Refine

**If results don't match expectations:**

1. **Check extracted demographics** - Did LLM parse correctly?
2. **Adjust your prompt** - Add more specific percentages
3. **Regenerate with different seed** - Changes random distribution
4. **Increase sample size** - Larger n = more accurate distributions

**Common adjustments:**
- ❌ "Mainly young people" → ✅ "Age 25-35, average 30 years old"
- ❌ "Most have bachelor's" → ✅ "Bachelor 50%, Master 30%, Associate 20%"
- ❌ "Urban residents" → ✅ "Urban 70%, Rural 30%"

---

## Comprehensive Prompt Examples

### 📋 What Information Does the LLM Need?

To generate accurate personas, provide as much detail as possible about:

**1. Demographics** (Who are they?)
- Age range or distribution
- Gender breakdown with percentages
- Education levels (be specific: middle school to bachelor's as primary, covering illiterate to doctorate)
- Occupation types or industries

**2. Geographic** (Where are they?)
- Urban vs rural distribution with percentages
- Specific regions, cities, or provinces
- Living arrangements (urban residents 63.89%, rural residents 36.11%)

**3. Social Status** (What's their background?)
- Marital status distribution (single/married/divorced/widowed)
- Ethnicity composition (Han Chinese 91%, ethnic minorities 9%)
- Political affiliation (mass/party member/youth league)
- Religious beliefs (no religion/Buddhism/Taoism/Christianity)

**4. Economic** (Financial situation?)
- Income levels or ranges
- Employment status
- Household income

**5. Psychological** (What do they care about?)
- Core values and beliefs
- Interests and hobbies
- Concerns or challenges
- Lifestyle preferences

**6. Context** (Additional details?)
- Health status or concerns
- Technology usage
- Family structure
- Cultural background

---

### Example 1: Chinese Population Survey with Policy Context (Most Comprehensive)

**Context Background:**
This survey targets Chinese residents for research on environmental behavior and climate action awareness in the context of China's dual carbon goals (carbon peak by 2030, carbon neutrality by 2060), aging population challenges, and severe environmental pollution concerns.

**💡 Key Features of This Example:**
- ✅ **Clear Research Context**: Explains why this population is being studied
- ✅ **Continuous Variables with Distribution Parameters**: Age (mean, range), Income (ranges with percentages)
- ✅ **Categorical Variables with Exact Percentages**: All categories sum to 100%
- ✅ **Hierarchical Structure**: Demographics → Attitudes → Behaviors → Concerns
- ✅ **LLM-Friendly Format**: Clear labels, structured sections, explicit percentages

**📊 Variable Type Guide in This Example:**

**Continuous Variables** (with suggested parameters):
- **Age**: Provide mean + standard deviation, OR range with distribution shape
  - Example: "mean age 45 years, SD=15" OR "18-75 years, normally distributed"
- **Income**: Provide ranges with percentages (ordinal categorical treated as quasi-continuous)
  - Example: "Below 30K (18%), 30K-80K (35%), 80K-150K (28%), ..."
- **Household Size**: Mean + range
  - Example: "Average 3.1 persons, range 1-7"

**Categorical Variables** (must sum to 100%):
- **Gender**: Male (X%), Female (Y%), Other (Z%)
- **Education**: List all levels with percentages
- **Marital Status**: Single (A%), Married (B%), Divorced (C%), Separated (D%), Widowed (E%)
- **Occupation**: All categories must be mutually exclusive and exhaustive

**Ordinal Variables** (ordered categories):
- **Income levels**: Low → Middle → High with clear boundaries
- **Education levels**: Illiterate → Primary → ... → Doctorate
- **Health status**: Healthy → Sub-healthy → Chronic disease → Disabled

**Likert-Scale Attitudes** (percentage agreeing):
- Importance ratings: "83% very concerned", "58% moderately concerned"
- Willingness measures: "55% willing to adopt", "30% neutral", "15% unwilling"

---

**Prompt:**

```text
BACKGROUND CONTEXT:
Study on environmental awareness and pro-environmental behaviors among Chinese residents. 
Research context: China's dual carbon goals (carbon peak by 2030, carbon neutrality by 2060), 
rapidly aging population (14.9% aged 65+), and severe environmental pollution concerns 
(air quality, water contamination, soil degradation).

TARGET POPULATION DEMOGRAPHICS:

Age Distribution (Continuous Variable):
- Range: 18-75 years old
- Mean: 45 years, Standard Deviation: 15 years
- Distribution shape: Slightly right-skewed (more older adults)
- Age groups breakdown:
  * 18-30 years: 20%
  * 31-45 years: 30%
  * 46-60 years: 35%
  * 61-75 years: 15%
- Note: Use normal distribution with mean=45, sd=15, truncated at 18 and 75

Gender (Binary Categorical): Male (48.5%), Female (51.5%)

Education (Fixed Categories with Exact Percentages):
- Primary school and below: 25%
- Middle school: 35%
- High school/Technical school: 22%
- Bachelor's degree: 14%
- Master's degree and above: 4%

Marital Status (Fixed Categories):
- Married or cohabiting: 68%
- Separated: 3%
- Never married: 20%
- Divorced: 6%
- Widowed: 3%

Geographic Distribution:
- Urban residents: 64%
- Rural residents: 36%
Primary regions: Eastern coastal provinces (Shanghai, Jiangsu, Zhejiang, Guangdong) 45%, 
Central cities (Wuhan, Changsha, Zhengzhou) 30%, Western regions (Chengdu, Xi'an, Chongqing) 25%

Ethnicity:
- Han Chinese: 91.5%
- Ethnic minorities (Hui, Manchu, Mongol, Zang, Uyghur, etc.): 8.5%

Political Affiliation:
- Mass (no affiliation): 72%
- Communist Party member: 23%
- Communist Youth League member: 4%
- Democratic party member: 1%

Religious Beliefs:
- No religious belief: 87%
- Buddhism: 7%
- Taoism: 3%
- Christianity: 2%
- Islam: 1%

Occupation Distribution:
- Enterprise employees: 32%
- Self-employed/Small business owners: 15%
- Civil servants/Public institution staff: 11%
- Migrant workers: 12%
- Farmers: 10%
- Retirees: 13%
- Students: 4%
- Unemployed/Other: 3%

Household Annual Income (CNY):
- Low income (below 30,000): 18%
- Lower-middle income (30,000-80,000): 35%
- Middle income (80,000-150,000): 28%
- Upper-middle income (150,000-300,000): 14%
- High income (above 300,000): 5%

Family Structure:
- Nuclear family (couple with children): 55%
- Three-generation household: 22%
- Empty nest elderly: 12%
- Single-person household: 8%
- Other: 3%
Average household size: 3.1 persons

Health Status:
- Healthy: 62%
- Sub-healthy (fatigue, stress, minor ailments): 28%
- Chronic disease patients (hypertension, diabetes, cardiovascular): 8%
- Disabled/Severely ill: 2%

Environmental Concerns (Ranked by Importance):
1. Air pollution and smog (83% very concerned)
2. Water safety and contamination (79% very concerned)
3. Food safety and pesticide residues (76% very concerned)
4. Climate change and extreme weather (58% very concerned)
5. Waste management and recycling (51% very concerned)

Technology Usage:
- Smartphone ownership: 93%
- Daily internet usage: 88%
- Mobile payment usage: 86%
- Social media active users: 75%
- Electric vehicle awareness: 45%

Core Values and Attitudes:
- Family harmony and filial piety: 92%
- Economic security and income growth: 78%
- Children's education: 85%
- Environmental protection importance: 62%
- Climate action urgency: 48%
- Willingness to adopt green lifestyle: 55%
- Government policy trust: 71%

Key Concerns:
- Rising cost of living and housing prices
- Healthcare accessibility and quality
- Pension security and elderly care
- Children's education competition
- Environmental health impacts on family
- Job stability and career development
- Climate change adaptation
```

**Why This Example Is Excellent:**

✅ **Clear Policy/Research Context**: Establishes the "why" (dual carbon goals, aging, pollution) upfront

✅ **Fixed Categories with Exact Percentages**: Every demographic variable has precise, mutually exclusive categories
- Education: 5 clear levels (25% + 35% + 22% + 14% + 4% = 100%)
- Marital: 5 categories with exact splits (68% + 3% + 20% + 6% + 3% = 100%)
- Age groups, income brackets, family structure - all specified with percentages

✅ **Comprehensive Coverage**: 12+ demographic dimensions plus contextual information

✅ **Research-Relevant Context**: Environmental concerns, climate attitudes, technology adoption directly tied to study objectives

✅ **Realistic Distributions**: Based on actual Chinese demographic patterns (91.5% Han, 64% urban, etc.)

✅ **Actionable for LLM**: Clear structure makes it easy for AI to parse categorical variables vs continuous variables

✅ **Values & Concerns**: Provides rich context for generating realistic persona backgrounds and behaviors

✅ **Continuous Variables Properly Specified**: Age includes mean, SD, and distribution shape for accurate generation

---

### 📘 How to Adapt This Example for Your Research

**Step 1: Define Your Research Context**
Replace the background with YOUR study objectives:
- What policy or phenomenon are you studying?
- What population behaviors/attitudes matter?
- Why is this research important?

Example templates:
- "Study on consumer purchasing behavior in the context of [policy/trend]"
- "Research on health-seeking behaviors among [population] facing [challenge]"
- "Investigation of social attitudes toward [topic] in [context]"

**Step 2: Specify Continuous Variables with Distribution Parameters**

For **Age**:
```
Age: [min]-[max] years, mean=[X], standard deviation=[Y]
Distribution: [normal/uniform/skewed]
Age groups: [list percentages for each bracket]
```

For **Income** (if continuous):
```
Annual income: mean=[X] CNY, median=[Y] CNY
Range: [min]-[max]
Distribution: right-skewed (common for income)
OR provide brackets: <30K (%), 30-80K (%), 80-150K (%), >150K (%)
```

For **Household Size**:
```
Household size: mean=[X], range=[min]-[max]
Distribution: [1 person (%), 2-3 (%), 4-5 (%), 6+ (%)]
```

For **Years of Experience/Education**:
```
Work experience: mean=[X] years, SD=[Y]
Range: [min]-[max] years
```

**Step 3: Define Categorical Variables (Must Sum to 100%)**

✅ **Good Example** (mutually exclusive, exhaustive):
```
Marital Status:
- Never married: 20%
- Married/Cohabiting: 68%
- Separated: 3%
- Divorced: 6%
- Widowed: 3%
Total: 100% ✓
```

❌ **Bad Example** (overlapping, incomplete):
```
Marital Status:
- Married: 70%
- Single: 25%
Total: 95% ✗ (missing 5%, what category?)
```

**Step 4: Add Ordinal Variables with Clear Ordering**

For **Education Levels**:
```
Education (from lowest to highest):
- Illiterate/No formal education: X%
- Primary school (1-6 years): Y%
- Middle school (7-9 years): Z%
- High school/Technical (10-12 years): W%
- Bachelor's degree (13-16 years): V%
- Master's degree (17-19 years): U%
- Doctoral degree (20+ years): T%
Total: 100%
```

For **Income Categories** (ordinal):
```
Household Annual Income (CNY):
- Low income (<30,000): 18%
- Lower-middle (30,000-80,000): 35%
- Middle (80,000-150,000): 28%
- Upper-middle (150,000-300,000): 14%
- High income (>300,000): 5%
Total: 100%
```

**Step 5: Include Attitude Variables (Likert-Scale or Percentage Agreement)**

For **Concerns/Importance**:
```
Environmental Concerns (Ranked by % very concerned):
1. Air pollution: 83% very concerned, 12% somewhat, 5% not concerned
2. Water safety: 79% very concerned, 15% somewhat, 6% not concerned
3. Food safety: 76% very concerned, 18% somewhat, 6% not concerned
```

For **Behavioral Intentions**:
```
Willingness to adopt green lifestyle:
- Very willing: 25%
- Somewhat willing: 30%
- Neutral: 25%
- Somewhat unwilling: 12%
- Very unwilling: 8%
Total: 100%
```

**Step 6: Add Contextual Variables for Rich Backgrounds**

Include qualitative information that helps LLM generate realistic narratives:
- **Technology usage**: "93% own smartphones, 88% daily internet users"
- **Health status**: "62% healthy, 28% sub-healthy, 8% chronic disease, 2% disabled"
- **Family structure**: "55% nuclear family, 22% three-generation, 12% empty nest elderly"
- **Values ranking**: "Family harmony (92% prioritize), Economic security (78%), Education (85%)"

**Step 7: Specify Sample Size and Validation Checks**

Add at the end:
```
TARGET SAMPLE SIZE: [N] personas

VALIDATION REQUIREMENTS:
- All categorical variables must match specified percentages (±2% tolerance)
- Age distribution should follow normal(mean=45, sd=15)
- No logical inconsistencies (e.g., 20-year-old retiree, illiterate PhD holder)
- Personas should reflect research context and background
```

---

### 🎯 Quick Checklist for Your Prompt

Before submitting your prompt, verify:

**Continuous Variables:**
- [ ] Age: min, max, mean, SD specified?
- [ ] Income: ranges or mean/median provided?
- [ ] Other continuous vars: distribution shape noted?

**Categorical Variables:**
- [ ] All categories mutually exclusive?
- [ ] Percentages sum to 100%?
- [ ] "Other" category included if needed?

**Ordinal Variables:**
- [ ] Clear ordering from low to high?
- [ ] Boundaries between categories defined?
- [ ] No gaps or overlaps in ranges?

**Context Information:**
- [ ] Research background explained?
- [ ] Target population clearly described?
- [ ] Relevant attitudes/behaviors included?

**Validation:**
- [ ] Sample size specified?
- [ ] Tolerance levels noted (e.g., ±2%)?
- [ ] Logical consistency requirements stated?

---

### Example 2: Healthcare Workers

**Prompt:**

```
Nurses and healthcare workers, ages 28-55, with peak distribution at 35-45 years old. 
Gender: Female (80%), Male (20%).

Education: Most have bachelor's or associate degrees in nursing (75%), some have master's 
degrees in healthcare administration (15%), others have diploma or certificate programs (10%).

Location: Working in urban hospitals (85%) and rural healthcare centers (15%). Primarily 
located in major metropolitan areas: New York, Los Angeles, Chicago, Houston.

Marital Status: Married (65%), Single (25%), Divorced (8%), Widowed (2%).

Occupation: Registered Nurses (60%), Licensed Practical Nurses (20%), Nurse Practitioners (10%), 
Healthcare Administrators (5%), Other medical support staff (5%).

Income: $45K-$85K annually, with RNs averaging $65K and NPs averaging $95K.

Values: Patient care (highest priority), work-life balance, professional development, 
healthcare access, compassion, ethical practice.

Challenges: Long working hours (often 12-hour shifts), high stress environments, 
emotional burnout, understaffing issues, exposure to illnesses.

Health: Generally health-conscious but experience higher rates of back pain, 
stress-related conditions, and sleep disorders due to shift work.

Interests: Medical continuing education, fitness and wellness, family time, 
reading (especially medical journals), volunteer work in community health.
```

**What This Extracts:**
- Age: 28-55 range with normal distribution
- Gender: 80/20 female/male split
- Education: 3 levels with specific percentages
- Location: Urban/rural 85/15 split
- Occupation: 5 specific roles with percentages
- Plus: income, values, challenges for rich backgrounds

---

### Example 3: Tech Professionals

**Prompt:**

```text
Tech industry professionals, age 25-40, average age 32. Gender: Male (65%), Female (35%).

Education: Bachelor's degree 50%, Master's degree 40%, Doctorate 7%, Associate degree or below 3%.
Major fields: Computer Science, Software Engineering, Data Science, Information Technology.

Location: Tier-1 cities 70% (Beijing 30%, Shanghai 25%, Shenzhen 15%), New tier-1 cities 25% 
(Hangzhou, Chengdu, Xi'an), Other cities 5%. Urban 98%, Rural 2%.

Marital Status: Single 55%, Married 40%, Divorced 4%, Widowed 1%.

Occupation: Software Engineer 45%, Product Manager 15%, Data Analyst 12%, UI/UX Designer 10%, 
Project Manager 8%, Technical Management 5%, Other 5%.

Income: Annual salary 150K-300K CNY (40%), 300K-500K (35%), 500K-800K (15%), 
Above 800K (7%), Below 150K (3%).

Ethnicity: Han Chinese 95%, Ethnic minorities 5%.

Political Affiliation: Mass 75%, Party member 18%, Youth League 6%, Other 1%.

Religion: No religion 95%, Buddhism 2%, Christianity 2%, Other 1%.

Work: 50-60 hours per week, flexible schedule, remote work option available.

Technical Skills: Proficient in at least 2 programming languages, familiar with cloud platforms, 
understand AI/ML basics.

Core Values: Technical innovation, career development, high compensation, work flexibility, 
lifelong learning, tech community participation.

Lifestyle: Efficiency-focused, tech-dependent, prefer online shopping and food delivery, 
follow tech news, participate in open source projects, active in tech forums.

Concerns: Career advancement, skill development, industry trends, work stress, 
work-life balance, stock options.

Health: Sub-healthy 35% (neck pain, back pain, vision decline, sleep deprivation), 
Healthy 60%, Other 5%.

Interests: Programming, gaming, tech product reviews, outdoor sports (running, cycling), 
reading tech books, attending tech conferences and meetups.
```

**Why This Is Comprehensive:**
- ✅ 9 demographic dimensions with exact percentages
- ✅ Occupation breakdown with 7 specific roles
- ✅ Income stratification with 5 levels
- ✅ Work environment details (hours, remote work)
- ✅ Technology skills and proficiency
- ✅ Lifestyle patterns and behaviors
- ✅ Health considerations specific to the profession

---

### Example 4: College Students

**Prompt:**

```
College students aged 18-24 in California universities. 
Age distribution: 18-19 (25%), 20-21 (35%), 22-23 (30%), 24+ (10%).
Gender: Female (60%), Male (40%).

Education: Currently enrolled - Freshman (25%), Sophomore (25%), Junior (25%), Senior (20%), 
Graduate students (5%).

Major fields: STEM (35%), Business (20%), Social Sciences (15%), Arts & Humanities (12%), 
Health Sciences (10%), Education (5%), Other (3%).

Location: Urban campuses (70%), Suburban campuses (25%), Rural campuses (5%).
Geographic origin: California residents (70%), Out-of-state domestic (20%), International (10%).

Ethnicity: Hispanic/Latino (40%), White (30%), Asian (20%), Black/African American (5%), 
Other (5%).

Marital Status: Single (95%), Married (4%), Other (1%).

Family Income: $0-30K (15%), $30K-75K (25%), $75K-150K (35%), $150K+ (25%).

Housing: On-campus dorms (40%), Off-campus apartments (35%), Living with parents (20%), 
Other (5%).

Employment: Not employed (40%), Part-time work (45%), Full-time work (10%), Internships (5%).

Financial: Receiving financial aid (60%), Student loans (45%), Scholarships (30%), 
Family support (70%).

Values: Education and career success (highest), Work-life balance, Social responsibility, 
Diversity and inclusion, Environmental sustainability, Mental health awareness.

Technology: Smartphone ownership (99%), Laptop ownership (95%), Social media usage (95%), 
Online learning platforms (90%), Video streaming (95%).

Concerns: Academic performance, Career prospects, Student debt, Mental health, 
Cost of living, Social connections.

Interests: Social media, Music and concerts, Sports and fitness, Video games, 
Travel, Volunteering, Campus clubs and organizations.

Health: Generally healthy (80%), Mental health concerns (anxiety 25%, depression 15%), 
Sleep deprivation (40%), Stress-related issues (35%).
```

**Key Features:**
- Age sub-groups with percentages
- Academic year distribution
- Major field breakdown
- Multiple geographic dimensions
- Ethnicity diversity
- Detailed financial context
- Technology adoption rates
- Mental health considerations

---

### Example 5: Senior Citizens

**Prompt:**

```
退休老年人群体，年龄65-85岁。年龄段分布：65-70岁占35%，71-75岁占30%，76-80岁占20%，81-85岁占15%。
性别：Female (55%), Male (45%)。

教育水平：初中及以下占45%，高中占30%，本科占20%，硕士及以上占5%。

居住地：城镇居民60%，农村居民40%。地区分布：东部地区40%，中部地区30%，西部地区20%，东北地区10%。

婚姻状况：已婚占60%，丧偶占35%，离异占4%，未婚占1%。

民族：汉族93%，少数民族7%。

政治面貌：群众55%，党员40%，民主党派4%，团员1%。

宗教信仰：无宗教信仰70%，佛教20%，道教5%，基督教3%，其他2%。

退休前职业：企业职工35%，公务员和事业单位25%，农民20%，个体工商户10%，
教师8%，其他2%。

收入来源：退休金/养老金占主要来源（平均每月2000-4000元）。低收入（2000以下）30%，
中等收入（2000-4000）45%，中高收入（4000-6000）15%，高收入（6000以上）10%。

居住安排：与配偶同住占50%，独居占20%，与子女同住占25%，养老院占3%，其他占2%。

家庭结构：有子女占95%（平均2.1个子女），有孙子女占85%。

健康状况：健康占30%，患有慢性病占60%（高血压、糖尿病、心脏病、关节炎等），
失能/半失能占8%，其他占2%。

日常活动：广场舞/健身操40%，看电视/听广播80%，照顾孙辈50%，社区活动30%，
打牌/下棋25%，园艺/养花20%，志愿服务15%，旅游10%。

技术使用：智能手机使用60%（主要用于微信、视频通话），互联网使用40%，
电子支付使用35%，不使用智能设备40%。

核心价值观：重视家庭和睦（95%），关注健康养生（90%），追求晚年幸福（85%），
注重传统文化（70%），关心社区邻里（65%）。

主要关注：身体健康、医疗保障、养老金充足性、子女发展、孙辈教育、
防诈骗安全、社交活动、晚年生活质量。

生活节奏：早睡早起（平均6:00起床，21:00就寝），规律饮食，注重养生保健，
参与社区活动，保持社交联系。
```

**Comprehensive Coverage:**
- Age sub-groups within senior range
- Detailed health status (critical for this demographic)
- Living arrangements and family structure
- Technology adoption (generational digital divide)
- Daily activities and lifestyle
- Financial situation (retirement income)
- Values specific to life stage

---

## 🎯 Tips for Writing Effective Prompts

### ✅ DO:
- **Use percentages** whenever possible (Male 51.24%, Female 48.76%)
- **Specify ranges** for continuous variables (age 25-35, income $50K-$80K)
- **Include distribution keywords** (为主, 涵盖, 包括, 从...到...)
- **Provide context** (why this matters, what they care about)
- **Be specific** about categories (初中, 高中, 本科 instead of just "educated")
- **Cover multiple dimensions** (at least 5-6 demographic fields)
- **Add qualitative details** (values, concerns, behaviors)

### ❌ DON'T:
- Use vague terms ("some", "many", "most" without numbers)
- Omit important demographics (age, gender, education basics)
- Provide contradictory information
- Use only English OR Chinese - mixing is fine!
- Forget about context (lifestyle, values, concerns)
- Leave out percentages when you have them

### 💡 Pro Tips:
1. **Start with the basics**: Age, gender, education, location
2. **Add social context**: Marital status, ethnicity, religion, political affiliation
3. **Include economic info**: Income, employment, financial situation
4. **Describe lifestyle**: Technology use, interests, daily activities
5. **Explain values**: What matters to them, what they worry about
6. **Mention health**: Physical and mental health considerations

---

## Technical Implementation

### Architecture Overview

```
User Input (Natural Language)
         ↓
AI Extraction (LLM Analysis)
         ↓
JSON Demographic Data
         ↓
Intelligent Parsers (7+ specialized parsers)
         ↓
Statistical Distributions
         ↓
PersonaGenerator Engine
         ↓
Generated Personas (with coherent backgrounds)
```

### Files Modified

1. **`src/persona_generator.py`** (952 lines)
   - `extract_demographics_with_ai()` - AI extraction with specialized prompt
   - `generate_personas_from_ai_extraction()` - Distribution creation and generation
   - `_generate_background()` - Coherent Chinese narrative generation
   - **7 Intelligent Parsers**:
     - Education parser (handles range keywords like "涵盖", "至")
     - Location parser (extracts urban/rural percentages)
     - Gender parser (regex for exact percentages)
     - Marital status parser (keyword detection + weighting)
     - Ethnicity parser (汉族 + minorities)
     - Political affiliation parser (党员/团员/群众)
     - Religion parser (5+ major religions)

2. **`pages/1_Setup.py`** (1413 lines)
   - AI-Powered Extraction tab UI
   - Demographics extraction and display
   - Comprehensive statistics summary (9 dimensions)
   - Integration with PersonaManager
   - `Persona.from_dict()` for preserving all fields including dynamic attributes

3. **`src/persona.py`** (272 lines)
   - Extended Persona dataclass with 4 new fixed fields
   - `_extra_attributes` for unlimited dynamic fields
   - `__setattr__`/`__getattr__` for dynamic attribute handling
   - `from_dict()` class method for proper deserialization

### Key Functions

#### `extract_demographics_with_ai(text_input, llm_client, model)`

**Purpose**: Extract structured demographic data from natural language

**Process**:
1. Sends specialized prompt to LLM with temperature=0.3
2. Instructs LLM to return ONLY JSON (no markdown, no explanations)
3. Parses JSON response with error handling
4. Returns dict with demographic fields

**Extracted Fields**:
- age, gender, occupation, education
- location, marital_status, ethnicity
- political_affiliation, religion
- income, family, health, technology
- interests, values, sample_size

#### `generate_personas_from_ai_extraction(extracted_data, n, seed)`

**Purpose**: Convert extracted demographics into statistical distributions and generate personas

**Process**:
1. Creates PersonaGenerator instance
2. Parses each demographic field with specialized parser
3. Creates DistributionConfig for each attribute
4. Generates n personas with coherent backgrounds
5. Returns list of persona dictionaries with all fields

**Intelligence Features**:
- Range detection: "Middle school to bachelor's" → includes all levels between
- Percentage extraction: "Male 51.24%" → exact float parsing
- Keyword weighting: "primarily" keywords → boost weight by 1.8x
- Default distributions: Fallback to reasonable defaults if parsing fails

#### `_generate_background(age, education, occupation, marital_status, location, ...)`

**Purpose**: Generate coherent narrative backgrounds (supports Chinese and English)

**Features**:
- Demographic-aware descriptions (e.g., married + urban + bachelor's → contextual narrative)
- Context integration (income, family, health, technology usage)
- Natural language flow tailored to demographic attributes
- Consistent with all demographic attributes

### Intelligent Parser Details

#### 1. Education Parser (Lines 633-680)

```python
# Detects range keywords: 涵盖, 包括, 从, 到, 至
has_range = any(keyword in education_str for keyword in ['涵盖', '包括', '从', '到', '至'])

if has_range:
    # Include ALL 7 levels: illiterate, primary, middle, high, bachelor, master, doctorate
    # Boost weights for levels mentioned with primary keywords
```

**Input**: "Mainly middle school to bachelor's degree, covering illiterate to doctorate"

**Output**: All 7 levels with weights → Middle school(32%), Bachelor(35%), others(33%)

#### 2. Gender Parser (Lines 588-631)

```python
# Regex: r'male[:\s]*\(?(\d+\.?\d*)\s*%'
male_match = re.search(r'male[:\s]*\(?(\d+\.?\d*)\s*%', gender_str, re.IGNORECASE)
```

**Input**: "Gender: Male (51.24%), Female (48.76%)"

**Output**: Exact distribution [0.5124, 0.4876]

#### 3. Location Parser (Lines 682-710)

```python
# Regex: r'城镇[居民]*[占]*\s*(\d+\.?\d*)\s*%' (supports Chinese keywords)
urban_match = re.search(r'城镇[居民]*[占]*\s*(\d+\.?\d*)\s*%', location_str)
```

**Input**: "Urban residents 63.89%, rural residents 36.11%"

**Output**: ['Urban', 'Rural'] with [0.6389, 0.3611]

#### 4-7. Status Parsers (Lines 712-820)

Similar pattern for:
- Marital status (Single/Married/Divorced/Widowed)
- Ethnicity (Han Chinese + 55 ethnic minorities)
- Political affiliation (Mass/Party member/Youth League/Democratic parties)
- Religion (No religion/Buddhism/Taoism/Christianity/Islam)

### AI Prompt Design

**Temperature**: 0.3 (for consistent, deterministic extraction)

**Instructions**:
- Extract specific demographic fields from natural language
- Return ONLY valid JSON (no markdown code blocks, no explanations)
- Use null for missing fields
- Include all mentioned attributes
- Preserve exact percentages and ranges

**Example Output Format**:
```json
{
  "age": "25-35",
  "gender": "Male (51.24%), Female (48.76%)",
  "education": "初中至本科学历为主，涵盖文盲到博士",
  "occupation": "企业员工, 个体工商户, 公务员",
  "location": "城镇居民63.89%, 农村居民36.11%",
  "marital_status": "已婚68%, 未婚22%, 离异8%, 丧偶2%",
  "ethnicity": "汉族91%, 少数民族9%",
  "political_affiliation": "群众70%, 党员25%, 团员4%, 民主党派1%",
  "religion": "无宗教信仰85%, 佛教8%, 道教3%, 基督教2%, 伊斯兰教1%",
  "sample_size": 1000
}
```

## Demographics Summary Table

After generating personas, a comprehensive **Population Demographics Summary** is automatically displayed with the following information:

### Column 1: Age Statistics 📈
- **Mean Age**: Average age of the population
- **Age Range**: Minimum to maximum age
- **Age Groups**: Distribution across age brackets:
  - 18-25
  - 26-35
  - 36-45
  - 46-55
  - 56-65
  - 65+
- Shows count and percentage for each group

### Column 2: Gender & Education ⚧🎓
- **Gender Distribution**: Breakdown with counts and percentages
- **Education Levels**: Top 3 education levels with counts and percentages

### Column 3: Occupations & Locations 💼📍
- **Top Occupations**: Top 5 most common occupations with percentages
- **Top Locations**: Top 3 geographic locations with percentages

This summary helps you verify that the generated population matches your target demographics before using them in simulations.

## Benefits

1. **Speed**: Generate personas from text in seconds
2. **Accuracy**: AI extracts nuanced demographic details
3. **Flexibility**: Works with any text description
4. **Natural**: No need to understand statistical distributions
5. **Comprehensive**: Captures both numeric and categorical attributes
6. **Verification**: Demographics summary table validates generated population

## Limitations

1. Requires active LLM connection
2. Quality depends on LLM capabilities
3. May need multiple attempts for complex descriptions
4. JSON parsing can fail if LLM response is malformed

## Future Enhancements

- [ ] Support for uploading research papers/PDFs
- [ ] Multi-language support for input text
- [ ] Ability to refine/edit extracted demographics before generation
- [ ] Save extraction templates for reuse
- [ ] Batch processing multiple text descriptions
- [ ] Integration with external demographic databases

## Testing

Run the test script to verify installation:
```bash
python3 test_ai_extraction.py
```

Then test in the UI:
```bash
streamlit run app.py
```

## Troubleshooting

**Issue**: "LLM not connected" warning
- **Solution**: Go to Home page and connect to LLM first

**Issue**: "Failed to parse AI response as JSON"
- **Solution**: Try again with clearer text, or check LLM logs

**Issue**: Extracted demographics look incorrect
- **Solution**: Provide more specific details in your input text

**Issue**: Generated personas don't match description
- **Solution**: Review extracted demographics and regenerate with different seed

## License
Same as parent project

## Questions?
Please open an issue on GitHub with the tag "ai-extraction"
