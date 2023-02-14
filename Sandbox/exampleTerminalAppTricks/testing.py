import pandas as pd

data = pd.DataFrame({'a':['10000','-2423.34','3','4','5'], 'b':['2','3','4','54332','13426.42']})
data = pd.to_numeric(data['b'], errors='coerce')
print(data)