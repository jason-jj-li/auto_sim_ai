# 🎨 Design System - LLM Simulation Survey System

## Overview
Professional, enterprise-grade design system applied across all pages of the LLM Simulation Survey System.

---

## 🌈 Color Palette

### Primary Colors
```css
--gradient-primary-start: #667eea;  /* Purple Blue */
--gradient-primary-end: #764ba2;    /* Deep Purple */
--gradient-accent-start: #4facfe;   /* Sky Blue */
--gradient-accent-end: #00f2fe;     /* Cyan */
```

### Status Colors
```css
--success: #4caf50;   /* Green */
--info: #2196f3;      /* Blue */
--warning: #ff9800;   /* Orange */
--error: #f44336;     /* Red */
```

### Neutral Colors
```css
--text-primary: #333;
--text-secondary: #666;
--border: #e0e0e0;
--background: #f8f9fa;
--card-bg: #ffffff;
```

---

## 🎯 Components

### 1. Hero Section
**Used on:** All pages

```html
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    color: white;
">
    <h1>Page Title</h1>
    <p>Page description...</p>
</div>
```

**Features:**
- Purple gradient background
- Large, bold typography
- Drop shadow for depth
- Rounded corners (16px)
- White text with opacity variants

---

### 2. Status Cards
**Used on:** Setup, Results pages

```html
<div style="
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    text-align: center;
">
    <div style="font-size: 2.5rem; font-weight: 700; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;">
        123
    </div>
    <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">
        Metric Label
    </div>
</div>
```

**Features:**
- Gradient number display
- Uppercase labels with letter spacing
- Subtle shadow
- Hover effects (in CSS)
- 4-column responsive grid

---

### 3. Info Cards
**Used on:** All pages for section headers

```html
<div style="
    background: white;
    border-left: 4px solid #667eea;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
">
    <h3 style="color: #667eea; font-size: 1.3rem; margin: 0;">
        Section Title
    </h3>
</div>
```

**Features:**
- Left border accent (4px, brand color)
- Subtle shadow
- Clean typography
- Consistent padding

---

### 4. Welcome/Info Banners
**Used on:** Home, Setup pages

```html
<div style="
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    text-align: center;
">
    <h3 style="color: white; margin-top: 0;">Title</h3>
    <p style="color: rgba(255,255,255,0.95);">Message</p>
</div>
```

**Features:**
- Cyan gradient (different from hero)
- Center-aligned text
- White text with opacity
- Friendly, approachable tone

---

### 5. Progress Indicators

```html
<div class="progress-step completed">
    <span>✓</span>
</div>
```

```css
.progress-step {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #e0e0e0;
    color: #666;
    font-weight: 600;
}

.progress-step.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.progress-step.completed {
    background: #4caf50;
    color: white;
}
```

**States:**
- Not started (gray)
- Active (gradient)
- Completed (green)

---

## 📏 Typography

### Headings
```css
h1 {
    font-size: 2.5rem - 2.8rem;
    font-weight: 700;
    line-height: 1.2;
}

h2 {
    font-size: 1.8rem;
    font-weight: 600;
}

h3 {
    font-size: 1.3rem;
    font-weight: 600;
    color: #667eea;
}
```

### Body Text
```css
p {
    font-size: 1rem - 1.1rem;
    line-height: 1.6 - 1.8;
    color: #333;
}

.caption {
    font-size: 0.9rem;
    color: #666;
}
```

### Labels
```css
.label {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #666;
}
```

---

## 🎯 Spacing System

```css
--spacing-xs: 0.5rem;   /* 8px */
--spacing-sm: 1rem;     /* 16px */
--spacing-md: 1.5rem;   /* 24px */
--spacing-lg: 2rem;     /* 32px */
--spacing-xl: 3rem;     /* 48px */
```

**Card Padding:** 1.5rem  
**Hero Padding:** 2.5rem horizontal, 2rem vertical  
**Section Margins:** 1.5rem - 2rem  

---

## 🔲 Border Radius

```css
--radius-sm: 8px;    /* Info cards, inputs */
--radius-md: 12px;   /* Status cards, containers */
--radius-lg: 16px;   /* Hero sections */
--radius-full: 50%;  /* Progress indicators, avatars */
```

---

## 💫 Shadows

```css
/* Subtle - Info cards */
box-shadow: 0 2px 8px rgba(0,0,0,0.05);

/* Medium - Status cards */
box-shadow: 0 4px 12px rgba(0,0,0,0.08);

/* Strong - Hero sections */
box-shadow: 0 10px 30px rgba(0,0,0,0.1);

/* Hover - Interactive cards */
box-shadow: 0 8px 20px rgba(0,0,0,0.12);
```

---

## 🎭 Button Styles

### Primary Button
```css
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 8px;
    font-weight: 500;
    padding: 0.5rem 2rem;
    transition: all 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}
```

### Secondary Button
```css
.stButton > button {
    border-radius: 8px;
    font-weight: 500;
}
```

---

## 📱 Responsive Grid

### Desktop (> 1024px)
- 4-column status cards
- 3-column settings
- 2-column forms

### Tablet (768px - 1024px)
- 2-column status cards
- 2-column settings
- 1-column forms

### Mobile (< 768px)
- 1-column everything
- Stack all grids
- Full-width buttons

---

## 🎨 Page-Specific Designs

### Home Page (`app.py`)
- **Hero:** Purple gradient with system title
- **Welcome Banner:** Cyan gradient for new users
- **Connection Card:** Info card style

### Setup Page (`1_Setup.py`)
- **Hero:** Purple gradient
- **Status Grid:** 4 metric cards (Total, Saved, Uploaded, Generated)
- **Color Coding:**
  - Total: Gradient
  - Saved: Green
  - Uploaded: Blue
  - Generated: Orange

### Simulation Page (`2_Simulation.py`)
- **Hero:** Purple gradient
- **Mode Info Card:** Clean white card with border accent
- **Form Sections:** Organized with info cards

### Results Page (`3_Results.py`)
- **Hero:** Purple gradient
- **Empty State:** Cyan gradient banner
- **Stats Grid:** 4 cards (Simulations, Surveys, Interventions, Responses)
- **Color Coding:**
  - Total: Gradient
  - Surveys: Green
  - Interventions: Blue
  - Responses: Orange

---

## ✨ Animations & Transitions

```css
/* Standard transition */
transition: all 0.3s ease;

/* Hover lift */
transform: translateY(-2px);
transform: translateY(-4px);

/* Shadow expansion */
box-shadow: 0 4px 12px → 0 8px 20px;

/* Color transitions */
border-color: #e0e0e0 → #667eea;
```

---

## 🎯 Hover States

### Cards
```css
.status-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}
```

### Buttons
```css
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}
```

### Inputs
```css
.stTextInput > div > div > input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}
```

---

## 📋 Tabs Enhancement

```css
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #f8f9fa;
    padding: 0.5rem;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    background-color: white;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white !important;
}
```

---

## 🔧 Implementation Notes

### Global Styles
Applied via `src/styles.py` → `apply_global_styles()`

### Inline Styles
Used for component-specific designs (Hero sections, status cards)

### Streamlit Native
Enhanced with custom CSS where needed

### Consistency
- All pages use same hero style
- All status cards use same structure
- All info cards use same accent color
- All buttons use gradient on primary type

---

## 🎨 Best Practices

1. **Use Gradient Sparingly:** Hero sections and primary buttons only
2. **Maintain Hierarchy:** Hero > Section headers > Content
3. **Consistent Spacing:** Use spacing system values
4. **Shadow Depth:** Subtle for most, strong for hero only
5. **Color Meaning:** Green = success, Blue = info, Orange = warning
6. **White Space:** Don't overcrowd - let content breathe
7. **Typography Scale:** Clear h1 > h2 > h3 > p hierarchy
8. **Interactive Feedback:** All buttons and cards have hover states

---

## 📊 Usage Statistics

- **Total Pages Redesigned:** 4 (Home, Setup, Simulation, Results)
- **Components Created:** 10+ (Hero, Status Cards, Info Cards, Progress Indicators, etc.)
- **Color Palette:** 12 defined colors
- **Typography Styles:** 6 heading/body combinations
- **Spacing Values:** 5 standardized sizes
- **Shadow Depths:** 4 levels

---

## 🚀 Future Enhancements

1. **Dark Mode:** Toggle for dark theme
2. **Custom Themes:** User-selectable color schemes
3. **Animation Library:** Consistent micro-interactions
4. **Component Library:** Reusable React/Streamlit components
5. **Accessibility:** WCAG AA compliance
6. **Mobile App:** Native mobile design system
7. **Print Styles:** Optimized for PDF export

---

**Design Philosophy:** Professional, modern, approachable - enterprise SaaS quality with academic research credibility.
