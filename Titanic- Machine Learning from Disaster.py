#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Load data
import pandas as pd

train = pd.read_csv('/users/Anurag/desktop/titanic/train.csv')
test = pd.read_csv('/users/Anurag/desktop/titanic/test.csv')

#Drop features we are not going to use
train = train.drop(['Name','SibSp','Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked'],axis=1)
test = test.drop(['Name','SibSp','Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked'],axis=1)

#Look at the first 3 rows of our training data
train.head(3)


# In[2]:


#Convert ['male','female'] to [1,0] so that our decision tree can be built
for df in [train,test]:
    df['Sex_binary']=df['Sex'].map({'male':1,'female':0})
    
#Fill in missing age values with 0 (presuming they are a baby if they do not have a listed age)
train['Age'] = train['Age'].fillna(0)
test['Age'] = test['Age'].fillna(0)

#Select feature column names and target variable we are going to use for training
features = ['Pclass','Age','Sex_binary']
target = 'Survived'

#Look at the first 3 rows (we have over 800 total rows) of our training data.; 
#This is input which our classifier will use as an input.
train[features].head(3)


# In[3]:


#Display first 3 target variables
train[target].head(3).values


# In[ ]:


from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression 
from sklearn.model_selection import GridSearchCV 
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold

c_space = np.logspace(-4, 8, 25) 
param_grid = {'C': c_space,} 
  

logreg = LogisticRegression() 

logreg_cv = GridSearchCV(logreg, param_grid, cv = 5) 
logreg_cv.fit(train[features],train[target]) 


# In[28]:


#Make predictions using the features from the test data set
predictions = logreg_cv.predict(test[features])

#Display our predictions - they are either 0 or 1 for each training instance 
#depending on whether our algorithm believes the person survived or not.
predictions


# In[29]:


#Create a  DataFrame with the passengers ids and our prediction regarding whether they survived or not
submission = pd.DataFrame({'PassengerId':test['PassengerId'],'Survived':predictions})

#Visualize the first 5 rows
submission.head()


# In[30]:


#Convert DataFrame to a csv file that can be uploaded
#This is saved in the same directory as your notebook
filename = 'Titanic Predictions 1.csv'

submission.to_csv(filename,index=False)

print('Saved file: ' + filename)

