#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for recipe_utils"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Ingredient, NutritionInfo, RecipeStep, Recipe,
    UnitType, IngredientCategory, DietaryRestriction, DifficultyLevel, MealType,
    RecipeScaler, UnitConverter, NutritionCalculator, IngredientSubstitutor,
    ShoppingListGenerator, RecipeParser, CostCalculator, RecipeAnalyzer,
    scale_recipe, convert_unit, get_nutrition, get_substitutions,
    analyze_recipe, generate_shopping_list, parse_ingredient,
    estimate_recipe_cost, get_common_conversions, get_example_recipe
)

import unittest


class TestIngredient(unittest.TestCase):
    def test_creation(self):
        ing = Ingredient("鸡蛋", 3, UnitType.PIECE, IngredientCategory.PROTEIN)
        self.assertEqual(ing.name, "鸡蛋")
        self.assertEqual(ing.amount, 3)
        self.assertEqual(ing.unit, UnitType.PIECE)

    def test_to_grams_weight(self):
        ing = Ingredient("面粉", 100, UnitType.GRAM, IngredientCategory.GRAIN)
        self.assertEqual(ing.to_grams(), 100)

    def test_to_grams_volume(self):
        ing = Ingredient("水", 100, UnitType.MILLILITER, IngredientCategory.LIQUID)
        self.assertGreater(ing.to_grams(), 0)


class TestNutritionInfo(unittest.TestCase):
    def test_addition(self):
        n1 = NutritionInfo(calories=100, protein=10)
        n2 = NutritionInfo(calories=200, protein=20)
        n3 = n1 + n2
        self.assertEqual(n3.calories, 300)
        self.assertEqual(n3.protein, 30)

    def test_multiplication(self):
        n1 = NutritionInfo(calories=100, protein=10)
        n2 = n1 * 2
        self.assertEqual(n2.calories, 200)
        self.assertEqual(n2.protein, 20)

    def test_to_dict(self):
        n = NutritionInfo(calories=100.5, protein=10.2)
        d = n.to_dict()
        self.assertEqual(d["calories"], 100.5)
        self.assertEqual(d["protein"], 10.2)


class TestRecipe(unittest.TestCase):
    def test_total_time(self):
        recipe = get_example_recipe()
        self.assertEqual(recipe.total_time_minutes, 15)

    def test_scale(self):
        recipe = get_example_recipe()
        scaled = recipe.scale(4)
        self.assertEqual(scaled.servings, 4)


class TestRecipeScaler(unittest.TestCase):
    def test_scale_recipe(self):
        recipe = get_example_recipe()
        scaled = RecipeScaler.scale_recipe(recipe, 4)
        self.assertEqual(scaled.servings, 4)
        self.assertEqual(scaled.ingredients[0].amount, 6)

    def test_smart_round(self):
        self.assertEqual(RecipeScaler.smart_round(1.5, UnitType.TABLESPOON), 1.5)
        self.assertEqual(RecipeScaler.smart_round(1.7, UnitType.PIECE), 2)


class TestUnitConverter(unittest.TestCase):
    def test_same_unit(self):
        result, success = UnitConverter.convert(100, UnitType.GRAM, UnitType.GRAM)
        self.assertEqual(result, 100)
        self.assertTrue(success)

    def test_volume_to_volume(self):
        result, success = UnitConverter.convert(1, UnitType.TABLESPOON, UnitType.MILLILITER)
        self.assertAlmostEqual(result, 14.7868, places=2)
        self.assertTrue(success)

    def test_temperature_c_to_f(self):
        result = UnitConverter.convert_temperature(100, "celsius", "fahrenheit")
        self.assertAlmostEqual(result, 212, places=1)

    def test_temperature_f_to_c(self):
        result = UnitConverter.convert_temperature(212, "fahrenheit", "celsius")
        self.assertAlmostEqual(result, 100, places=1)


class TestNutritionCalculator(unittest.TestCase):
    def test_get_ingredient_nutrition(self):
        ing = Ingredient("鸡蛋", 100, UnitType.GRAM, IngredientCategory.PROTEIN)
        nutrition = NutritionCalculator.get_ingredient_nutrition(ing)
        self.assertGreater(nutrition.calories, 0)

    def test_get_recipe_nutrition(self):
        recipe = get_example_recipe()
        nutrition = NutritionCalculator.get_recipe_nutrition(recipe)
        self.assertGreater(nutrition.calories, 0)

    def test_get_nutrition_per_serving(self):
        recipe = get_example_recipe()
        nutrition = NutritionCalculator.get_nutrition_per_serving(recipe)
        self.assertGreater(nutrition.calories, 0)


class TestIngredientSubstitutor(unittest.TestCase):
    def test_get_substitutions(self):
        subs = IngredientSubstitutor.get_substitutions("鸡蛋")
        self.assertGreater(len(subs), 0)

    def test_find_vegan_alternative(self):
        alt = IngredientSubstitutor.find_vegan_alternative("鸡蛋")
        self.assertIsNotNone(alt)

    def test_find_gluten_free_alternative(self):
        alt = IngredientSubstitutor.find_gluten_free_alternative("面粉")
        self.assertIsNotNone(alt)


class TestShoppingListGenerator(unittest.TestCase):
    def test_generate(self):
        recipe = get_example_recipe()
        shopping = ShoppingListGenerator.generate([recipe])
        self.assertGreater(shopping["total_ingredients"], 0)
        self.assertIn("by_category", shopping)


class TestRecipeParser(unittest.TestCase):
    def test_parse_with_unit(self):
        ing = RecipeParser.parse_ingredient_line("100g 面粉")
        self.assertIsNotNone(ing)
        self.assertEqual(ing.amount, 100)

    def test_parse_fraction(self):
        ing = RecipeParser.parse_ingredient_line("1/2 杯牛奶")
        self.assertIsNotNone(ing)
        self.assertEqual(ing.amount, 0.5)


class TestCostCalculator(unittest.TestCase):
    def test_estimate_cost(self):
        recipe = get_example_recipe()
        cost = CostCalculator.estimate_cost(recipe)
        self.assertIn("total_cost", cost)
        self.assertGreater(cost["total_cost"], 0)


class TestRecipeAnalyzer(unittest.TestCase):
    def test_analyze(self):
        recipe = get_example_recipe()
        analysis = RecipeAnalyzer.analyze(recipe)
        self.assertIn("total_nutrition", analysis)
        self.assertIn("cost", analysis)
        self.assertIn("health_score", analysis)


class TestConvenienceFunctions(unittest.TestCase):
    def test_scale_recipe(self):
        recipe = get_example_recipe()
        scaled = scale_recipe(recipe, 4)
        self.assertEqual(scaled.servings, 4)

    def test_convert_unit(self):
        result, success = convert_unit(1, UnitType.TABLESPOON, UnitType.MILLILITER)
        self.assertTrue(success)

    def test_get_nutrition(self):
        ing = Ingredient("鸡蛋", 100, UnitType.GRAM, IngredientCategory.PROTEIN)
        nutrition = get_nutrition(ing)
        self.assertGreater(nutrition.calories, 0)

    def test_get_substitutions(self):
        subs = get_substitutions("鸡蛋")
        self.assertIsInstance(subs, list)

    def test_analyze_recipe(self):
        recipe = get_example_recipe()
        analysis = analyze_recipe(recipe)
        self.assertIn("recipe_name", analysis)

    def test_generate_shopping_list(self):
        recipe = get_example_recipe()
        shopping = generate_shopping_list([recipe])
        self.assertGreater(shopping["total_ingredients"], 0)

    def test_parse_ingredient(self):
        ing = parse_ingredient("100g 面粉")
        self.assertIsNotNone(ing)

    def test_estimate_recipe_cost(self):
        recipe = get_example_recipe()
        cost = estimate_recipe_cost(recipe)
        self.assertIn("total_cost", cost)

    def test_get_common_conversions(self):
        conversions = get_common_conversions()
        self.assertIn("体积", conversions)

    def test_get_example_recipe(self):
        recipe = get_example_recipe()
        self.assertEqual(recipe.name, "番茄炒蛋")
        self.assertEqual(recipe.servings, 2)


if __name__ == "__main__":
    unittest.main()