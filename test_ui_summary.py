#!/usr/bin/env python3
"""测试 UI 统计展示功能（模拟数据）"""

import sys
import os

# 设置环境变量防止导入 streamlit
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'

sys.path.insert(0, os.path.dirname(__file__))

from src.persona_generator import PersonaGenerator
from collections import Counter
import pandas as pd

# 模拟从 LLM 提取的完整 JSON 数据（包含动态字段）
extracted_data = {
    "age_range": "18-64岁为主 (84%)",
    "gender": "Male (51.2%), Female (48.8%)",
    "education": "文盲2.67%, 小学25%, 初中35%, 高中/中专15%, 大专及以上15%",
    "occupation": "国家机关3.8%, 专业技术人员15.8%, 商业服务业16.3%, 农林牧渔20.6%",
    "location": "城镇63.89%, 农村36.11%",
    "marital_status": "已婚为主 (70%)",
    "ethnicity": "汉族为主 (92%)",
    "political_affiliation": "群众为主, 党员25%",
    "religion": "无宗教信仰为主",
    "health_status": "非常好25.8%, 比较好37.5%, 一般28.3%",
    "income_range": "2000-9999元68.4%, 3000-5000元26.3%",
    "children": "无子女50%, 0-3岁4.4%, 3-6岁5.66%",
    "social_insurance": "医疗96.5%, 养老91.8%",
    "family_structure": "2-4人同住为主, 平均2.62人",
    "tech_usage": "年轻高学历城镇43.7%, 年长低学历农村12.5%",
}

print("生成虚拟人...")
generator = PersonaGenerator()
personas = generator.generate_personas_from_ai_extraction(
    extracted_data=extracted_data,
    n=500,
    use_llm_parser=False  # 不使用 LLM 解析器，只用内置解析器
)

print(f"成功生成 {len(personas)} 个虚拟人\n")

# 模拟 UI 的统计展示逻辑
persona_dicts_list = [p if isinstance(p, dict) else p.__dict__ for p in personas]

# 转换为 dict 如果是对象
if personas and hasattr(personas[0], 'to_dict'):
    persona_dicts_list = [p.to_dict() for p in personas]
elif personas and hasattr(personas[0], '__dict__'):
    persona_dicts_list = [p.__dict__ for p in personas]

print("=" * 80)
print("📊 Population Demographics Summary")
print("=" * 80)

# Collect all fields and their distributions
all_variable_stats = []

# 1. Age (special handling - continuous variable)
ages = [p.get('age') for p in persona_dicts_list if p.get('age')]
if ages:
    age_mean = sum(ages) / len(ages)
    age_min = min(ages)
    age_max = max(ages)
    all_variable_stats.append({
        "变量名": "Age (年龄)",
        "类型": "连续型",
        "分布": f"均值={age_mean:.1f}, 范围=[{age_min}, {age_max}]"
    })

# 2. Collect all categorical fields
categorical_fields = {
    'gender': '性别 (Gender)',
    'occupation': '职业 (Occupation)',
    'education': '教育程度 (Education)',
    'location': '居住地 (Location)',
    'marital_status': '婚姻状况 (Marital Status)',
    'ethnicity': '民族 (Ethnicity)',
    'political_affiliation': '政治面貌 (Political)',
    'religion': '宗教信仰 (Religion)',
    'health_status': '健康状况 (Health)',
    'income_range': '收入区间 (Income)',
    'children': '子女情况 (Children)',
    'social_insurance': '社会保险 (Insurance)',
    'family_structure': '家庭结构 (Family)',
    'tech_usage': '科技使用 (Tech Usage)'
}

# Find all additional dynamic fields not in the standard list
all_fields = set()
for p_dict in persona_dicts_list:
    all_fields.update(p_dict.keys())

# Exclude non-demographic fields
excluded_fields = {'name', 'background', 'personality_traits', 'values', 'interests'}
dynamic_fields = all_fields - set(categorical_fields.keys()) - excluded_fields - {'age'}

# Add dynamic fields to categorical_fields dict
for field in sorted(dynamic_fields):
    field_display = field.replace('_', ' ').title()
    categorical_fields[field] = field_display

# Calculate distributions for all categorical fields
for field, display_name in sorted(categorical_fields.items(), key=lambda x: x[1]):
    field_values = [
        str(d.get(field)) for d in persona_dicts_list 
        if d.get(field) is not None
    ]
    
    if field_values:
        counts = Counter(field_values)
        total = len(field_values)
        
        # Format distribution string (top 5 categories)
        dist_parts = []
        for value, count in counts.most_common(5):
            pct = (count / total) * 100
            # Truncate long values
            display_value = value[:15] + "..." if len(value) > 15 else value
            dist_parts.append(f"{display_value} ({pct:.1f}%)")
        
        if len(counts) > 5:
            dist_parts.append(f"...+{len(counts)-5} more")
        
        dist_str = ", ".join(dist_parts)
        
        all_variable_stats.append({
            "变量名": display_name,
            "类型": "分类型",
            "分布": dist_str
        })

# Display as table
if all_variable_stats:
    df_stats = pd.DataFrame(all_variable_stats)
    print(df_stats.to_string(index=False))
    print("\n" + "=" * 80)
    print(f"✅ 共生成 {len(all_variable_stats)} 个人口统计变量")
    print("=" * 80)

# 展示一个示例 persona
print("\n示例虚拟人:")
print("-" * 80)
example = persona_dicts_list[0]
for key, value in sorted(example.items()):
    if key not in ['background', 'personality_traits', 'values', 'interests']:
        print(f"{key}: {value}")
