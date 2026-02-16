import os, glob
import pandas as pd

paths = glob.glob("output/**/*communit*.*", recursive=True)
print("found:", *paths, sep="\n- ")

# parquet優先で、最初の1つだけ中身確認
for p in paths:
    if p.lower().endswith(".parquet"):
        df = pd.read_parquet(p)
        print("\nFILE:", p)
        print("rows:", len(df))
        print("cols:", list(df.columns))
        print(df.head(3))
        break
