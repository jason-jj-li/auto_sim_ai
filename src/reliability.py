"""Reliability and distribution-validity metrics for simulated survey data.

Why these exist: LLM respondents are "plausible but not valid" by default —
independent agents collapse onto modal answers (arXiv:2607.18310 reports ~85%
collapse) and demographic persona conditioning adds little psychometric signal
(arXiv:2608.14606). These metrics make that visible instead of trusting averages.
"""
from typing import Callable, Dict, Any, List
import numpy as np
import pandas as pd

# Modal share at or above this means the answer distribution collapsed
COLLAPSE_THRESHOLD = 0.85


def cronbach_alpha(items) -> float:
    """Internal consistency of a scale. items: n_respondents × k items, numeric."""
    x = np.asarray(items, dtype=float)
    k = x.shape[1]
    if k < 2 or x.shape[0] < 2:
        return float('nan')
    item_vars = x.var(axis=0, ddof=1)
    total_var = x.sum(axis=1).var(ddof=1)
    if total_var == 0:
        return float('nan')
    return float(k / (k - 1) * (1 - item_vars.sum() / total_var))


def question_collapse_report(df: pd.DataFrame) -> pd.DataFrame:
    """Per-question distribution-collapse check.

    Args:
        df: rows with columns 'question' and 'response'

    Returns:
        One row per question: modal answer/share, effective answer count
        (exp Shannon entropy), and whether modal share >= COLLAPSE_THRESHOLD.
    """
    rows = []
    for q, all_rows in df.groupby('question', sort=False):
        invalid = pd.Series(False, index=all_rows.index)
        if 'validation_status' in all_rows.columns:
            invalid |= all_rows['validation_status'].fillna('not_requested').eq('invalid')
        invalid |= all_rows['response'].astype(str).str.startswith('[Error:')
        grp = all_rows.loc[~invalid]
        if grp.empty:
            rows.append({
                'question': q, 'n': 0, 'invalid_or_failed': int(invalid.sum()),
                'modal_answer': None, 'modal_share': float('nan'),
                'effective_answers': 0.0, 'collapsed': False
            })
            continue
        shares = grp['response'].astype(str).value_counts(normalize=True)
        entropy = float(-(shares * np.log(shares)).sum())
        rows.append({
            'question': q,
            'n': len(grp),
            'invalid_or_failed': int(invalid.sum()),
            'modal_answer': shares.index[0],
            'modal_share': round(float(shares.iloc[0]), 3),
            'effective_answers': round(float(np.exp(entropy)), 2),
            'collapsed': bool(shares.iloc[0] >= COLLAPSE_THRESHOLD)
        })
    return pd.DataFrame(rows)


def distribution_divergence(observed: pd.Series, ref_probs: Dict[str, float]) -> Dict[str, float]:
    """Distance between an observed answer distribution and a human reference.

    Standard silicon-sampling practice: compare simulated distributions against
    real survey benchmarks (Sun et al. 2024 uses KL; JSD is the symmetric,
    always-finite variant; TVD is the easiest to read — half the L1 distance).

    Args:
        observed: raw answers for one question (any dtype; cast to str)
        ref_probs: {answer: probability} from a human survey; renormalized here

    Returns:
        {'tvd': ..., 'jsd': ..., 'coverage': share of observed mass that has a
        reference probability} — coverage < 1 means the simulation produced
        answers absent from the reference (e.g. off-scale text).
    """
    obs = observed.astype(str).value_counts(normalize=True)
    ref = pd.Series({str(k): float(v) for k, v in ref_probs.items()}, dtype=float)
    ref = ref / ref.sum()
    idx = obs.index.union(ref.index)
    p = obs.reindex(idx, fill_value=0.0).to_numpy(dtype=float)
    q = ref.reindex(idx, fill_value=0.0).to_numpy(dtype=float)
    tvd = float(0.5 * np.abs(p - q).sum())
    m = 0.5 * (p + q)
    with np.errstate(divide='ignore', invalid='ignore'):
        kl_pm = np.where(p > 0, p * np.log2(p / m), 0.0)
        kl_qm = np.where(q > 0, q * np.log2(q / m), 0.0)
    jsd = float(0.5 * kl_pm.sum() + 0.5 * kl_qm.sum())
    coverage = float(obs[obs.index.isin(ref.index)].sum())
    return {'tvd': round(tvd, 3), 'jsd': round(jsd, 3), 'coverage': round(coverage, 3)}


def test_retest(run_fn: Callable, personas: List[Any], questions: List[str], **kw) -> Dict[str, Any]:
    """Run the same survey twice and report answer stability.

    Args:
        run_fn: callable(personas=..., questions=..., **kw) -> SimulationResult
                (e.g. SimulationEngine.run_survey or a lambda wrapping the parallel engine)

    Returns:
        n_pairs, n_numeric, pearson_r (numeric answers), exact_match_rate (all answers)
    """
    r1 = run_fn(personas=personas, questions=questions, **kw)
    r2 = run_fn(personas=personas, questions=questions, **kw)

    def _pairs(res):
        return {
            (d.get('persona_id') or d['persona_name'], d['question']): d['response']
            for d in res.persona_responses
        }

    a, b = _pairs(r1), _pairs(r2)
    keys = [k for k in a if k in b]
    exact = float(np.mean([a[k] == b[k] for k in keys])) if keys else float('nan')

    num_a, num_b = [], []
    for k in keys:
        try:
            num_a.append(float(a[k]))
            num_b.append(float(b[k]))
        except (ValueError, TypeError):
            pass
    r = float(np.corrcoef(num_a, num_b)[0, 1]) if len(num_a) >= 3 else float('nan')
    return {'n_pairs': len(keys), 'n_numeric': len(num_a),
            'pearson_r': r, 'exact_match_rate': exact}


if __name__ == '__main__':
    # Self-check: alpha of a perfectly consistent scale ≈ 1; collapsed question flagged
    consistent = np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3], [5, 5, 5], [4, 4, 4]])
    assert cronbach_alpha(consistent) > 0.99
    df = pd.DataFrame({'question': ['q1'] * 20 + ['q2'] * 20,
                       'response': ['yes'] * 19 + ['no'] + list('abcd' * 5)})
    rep = question_collapse_report(df)
    assert rep.loc[rep['question'] == 'q1', 'collapsed'].iloc[0]
    assert not rep.loc[rep['question'] == 'q2', 'collapsed'].iloc[0]
    # Divergence: identical distributions → 0; disjoint → TVD 1, JSD 1
    d_same = distribution_divergence(pd.Series(['a', 'a', 'b']), {'a': 2 / 3, 'b': 1 / 3})
    assert d_same['tvd'] == 0.0 and d_same['jsd'] == 0.0
    d_diff = distribution_divergence(pd.Series(['a'] * 10), {'b': 1.0})
    assert d_diff['tvd'] == 1.0 and d_diff['jsd'] == 1.0 and d_diff['coverage'] == 0.0
    print('reliability self-check OK')
