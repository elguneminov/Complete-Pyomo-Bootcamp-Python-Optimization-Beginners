#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyomo.environ import *
import matplotlib.pyplot as plt
import numpy as np


# In[2]:


model = ConcreteModel()
model.epsilon=Param(initialize=10000,mutable=True)
model.x1 = Var(bounds=(1,2), within=NonNegativeReals)
model.x2 = Var(bounds=(1,3), within=NonNegativeReals)
model.OF1= Var(bounds=(-10000,10000), within=NonNegativeReals)
model.OF2= Var(bounds=(-10000,10000), within=NonNegativeReals)

model.eq1= Constraint(expr= model.OF2==-1.2*model.x1**2+5*model.x2)
model.eq2= Constraint(expr= model.OF2<=model.epsilon)
model.eq3= Constraint(expr= model.OF1==2*model.x1-0.5*model.x2**2)

model.obj1 = Objective(expr=model.OF1, sense=maximize)
model.obj2 = Objective(expr=model.OF2, sense=maximize)
opt = SolverFactory('ipopt')


# In[3]:


model.obj2.deactivate() 
results = opt.solve(model) # solves and updates instance
print('x1 = ',round(value(model.x1),2))
print('x2 = ',round(value(model.x2),2))
print('obj1 = ',round(value(model.obj1),2))
print('obj2 = ',round(value(model.obj2),2))
maxOF1=value(model.obj1)
minOF2=value(model.obj2)


# In[4]:


model.obj1.deactivate() 
model.obj2.activate() 
results = opt.solve(model) # solves and updates instance
print('x1 = ',round(value(model.x1),2))
print('x2 = ',round(value(model.x2),2))
print('obj1 = ',round(value(model.obj1),2))
print('obj2 = ',round(value(model.obj2),2))
minOF1=value(model.obj1)
maxOF2=value(model.obj2)


# In[5]:


Nsteps=21
X=[]
Y=[]
print('  x1  ',' x2 ',' OF1 ',' OF2 ',' Epsilon ')
for counter in range(1,Nsteps+1):
    model.epsilon=minOF2+(maxOF2-minOF2)*(counter-1)/(Nsteps-1)
    results = opt.solve(model) # solves and updates instance
    print("%5.2f"% value(model.x1),"%5.2f"% value(model.x2),"%5.2f"% value(model.obj1),"%5.2f"% value(model.obj2), "%5.2f"% value(model.epsilon))
    X.append(value(model.obj1))
    Y.append(value(model.obj2))


# In[6]:


fig = plt.figure(figsize=(8,6))
plt.scatter(X,Y)
plt.xlabel('OF1',fontweight='bold')
plt.ylabel('OF2',fontweight='bold')
plt.grid()
plt.show()

