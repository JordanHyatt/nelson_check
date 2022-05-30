from pandas import DataFrame as DF
from pandas import Series
from pandas import concat
import numpy as np
import plotly.graph_objects as go

class NelsonRule:
    RULES = {
        1:{
            'num':1,
            'desc':'One point is more than 3 standard deviations from the mean',
            'problem':'One sample is grossly out of control.',
        },
        2:{
            'num':2,
            'desc':'Nine or more points in a row are on the same side of the mean',
            'problem':'Some prolonged bias exists'
        },
        3:{
            'num':3,
            'desc':'Six or more points in a row are continually increasing or decreasing',
            'problem':'A trend exist',
        },
        4:{
            'num':4,
            'desc':'Fourteen or more points in a row alternate in direction, increasing then decreasing',
            'problem':'This much oscillation is beyond noise',
        },
        5:{
            'num':5,
            'desc':'Two or three out of three points in a row are more than 2 standard deviations from the mean in the same direction',
            'problem':'Medium tendency for samples to be mediumly out of control',
        },
        6:{
            'num':6,
            'desc':'Four or five out of five points in a row are more than 1 standard deviation from the mean in the same direction',
            'problem':'Strong tendency for samples to be slightly out of control',
        },
        7:{
            'num':7,
            'desc':'Fifteen points in a row are all within 1 standard deviation of the mean on either side of the mean',
            'problem':'Greater variation would be expected',
        },
        8:{
            'num':8,
            'desc':'Eight points in a row exist, but none within 1 standard deviation of the mean, and the points are in both directions from the mean',
            'problem':'Jumping about and below while skipping the 1 sigma band is rarely random',
        },
    }
    def __init__(self,num):
        assert type(num)==int, "Rule Number Must Be an Integer Between 1-8"
        assert (num>=1 and num<=8), "Rule Number Must Be an Integer Between 1-8"
        self.num = num
        self.desc = self.RULES[self.num]['desc']
        self.problem = self.RULES[self.num]['problem']
    def __str__(self):
        return f'Nelson Rule {self.num}'

    def __repr__(self):
        return f'NelsonRule({self.num})'
        
        
class NelsonViolation:
    def __init__(self,rule,offenders):
        self.rule = rule
        self.offenders = offenders
        
    def __str__(self):
        return f'Nelson Violation {self.rule}'

    def __repr__(self):
        return f'NelsonViolation({self.rule},{self.offenders})' 
        
        
class NelsonCheck:
    def __init__(self, data, CL=None, LCL=None, UCL=None, exclude_rules=[]):
        self.violations = []#List Of Nelston Violation Objects
        self.result = True # Result after testing rules
        self.data=Series(data, name='data'); self.CL=CL; self.LCL=LCL; self.UCL=UCL
        if self.CL==None: self.CL=np.mean(self.data)
        std = np.std(self.data)
        if self.LCL==None: self.LCL=self.CL - 3*std
        if self.UCL==None: self.UCL=self.CL + 3*std
        
        self.rule_check_dict = {
            1:self.check_rule1,2:self.check_rule2,3:self.check_rule3,
            4:self.check_rule4,5:self.check_rule5,6:self.check_rule6,
            7:self.check_rule7,
            8:self.check_rule8,
        }
        for rule_num in exclude_rules:
            self.rule_check_dict.pop(rule_num)
        for rule_check in self.rule_check_dict.values():
            rule_check()
       
    def process_offenders(self,rule,offenders):
        if len(offenders) > 0:
            local_result = False
            self.result=False
            violation = NelsonViolation(rule,offenders)
            self.violations.append(violation)
        else:
            local_result=True
        return local_result,offenders     
        
    
    def check_rule1(self):
        ''' Method to check for and process Rule1 violations'''
        rule = NelsonRule(1) # Pull rule1 object for processing
        # Create masks for data points above and below UCL and LCL
        mask1 = self.data<self.LCL
        mask2 = self.data>self.UCL
        # Filter the data to only contain those points in violation 
        _r1_offenders = self.data[mask1|mask2]
        return self.process_offenders(rule,_r1_offenders)

    def check_rule2(self):
        rule = NelsonRule(2)
        df = DF()
        df['ser'] = self.data
        df['above'] = self.data > self.CL
        df['grouping'] = (df['above'] != df['above'].shift()).cumsum()
        group_counts = df.groupby('grouping')['above'].count()
        offending_groups = group_counts[group_counts >= 9]
        _r2_offenders = df[df['grouping'].isin(offending_groups.index)]['ser']
        return self.process_offenders(rule,_r2_offenders)
    
    def check_rule3(self):
        rule = NelsonRule(3)
        df = DF()
        df['ser'] = self.data
        df['above'] = (self.data - self.data.shift())>0
        df['grouping'] = (df['above'] != df['above'].shift()).cumsum()
        group_counts = df.groupby('grouping')['above'].count()
        offending_groups = group_counts[group_counts >= 6]
        _r3_offenders = df[df['grouping'].isin(offending_groups.index)]['ser']
        return self.process_offenders(rule,_r3_offenders)     

    def check_rule4(self):
        rule = NelsonRule(4)
        df = DF()
        data = self.data
        df['ser'] = data
        df['position'] = [i for i in range(len(df))]
        df['prev'] = data.shift(1)
        df['dif'] = df['ser'] - df['prev']
        def get_label(val):
            if val>0:
                return 'up'
            elif val==0:
                return 'same'
            else:
                return 'down'
        df['label'] = df.dif.apply(get_label)
        df['nlabel'] = df['label'].shift(-1)
        def get_same_dir(ser):
            m1 = ser.label != ser.nlabel
            m2 = ser.label != 'same'
            m3 = ser.nlabel != 'same'
            if m1 and m2 and m3:
                return False
            else:
                return True
        df['same_dir']=df.apply(get_same_dir,axis=1)
        df['rsum'] = df['same_dir'].rolling(12).sum()

        bad_positions = list(df[df.rsum==0].position)
        all_bad_positions = []
        for pos in bad_positions:
            all_bad_positions += [pos-i for i in range(-1,13)]
        _r4_offenders = df[df.position.isin(all_bad_positions)]['ser']
        return self.process_offenders(rule,_r4_offenders)   
    
    def check_rule5(self):
        rule = NelsonRule(5)
        df = DF()
        df['ser'] = self.data
        df['position'] = [i for i in range(len(df))]
        ulim=(self.CL + 2*(self.UCL-self.CL)/3)
        llim=(self.CL - 2*(self.CL-self.LCL)/3)
        df['high']=df['ser']>ulim
        df['low']=df['ser']<llim
        df['high_count'] = df.high.rolling(3).sum()
        df['low_count'] = df.low.rolling(3).sum()
        m = df.high_count >= 2
        bad_high_positions = list(df[m].position)
        m = df.low_count >= 2 
        bad_low_positions = list(df[m].position)
        all_bad_high = []
        for pos in bad_high_positions:
            all_bad_high += [pos, pos-1, pos-2]
        all_bad_low = []
        for pos in bad_low_positions:
            all_bad_low += [pos, pos-1, pos-2]
        m1 = df['high'] == True
        m2= df.position.isin(all_bad_high)
        high_offenders = df[m1&m2]['ser']
        m1 = df['low'] == True
        m2= df.position.isin(all_bad_low)
        low_offenders = df[m1&m2]['ser']
        _r5_offenders = concat([high_offenders, low_offenders])
        return self.process_offenders(rule,_r5_offenders) 

    def check_rule6(self):
        rule = NelsonRule(6)
        df = DF()
        df['ser'] = self.data
        df['position'] = [i for i in range(len(df))]
        ulim=(self.CL + 1*(self.UCL-self.CL)/3)
        llim=(self.CL - 1*(self.CL-self.LCL)/3)
        df['high']=df['ser']>ulim
        df['low']=df['ser']<llim
        df['high_count'] = df.high.rolling(5).sum()
        df['low_count'] = df.low.rolling(5).sum()
        m = df.high_count >= 4
        bad_high_positions = list(df[m].position)
        m = df.low_count >= 4
        bad_low_positions = list(df[m].position)
        all_bad_high = []
        for pos in bad_high_positions:
            all_bad_high += [pos, pos-1, pos-2, pos-3, pos-4]
        all_bad_low = []
        for pos in bad_low_positions:
            all_bad_low += [pos, pos-1, pos-2, pos-3, pos-4]
        m1 = df['high'] == True
        m2= df.position.isin(all_bad_high)
        high_offenders = df[m1&m2]['ser']
        m1 = df['low'] == True
        m2= df.position.isin(all_bad_low)
        low_offenders = df[m1&m2]['ser']
        _r5_offenders = concat([high_offenders, low_offenders])
        return self.process_offenders(rule,_r5_offenders) 


    def check_rule7(self):
        rule = NelsonRule(7)
        df = DF()
        df['ser'] = self.data
        df['ulim']=(self.CL + 1*(self.UCL-self.CL)/3)
        df['llim']=(self.CL - 1*(self.CL-self.LCL)/3)
        mask1 = df['ser']>df['llim']
        mask2 = df['ser']<df['ulim']    
        df['inside']=mask1&mask2 
        df['grouping']=(df['inside'] != df['inside'].shift()).cumsum()
        group_counts = df.groupby('grouping')['inside'].count()
        offending_groups = group_counts[group_counts >= 15]
        _r7_offenders = df[df['grouping'].isin(offending_groups.index)]['ser']
        return self.process_offenders(rule,_r7_offenders)   

    def check_rule8(self):
        rule = NelsonRule(8)
        df = DF()
        df['ser'] = self.data
        df['ulim']=(self.CL + 1*(self.UCL-self.CL)/3)
        df['llim']=(self.CL - 1*(self.CL-self.LCL)/3)
        mask1 = df['ser']<df['llim']
        mask2 = df['ser']>df['ulim']    
        df['outside']=mask1|mask2
        df['grouping']=(df['outside'] != df['outside'].shift()).cumsum()
        group_counts = df.groupby('grouping')['outside'].sum()
        offending_groups = group_counts[group_counts >= 8]
        _r8_offenders = df[df['grouping'].isin(offending_groups.index)]['ser']
        return self.process_offenders(rule,_r8_offenders)   
        
    def plot(self):
        ''' Method generates and returns a plotly figure of the data + violations '''
        df = DF(self.data)
        df['UCL'] = self.UCL
        df['LCL'] = self.LCL
        df['CL'] = self.CL
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df.data, name='data', mode='markers'))
        fig.add_trace(go.Scatter(x=df.index, y=df.LCL, name='LCL', marker_color='orange'))
        fig.add_trace(go.Scatter(x=df.index, y=df.CL, name='CL', marker_color='tan'))
        fig.add_trace(go.Scatter(x=df.index, y=df.UCL, name='UCL', marker_color='orange'))
        for vio in self.violations:
            fig.add_trace(go.Scatter(x=vio.offenders.index, y=vio.offenders.values, name=str(vio.rule), marker_color='red', mode='markers'))    
        return fig

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
