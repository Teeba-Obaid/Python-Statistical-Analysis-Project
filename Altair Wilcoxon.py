import os
import pandas as pd
import numpy as np
import altair as alt
from scipy.stats import kendalltau, wilcoxon
from pingouin import compute_effsize
from statsmodels.stats.multitest import multipletests


os.environ['OUTDATED_IGNORE'] = '1'

# Define the dependent variables as the outcome variables
dependent_variables = [
    'Post-test: Voltage Drop non-normative',
    'Post-test: Current non-normative',
    'Post-test: Current partial',
    'Post-test: Voltage Drop partial',
    'Post-test: Current 1 Valid link',
    'Post-test: Voltage Drop 1 Valid link',
    'Post-test: Current 2 Valid links',
    'Post-test: Voltage Drop 2 Valid links',
    'No action',
    'No new comparative trial',
    'Prediction Current: same rule',
    'Prediction Voltage Drop: same rule',
    'Confidence Current: verify prediction',
    'Confidence Voltage Drop: verify prediction',
    'Rule Current: Confirming Redundancy',
    'Rule Voltage Drop: Confirming Redundancy',
    'New comparative trial',
    'Prediction Current: Fill up gaps',
    'Prediction Voltage Drop: Fill up gaps',
    'Confidence Current: falsify prediction',
    'Confidence Voltage Drop: falsify prediction',
    'Identify problem: goal stated',
    'Rule Current: Simultaneous scanning',
    'Rule Voltage Drop: Simultaneous scanning',
    'Rule Current: Successive scanning',
    'Rule Voltage Drop: Successive scanning',
    'Rule Current: Focus gambling',
    'Rule Voltage Drop: Focus gambling',
    'Rule Current: Conservative Focusing',
    'Rule Voltage Drop: Conservative Focusing'
]

data = pd.read_csv("data10.csv")

data['group'] = ['control'] * 20 + ['experimental 1'] * 20 + ['experimental 2'] * 20

groups = {
    'control': data.loc[data['group'] == 'control', :],
    'experimental 1': data.loc[data['group'] == 'experimental 1', :],
    'experimental 2': data.loc[data['group'] == 'experimental 2', :]
}

def perform_within_group_tests(group, dependent_variables):
    results = []
    for i, var1 in enumerate(dependent_variables):
        for j, var2 in enumerate(dependent_variables):
            if i >= j:
                continue
            if np.all(group[var1] == group[var1].iloc[0]) or np.all(group[var2] == group[var2].iloc[0]):
                correlation, corr_pvalue, wilcoxon_pvalue, effect_size = np.nan, np.nan, np.nan, np.nan
            else:
                correlation, corr_pvalue = kendalltau(group[var1], group[var2])
                try:
                    _, wilcoxon_pvalue = wilcoxon(group[var1], group[var2])
                except ValueError:
                    wilcoxon_pvalue = 1.0  # Set to 1 if the differences are all zero
                effect_size = compute_effsize(group[var1],group[var2],eftype='r')

            results.append({
                'variable1': var1,
                'variable2': var2,
                'correlation': correlation,
                'corr_pvalue': corr_pvalue,
                'wilcoxon_pvalue': wilcoxon_pvalue,
                'effect_size': effect_size
            })

    return pd.DataFrame(results)

def perform_fdr_correction(results, alpha=0.05):
    pvalues = results['wilcoxon_pvalue'].dropna().values
    reject, pvals_corrected = multipletests(pvalues, alpha, method='fdr_bh')[:2]
    results.loc[results['wilcoxon_pvalue'].notna(), 'wilcoxon_pvalue'] = pvals_corrected
    return results

for group_name,group_data in groups.items():
    results = perform_within_group_tests(group_data,dependent_variables)
    results = perform_fdr_correction(results)

    matrix_pvalues = results.pivot(
        index='variable1',
        columns='variable2',
        values='wilcoxon_pvalue'
    )
    matrix_effect_sizes = results.pivot(
        index='variable1',
        columns='variable2',
        values='effect_size'
    )
    matrix_correlation = results.pivot(
        index='variable1',
        columns='variable2',
        values='correlation'
    )

    mask_pvalues = np.tril(np.ones_like(matrix_pvalues,dtype=bool))
    mask_correlation = np.tril(np.ones_like(matrix_correlation,dtype=bool))

    np.fill_diagonal(mask_pvalues,False)
    np.fill_diagonal(mask_correlation,False)

    matrix_pvalues = matrix_pvalues.mask(mask_pvalues)
    matrix_correlation = matrix_correlation.mask(mask_correlation)

    melted_pvalues = matrix_pvalues.reset_index().melt(
        id_vars=['variable1'],
        var_name='variable2',
        value_name='wilcoxon_pvalue'
    )
    melted_correlation = matrix_correlation.reset_index().melt(
        id_vars=['variable1'],
        var_name='variable2',
        value_name='correlation'
    )

    melted_effect_sizes = matrix_effect_sizes.reset_index().melt(
        id_vars=['variable1'],
        var_name='variable2',
        value_name='effect_size'
    )

    merged_melted = melted_pvalues.merge(
        melted_correlation,
        on=['variable1','variable2'],
        suffixes=('_pvalue','_correlation')
    )

    merged_melted = merged_melted.merge(
        melted_effect_sizes,
        on=['variable1','variable2'],
    )

    merged_melted.loc[merged_melted['wilcoxon_pvalue'].isna() & (
            merged_melted['variable1'] < merged_melted['variable2']),'wilcoxon_pvalue'] = 1.1
    merged_melted.loc[merged_melted['effect_size'].isna() & (
            merged_melted['variable1'] < merged_melted['variable2']),'effect_size'] = 1.1

    heatmap = alt.Chart(merged_melted).mark_rect().encode(
        x=alt.X(
            'variable1:N',
            axis=alt.Axis(labelAngle=90,labelAlign='left',labelFontSize=10,labelLimit=800)
        ),
        y=alt.Y('variable2:N',axis=alt.Axis(labelLimit=800)),
        color=alt.condition(
            alt.datum.wilcoxon_pvalue > 1,  # If wilcoxon_pvalue is NaN
            alt.value('#d5eaf4'),  # use light blue color
            alt.Color(
                'wilcoxon_pvalue:Q',
                scale=alt.Scale(
                    range=['#283655','#4D648D','#b3b7b8','#d8dcd6'],
                    domain=[0,0.05,0.05,1]
                ),
                legend=alt.Legend(title='Wilcoxon p-value')
            )
        ),
        tooltip=['variable1','variable2','wilcoxon_pvalue','correlation','effect_size'],
    ).properties(
        width=600,
        height=600,
        title=f'Wilcoxon p-values and Correlation Heatmap for {group_name} Group'
    )

    scatterplot = alt.Chart(merged_melted).mark_point().encode(
        x=alt.X('variable1:N',axis=alt.Axis(labelAngle=90,labelAlign='left',labelFontSize=10)),
        y=alt.Y('variable2:N',axis=alt.Axis(labelLimit=800)),
        size=alt.Size('correlation:Q',scale=alt.Scale(domain=[-1,1]),
                      legend=alt.Legend(title="Kendall's Tau Correlation")),
        color=alt.condition(
            alt.datum.effect_size > 1,  # If effect_size is NaN
            alt.value('black'),  # use light blue color
            alt.Color('effect_size:Q',scale=alt.Scale(range=["#FFE901","#fd03f5"],domainMid=0),
                      legend=alt.Legend(title='Effect Size')),
        )
    ).transform_filter(
        (alt.datum.correlation != 'NaN') & (alt.datum.effect_size != 'NaN')
    )

    combined_chart = (heatmap + scatterplot).resolve_scale(color='independent')

    combined_chart.save(f'heatmap_{group_name}.html')

    chart_json = combined_chart.to_json()

    print(chart_json)

