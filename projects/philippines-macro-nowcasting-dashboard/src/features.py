"""Feature engineering utilities for macroeconomic nowcasting."""


def add_lag_features(df, columns, lags):
    """Add lag features for selected columns."""
    output = df.copy()
    for column in columns:
        if column in output.columns:
            for lag in lags:
                output[f"{column}_lag_{lag}"] = output[column].shift(lag)
    return output


def add_rolling_features(df, columns, windows):
    """Add rolling mean features for selected columns."""
    output = df.copy()
    for column in columns:
        if column in output.columns:
            for window in windows:
                output[f"{column}_rolling_{window}"] = (
                    output[column].rolling(window=window, min_periods=window).mean()
                )
    return output


def add_change_features(df, columns):
    """Add one-period change features for selected columns."""
    output = df.copy()
    for column in columns:
        if column in output.columns:
            output[f"{column}_change_1"] = output[column].diff()
    return output


def build_inflation_feature_table(monthly_df):
    """Build an inflation-first monthly indicator table with simple lag features."""
    output = monthly_df.sort_values("date").reset_index(drop=True).copy()
    output = add_lag_features(output, ["inflation_rate"], [1, 3, 6])
    output = add_rolling_features(output, ["inflation_rate"], [3, 6])
    output = add_change_features(output, ["inflation_rate"])
    if "usd_php" in output.columns:
        output = add_lag_features(output, ["usd_php"], [1])
        output = add_change_features(output, ["usd_php"])
    return output
