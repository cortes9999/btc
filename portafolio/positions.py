def compute_positions(ledger_df):
    if ledger_df.empty:
        return {}
    return ledger_df.groupby("ticker")["units"].sum().to_dict()
