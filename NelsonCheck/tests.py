import unittest
import NelsonCheck as NC
import numpy, random

def get_gauss_data(mu=0, sigma=1, size=15):
    return [random.gauss(mu,sigma) for i in range(size)]

class TestRuleViolations(unittest.TestCase):
    nrd = {}
    for i in range(1,9):
        nrd[f'nr{i}'] = NC.NelsonRule(i)
    def test_rule1(self):
        rule_num=1
        data = [1,2,3,2,4,1,2,3,2,1,2,5,1000]
        nc = NC.NelsonCheck(data=data)
        cond = rule_num in [nv.rule.num for nv in nc.violations] 
        self.assertTrue(cond)
        
        data = [1,2,3,2,4,1,2,3,2,1,2,5]
        nc = NC.NelsonCheck(data=data)
        cond = rule_num in [nv.rule.num for nv in nc.violations] 
        self.assertFalse(cond)
        
    def test_rule2(self):
        rule_num = 2
        bdatas = [
            [1,2,3,2,4,1,2,3,2,1,2,5,4,1000],
            [1,2,3,2,4,1,2,3,2,1,2,5,4,-1000],
        ]
        for data in bdatas:
            nc = NC.NelsonCheck(data=data)
            cond = rule_num in [nv.rule.num for nv in nc.violations] 
            self.assertTrue(cond)
        gdatas = [
            [1,2,3,2,4,1,2,3,2,1,2,5,4],
            [1,2,3,2,4,1,2,3,2,1,2,5,4],
            get_gauss_data(15)
        ]
        for data in gdatas:
            nc = NC.NelsonCheck(data=data)
            cond = rule_num in [nv.rule.num for nv in nc.violations] 
            self.assertFalse(cond)    
              
    def test_rule3(self):
        rule_num=3
        bdatas = [
            [1,2,3,4,5,6,7],
            [1,0,-1,-45,-100,-134,-400],
        ]
        for data in bdatas:
            nc = NC.NelsonCheck(data=data)
            cond = rule_num in [nv.rule.num for nv in nc.violations] 
            self.assertTrue(cond)
        gdatas = [
            [1,2,3,2,4,1,2,3,2,1,2,5,4],
            [1,2,3,2,4,1,2,3,2,1,2,5,4],
            get_gauss_data(15)
        ]
        for data in gdatas:
            nc = NC.NelsonCheck(data=data)
            cond = rule_num in [nv.rule.num for nv in nc.violations] 
            self.assertFalse(cond)         
        
    def test_rule4(self):
        rule_num=4
        bdatas = [
            [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1],
            [-1,2,1,2,-4,2,1,2,1,2,1,2,1,2,-2,5,1,89],
        ]
        for data in bdatas:
            nc = NC.NelsonCheck(data=data)
            cond = rule_num in [nv.rule.num for nv in nc.violations] 
            self.assertTrue(cond)
        gdatas = [
            [1,2,1,2,1,2,1,1,1,2,1,2,1,2,1],
            [-1,2,1,2,-4,-45,1,2,1,2,1,2,3,2,-2,5,1,89],
            get_gauss_data(15)
        ]
        for data in gdatas:
            nc = NC.NelsonCheck(data=data)
            cond = rule_num in [nv.rule.num for nv in nc.violations] 
            self.assertFalse(cond)            
            
    def test_rule5(self):
        rule_num=5
        bdatas = [
            [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,3,4,2,2,2,1,2,500,500],
            [-1,2,1,2,-4,2,1,2,1,2,1,2,1,2,-2,1,2,3,1,1,1,2,-500,-500],
        ]
        for data in bdatas:
            nc = NC.NelsonCheck(data=data)
            cond = rule_num in [nv.rule.num for nv in nc.violations] 
            self.assertTrue(cond)
        gdatas = [
            [1,2,1,2,1,2,1,1,1,2,1,2,1,2,1,200],
            [-1,2,1,2,-4,1,2,1,2,1,2,3,2,-2,5,1,-200],
            get_gauss_data(15)
        ]
        for data in gdatas:
            nc = NC.NelsonCheck(data=data)
            cond = rule_num in [nv.rule.num for nv in nc.violations] 
            self.assertFalse(cond)                  
            
    def test_rule6(self):
        rule_num=6
        bdatas = [
            [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,3,4,2,2,20,20,20,20],
            [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,3,4,2,2,-20,-20,-20,-20],
        ]
        for data in bdatas:
            nc = NC.NelsonCheck(data=data)
            cond = rule_num in [nv.rule.num for nv in nc.violations] 
            self.assertTrue(cond)
        gdatas = [
            #[1,2,1,2,1,2,1,1,1,2,1,2,1,2,1,20,20,20],
            #[-1,2,1,2,-4,1,2,1,2,1,2,3,2,-2,2,1,-20,-20,-20],
            get_gauss_data(15)
        ]
        for data in gdatas:
            nc = NC.NelsonCheck(data=data)
            cond = rule_num in [nv.rule.num for nv in nc.violations] 
            self.assertFalse(cond)
                               
            
    def test_rule7(self):
        rule_num=7
        bdatas = [
            [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,1,2,2,2,1,2,1,2,200,200],
        ]
        for data in bdatas:
            nc = NC.NelsonCheck(data=data)
            cond = rule_num in [nv.rule.num for nv in nc.violations] 
            self.assertTrue(cond)
        gdatas = [
            get_gauss_data(15)
        ]
        for data in gdatas:
            nc = NC.NelsonCheck(data=data)
            cond = rule_num in [nv.rule.num for nv in nc.violations] 
            self.assertFalse(cond)               
            

    def test_rule8(self):
        rule_num=8
        bdatas = [
            [0,10,0,10,0,10,0,10,0,10,0,10,0,10,0,10],
        ]
        for data in bdatas:
            nc = NC.NelsonCheck(data=data,UCL=4,LCL=6)
            cond = rule_num in [nv.rule.num for nv in nc.violations] 
            self.assertTrue(cond)
        gdatas = [
            get_gauss_data(15)
        ]
        for data in gdatas:
            nc = NC.NelsonCheck(data=data)
            cond = rule_num in [nv.rule.num for nv in nc.violations] 
            self.assertFalse(cond)   
                        
            
if __name__ == '__main__':
    unittest.main()
    
    
    
    
    
    
    
    
    
    
    
    