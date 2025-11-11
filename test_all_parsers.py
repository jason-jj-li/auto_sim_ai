#!/usr/bin/env python3
"""测试所有字段的解析器"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.persona_generator import PersonaGenerator
from collections import Counter

# 模拟从 LLM 提取的完整 JSON 数据
extracted_data = {
    "age_range": "18-64岁为主 (84%)",
    "gender": "Male (51.2%), Female (48.8%)",
    "education": "文盲2.67%, 小学25%, 初中35%, 高中/中专15%, 大专及以上15%",
    "occupation": "国家机关、党群组织、企业事业单位负责人3.8%, 专业技术人员15.8%, 商业、服务业人员16.3%, 农林牧渔从业者20.6%",
    "location": "城镇63.89%, 农村36.11%",
    "marital_status": "已婚为主 (70%)",
    "ethnicity": "汉族为主 (92%), 其他少数民族 (8%)",
    "political_affiliation": "群众为主, 党员占比约25%",
    "religion": "无宗教信仰为主",
    "health_status": "非常好25.8%, 比较好37.5%, 一般28.3%, 比较不好6.7%, 非常不好1.7%",
    "income_range": "2000-9999元68.4%, 其中3000-5000元26.3%, 5000-8000元24.2%",
    "children": "无子女50%, 0-3岁4.4%, 3-6岁5.66%, 6-14岁11.55%",
    "social_insurance": "医疗96.5%, 养老91.8%",
    "family_structure": "2-4人同住为主, 平均2.62人",
    "tech_usage": "年轻高学历城镇43.7%, 年长低学历农村12.5%"
}

print("=" * 80)
print("测试所有解析器 - 生成500个虚拟人")
print("=" * 80)

generator = PersonaGenerator()
personas = generator.generate_personas_from_ai_extraction(
    extracted_data=extracted_data,
    n=500
)

print(f"\n成功生成 {len(personas)} 个虚拟人\n")

# 检查所有关键字段的分布
fields_to_check = [
    ('gender', '性别'),
    ('education', '教育程度'),
    ('occupation', '职业'),
    ('location', '居住地'),
    ('marital_status', '婚姻状况'),
    ('ethnicity', '民族'),
    ('political_affiliation', '政治面貌'),
    ('religion', '宗教信仰'),
    ('health_status', '健康状况'),
    ('income_range', '收入区间'),
    ('children', '子女情况'),
    ('social_insurance', '社会保险'),
    ('family_structure', '家庭结构'),
    ('tech_usage', '科技使用')
]

for field, field_name in fields_to_check:
    values = [p.get(field) for p in personas if p.get(field)]
    
    if values:
        counter = Counter(values)
        total = len(values)
        
        print(f"{field_name} 分布 (n={total}):")
        for value, count in counter.most_common():
            percentage = (count / total) * 100
            print(f"  {value}: {count} ({percentage:.1f}%)")
        print()
    else:
        print(f"❌ {field_name}: 未找到数据")
        print()

# 检查示例 persona 的完整属性
print("=" * 80)
print("示例虚拟人的所有属性:")
print("=" * 80)
example = personas[0]
for key, value in sorted(example.items()):
    if key != 'background':  # 跳过背景文本，太长
        print(f"{key}: {value}")

print("\n" + "=" * 80)
print("测试总结:")
print("=" * 80)

# 统计有多少字段成功解析
parsed_fields = []
missing_fields = []

for field, field_name in fields_to_check:
    has_values = any(p.get(field) for p in personas)
    if has_values:
        parsed_fields.append(field_name)
    else:
        missing_fields.append(field_name)

print(f"✅ 成功解析的字段 ({len(parsed_fields)}):")
for field in parsed_fields:
    print(f"   - {field}")

if missing_fields:
    print(f"\n❌ 缺失的字段 ({len(missing_fields)}):")
    for field in missing_fields:
        print(f"   - {field}")
else:
    print(f"\n🎉 所有字段都成功解析！")
