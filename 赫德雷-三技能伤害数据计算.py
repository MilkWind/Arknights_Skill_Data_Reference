import random


def vertigo_probability(probability: float):
    return random.random() < probability


# 默认满级满潜
base_attack = 1576 + 80 + 45  # 基础攻击
attack_interval = 2.5  # 攻击间隔
talent_triggering_addition = 1.4  # 天赋触发攻击力提升至比例
talent_not_triggering_addition = 1.1  # 天赋未触发攻击力提升至比例
skill_addition = 1.2  # 技能加成比例
skill_duration = 70  # 技能持续
skill_cooling = 50  # 技能回转
skill_vertigo_probability = 0.25  # 技能眩晕概率
skill_vertigo_duration = 5  # 技能眩晕时间
true_damage_dps = 200  # 技能每秒真伤

attacks_num = int(skill_duration / attack_interval)  # 技能期间攻击次数
actual_attack_in_skill = base_attack * (1 + skill_addition)  # 技能期间实际攻击力

cycles_num = 100000  # 模拟次数
damage_sum = 0  # 模拟总伤
total_true_damage = true_damage_dps * (skill_duration - 0.5)  # 假设抬手15帧、真伤判定按帧计数

for _ in range(cycles_num):
    total_damage = total_true_damage  # 初始设置为真伤总伤
    vertigo_duration = 0  # 眩晕剩余时间

    for _ in range(attacks_num):
        # vertigo_duration = skill_vertigo_duration
        if vertigo_probability(skill_vertigo_probability):
            vertigo_duration = skill_vertigo_duration
        if vertigo_duration > 0:  # 当眩晕时间为0时，假定刚好不触发天赋
            total_damage += actual_attack_in_skill * talent_triggering_addition
        else:
            total_damage += actual_attack_in_skill * talent_not_triggering_addition
        vertigo_duration -= attack_interval

    damage_sum += total_damage  # 总伤叠加

average_damage = damage_sum / cycles_num  # 平均总伤
average_dps = (int(skill_cooling / attack_interval) * base_attack * talent_not_triggering_addition + average_damage) / (
        skill_duration + skill_cooling)  # 平均dps

print(f"技能总伤：{average_damage}")
print(f"技能真伤总伤：{total_true_damage}")
print(f"技能dps：{average_damage / skill_duration}")
print(f"技能dph（触发天赋）：{actual_attack_in_skill * talent_triggering_addition}")
print(f"技能dph（不触发天赋）：{actual_attack_in_skill * talent_not_triggering_addition}")
print(f"平均dps：{average_dps}")
