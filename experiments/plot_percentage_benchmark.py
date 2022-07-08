import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df1 = pd.read_csv("original-benchmark-results.csv")
df2 = pd.read_csv("warped-benchmark-results.csv")
random_cached1 = df1[(df1["sampler"] == "RandomGeoSampler") & (df1["cached"])]
random_cached2 = df2[(df2["sampler"] == "RandomGeoSampler") & (df2["cached"])]
random_cachedp = random_cached1
random_cachedp["rate"] /= random_cached2["rate"]

random_batch_cached1 = df1[(df1["sampler"] == "RandomBatchGeoSampler") & (df1["cached"])]
random_batch_cached2 = df2[(df2["sampler"] == "RandomBatchGeoSampler") & (df2["cached"])]
random_batch_cachedp = random_batch_cached1
random_batch_cachedp["rate"] /= random_batch_cached2["rate"]

grid_cached1 = df1[(df1["sampler"] == "Grid GeoSampler") & (df1["cached"])]
grid_cached2 = df2[(df2["sampler"] == "Grid GeoSampler") & (df2["cached"])]
grid_cachedp = grid_cached1
grid_cachedp["rate"] /= grid_cached2["rate"]

other = [
    ("RandomGeoSampler (cached)", random_cachedp),
    ("RandomBatchGeoSampler (cached)", random_batch_cachedp),
    ("GridGeoSampler (cached)", grid_cachedp),
]

cmap = sns.color_palette()

ax = plt.gca()

for i, (label, df) in enumerate(other):
    df = df.groupby("batch_size")
    ax.plot(df.mean().index, df.mean()["rate"], color=cmap[i], label=label)
    ax.fill_between(
        df.mean().index, df.min()["rate"], df.max()["rate"], color=cmap[i], alpha=0.2
    )

ax.set_xscale("log")
ax.set_xticks([16, 32, 64, 128, 256])
ax.set_xtickslabels([16, 32, 64, 128, 256], fontsize=14)
ax.set_xlabel("batch_size", fontsize=14)
ax.set_ylabel("sampling rate (patches/sec)", fontsize=14)
ax.legend(loc="center right", fontsize="large")

plt.gca().spines.right.set_visible(False)
plt.gca().spines.top.set_visible(False)
plt.tight_layout()
plt.show()