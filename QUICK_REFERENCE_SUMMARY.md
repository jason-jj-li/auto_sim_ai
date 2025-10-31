# Quick Reference: Demographics Summary Table

## What is it?
A summary table that automatically appears after generating personas, showing comprehensive population statistics.

## When does it appear?
✅ After AI-powered persona extraction  
✅ After statistical distribution generation  
✅ Before sample persona display  
✅ Before "Continue to Simulation" button

## What does it show?

| Column | Content | Example |
|--------|---------|---------|
| **1. Age Stats** 📈 | Mean age, Range, Age groups | Mean: 21.3, Range: 18-24, 18-25: 96% |
| **2. Gender & Education** ⚧🎓 | Gender distribution, Top education levels | Female: 60%, Male: 40%, Bachelor's: 100% |
| **3. Jobs & Locations** 💼📍 | Top 5 occupations, Top 3 locations | STEM Student: 100%, California: 100% |

## Why use it?

| Benefit | Description |
|---------|-------------|
| ✅ **Verification** | Confirm personas match your target demographics |
| ✅ **Quality Control** | Catch issues before running simulations |
| ✅ **Transparency** | See exact distributions, not just samples |
| ✅ **Documentation** | Screenshot for research reports |
| ✅ **Decision Making** | Data-driven choice to proceed or regenerate |

## Quick Stats Displayed

- **Age**: Mean, Min, Max, Distribution by groups (18-25, 26-35, etc.)
- **Gender**: All genders with counts and percentages
- **Occupations**: Top 5 most common jobs
- **Education**: Top 3 education levels
- **Locations**: Top 3 geographic locations

## How to use?

1. Generate personas (AI or manual method)
2. **Summary appears automatically** ← No extra action needed!
3. Review the statistics
4. Decide next step:
   - ✅ Stats look good → Click "Continue to Simulation"
   - 🔄 Need adjustment → Regenerate with new parameters
   - 💾 Want to keep → Click "Save Permanently"

## Code Location

- File: `pages/1_Setup.py`
- AI extraction: Line ~710
- Manual generation: Line ~1055

## Dependencies

- `pandas` (for age binning)
- `collections.Counter` (for frequency counts)
- Built into Streamlit (no extra installation)

## Performance

- ⚡ **Instant**: Calculates in < 0.1 seconds for 500 personas
- 📱 **Responsive**: Works on mobile and desktop
- 🎨 **Clean**: 3-column layout with metrics

## Example Scenario

```
Input: "Students aged 18-24, 60% female"
↓
Generate 50 personas
↓
📊 Summary shows:
  • Mean age: 21.2 ✅
  • Female: 58% (close to 60%) ✅
  • Age range: 18-24 ✅
↓
Continue to Simulation!
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Summary not appearing | Make sure personas were generated successfully |
| Wrong statistics | Regenerate with adjusted parameters |
| Need more detail | Check individual persona samples below summary |

## Related Documentation

- Full guide: `docs/DEMOGRAPHICS_SUMMARY.md`
- AI extraction: `docs/AI_PERSONA_GENERATION.md`
- Test script: `test_demographic_summary.py`
- Visual example: `docs/VISUAL_EXAMPLE_SUMMARY.py`

---

**Quick Start**: Just generate personas and the summary appears automatically! 🎉
