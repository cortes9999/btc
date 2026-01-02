import pandas as pd

def indicators(price):
    df = pd.DataFrame(price, columns=["price"])

    df["ma180"] = df["price"].rolling(180).mean()
    df["ret_8w"] = df["price"].pct_change(56)
    df["vol_6w"] = df["price"].pct_change().rolling(42).std()

    df["max_20w"] = df["price"].rolling(140).max()
    df["dd"] = df["price"] / df["max_20w"] - 1

    df["z_price"] = (df["price"] - df["ma180"]) / df["price"].rolling(180).std()
    df["ret_daily"] = df["price"].pct_change()
    df["autocorr"] = df["ret_daily"].rolling(30).apply(
        lambda x: x.autocorr(lag=1), raw=False
    )

    return df.dropna()
