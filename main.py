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
        # 评估高度对应的作战意图
        for (low, high), intentions in self.target_height_mapping.items():
            if low <= height < high:
                primary_intent, secondary_intent = intentions
                break
        else:
            primary_intent, secondary_intent = ("未知", "未知")

        # 评估机动类型对应的作战意图
        primary_maneuver_intent, secondary_maneuver_intent = self.maneuver_type_mapping.get(maneuver_type,
                                                                                            ("未知", "未知"))

        # 计算有效探测概率
        effective_detection_probability = detection_probability * correction_factor

        # 计算探测有效性因子
        def calculate_rho(k, P_a):
            term1 = (1 / (math.exp(k) - 1)) * math.exp(k * P_a)
            term2 = 1 / (math.exp(k) - 1)
            rho = term1 - term2
            return rho

        rho = calculate_rho(correction_factor, detection_probability)

        # 输出结果
        return {
            "目标高度": height,
            "机动类型": maneuver_type,
            "主要作战意图": primary_intent,
            "次要作战意图": secondary_intent,
            "机动主要作战意图": primary_maneuver_intent,
            "机动次要作战意图": secondary_maneuver_intent,
            "有效探测概率": effective_detection_probability,
            "探测有效性因子": rho
        }


if __name__ == "__main__":
    model = ThreatAssessmentModel()
    result = model.assess_threat(height=650, maneuver_type="8字型", detection_probability=0.75, correction_factor=0.9)

    print("威胁评估结果:")
    for key, value in result.items():
        print(f"{key}: {value}")

k = 1.0  # 可以根据需要修改
P_a = 2.0  # 可以根据需要修改

# 计算探测有效性因子
def calculate_rho(k, P_a):
    term1 = (1 / (math.exp(k) - 1)) * math.exp(k * P_a)
    term2 = 1 / (math.exp(k) - 1)
    rho = term1 - term2
    return rho

# 计算结果
result = calculate_rho(k, P_a)
print(f"计算结果 ρ: {result}")
