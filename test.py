import unittest
import pandas as pd, random


def create_data():
    sample_size = 10
    num_samples = 20

    df = pd.DataFrame(columns=['mean','std'])

    for i in range(1,num_samples+1):
        points = [random.gauss(sample_size,1) for i in range(0,sample_size)]
        df.loc[f'sample{i}'] = {'mean':np.mean(points),'std':np.std(points)}
    output = {}
    output['CL'] = df['mean'].mean()
    output['LCL'] = CL - 3*df['std'].mean()
    output['UCL'] = CL + 3*df['std'].mean()
    output['data'] = df['mean']
    return output


class TestCheckRule1(unittest.TestCase):
    pass
    
    
    
    