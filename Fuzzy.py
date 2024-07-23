import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def setup_fuzzy_system():
    # 输入变量
    Pa = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'Pa')
    ECM = ctrl.Antecedent(np.arange(0, 101, 1), 'ECM')
    RCS = ctrl.Antecedent(np.arange(0, 21, 1), 'RCS')
    ENV = ctrl.Antecedent(np.arange(0, 11, 1), 'ENV')

    # 输出变量
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
    # ... 添加更多规则

    # 创建控制系统
    rho_ctrl = ctrl.ControlSystem([rule1, rule2])  # 添加所有规则
    return ctrl.ControlSystemSimulation(rho_ctrl)

def calculate_rho_fuzzy(Pa, ECM, RCS, ENV):
    fuzzy_system = setup_fuzzy_system()
    fuzzy_system.input['Pa'] = Pa
    fuzzy_system.input['ECM'] = ECM
    fuzzy_system.input['RCS'] = RCS
    fuzzy_system.input['ENV'] = ENV
    fuzzy_system.compute()
    return fuzzy_system.output['rho']