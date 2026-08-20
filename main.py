import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = {
        "Name": ["Alice", "Bob", "Charlie", "David", "Eva"],
        "Age": [25, 30, 35, 40, 45],
}
df = pd.DataFrame(data)
print(df)
plt.bar(df["Name"], df["Age"])
plt.xlabel("Name")
plt.ylabel("Age")
plt.title("Age of Individuals")
plt.show()