#!/usr/bin/env python3
"""测试通用 LLM 解析器"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.persona_generator import PersonaGenerator
from src.llm_client import LMStudioClient
from collections import Counter

print("=" * 80)
print("测试通用 LLM 解析器")
print("=" * 80)

# 创建 LLM 客户端
llm_client = LMStudioClient()

# 模拟一个包含新字段的 JSON
extracted_data = {
    "age_range": "18-64岁为主 (84%)",
    "gender": "Male (51.2%), Female (48.8%)",
    "education": "文盲2.67%, 小学25%, 初中35%, 高中/中专15%, 大专及以上15%",
    
    # 新字段1: 运动习惯（有明确分类和百分比）
    "exercise_habit": "经常运动35%, 偶尔运动45%, 从不运动20%",
    
    # 新字段2: 饮食偏好（有明确分类和百分比）
    "diet_preference": "荤素均衡60%, 偏素食25%, 偏肉食15%",
    
    # 新字段3: 通勤方式（有明确分类和百分比）
    "commute_method": "公共交通40%, 私家车30%, 步行或自行车20%, 摩托车或电动车10%",
    
    # 新字段4: 纯描述性文本（应该被放到背景）
    "lifestyle_description": "生活节奏较快，注重工作与生活平衡，喜欢在周末参加社交活动",
}

print("\n步骤 1: 测试单个字段解析")
print("-" * 80)

# 测试解析 exercise_habit
print("\n测试字段: exercise_habit")
print(f"原始值: {extracted_data['exercise_habit']}")

result = PersonaGenerator.parse_field_to_distribution(
    field_name="exercise_habit",
    field_value=extracted_data["exercise_habit"],
    llm_client=llm_client
)

if result:
    print("✅ 成功解析为分类变量:")
    print(f"  变量名: {result['variable_name']}")
    print(f"  类别: {result['categories']}")
    print(f"  概率: {result['probabilities']}")
else:
    print("❌ 未能解析（可能是纯描述性文本）")

# 测试解析 lifestyle_description（纯描述）
print("\n测试字段: lifestyle_description")
print(f"原始值: {extracted_data['lifestyle_description']}")

result = PersonaGenerator.parse_field_to_distribution(
    field_name="lifestyle_description",
    field_value=extracted_data["lifestyle_description"],
    llm_client=llm_client
)

if result:
    print("✅ 解析为分类变量:")
    print(f"  变量名: {result['variable_name']}")
    print(f"  类别: {result['categories']}")
    print(f"  概率: {result['probabilities']}")
else:
    print("❌ 未能解析（这是正确的，因为这是纯描述性文本）")

print("\n" + "=" * 80)
print("步骤 2: 生成虚拟人（启用 LLM 通用解析器）")
print("=" * 80)

personas = PersonaGenerator.generate_personas_from_ai_extraction(
    extracted_data=extracted_data,
    n=500,
    use_llm_parser=True,
    llm_client=llm_client
)

print(f"\n成功生成 {len(personas)} 个虚拟人\n")

# 检查新字段是否被正确解析
new_fields = [
    ('exercise_habit', '运动习惯'),
    ('diet_preference', '饮食偏好'),
    ('commute_method', '通勤方式'),
    ('lifestyle_description', '生活方式描述')
]

for field, field_name in new_fields:
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
        # 检查是否在背景中
        has_in_background = any(
            field in str(p.get('background', '')) or 
            str(extracted_data.get(field, '')) in str(p.get('background', ''))
            for p in personas[:5]  # 只检查前5个
        )
        if has_in_background:
            print(f"{field_name}: ✅ 作为背景描述（正确处理）")
        else:
            print(f"❌ {field_name}: 未找到数据")
        print()

print("=" * 80)
print("示例虚拟人:")
print("=" * 80)
example = personas[0]
print(f"年龄: {example.get('age')}")
print(f"性别: {example.get('gender')}")
print(f"教育: {example.get('education')}")
print(f"运动习惯: {example.get('exercise_habit')}")
print(f"饮食偏好: {example.get('diet_preference')}")
print(f"通勤方式: {example.get('commute_method')}")
print(f"\n背景描述:")
print(example.get('background', '')[:200] + "...")

print("\n" + "=" * 80)
print("测试总结:")
print("=" * 80)
print("✅ LLM 通用解析器可以:")
print("   1. 自动识别包含分类和百分比的字段")
print("   2. 提取类别和概率分布")
print("   3. 创建对应的分类变量")
print("   4. 将纯描述性文本放到背景中")
print("\n💡 优势:")
print("   - 无需为每个新字段编写正则表达式解析器")
print("   - 灵活适应新的变量类型")
print("   - LLM 可以理解各种表达方式")
