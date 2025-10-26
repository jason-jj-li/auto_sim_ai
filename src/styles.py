"""全局UI样式定义 - 现代化设计系统

This module provides a unified design system for all Streamlit pages.
Includes color palette, typography, button styles, and component styles.
"""

GLOBAL_STYLES = """
<style>
    /* ========================================
       设计系统变量 (Design System Variables)
       ======================================== */
    :root {
        /* 主色调 (Primary Colors) */
        --primary: #3b82f6;
        --primary-hover: #2563eb;
        --primary-light: #eff6ff;
        
        /* 语义色彩 (Semantic Colors) */
        --success: #22c55e;
        --success-light: #dcfce7;
        --warning: #f59e0b;
        --warning-light: #fef3c7;
        --error: #ef4444;
        --error-light: #fee2e2;
        --info: #3b82f6;
        --info-light: #dbeafe;
        
        /* 灰度色彩 (Gray Scale) */
        --gray-50: #f8fafc;
        --gray-100: #f1f5f9;
        --gray-200: #e2e8f0;
        --gray-300: #cbd5e1;
        --gray-400: #94a3b8;
        --gray-500: #64748b;
        --gray-600: #475569;
        --gray-700: #334155;
        --gray-800: #1e293b;
        --gray-900: #0f172a;
        
        /* 阴影 (Shadows) */
        --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        
        /* 圆角 (Border Radius) */
        --radius-sm: 4px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;
        --radius-full: 9999px;
        
        /* 间距 (Spacing) */
        --space-xs: 0.25rem;
        --space-sm: 0.5rem;
        --space-md: 1rem;
        --space-lg: 1.5rem;
        --space-xl: 2rem;
    }
    
    /* ========================================
       全局重置 (Global Resets)
       ======================================== */
    .stApp {
        background: #ffffff;
    }
    
    /* 隐藏侧边栏 (使用顶部导航) */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* ========================================
       字体系统 (Typography)
       ======================================== */
    h1 {
        font-size: 2.25rem;
        font-weight: 700;
        color: var(--gray-900);
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    h2 {
        font-size: 1.875rem;
        font-weight: 600;
        color: var(--gray-900);
        margin-bottom: 0.75rem;
        line-height: 1.3;
    }
    
    h3 {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--gray-800);
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    p, .stMarkdown {
        line-height: 1.6;
        color: var(--gray-700);
    }
    
    /* ========================================
       按钮样式 (Button Styles)
       ======================================== */
    
    /* 主要按钮 (Primary Button) */
    .stButton button[kind="primary"] {
        background: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md);
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
        box-shadow: var(--shadow-sm);
    }
    
    .stButton button[kind="primary"]:hover {
        background: var(--primary-hover) !important;
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }
    
    /* 次要按钮 (Secondary Button) */
    .stButton button[kind="secondary"] {
        background: white !important;
        color: var(--gray-700) !important;
        border: 1px solid var(--gray-300) !important;
        border-radius: var(--radius-md);
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton button[kind="secondary"]:hover {
        background: var(--gray-50) !important;
        border-color: var(--gray-400) !important;
    }
    
    /* 禁用按钮 */
    .stButton button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    
    /* ========================================
       卡片样式 (Card Styles)
       ======================================== */
    .card {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
    }
    
    .card:hover {
        box-shadow: var(--shadow-md);
    }
    
    .card-header {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--gray-900);
        margin-bottom: var(--space-md);
    }
    
    /* ========================================
       Alert/Info 样式 (Alert Styles)
       ======================================== */
    .stAlert {
        border-radius: var(--radius-md);
        border: none;
        padding: var(--space-md);
    }
    
    /* Success Alert */
    div[data-baseweb="notification"][kind="success"] {
        background-color: var(--success-light);
        border-left: 4px solid var(--success);
    }
    
    /* Info Alert */
    div[data-baseweb="notification"][kind="info"] {
        background-color: var(--info-light);
        border-left: 4px solid var(--info);
    }
    
    /* Warning Alert */
    div[data-baseweb="notification"][kind="warning"] {
        background-color: var(--warning-light);
        border-left: 4px solid var(--warning);
    }
    
    /* Error Alert */
    div[data-baseweb="notification"][kind="error"] {
        background-color: var(--error-light);
        border-left: 4px solid var(--error);
    }
    
    /* ========================================
       输入框样式 (Input Styles)
       ======================================== */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select {
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--gray-300) !important;
        transition: all 0.2s ease;
    }
    
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stSelectbox select:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px var(--primary-light) !important;
    }
    
    /* ========================================
       Tabs 样式 (Tab Styles)
       ======================================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid var(--gray-200);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-md) var(--radius-md) 0 0;
        padding: 0.5rem 1rem;
        color: var(--gray-600);
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-light);
        color: var(--primary);
    }
    
    /* ========================================
       Expander 样式 (Expander Styles)
       ======================================== */
    .streamlit-expanderHeader {
        border-radius: var(--radius-md);
        background-color: var(--gray-50);
        border: 1px solid var(--gray-200);
        font-weight: 500;
        color: var(--gray-800);
    }
    
    .streamlit-expanderHeader:hover {
        background-color: var(--gray-100);
    }
    
    /* ========================================
       Metric 样式 (Metric Styles)
       ======================================== */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: var(--gray-900);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        color: var(--gray-500);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.875rem;
    }
    
    /* ========================================
       DataFrame 样式 (DataFrame Styles)
       ======================================== */
    .stDataFrame {
        border-radius: var(--radius-md);
        overflow: hidden;
        border: 1px solid var(--gray-200);
    }
    
    /* ========================================
       导航栏样式 (Navigation Bar Styles)
       ======================================== */
    .nav-container {
        background: #ffffff;
        border-bottom: 1px solid var(--gray-200);
        padding: 0.75rem 0;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-sm);
    }
    
    /* ========================================
       状态标签 (Status Badge)
       ======================================== */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: var(--radius-full);
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .status-connected {
        background: var(--success-light);
        color: var(--success);
    }
    
    .status-disconnected {
        background: var(--error-light);
        color: var(--error);
    }
    
    /* ========================================
       加载动画 (Loading Animation)
       ======================================== */
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    .loading-shimmer {
        animation: shimmer 2s infinite;
        background: linear-gradient(
            to right,
            var(--gray-100) 4%,
            var(--gray-200) 25%,
            var(--gray-100) 36%
        );
        background-size: 1000px 100%;
    }
    
    /* ========================================
       响应式设计 (Responsive Design)
       ======================================== */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.875rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        .card {
            padding: var(--space-md);
        }
    }
</style>
"""


def apply_global_styles():
    """应用全局样式到当前Streamlit页面
    
    在每个页面的顶部调用此函数以应用统一的设计系统。
    
    Example:
        ```python
        import streamlit as st
        from src.styles import apply_global_styles
        
        st.set_page_config(...)
        apply_global_styles()
        ```
    """
    import streamlit as st
    st.markdown(GLOBAL_STYLES, unsafe_allow_html=True)


# 可复用的HTML组件
def create_card(content: str, header: str = None) -> str:  # type: ignore
    """创建卡片样式的HTML
    
    Args:
        content: 卡片内容
        header: 可选的卡片标题
        
    Returns:
        HTML字符串
    """
    header_html = f'<div class="card-header">{header}</div>' if header else ''
    return f'''
    <div class="card">
        {header_html}
        {content}
    </div>
    '''


def create_status_badge(status: str, text: str) -> str:
    """创建状态标签
    
    Args:
        status: 状态类型 ('connected', 'disconnected', 'warning')
        text: 显示文本
        
    Returns:
        HTML字符串
    """
    css_class = f"status-{status}"
    return f'<span class="status-badge {css_class}">{text}</span>'


def create_metric_card(label: str, value: str, delta: str = None, color: str = "primary") -> str:  # type: ignore
    """创建现代化的metric卡片
    
    Args:
        label: 标签文本
        value: 数值
        delta: 可选的变化值
        color: 颜色主题 (primary, success, warning, error)
        
    Returns:
        HTML字符串
    """
    delta_html = f'<div style="font-size: 0.875rem; color: var(--{color});">{delta}</div>' if delta else ''
    
    return f'''
    <div class="card" style="text-align: center;">
        <div style="font-size: 0.875rem; color: var(--gray-500); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">
            {label}
        </div>
        <div style="font-size: 2rem; font-weight: 700; color: var(--gray-900); margin-bottom: 0.25rem;">
            {value}
        </div>
        {delta_html}
    </div>
    '''
