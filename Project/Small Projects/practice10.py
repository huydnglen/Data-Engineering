import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
data = {'Category': ['A', 'B', 'C', 'D'], 'Value': [10, 20, 15, 30]}
df = pd.DataFrame(data)
sns.barplot(x='Category', y='Value', data=df)
plt.title('Seaborn Bar Plot')
plt.show()


