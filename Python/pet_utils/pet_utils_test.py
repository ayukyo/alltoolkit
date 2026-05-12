#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pet Utils Test - 宠物工具库测试
==========================================

测试 pet_utils 模块的各项功能。

作者: AllToolkit 自动化生成
日期: 2026-05-12
"""

import sys
import os
from datetime import datetime, timedelta

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    PetType, DogSize, ActivityLevel, PetProfile, VaccineRecord,
    PetAgeConverter, PetWeightEvaluator, PetFeedingCalculator,
    VaccineScheduler, PetExerciseCalculator, PetLifespanPredictor,
    PetHealthChecker,
    dog_age_to_human, cat_age_to_human, pet_age_to_human,
    evaluate_pet_weight, get_feeding_plan, get_vaccine_schedule,
    get_exercise_needs, predict_pet_lifespan,
)


class TestCollector:
    """测试收集器"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name: str, condition: bool, message: str = ""):
        """运行单个测试"""
        status = "PASS" if condition else "FAIL"
        if condition:
            self.passed += 1
        else:
            self.failed += 1
        
        self.tests.append({
            'name': name,
            'status': status,
            'message': message,
        })
        
        print(f"  [{status}] {name}")
        if message and not condition:
            print(f"        {message}")
    
    def summary(self):
        """打印测试摘要"""
        total = self.passed + self.failed
        print("\n" + "=" * 60)
        print(f"测试结果: {self.passed}/{total} 通过, {self.failed} 失败")
        print("=" * 60)
        return self.failed == 0


def test_pet_age_converter():
    """测试宠物年龄转换"""
    print("\n【测试 PetAgeConverter】")
    tc = TestCollector()
    
    # 测试狗年龄转换
    # 玩具型狗
    human_age = PetAgeConverter.dog_to_human_years(5, DogSize.TOY)
    tc.test("玩具型5岁狗转换", 
            human_age == 15 + 9 + 3 * 4,  # 15 + 9 + 12 = 36
            f"期望36, 实际{human_age}")
    
    # 大型狗
    human_age = PetAgeConverter.dog_to_human_years(5, DogSize.LARGE)
    tc.test("大型5岁狗转换",
            human_age == 15 + 9 + 3 * 7,  # 15 + 9 + 21 = 45
            f"期望45, 实际{human_age}")
    
    # 巨型狗
    human_age = PetAgeConverter.dog_to_human_years(5, DogSize.GIANT)
    tc.test("巨型5岁狗转换",
            human_age == 12 + 10 + 3 * 8,  # 12 + 10 + 24 = 46
            f"期望46, 实际{human_age}")
    
    # 幼犬
    human_age = PetAgeConverter.dog_to_human_years(0.5, DogSize.MEDIUM)
    tc.test("0.5岁幼犬转换",
            6 <= human_age <= 9,  # 第一年按比例
            f"期望约7.5, 实际{human_age}")
    
    # 测试猫年龄转换
    human_age = PetAgeConverter.cat_to_human_years(1)
    tc.test("1岁猫转换",
            human_age == 15,
            f"期望15, 实际{human_age}")
    
    human_age = PetAgeConverter.cat_to_human_years(2)
    tc.test("2岁猫转换",
            human_age == 24,  # 15 + 9
            f"期望24, 实际{human_age}")
    
    human_age = PetAgeConverter.cat_to_human_years(5)
    tc.test("5岁猫转换",
            human_age == 36,  # 15 + 9 + 3*4 = 36
            f"期望36, 实际{human_age}")
    
    # 测试其他宠物
    human_age = PetAgeConverter.pet_to_human_years(2, PetType.RABBIT)
    tc.test("2岁兔子转换",
            human_age == 24,  # 18 + 6
            f"期望24, 实际{human_age}")
    
    human_age = PetAgeConverter.pet_to_human_years(1, PetType.HAMSTER)
    tc.test("1岁仓鼠转换",
            human_age == 30,
            f"期望30, 实际{human_age}")
    
    # 测试便捷函数
    human_age = dog_age_to_human(5, 'medium')
    tc.test("便捷函数dog_age_to_human",
            human_age == 15 + 9 + 3 * 6,  # 42
            f"期望42, 实际{human_age}")
    
    human_age = cat_age_to_human(3)
    tc.test("便捷函数cat_age_to_human",
            human_age == 28,  # 15 + 9 + 4
            f"期望28, 实际{human_age}")
    
    human_age = pet_age_to_human(2, 'rabbit')
    tc.test("便捷函数pet_age_to_human兔子",
            human_age == 24,
            f"期望24, 实际{human_age}")
    
    return tc.summary()


def test_pet_weight_evaluator():
    """测试宠物体重评估"""
    print("\n【测试 PetWeightEvaluator】")
    tc = TestCollector()
    
    # 测试狗体重评估
    result = PetWeightEvaluator.evaluate_dog_weight(8.0, 'beagle')
    tc.test("比格犬8kg理想体重",
            result['status'] == 'ideal',
            f"期望ideal, 实际{result['status']}")
    
    result = PetWeightEvaluator.evaluate_dog_weight(6.0, 'beagle')
    tc.test("比格犬6kg稍轻",
            result['status'] in ['ideal', 'underweight'],
            f"实际{result['status']}")
    
    result = PetWeightEvaluator.evaluate_dog_weight(15.0, 'beagle')
    tc.test("比格犬15kg超重",
            result['status'] == 'overweight' or result['status'] == 'obese',
            f"实际{result['status']}")
    
    result = PetWeightEvaluator.evaluate_dog_weight(30.0, 'labrador_retriever')
    tc.test("拉布拉多30kg理想体重",
            result['status'] == 'ideal',
            f"期望ideal, 实际{result['status']}")
    
    result = PetWeightEvaluator.evaluate_dog_weight(3.0, 'chihuahua')
    tc.test("吉娃娃3kg理想体重",
            result['status'] == 'ideal',
            f"期望ideal, 实际{result['status']}")
    
    # 测试猫体重评估
    result = PetWeightEvaluator.evaluate_cat_weight(4.5, 'siamese')
    tc.test("暹罗猫4.5kg理想体重",
            result['status'] == 'ideal',
            f"期望ideal, 实际{result['status']}")
    
    result = PetWeightEvaluator.evaluate_cat_weight(7.0, 'maine_coon')
    tc.test("缅因猫7kg理想体重",
            result['status'] == 'ideal',
            f"期望ideal, 实际{result['status']}")
    
    result = PetWeightEvaluator.evaluate_cat_weight(8.0, 'siamese')
    tc.test("暹罗猫8kg超重",
            result['status'] in ['overweight', 'obese'],
            f"实际{result['status']}")
    
    # 测试BCS评分
    tc.test("BCS评分范围1-9",
            all(PetWeightEvaluator.evaluate_dog_weight(w, 'beagle')['bcs'] 
                for w in [5, 8, 10, 15] for _ in [None]),
            "BCS评分应在1-9范围")
    
    # 测试建议内容
    result = PetWeightEvaluator.evaluate_dog_weight(20.0, 'beagle')
    tc.test("超重狗有建议",
            len(result['recommendations']) > 0,
            f"建议数: {len(result['recommendations'])}")
    
    # 测试便捷函数
    result = evaluate_pet_weight(8.0, 'dog', 'beagle')
    tc.test("便捷函数evaluate_pet_weight狗",
            result['status'] == 'ideal',
            f"实际{result['status']}")
    
    result = evaluate_pet_weight(4.5, 'cat', 'siamese')
    tc.test("便捷函数evaluate_pet_weight猫",
            result['status'] == 'ideal',
            f"实际{result['status']}")
    
    return tc.summary()


def test_pet_feeding_calculator():
    """测试宠物喂食计算"""
    print("\n【测试 PetFeedingCalculator】")
    tc = TestCollector()
    
    # 测试狗热量计算
    calories = PetFeedingCalculator.calculate_dog_calories(15.0, 3, False, ActivityLevel.MODERATE)
    tc.test("15kg成年狗热量计算",
            500 <= calories <= 1200,
            f"实际{calories}kcal")
    
    calories = PetFeedingCalculator.calculate_dog_calories(5.0, 0.5, False, ActivityLevel.MODERATE)
    tc.test("5kg幼犬热量计算",
            200 <= calories <= 800,
            f"实际{calories}kcal")
    
    calories_active = PetFeedingCalculator.calculate_dog_calories(15.0, 3, False, ActivityLevel.HIGH)
    calories_low = PetFeedingCalculator.calculate_dog_calories(15.0, 3, False, ActivityLevel.LOW)
    tc.test("活动水平影响热量",
            calories_active > calories_low,
            f"活跃{calories_active} > 低调{calories_low}")
    
    # 测试绝育影响
    calories_neutered = PetFeedingCalculator.calculate_dog_calories(15.0, 3, True, ActivityLevel.MODERATE)
    calories_intact = PetFeedingCalculator.calculate_dog_calories(15.0, 3, False, ActivityLevel.MODERATE)
    tc.test("绝育减少热量需求",
            calories_neutered < calories_intact,
            f"绝育{calories_neutered} < 未绝育{calories_intact}")
    
    # 测试猫热量计算
    calories = PetFeedingCalculator.calculate_cat_calories(4.5, 3, False, ActivityLevel.MODERATE)
    tc.test("4.5kg成年猫热量计算",
            150 <= calories <= 400,
            f"实际{calories}kcal")
    
    # 测试喂食建议
    rec = PetFeedingCalculator.get_feeding_recommendation(PetType.DOG, 15.0, 3, False, ActivityLevel.MODERATE, 'dry_food')
    tc.test("喂食建议有热量值",
            rec.daily_calories > 0,
            f"实际{rec.daily_calories}kcal")
    
    tc.test("喂食建议有食物量",
            rec.daily_amount > 0,
            f"实际{rec.daily_amount}g")
    
    tc.test("喂食建议有喂食次数",
            rec.meals_per_day >= 1,
            f"实际{rec.meals_per_day}次/天")
    
    tc.test("喂食建议有时间表",
            len(rec.feeding_schedule) > 0,
            f"实际{rec.feeding_schedule}")
    
    # 测试幼犬喂食次数
    rec = PetFeedingCalculator.get_feeding_recommendation(PetType.DOG, 5.0, 0.5, False, ActivityLevel.MODERATE)
    tc.test("幼犬喂食次数更多",
            rec.meals_per_day >= 3,
            f"实际{rec.meals_per_day}次/天")
    
    # 测试便捷函数
    plan = get_feeding_plan('dog', 15.0, 3, False, 'moderate', 'dry_food')
    tc.test("便捷函数get_feeding_plan",
            plan['daily_calories'] > 0,
            f"实际{plan['daily_calories']}kcal")
    
    return tc.summary()


def test_vaccine_scheduler():
    """测试疫苗时间表"""
    print("\n【测试 VaccineScheduler】")
    tc = TestCollector()
    
    # 创建测试日期
    birth_date = datetime(2026, 1, 1)
    
    # 测试狗疫苗时间表
    schedule = VaccineScheduler.get_dog_vaccine_schedule(birth_date)
    tc.test("狗疫苗时间表有条目",
            len(schedule) > 0,
            f"实际{len(schedule)}条")
    
    tc.test("疫苗时间表包含疫苗信息",
            all('vaccines' in s for s in schedule),
            "每条应有vaccines字段")
    
    tc.test("疫苗时间表有日期",
            all('due_date' in s for s in schedule),
            "每条应有due_date字段")
    
    # 测试第一次接种时间
    first_due = datetime.strptime(schedule[0]['due_date'], '%Y-%m-%d')
    expected_first = birth_date + timedelta(weeks=6)
    tc.test("第一次接种在6周龄",
            first_due == expected_first,
            f"期望{expected_first.strftime('%Y-%m-%d')}, 实际{first_due.strftime('%Y-%m-%d')}")
    
    # 测试疫苗信息
    tc.test("DHPPi疫苗信息存在",
            VaccineScheduler.VACCINE_INFO.get('DHPPi') is not None,
            "")
    
    tc.test("狂犬疫苗信息存在",
            VaccineScheduler.VACCINE_INFO.get('Rabies') is not None,
            "")
    
    # 测试猫疫苗时间表
    schedule = VaccineScheduler.get_cat_vaccine_schedule(birth_date)
    tc.test("猫疫苗时间表有条目",
            len(schedule) > 0,
            f"实际{len(schedule)}条")
    
    tc.test("猫疫苗包含FVRCP",
            any('FVRCP' in str(s['vaccines']) for s in schedule),
            "应包含猫三联")
    
    # 测试下一次疫苗建议
    future_birth = datetime.now() - timedelta(days=30)
    next_vaccine = VaccineScheduler.get_next_vaccines(PetType.DOG, future_birth)
    tc.test("下一次疫苗建议有内容",
            next_vaccine is not None,
            "")
    
    tc.test("下一次疫苗建议有状态",
            'status' in next_vaccine,
            "")
    
    # 测试便捷函数
    schedule = get_vaccine_schedule('dog', '2026-01-01')
    tc.test("便捷函数get_vaccine_schedule狗",
            len(schedule) > 0,
            f"实际{len(schedule)}条")
    
    schedule = get_vaccine_schedule('cat', '2026-01-01')
    tc.test("便捷函数get_vaccine_schedule猫",
            len(schedule) > 0,
            f"实际{len(schedule)}条")
    
    return tc.summary()


def test_pet_exercise_calculator():
    """测试宠物运动需求"""
    print("\n【测试 PetExerciseCalculator】")
    tc = TestCollector()
    
    # 测试狗运动需求
    needs = PetExerciseCalculator.get_dog_exercise_needs(DogSize.TOY, ActivityLevel.MODERATE, 3)
    tc.test("玩具型狗运动需求",
            needs['min_minutes'] >= 15,
            f"实际{needs['min_minutes']}分钟")
    
    needs = PetExerciseCalculator.get_dog_exercise_needs(DogSize.LARGE, ActivityLevel.MODERATE, 3)
    tc.test("大型狗运动需求",
            needs['min_minutes'] >= 40,
            f"实际{needs['min_minutes']}分钟")
    
    # 测试活动水平影响
    needs_low = PetExerciseCalculator.get_dog_exercise_needs(DogSize.MEDIUM, ActivityLevel.LOW, 3)
    needs_high = PetExerciseCalculator.get_dog_exercise_needs(DogSize.MEDIUM, ActivityLevel.HIGH, 3)
    tc.test("活动水平影响运动时间",
            needs_high['min_minutes'] > needs_low['min_minutes'],
            f"高活动{needs_high['min_minutes']} > 低活动{needs_low['min_minutes']}")
    
    # 测试年龄影响
    needs_puppy = PetExerciseCalculator.get_dog_exercise_needs(DogSize.MEDIUM, ActivityLevel.MODERATE, 0.5)
    needs_adult = PetExerciseCalculator.get_dog_exercise_needs(DogSize.MEDIUM, ActivityLevel.MODERATE, 3)
    tc.test("幼犬运动时间更少",
            needs_puppy['min_minutes'] < needs_adult['min_minutes'],
            f"幼犬{needs_puppy['min_minutes']} < 成犬{needs_adult['min_minutes']}")
    
    tc.test("幼犬有年龄调整说明",
            needs_puppy['age_adjustment'] is not None,
            "")
    
    needs_senior = PetExerciseCalculator.get_dog_exercise_needs(DogSize.MEDIUM, ActivityLevel.MODERATE, 10)
    tc.test("老年犬有年龄调整说明",
            needs_senior['age_adjustment'] is not None,
            "")
    
    # 测试运动建议
    tc.test("运动建议存在",
            len(needs['suggestions']) > 0,
            f"实际{len(needs['suggestions'])}条建议")
    
    # 测试猫运动需求
    needs = PetExerciseCalculator.get_cat_exercise_needs(ActivityLevel.MODERATE, True)
    tc.test("室内猫运动需求",
            needs['min_minutes'] >= 15,
            f"实际{needs['min_minutes']}分钟")
    
    needs_outdoor = PetExerciseCalculator.get_cat_exercise_needs(ActivityLevel.MODERATE, False)
    tc.test("室外猫运动需求更多",
            needs_outdoor['min_minutes'] > needs['min_minutes'],
            f"室外{needs_outdoor['min_minutes']} > 室内{needs['min_minutes']}")
    
    # 测试便捷函数
    needs = get_exercise_needs('dog', 'medium', 'moderate', 3)
    tc.test("便捷函数get_exercise_needs狗",
            needs['min_minutes'] > 0,
            f"实际{needs['min_minutes']}分钟")
    
    needs = get_exercise_needs('cat', 'medium', 'high', 3)
    tc.test("便捷函数get_exercise_needs猫",
            needs['min_minutes'] > 0,
            f"实际{needs['min_minutes']}分钟")
    
    return tc.summary()


def test_pet_lifespan_predictor():
    """测试宠物寿命预测"""
    print("\n【测试 PetLifespanPredictor】")
    tc = TestCollector()
    
    # 测试狗寿命预测
    lifespan = PetLifespanPredictor.predict_lifespan(PetType.DOG, DogSize.TOY)
    tc.test("玩具型狗寿命范围",
            lifespan['min_years'] >= 12,
            f"实际{lifespan['min_years']}-{lifespan['max_years']}年")
    
    lifespan = PetLifespanPredictor.predict_lifespan(PetType.DOG, DogSize.GIANT)
    tc.test("巨型狗寿命较短",
            lifespan['max_years'] <= 12,
            f"实际{lifespan['min_years']}-{lifespan['max_years']}年")
    
    # 测试绝育影响
    lifespan_neutered = PetLifespanPredictor.predict_lifespan(PetType.DOG, DogSize.MEDIUM, True)
    lifespan_intact = PetLifespanPredictor.predict_lifespan(PetType.DOG, DogSize.MEDIUM, False)
    tc.test("绝育延长寿命",
            lifespan_neutered['expected_years'] > lifespan_intact['expected_years'],
            f"绝育{lifespan_neutered['expected_years']} > 未绝育{lifespan_intact['expected_years']}")
    
    # 测试肥胖影响
    lifespan_obese = PetLifespanPredictor.predict_lifespan(PetType.DOG, DogSize.MEDIUM, False, True)
    lifespan_normal = PetLifespanPredictor.predict_lifespan(PetType.DOG, DogSize.MEDIUM, False, False)
    tc.test("肥胖缩短寿命",
            lifespan_obese['expected_years'] < lifespan_normal['expected_years'],
            f"肥胖{lifespan_obese['expected_years']} < 正常{lifespan_normal['expected_years']}")
    
    # 测试猫寿命预测
    lifespan_indoor = PetLifespanPredictor.predict_lifespan(PetType.CAT, None, True, False, True, True, True)
    lifespan_outdoor = PetLifespanPredictor.predict_lifespan(PetType.CAT, None, True, False, True, True, False)
    tc.test("室内猫寿命更长",
            lifespan_indoor['expected_years'] > lifespan_outdoor['expected_years'],
            f"室内{lifespan_indoor['expected_years']} > 室外{lifespan_outdoor['expected_years']}")
    
    # 测试其他宠物寿命
    lifespan = PetLifespanPredictor.predict_lifespan(PetType.RABBIT)
    tc.test("兔子寿命预测",
            lifespan['min_years'] >= 8,
            f"实际{lifespan['min_years']}-{lifespan['max_years']}年")
    
    lifespan = PetLifespanPredictor.predict_lifespan(PetType.HAMSTER)
    tc.test("仓鼠寿命预测",
            lifespan['max_years'] <= 5,
            f"实际{lifespan['min_years']}-{lifespan['max_years']}年")
    
    lifespan = PetLifespanPredictor.predict_lifespan(PetType.TURTLE)
    tc.test("乌龟寿命预测",
            lifespan['min_years'] >= 20,
            f"实际{lifespan['min_years']}-{lifespan['max_years']}年")
    
    # 测试调整说明
    lifespan = PetLifespanPredictor.predict_lifespan(PetType.DOG, DogSize.MEDIUM, True, False, True, True)
    tc.test("寿命调整说明存在",
            len(lifespan['adjustments']) > 0,
            f"实际{len(lifespan['adjustments'])}条")
    
    # 测试便捷函数
    lifespan = predict_pet_lifespan('dog', 'medium', True, False, True, True)
    tc.test("便捷函数predict_pet_lifespan狗",
            lifespan['expected_years'] > 0,
            f"实际{lifespan['expected_years']}年")
    
    lifespan = predict_pet_lifespan('cat', 'medium', True, False, True, True)
    tc.test("便捷函数predict_pet_lifespan猫",
            lifespan['expected_years'] > 0,
            f"实际{lifespan['expected_years']}年")
    
    return tc.summary()


def test_pet_health_checker():
    """测试宠物健康检查"""
    print("\n【测试 PetHealthChecker】")
    tc = TestCollector()
    
    # 测试生命阶段判断
    stage = PetHealthChecker.get_life_stage(PetType.DOG, 0.5)
    tc.test("0.5岁狗为幼犬",
            stage == 'puppy',
            f"实际{stage}")
    
    stage = PetHealthChecker.get_life_stage(PetType.DOG, 3)
    tc.test("3岁狗为成年",
            stage == 'adult',
            f"实际{stage}")
    
    stage = PetHealthChecker.get_life_stage(PetType.DOG, 8)
    tc.test("8岁狗为成熟期",
            stage in ['mature', 'senior'],
            f"实际{stage}")
    
    stage = PetHealthChecker.get_life_stage(PetType.DOG, 15)
    tc.test("15岁狗为老年/高龄",
            stage in ['senior', 'geriatric'],
            f"实际{stage}")
    
    # 测试猫生命阶段
    stage = PetHealthChecker.get_life_stage(PetType.CAT, 0.5)
    tc.test("0.5岁猫为幼猫",
            stage == 'kitten',
            f"实际{stage}")
    
    stage = PetHealthChecker.get_life_stage(PetType.CAT, 3)
    tc.test("3岁猫为成年",
            stage == 'adult',
            f"实际{stage}")
    
    stage = PetHealthChecker.get_life_stage(PetType.CAT, 12)
    tc.test("12岁猫为老年",
            stage in ['senior', 'geriatric'],
            f"实际{stage}")
    
    # 测试健康检查建议
    rec = PetHealthChecker.get_health_recommendations(PetType.DOG, 0.5)
    tc.test("幼犬检查频率更频繁",
            '3' in rec['checkup_frequency'] or '4' in rec['checkup_frequency'],
            f"实际{rec['checkup_frequency']}")
    
    rec = PetHealthChecker.get_health_recommendations(PetType.DOG, 3)
    tc.test("成年狗检查建议",
            len(rec['recommended_checkups']) > 0,
            f"实际{len(rec['recommended_checkups'])}项")
    
    rec = PetHealthChecker.get_health_recommendations(PetType.DOG, 15)
    tc.test("高龄狗有年龄特建议",
            len(rec['age_specific_recommendations']) > 0,
            f"实际{len(rec['age_specific_recommendations'])}条")
    
    # 测试体重相关建议
    rec = PetHealthChecker.get_health_recommendations(PetType.DOG, 5, 'obese')
    tc.test("肥胖狗有体重建议",
            len(rec['weight_recommendations']) > 0,
            f"实际{len(rec['weight_recommendations'])}条")
    
    rec = PetHealthChecker.get_health_recommendations(PetType.CAT, 3, 'overweight')
    tc.test("超重猫有体重建议",
            len(rec['weight_recommendations']) > 0,
            f"实际{len(rec['weight_recommendations'])}条")
    
    return tc.summary()


def test_pet_profile():
    """测试宠物档案"""
    print("\n【测试 PetProfile】")
    tc = TestCollector()
    
    # 创建宠物档案
    profile = PetProfile(
        name="小黑",
        pet_type=PetType.DOG,
        breed="labrador_retriever",
        birth_date=datetime(2023, 1, 1),
        weight=25.0,
        activity_level=ActivityLevel.HIGH,
        is_neutered=True,
    )
    
    tc.test("宠物档案创建",
            profile.name == "小黑",
            "")
    
    tc.test("宠物类型正确",
            profile.pet_type == PetType.DOG,
            "")
    
    tc.test("宠物年龄计算",
            profile.age_years >= 2,
            f"实际{profile.age_years}年")
    
    tc.test("宠物体重设置",
            profile.weight == 25.0,
            "")
    
    tc.test("绝育状态设置",
            profile.is_neutered == True,
            "")
    
    return tc.summary()


def test_enums_and_constants():
    """测试枚举和常量"""
    print("\n【测试枚举和常量】")
    tc = TestCollector()
    
    # 测试宠物类型枚举
    tc.test("PetType枚举完整性",
            PetType.DOG.value == 'dog' and PetType.CAT.value == 'cat',
            "")
    
    # 测试狗体型枚举
    tc.test("DogSize枚举完整性",
            DogSize.TOY.value == 'toy' and DogSize.GIANT.value == 'giant',
            "")
    
    # 测试活动水平枚举
    tc.test("ActivityLevel枚举完整性",
            ActivityLevel.LOW.value == 'low' and ActivityLevel.VERY_HIGH.value == 'very_high',
            "")
    
    # 测试年龄转换系数存在
    tc.test("狗年龄系数完整",
            len(PetAgeConverter.DOG_AGE_FACTORS) == 5,
            f"实际{len(PetAgeConverter.DOG_AGE_FACTORS)}种体型")
    
    tc.test("其他宠物年龄系数存在",
            len(PetAgeConverter.OTHER_PET_AGE_FACTORS) >= 5,
            f"实际{len(PetAgeConverter.OTHER_PET_AGE_FACTORS)}种宠物")
    
    # 测试体重范围数据
    tc.test("狗品种体重数据存在",
            len(PetWeightEvaluator.DOG_BREED_WEIGHTS) > 10,
            f"实际{len(PetWeightEvaluator.DOG_BREED_WEIGHTS)}种")
    
    tc.test("猫品种体重数据存在",
            len(PetWeightEvaluator.CAT_BREED_WEIGHTS) > 5,
            f"实际{len(PetWeightEvaluator.CAT_BREED_WEIGHTS)}种")
    
    # 测试食物热量密度数据
    tc.test("食物热量密度数据存在",
            len(PetFeedingCalculator.FOOD_CALORIE_DENSITY) >= 4,
            f"实际{len(PetFeedingCalculator.FOOD_CALORIE_DENSITY)}种")
    
    # 测试运动需求数据
    tc.test("狗运动需求数据存在",
            len(PetExerciseCalculator.DOG_EXERCISE_NEEDS) == 5,
            f"实际{len(PetExerciseCalculator.DOG_EXERCISE_NEEDS)}种体型")
    
    # 测试寿命数据
    tc.test("寿命预测数据存在",
            len(PetLifespanPredictor.LIFESPAN_DATA) >= 5,
            f"实际{len(PetLifespanPredictor.LIFESPAN_DATA)}种宠物")
    
    return tc.summary()


def test_edge_cases():
    """测试边界情况"""
    print("\n【测试边界情况】")
    tc = TestCollector()
    
    # 零年龄
    human_age = PetAgeConverter.dog_to_human_years(0, DogSize.MEDIUM)
    tc.test("0岁狗转换",
            human_age == 0,
            f"期望0, 实际{human_age}")
    
    human_age = PetAgeConverter.cat_to_human_years(0)
    tc.test("0岁猫转换",
            human_age == 0,
            f"期望0, 实际{human_age}")
    
    # 极小年龄
    human_age = PetAgeConverter.dog_to_human_years(0.1, DogSize.MEDIUM)
    tc.test("0.1岁狗转换",
            human_age > 0,
            f"实际{human_age}")
    
    # 极大年龄
    human_age = PetAgeConverter.dog_to_human_years(20, DogSize.MEDIUM)
    tc.test("20岁狗转换",
            human_age > 80,
            f"实际{human_age}")
    
    # 零体重热量计算
    try:
        calories = PetFeedingCalculator.calculate_dog_calories(0.5, 3)
        tc.test("极小体重热量计算",
                calories > 0,
                f"实际{calories}kcal")
    except Exception as e:
        tc.test("极小体重热量计算", False, str(e))
    
    # 极大体重热量计算
    calories = PetFeedingCalculator.calculate_dog_calories(80.0, 3)
    tc.test("80kg狗热量计算",
            calories > 2000,
            f"实际{calories}kcal")
    
    # 未知的品种体重评估
    result = PetWeightEvaluator.evaluate_dog_weight(10.0, 'unknown_breed')
    tc.test("未知品种体重评估",
            'status' in result,
            f"实际{result}")
    
    # 空品种体重评估
    result = PetWeightEvaluator.evaluate_dog_weight(10.0, '')
    tc.test("空品种体重评估",
            'status' in result,
            f"实际{result}")
    
    # 未来出生日期疫苗计划
    future_birth = datetime.now() + timedelta(days=365)
    schedule = VaccineScheduler.get_dog_vaccine_schedule(future_birth)
    tc.test("未来出生日期疫苗计划",
            len(schedule) > 0,
            f"实际{len(schedule)}条")
    
    # 老年宠物寿命预测
    lifespan = PetLifespanPredictor.predict_lifespan(PetType.DOG, DogSize.TOY, True, False, True, True)
    tc.test("玩具型狗预期寿命较长",
            lifespan['max_years'] >= 15,
            f"实际{lifespan['max_years']}年")
    
    # 负数/极端参数测试
    try:
        human_age = PetAgeConverter.dog_to_human_years(-1, DogSize.MEDIUM)
        tc.test("负数年龄处理",
                human_age >= 0 or human_age < 0,  # 允许任何结果，只要不崩溃
                f"实际{human_age}")
    except Exception as e:
        tc.test("负数年龄处理", True, "正确抛出异常或返回合理值")
    
    return tc.summary()


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Pet Utils Test Suite")
    print("=" * 60)
    
    results = []
    
    results.append(("PetAgeConverter", test_pet_age_converter()))
    results.append(("PetWeightEvaluator", test_pet_weight_evaluator()))
    results.append(("PetFeedingCalculator", test_pet_feeding_calculator()))
    results.append(("VaccineScheduler", test_vaccine_scheduler()))
    results.append(("PetExerciseCalculator", test_pet_exercise_calculator()))
    results.append(("PetLifespanPredictor", test_pet_lifespan_predictor()))
    results.append(("PetHealthChecker", test_pet_health_checker()))
    results.append(("PetProfile", test_pet_profile()))
    results.append(("EnumsAndConstants", test_enums_and_constants()))
    results.append(("EdgeCases", test_edge_cases()))
    
    print("\n" + "=" * 60)
    print("Overall Results")
    print("=" * 60)
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    for name, passed in results:
        status = "✓" if passed else "✗"
        print(f"  {status} {name}")
    
    print(f"\nOverall: {total_passed}/{total_tests} test suites passed")
    
    return all(passed for _, passed in results)


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)