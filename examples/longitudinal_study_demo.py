"""
纵向研究示例 - 冥想干预对压力的影响

这个示例展示如何使用新的LongitudinalStudyEngine进行多波次纵向研究。
"""

from src import (
    LMStudioClient,
    Persona,
    LongitudinalStudyEngine,
    LongitudinalStudyBuilder
)


def create_sample_personas():
    """创建示例虚拟人物"""
    return [
        Persona(
            name="张伟",
            age=28,
            gender="男",
            occupation="软件工程师",
            background="""在北京一家互联网公司工作，经常需要加班到深夜。
最近项目紧急，压力特别大，经常失眠。虽然知道要注意健康，但总是没时间锻炼。
感觉自己一直处于高压状态，有时候会焦虑。""",
            personality_traits=["内向", "完美主义", "责任心强", "容易焦虑"],
            values=["职业发展", "技术成长", "工作生活平衡"],
            education="本科计算机科学",
            location="北京"
        ),
        Persona(
            name="李娜",
            age=35,
            gender="女",
            occupation="护士",
            background="""在上海某三甲医院工作，轮班制。既要照顾病人，又要照顾家里的两个孩子。
经常感到身心疲惫，睡眠不足。最近觉得压力很大，有时候情绪不太稳定。
想找一些简单有效的方法来缓解压力和改善睡眠。""",
            personality_traits=["外向", "有责任心", "善良", "容易紧张"],
            values=["家庭", "帮助他人", "健康", "工作价值"],
            education="本科护理学",
            location="上海"
        ),
        Persona(
            name="王明",
            age=42,
            gender="男",
            occupation="中学教师",
            background="""在广州一所中学教数学，已经教了15年。工作相对稳定，但每天面对学生、
家长和学校的各种压力。最近感觉有些倦怠，对工作的热情不如从前。
睡眠质量一般，有时候会因为工作上的事情而烦躁。""",
            personality_traits=["严谨", "耐心", "有些固执", "追求完美"],
            values=["教育", "稳定", "家庭和谐"],
            education="本科数学",
            location="广州"
        )
    ]


def main():
    """主函数"""
    
    print("="*60)
    print("纵向研究示例：冥想干预对压力的影响")
    print("="*60)
    
    # 1. 创建虚拟人物
    print("\n📋 步骤 1: 创建虚拟人物")
    personas = create_sample_personas()
    print(f"   已创建 {len(personas)} 个虚拟人物:")
    for p in personas:
        print(f"   - {p.name}, {p.age}岁, {p.occupation}")
    
    # 2. 配置LLM客户端
    print("\n🔌 步骤 2: 配置LLM客户端")
    
    # 请根据你的实际情况选择：
    
    # 选项A: 本地LM Studio
    # client = LMStudioClient(
    #     base_url="http://127.0.0.1:1234/v1"
    # )
    
    # 选项B: DeepSeek API（推荐）
    client = LMStudioClient(
        base_url="https://api.deepseek.com/v1",
        api_key="your-api-key-here"  # 替换为你的API key
    )
    
    # 选项C: OpenAI API
    # client = LMStudioClient(
    #     base_url="https://api.openai.com/v1",
    #     api_key="your-openai-key-here"
    # )
    
    print(f"   已配置: {client.base_url}")
    
    # 3. 创建研究设计
    print("\n🔬 步骤 3: 创建研究设计")
    
    study_config = LongitudinalStudyBuilder.create_pre_post_study(
        study_name="冥想干预压力研究",
        
        # 基线问题（所有波次）
        baseline_questions=[
            "请用1-10分评价你当前的压力水平，1分最低，10分最高，并简单说明原因。",
            "你最近一周的睡眠质量如何（1-10分）？",
            "你的整体幸福感如何（1-10分）？"
        ],
        
        # 干预内容
        intervention_text="""
【正念冥想压力管理训练】

研究背景：
多项科学研究表明，正念冥想（Mindfulness Meditation）是一种有效的压力管理方法。

科学证据：
• 8周练习可降低压力激素皮质醇水平30%
• 改善睡眠质量高达50%  
• 提升情绪调节能力和专注力
• 增强免疫系统功能

具体方法：
1. **每天早晨做10分钟正念冥想**
   - 找一个安静的地方坐下
   - 闭上眼睛，专注于自己的呼吸
   - 当思绪飘走时，温柔地把注意力拉回到呼吸上
   - 不要评判自己的表现，保持觉察即可

2. **使用4-7-8呼吸法应对急性压力**
   - 吸气4秒
   - 屏息7秒
   - 呼气8秒
   - 重复3-4次

3. **睡前写感恩日记（可选）**
   - 写下今天感恩的3件事
   - 有助于改善睡眠和情绪

建议：
请在接下来的4周内坚持练习。研究显示，21天可以初步形成习惯。
你可以使用手机APP辅助（如Calm、Headspace、潮汐等）。

重要提示：
这是一个科学实证的方法，但需要持续练习才能看到效果。
即使只是每天10分钟，也会带来显著的改变。
        """,
        
        # 干预后额外问题
        followup_questions=[
            "请用1-10分评价你当前的压力水平，1分最低，10分最高。",
            "你最近一周的睡眠质量如何（1-10分）？",
            "你的整体幸福感如何（1-10分）？",
            "你是否尝试了冥想练习？如果尝试了，大约练习了多少次？",
            "练习冥想后，你感受到了什么变化（如果有的话）？"
        ],
        
        # 研究参数
        num_pre_waves=2,       # 干预前2个波次（建立基线）
        num_post_waves=4,      # 干预后4个波次（追踪效果）
        days_between_waves=7   # 每周测量一次
    )
    
    print(f"   研究包含 {len(study_config.waves)} 个波次:")
    for wave in study_config.waves:
        marker = "🎯" if wave.is_intervention_wave else "📊"
        print(f"   {marker} 波次 {wave.wave_number}: {wave.wave_name} (第{wave.days_from_baseline}天)")
    
    # 4. 创建研究引擎
    print("\n⚙️  步骤 4: 初始化研究引擎")
    engine = LongitudinalStudyEngine(
        llm_client=client,
        storage_dir="data/longitudinal_studies"
    )
    print("   引擎已就绪")
    
    # 5. 运行研究
    print("\n🚀 步骤 5: 运行纵向研究")
    print("   这可能需要几分钟时间...")
    print()
    
    def progress_callback(message):
        """进度回调函数"""
        print(f"   📊 {message}")
    
    try:
        result = engine.run_study(
            config=study_config,
            personas=personas,
            temperature=0.7,      # 平衡的随机性
            max_tokens=300,       # 每个响应最多300 tokens
            progress_callback=progress_callback,
            save_checkpoints=True  # 每波次后自动保存
        )
        
        print("\n✅ 研究完成!")
        
        # 6. 保存对话历史
        print("\n💾 步骤 6: 保存对话历史")
        engine.save_conversation_histories(study_config.study_id)
        print(f"   对话历史已保存")
        
        # 7. 显示结果摘要
        print("\n" + "="*60)
        print("研究结果摘要")
        print("="*60)
        
        print(f"\n研究ID: {result.study_id}")
        print(f"研究名称: {result.study_name}")
        print(f"开始时间: {result.started_at}")
        print(f"完成时间: {result.completed_at}")
        print(f"参与人数: {len(result.persona_results)}")
        
        # 显示每个人物的结果
        for persona_name, wave_results in result.persona_results.items():
            print(f"\n{'─'*60}")
            print(f"👤 {persona_name}")
            print(f"{'─'*60}")
            
            for wave_result in wave_results:
                print(f"\n  波次 {wave_result.wave_number}: {wave_result.wave_name}")
                
                # 显示前2个问答
                for i, response_data in enumerate(wave_result.responses[:2]):
                    question = response_data['question']
                    answer = response_data['response']
                    
                    # 截断过长的问题和答案
                    if len(question) > 60:
                        question = question[:57] + "..."
                    if len(answer) > 100:
                        answer = answer[:97] + "..."
                    
                    print(f"    Q{i+1}: {question}")
                    print(f"    A{i+1}: {answer}")
                
                if len(wave_result.responses) > 2:
                    print(f"    ... 还有 {len(wave_result.responses)-2} 个问答")
        
        # 8. 提示查看详细结果
        print("\n" + "="*60)
        print("📁 详细结果已保存到:")
        print(f"   data/longitudinal_studies/{result.study_id}_final.json")
        print(f"   data/longitudinal_studies/{result.study_id}_conversations.json")
        print("="*60)
        
        # 9. 简单的数据分析示例
        print("\n" + "="*60)
        print("📈 简单数据分析")
        print("="*60)
        
        import re
        
        for persona_name, wave_results in result.persona_results.items():
            print(f"\n{persona_name} 的压力水平变化:")
            
            stress_scores = []
            for wave_result in wave_results:
                # 查找压力水平问题的回答
                for response_data in wave_result.responses:
                    if "压力水平" in response_data['question']:
                        # 尝试提取数字评分
                        numbers = re.findall(r'(\d+)分', response_data['response'])
                        if not numbers:
                            numbers = re.findall(r'\d+', response_data['response'])
                        
                        if numbers:
                            score = int(numbers[0])
                            stress_scores.append((wave_result.wave_number, score))
                            print(f"  波次 {wave_result.wave_number}: {score}分")
                        break
            
            if len(stress_scores) >= 3:
                # 简单统计
                pre_scores = [s for w, s in stress_scores if w <= 2]
                post_scores = [s for w, s in stress_scores if w > 3]
                
                if pre_scores and post_scores:
                    pre_avg = sum(pre_scores) / len(pre_scores)
                    post_avg = sum(post_scores) / len(post_scores)
                    change = post_avg - pre_avg
                    
                    print(f"  基线平均: {pre_avg:.1f}分")
                    print(f"  随访平均: {post_avg:.1f}分")
                    print(f"  变化: {change:+.1f}分 {'↓ 改善' if change < 0 else '↑ 恶化' if change > 0 else '→ 无变化'}")
        
        print("\n" + "="*60)
        print("🎉 示例运行完成！")
        print("="*60)
        
        return result
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # 运行示例
    result = main()
    
    print("\n💡 提示:")
    print("   - 查看 LONGITUDINAL_GUIDE.md 了解更多用法")
    print("   - 修改 API key 后可以实际运行这个示例")
    print("   - 查看 data/longitudinal_studies/ 目录获取详细结果")
