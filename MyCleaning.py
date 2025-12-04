import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("dirty_cafe_sales.csv")

print(df.head().to_string())
print(df.info())