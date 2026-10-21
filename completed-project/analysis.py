# Run from this project folder. All values are synthetic.

import sys
import pandas as pd

print(sys.executable)
print(pd.__version__)

data = pd.read_csv("data/practice.csv")
print(data)

means = data.groupby("condition")["rt_ms"].mean()
print(means)

from pathlib import Path
import matplotlib.pyplot as plt

Path("outputs").mkdir(exist_ok=True)
means.plot.bar(ylabel="Mean reaction time (ms)", rot=0)
plt.title("Practice data")
plt.tight_layout()
plt.savefig("outputs/means.png")
plt.show()
