# AASAT 
## 项目概述
Air-to-Air Situation Awareness and Threat assessment

本项目是一个针对空空战场态势感知和威胁评估的系统，主要关注对空作战搜索部分。系统能够根据目标高度、机动类型等参数，评估潜在威胁并判断作战意图。

## 主要功能

1. 基于目标高度判断可能的作战意图
2. 根据机动类型分析作战意图
3. 计算有效探测概率
4. 评估探测有效性因子

## 技术细节

### 威胁评估模型

威胁评估模型主要针对3代常规作战飞机，从以下三个方面对空中态势进行评估：

- 角度优势
- 距离优势
- 速度优势

该模型还对隐身飞机的情况进行了修正。
###项目结构
```plaintext  
project/
├── src/
│   ├── models/
│   ├── utils/
│   └── main.py
├── tests/
├── docs/
├── README.md
└── LICENSE
```


### 探测有效性因子
#### 多因素权重模型
$$ρ = w₁ * f(Pₐ) + w₂ * g(ECM) + w₃ * h(RCS) + w₄ * i(ENV)$$

在隐身作战条件下，我们引入多因素权重模型，引入多个影响因素，每个因素都有其对应的权重。这样可以更全面地考虑各种影响探测效果的因素。
|优点|缺点|
|------------|----------------|
|考虑多个影响因素，更全面 易于理解和实现,可以根据实际情况调整各因素的权重|可能难以准确确定各因素的权重,假设因素之间是线性关系，可能无法捕捉复杂的非线性相互作用|
```python
def calculate_rho_multi_factor(Pa, ECM, RCS, ENV, w1=0.4, w2=0.3, w3=0.2, w4=0.1):
    def f(Pa):
        return (1 / (math.exp(1) - 1)) * (math.exp(Pa) - 1)
    
    def g(ECM):
        return 1 - ECM / 100  # 假设ECM为0-100的值
    
    def h(RCS):
        return 1 / (1 + math.exp(-0.1 * (RCS - 10)))  # Sigmoid函数
    
    def i(ENV):
        return ENV / 10  # 假设ENV为0-10的值

    rho = w1 * f(Pa) + w2 * g(ECM) + w3 * h(RCS) + w4 * i(ENV)
    return rho
```
- f(Pa)：原有的探测概率函数
- g(ECM)：电子对抗能力函数
- h(RCS)：雷达截面积函数
- i(ENV)：环境因素函数（如天气、地形等）
- w1, w2, w3, w4：各因素的权重，且 w1 + w2 + w3 + w4 = 1
#### 非线性映射函数（Sigmoid）
|优点|缺点|
|------------|----------------|
|能够捕捉非线性关系输出范围固定（0到1之间），便于解释,参数较少，调整简单|可能过于简化，无法完全反映复杂的实际情况只考虑了单一因素（探测概率）|
```python
def calculate_rho_sigmoid(Pa, k=10, theta=0.5):
    return 1 / (1 + math.exp(-k * (Pa - theta)))
```
- k ：控制曲线陡度的参数
- θ：阈值参数，表示探测概率的中间值
#### 模糊逻辑方法
使用模糊逻辑来处理不确定性，可以更好地处理实际战场中的不确定因素。
|优点|缺点|
|------------|----------------|
|能够处理不确定性和模糊概念,可以融入专家知识,适合处理复杂的非线性关系|设置和调整模糊规则可能很耗时,计算复杂度较高,可能需要大量专家知识来定义规则|
```python
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def setup_fuzzy_system():

    Pa = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'Pa')
    ECM = ctrl.Antecedent(np.arange(0, 101, 1), 'ECM')
    RCS = ctrl.Antecedent(np.arange(0, 21, 1), 'RCS')
    ENV = ctrl.Antecedent(np.arange(0, 11, 1), 'ENV')

    rho = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'rho')

    # 定义模糊集
    Pa.automf(3, names=['low', 'medium', 'high'])
    ECM.automf(3, names=['weak', 'moderate', 'strong'])
    RCS.automf(3, names=['small', 'medium', 'large'])
    ENV.automf(3, names=['poor', 'fair', 'good'])
    rho.automf(5, names=['very_low', 'low', 'medium', 'high', 'very_high'])

    # 定义规则
    rule1 = ctrl.Rule(Pa['high'] & ECM['weak'] & RCS['large'] & ENV['good'], rho['very_high'])
    rule2 = ctrl.Rule(Pa['low'] & ECM['strong'] & RCS['small'] & ENV['poor'], rho['very_low'])


    # 创建控制系统
    rho_ctrl = ctrl.ControlSystem([rule1, rule2])  
    return ctrl.ControlSystemSimulation(rho_ctrl)
    
    def calculate_rho_fuzzy(Pa, ECM, RCS, ENV):
    fuzzy_system = setup_fuzzy_system()
    fuzzy_system.input['Pa'] = Pa
    fuzzy_system.input['ECM'] = ECM
    fuzzy_system.input['RCS'] = RCS
    fuzzy_system.input['ENV'] = ENV
    fuzzy_system.compute()
    return fuzzy_system.output['rho']
```
#### 动态修正因子

$$k = k0 + Δk(t, situation)$$
$$ρ = (1 / (e^k - 1)) * (e^(k*Pa) - 1)$$
|优点|缺点|
|------------|----------------|
|能够适应变化的战场环境,考虑了时间和情境因素|需要准确定义delta_k函数，这可能很复杂,需要实时数据输入和计算|
```python
def calculate_rho_dynamic(Pa, t, situation, k0=1):
    def delta_k(t, situation):
        # 根据时间和战场态势调整k值
        return 0.1 * math.sin(t) + 0.05 * situation
    k = k0 + delta_k(t, situation)
    return (1 / (math.exp(k) - 1)) * (math.exp(k * Pa) - 1)
```
其中 Δk(t, situation) 是一个随时间和战场态势变化的函数。

## 代码示例

以下是威胁评估模型的核心代码：

```python
import math

class ThreatAssessmentModel:
    def __init__(self):
        # 初始化目标高度与作战意图字典
        self.target_height_mapping = {
            (50, 200): ("突防", "攻击"),
            (200, 1000): ("运输", "攻击"),
            (1000, 6000): ("攻击", "电子干扰"),
            (6000, 8000): ("加油", "民航飞行"),
            (8000, 10000): ("预警探测", "电子干扰"),
            (10000, float('inf')): ("侦察", "突防")
        }
        
        # 初始化目标机动类型与作战意图字典
        self.maneuver_type_mapping = {
            "8字型": ("预警探测", "电子干扰"),
            "0字型": ("加油机", "预警探测"),
            "低位跃升": ("攻击", "运输"),
            "S型": ("电子干扰", ""),
            "后置跟踪转弯": ("攻击", ""),
            "水平剪刀机动": ("攻击", ""),
            "高速摇一摇": ("攻击", "")
        }

    def assess_threat(self, height, maneuver_type, detection_probability, correction_factor):

    def calculate_rho(self, k, P_a):
        term1 = (1 / (math.exp(k) - 1)) * math.exp(k * P_a)
        term2 = 1 / (math.exp(k) - 1)
        rho = term1 - term2
        return rho
if __name__ == "__main__":
    model = ThreatAssessmentModel()
    result = model.assess_threat(height=650, maneuver_type="8字型", detection_probability=0.75, correction_factor=0.9)
    print("威胁评估结果:")
    for key, value in result.items():
        print(f"{key}: {value}")
```
## 建议：
考虑到空空战场态势感知与威胁评估系统的复杂性，我们采取以下策略：

首先实施多因素权重模型，因为它相对简单且易于实现和调整。这可以作为基线模型。
如果发现单一因素（如探测概率）对结果影响特别大，可以考虑将该因素用非线性映射函数（如Sigmoid）处理，而保持其他因素线性。
如果能够实时获取战场数据，可以尝试实现动态修正因子，以适应不断变化的战场环境。
长期来看，如果能收集到足够的数据，可以训练机器学习模型。可以从简单的模型（如随机森林）开始，逐步过渡到更复杂的模型。
如果有丰富的领域专家知识，我们使用模糊逻辑方法，但要这可能需要较长的开发和调试时间。
