import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR

# Load and prepare data
df = pd.read_json("merged_data.json", lines=True)
df['date'] = pd.to_datetime(df['date'])
df.sort_values('date', inplace=True)

# Detect and standardize Close column
close_col = [col for col in df.columns if col.startswith("Close")][0]
df.rename(columns={close_col: 'Close'}, inplace=True)

# Compute returns
df['returns'] = df['Close'].pct_change()
df = df[['returns', 'sentiment_score']].dropna()

# Fit VAR
model = VAR(df)
var_result = model.fit(1)

# Manual GFEVD and Diebold-Yilmaz output
def diebold_yilmaz_manual(var_result, H=10):
    A = var_result.coefs[0]
    Sigma_u = var_result.sigma_u.values
    n = A.shape[0]

    # MA coefficients
    Phi = [np.eye(n)]
    for i in range(1, H):
        Phi.append(Phi[i-1] @ A)

    # GFEVD computation
    gfevd = np.zeros((n, n, H))
    sigma_diag = np.diag(Sigma_u)

    for h in range(H):
        for i in range(n):  # affected variable
            for j in range(n):  # shock
                num = (Phi[h][i, :] @ Sigma_u[:, j]) ** 2
                den = sigma_diag[i] * (Phi[h] @ Sigma_u @ Phi[h].T)[i, i]
                gfevd[i, j, h] = num / den if den != 0 else 0

    # DY table
    avg_gfevd = gfevd.mean(axis=2)
    row_sums = avg_gfevd.sum(axis=1).reshape(-1, 1)
    S_normalized = avg_gfevd / row_sums * 100
    TSI = (S_normalized.sum() - np.trace(S_normalized)) / n

    var_names = var_result.names
    spill_df = pd.DataFrame(S_normalized, index=var_names, columns=var_names)
    return TSI, spill_df.round(2)

# Run DY Spillover Index
TSI, spill_matrix = diebold_yilmaz_manual(var_result, H=10)

# Output
print(f"\nTotal Spillover Index (TSI): {TSI:.2f}%")
print("\nSpillover Table:")
print(spill_matrix.to_string())
