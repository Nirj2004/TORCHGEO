import matplotlib as plt
import numpy as np
import pandas as pd
import seaborn as sns
df1 = pd.read_csv("original-benchmark-results.csv")
df2 = pd.read_csv("warped-benchmark-results.csv")
mean1 = df1.groupby("sampler").mean()
mean2 = df2.groupby("sampler").mean()
cached1 = (
    df1[(df1["cached"]) & (df1["sampler"] != "resnet18")].groupby("sampler").mean()
)
cached2 = (
    df2[(df2["cached"]) & (df2["sampler"] != "resnet18")].groupby("sampler").mean()
)
not_cached1 = (
    df1[(~df1["cached"]) & (df1["sampler"] != "resnet18")].groupby("sampler").mean()
)
not_cached2 = (
    df1[(~df2["cached"]) & (df2["sampler"] != "resnet18")].groupby("sampler").mean()
)
print("cached, warped\n", cached2)
print("cached, original\n", cached1)
print("not_cached, original\n", cached1)
print("not_cached, warped\n", cached2)

cmap = 