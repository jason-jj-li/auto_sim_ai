import plotly.graph_objects as go
import streamlit.components.v1 as components

# 创建简单的测试图表
fig = go.Figure(data=[go.Bar(x=[1, 2, 3], y=[4, 5, 6])])
fig.update_layout(title="Test Chart")

# 测试HTML渲染
config = {'displayModeBar': True, 'displaylogo': False}
html_string = fig.to_html(include_plotlyjs='cdn', config=config)

print("HTML generated successfully!")
print(f"HTML length: {len(html_string)} characters")
print("First 200 chars:", html_string[:200])
