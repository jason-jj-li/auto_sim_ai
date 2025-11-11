"""
测试教育和职业解析器修复
"""
from src.persona_generator import PersonaGenerator

# 测试数据 - 您提供的提示词片段
test_prompt = """
4.受教育程度(education_level)
小学占比约25%、初中占比约35%、高中(含中专)占比约15%、大专及以上占比约15%，文盲率为2.67%。

11.职业(occupation)
• 国家机关、党群组织、企业事业单位负责人占 3.8%
• 专业技术人员占 15.8%
• 商业、服务业人员占 16.3%
• 农林牧渔从业者占 20.6%
"""

print("=" * 80)
print("测试教育程度和职业解析器")
print("=" * 80)

# 模拟AI提取的数据
extracted_data = {
    'education': '小学占比约25%、初中占比约35%、高中(含中专)占比约15%、大专及以上占比约15%，文盲率为2.67%',
    'occupation': '国家机关、党群组织、企业事业单位负责人占 3.8%；专业技术人员占 15.8%；商业、服务业人员占 16.3%；农林牧渔从业者占 20.6%',
    'age_range': '18-64',
    'gender': 'Mixed'
}

print("\n提取的数据:")
print(f"教育: {extracted_data['education']}")
print(f"职业: {extracted_data['occupation']}")

# 生成personas
print("\n生成5个测试persona...")
personas = PersonaGenerator.generate_personas_from_ai_extraction(
    extracted_data=extracted_data,
    n=5,
    seed=42
)

print("\n生成的Personas:")
print("-" * 80)
for i, p in enumerate(personas, 1):
    print(f"\nPersona {i}:")
    print(f"  姓名: {p.get('name', 'N/A')}")
    print(f"  年龄: {p.get('age', 'N/A')}")
    print(f"  性别: {p.get('gender', 'N/A')}")
    print(f"  教育: {p.get('education', 'N/A')}")
    print(f"  职业: {p.get('occupation', 'N/A')}")

# 统计分布
print("\n" + "=" * 80)
print("统计分布验证")
print("=" * 80)

from collections import Counter

# 教育程度统计
education_counts = Counter([p.get('education', 'Unknown') for p in personas])
print("\n教育程度分布 (n=5):")
for edu, count in education_counts.most_common():
    print(f"  {edu}: {count}")

# 职业统计
occupation_counts = Counter([p.get('occupation', 'Unknown') for p in personas])
print("\n职业分布 (n=5):")
for occ, count in occupation_counts.most_common():
    print(f"  {occ}: {count}")

# 生成更大样本以验证概率分布
print("\n" + "=" * 80)
print("大样本验证 (n=500)")
print("=" * 80)

large_sample = PersonaGenerator.generate_personas_from_ai_extraction(
    extracted_data=extracted_data,
    n=500,
    seed=42
)

education_counts_large = Counter([p.get('education', 'Unknown') for p in large_sample])
print("\n教育程度分布:")
print("期望值 -> 实际值")
print(f"文盲 2.67% -> {education_counts_large.get('文盲', 0)/500*100:.2f}%")
print(f"小学 25% -> {education_counts_large.get('小学', 0)/500*100:.2f}%")
print(f"初中 35% -> {education_counts_large.get('初中', 0)/500*100:.2f}%")
print(f"高中 15% -> {education_counts_large.get('高中', 0)/500*100:.2f}%")

occupation_counts_large = Counter([p.get('occupation', 'Unknown') for p in large_sample])
print("\n职业分布:")
print("期望值 -> 实际值")
for occ, count in occupation_counts_large.most_common():
    print(f"{occ}: {count/500*100:.2f}%")

print("\n✅ 测试完成!")
