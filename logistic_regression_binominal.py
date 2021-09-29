import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from collections import Counter

array_suport = ['num_If', 'num_Switch', 'num_Loof', 'num_Break', 'num_Priority', 'num_Sort', 'num_Hash_Map', 'num_Hash_Set', 'num_Recursive', 'num_Nasted_Loop', 'num_Variables', 'num_Method', 'num_State']
data_frame = pd.DataFrame(columns=array_suport)

data = pd.read_csv('base_dados/out_binomial.csv').dropna()

data_values = data.iloc[:, :13].values

data_complexity = data.iloc[:, 13:].values
data_complexity = [int(x) for x in data_complexity]

logmodel = LogisticRegression(n_jobs=5, max_iter=500).fit(data_values, data_complexity)
predictions = logmodel.predict(data_values)

print(logmodel.score(data_values, data_complexity))

print('Predictions', Counter(predictions))
print('True values', Counter(data_complexity))

print('Matrix de Confusão')
print(confusion_matrix(data_complexity, predictions))

print('Precisão Computacional')
print(classification_report(data_complexity, predictions))


for i in range(len(data_complexity)):
    data_frame.loc[i] = data_values[i]

array_true = [predictions[i] == data_complexity[i] for i in range(len(data_complexity))]

data_frame = data_frame.assign(complexity=data_complexity)
data_frame = data_frame.assign(complexity_predicted=predictions)
data_frame = data_frame.assign(acertos=array_true)

print(data_frame)

with open('models_regression_store/logistic_regression_binomial.pkl', 'wb') as file:
    pickle.dump(logmodel, file)
