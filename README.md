# NelsonCheck
A simple package for applying Nelson Rules to control chart data.


## Installation
Requires python V3 
```sh
$ pip install NelsonCheck
```

## Sample Usage 

### NelsonRule Class
Instances of the NelsonRule class give the description of the rule\
note: num parameter must be an integer 1-8
```python 
  from NelsonCheck import NelsonCheck as NC
  nr1 = NC.NelsonRule(num=1)
  nr5 = NC.NelsonRule(num=2)
  print(nr1,nr1.desc)
  print(nr5,nr5.desc)
```
output:
```
Nelson Rule 1 One point is more than 3 standard deviations from the mean
Nelson Rule 5 Two or three out of three points in a row are more than 2 standard 
deviations from the mean in the same direction
```

### Running Nelson Check on Dataset
```python
from NelsonCheck import NelsonCheck as NC
import random
#  Generate Random Data That will violate nelson rules
data = [random.random() for i in range(0,100)]
nc = NC.NelsonCheck(data=data)
```
The instance created will have an attribute called *violations*
which is a list of NelsonViolation objects.  Each NelsonViolation object will
have an attribute *rule* which will be a NelsonRule instance and an attribute 
*offenders* which will be a pandas series of the data points that violated the 
rule

```python
for nv in nc.violations:
  print (nv.rule)
  print (nv.rule.desc)
  print(nv.offenders)
  print('************')
```
output:
```
Nelson Rule 2
Nine or more points in a row are on the same side of the mean
34    10.531433
35    10.481213
36    10.893916
37    10.631122
38    10.668241
39    10.508670
40    10.747603
41    10.950496
42    10.938109
Name: ser, dtype: float64
************
Nelson Rule 6
Four or five out of five points in a row are more than 1 standard deviation from 
the mean in the same direction
93    10.115869
94    10.932090
95    10.595130
96    10.928870
99    10.905234
Name: ser, dtype: float64
************
```
