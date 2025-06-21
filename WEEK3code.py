# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris

# %%
iris = load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['species'] = iris.target_names[iris.target]

# %%
df.hist(figsize=(10, 8))
plt.suptitle('Feature Distributions in Iris Dataset')
plt.show()

# %%
sns.pairplot(df, hue='species')
plt.suptitle('Pairplot of Iris Features', y=1.02)
plt.show()

# %%
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, orient="h")
plt.title("Boxplot of Iris Features")
plt.show()

# %%
plt.figure(figsize=(8, 6))
sns.heatmap(df.drop('species', axis=1).corr(), annot=True, cmap="coolwarm")
plt.title("Feature Correlation Heatmap")
plt.show()


