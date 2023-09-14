import os
import pandas as pd
import numpy as np
import altair as alt
from scipy.stats import kendalltau, wilcoxon
from pingouin import compute_effsize
from statsmodels.stats.multitest import multipletests


os.environ['OUTDATED_IGNORE'] = '1'

# Define the dependent variables as the outcome variables
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
                effect_size = compute_effsize(group[var1], group[var2], eftype='r')

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

results_list = []

for group_name, group_data in groups.items():
    if group_name != 'experimental 2':  # Skip groups other than 'experimental 2'
        continue

    results = perform_within_group_tests(group_data, dependent_variables)
    results = perform_fdr_correction(results)

    results_list.append(results)

# Merge all the results dataframes
all_results = pd.concat(results_list)

filtered_results = all_results[all_results['wilcoxon_pvalue'] <= 0.05 - 1e-10]
filtered_results = filtered_results.dropna(subset=['correlation', 'wilcoxon_pvalue'])

filtered_results_json = filtered_results.to_json(orient='records')

print(filtered_results_json)
# Write the DataFrame to an Excel file
filtered_results.to_excel("filtered_results.xlsx")