"""
Markov Chain Utils 测试文件

测试所有模块的核心功能
"""

import unittest
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from markov_chain_utils import (
    MarkovChain,
    MarkovTextGenerator,
    SequencePredictor,
    TransitionMatrix
)


class TestMarkovChain(unittest.TestCase):
    """MarkovChain 测试"""
    
    def test_basic_training(self):
        """测试基础训练"""
        mc = MarkovChain(order=1)
        mc.train(['A', 'B', 'C', 'A', 'B', 'D'])
        
        self.assertEqual(mc.num_states, 4)
        self.assertIn('A', mc.states)
        self.assertIn('B', mc.states)
    
    def test_transition_probability(self):
        """测试转移概率"""
        mc = MarkovChain(order=1)
        mc.train(['A', 'B', 'A', 'B', 'A', 'C'])
        
        # A -> B: 2/3, A -> C: 1/3
        self.assertAlmostEqual(mc.get_transition_probability(('A',), 'B'), 2/3, places=2)
        self.assertAlmostEqual(mc.get_transition_probability(('A',), 'C'), 1/3, places=2)
    
    def test_generate(self):
        """测试生成"""
        mc = MarkovChain(order=1, seed=42)
        mc.train(['A', 'B', 'C'] * 10)
        
        result = mc.generate(start=('A',), steps=5)
        self.assertEqual(len(result), 6)  # start + 5 steps
        self.assertEqual(result[0], 'A')
    
    def test_predict_next(self):
        """测试预测"""
        mc = MarkovChain(order=1)
        mc.train(['A', 'B', 'A', 'B', 'A', 'B'])
        
        # A 后面最可能是 B
        prediction = mc.predict_next(('A',))
        self.assertEqual(prediction, 'B')
    
    def test_higher_order(self):
        """测试高阶马尔可夫链"""
        mc = MarkovChain(order=2)
        mc.train(['A', 'B', 'C', 'D', 'A', 'B', 'C', 'E'])
        
        # 在 AB 之后，C 最可能
        self.assertEqual(mc.predict_next(('A', 'B')), 'C')
    
    def test_train_multiple(self):
        """测试多序列训练"""
        mc = MarkovChain(order=1)
        mc.train_multiple([
            ['A', 'B', 'C'],
            ['A', 'B', 'D'],
            ['A', 'E', 'F']
        ])
        
        # A 可以转移到 B 或 E
        probs = mc.get_possible_next_states(('A',))
        self.assertEqual(len(probs), 2)
    
    def test_invalid_order(self):
        """测试无效阶数"""
        with self.assertRaises(ValueError):
            MarkovChain(order=0)
    
    def test_empty_sequence(self):
        """测试空序列"""
        mc = MarkovChain(order=1)
        with self.assertRaises(ValueError):
            mc.train(['A'])  # 太短


class TestMarkovTextGenerator(unittest.TestCase):
    """MarkovTextGenerator 测试"""
    
    def test_word_mode(self):
        """测试单词模式"""
        gen = MarkovTextGenerator(order=2, mode='word', seed=42)
        gen.train("The cat sat on the mat. The cat was happy.")
        
        text = gen.generate(start="The cat", max_length=10)
        self.assertTrue(text.startswith("The cat"))
    
    def test_char_mode(self):
        """测试字符模式"""
        gen = MarkovTextGenerator(order=3, mode='char', seed=42)
        gen.train("hello hello hello")
        
        text = gen.generate(start="hel", max_length=10)
        self.assertTrue(len(text) >= 3)
    
    def test_generate_sentence(self):
        """测试句子生成"""
        gen = MarkovTextGenerator(order=2, mode='word', seed=42)
        gen.train("Hello world. How are you. Nice day.")
        
        sentence = gen.generate_sentence(max_length=20)
        self.assertIsInstance(sentence, str)
    
    def test_continuations(self):
        """测试续写预测"""
        gen = MarkovTextGenerator(order=2, mode='word')
        gen.train("The quick brown fox jumps over the lazy dog.")
        
        continuations = gen.get_continuations("The quick", top_n=3)
        self.assertTrue(len(continuations) > 0)
    
    def test_temperature(self):
        """测试温度参数"""
        gen = MarkovTextGenerator(order=2, mode='word', seed=42)
        gen.train("a b c a b c a b c")
        
        # 温度为 0 应该完全确定性
        text1 = gen.generate(max_length=5, temperature=0)
        text2 = gen.generate(max_length=5, temperature=0)
        self.assertEqual(text1, text2)
    
    def test_train_from_sentences(self):
        """测试多句子训练"""
        gen = MarkovTextGenerator(order=1)  # 使用 order=1 以适应短句子
        gen.train_from_sentences([
            "Hello world",
            "Hello there",
            "World peace"
        ])
        
        self.assertGreater(gen.vocabulary_size, 0)


class TestSequencePredictor(unittest.TestCase):
    """SequencePredictor 测试"""
    
    def test_basic_prediction(self):
        """测试基础预测"""
        sp = SequencePredictor(order=2)
        sp.train([1, 2, 3, 1, 2, 4, 1, 2, 3])
        
        # 1, 2 后面最可能是 3
        prediction = sp.predict([1, 2])
        self.assertEqual(prediction, 3)
    
    def test_prediction_with_probability(self):
        """测试带概率的预测"""
        sp = SequencePredictor(order=1)
        sp.train(['A', 'B', 'A', 'B', 'A', 'C'])
        
        pred, prob = sp.predict_with_probability(['A'])
        self.assertEqual(pred, 'B')
        self.assertAlmostEqual(prob, 2/3, places=2)
    
    def test_predict_distribution(self):
        """测试概率分布预测"""
        sp = SequencePredictor(order=1)
        sp.train(['A', 'B', 'A', 'B', 'A', 'C', 'A', 'D'])
        
        dist = sp.predict_distribution(['A'])
        self.assertEqual(len(dist), 3)
        
        # 概率和应该接近 1
        total_prob = sum(p for _, p in dist)
        self.assertAlmostEqual(total_prob, 1.0, places=5)
    
    def test_multi_step_prediction(self):
        """测试多步预测"""
        sp = SequencePredictor(order=1)
        sp.train([1, 2, 3, 4, 5, 1, 2, 3, 4, 5])
        
        result = sp.predict_sequence([1], steps=3)
        self.assertEqual(result, [2, 3, 4])
    
    def test_evaluation(self):
        """测试评估"""
        sp = SequencePredictor(order=1)
        sp.train([1, 2, 3, 1, 2, 3, 1, 2, 3])
        
        metrics = sp.evaluate([1, 2, 3, 1, 2, 3])
        self.assertGreater(metrics['accuracy'], 0.5)
        self.assertEqual(metrics['samples'], 5)  # len(seq) - order = 6 - 1 = 5
    
    def test_anomaly_detection(self):
        """测试异常检测"""
        sp = SequencePredictor(order=1)
        sp.train([1, 2, 1, 2, 1, 2, 1, 2])
        
        # 序列中的 3 是异常
        anomalies = sp.detect_anomaly([1, 2, 1, 2, 1, 3], threshold=0.5)
        self.assertTrue(len(anomalies) > 0)
        
        # 检查 3 被检测为异常
        anomaly_values = [a[1] for a in anomalies]
        self.assertIn(3, anomaly_values)
    
    def test_smoothing(self):
        """测试平滑"""
        sp = SequencePredictor(order=1, smoothing=1.0)
        sp.train(['A', 'B', 'A', 'B'])
        
        # 未见过的状态也应该有小概率
        dist = sp.predict_distribution(['B'])
        probs = {v: p for v, p in dist}
        
        # B 的后继应该有概率
        self.assertIn('A', probs)


class TestTransitionMatrix(unittest.TestCase):
    """TransitionMatrix 测试"""
    
    def test_basic_transitions(self):
        """测试基础转移"""
        tm = TransitionMatrix()
        tm.add_transition('A', 'B')
        tm.add_transition('A', 'B')
        tm.add_transition('A', 'C')
        
        self.assertEqual(tm.get_count('A', 'B'), 2)
        self.assertEqual(tm.get_count('A', 'C'), 1)
    
    def test_probability(self):
        """测试概率计算"""
        tm = TransitionMatrix()
        tm.add_transition('A', 'B', count=3)
        tm.add_transition('A', 'C', count=1)
        
        self.assertAlmostEqual(tm.get_probability('A', 'B'), 0.75, places=2)
        self.assertAlmostEqual(tm.get_probability('A', 'C'), 0.25, places=2)
    
    def test_sequence_training(self):
        """测试序列训练"""
        tm = TransitionMatrix()
        tm.add_sequence(['A', 'B', 'C', 'A', 'B', 'D'])
        
        self.assertEqual(tm.get_count('A', 'B'), 2)
        self.assertEqual(tm.get_count('B', 'C'), 1)
        self.assertEqual(tm.get_count('B', 'D'), 1)
    
    def test_most_likely(self):
        """测试最可能转移"""
        tm = TransitionMatrix()
        tm.add_transition('A', 'B', count=9)
        tm.add_transition('A', 'C', count=1)
        
        state, prob = tm.get_most_likely('A')
        self.assertEqual(state, 'B')
        self.assertAlmostEqual(prob, 0.9, places=2)
    
    def test_stationary_distribution(self):
        """测试稳态分布"""
        tm = TransitionMatrix()
        # 简单循环 A -> B -> A
        tm.add_transition('A', 'B')
        tm.add_transition('B', 'A')
        
        dist = tm.get_stationary_distribution()
        self.assertAlmostEqual(dist['A'], 0.5, places=2)
        self.assertAlmostEqual(dist['B'], 0.5, places=2)
    
    def test_absorbing_states(self):
        """测试吸收态"""
        tm = TransitionMatrix()
        tm.add_transition('A', 'B')
        tm.add_transition('B', 'B')  # B 是吸收态
        
        absorbing = tm.get_absorbing_states()
        self.assertIn('B', absorbing)
    
    def test_to_matrix(self):
        """测试矩阵转换"""
        tm = TransitionMatrix()
        tm.add_transition('A', 'B')
        tm.add_transition('B', 'A')
        
        states, matrix = tm.to_matrix()
        
        self.assertEqual(len(states), 2)
        self.assertEqual(len(matrix), 2)
        self.assertEqual(len(matrix[0]), 2)
    
    def test_communicating_classes(self):
        """测试互通类"""
        tm = TransitionMatrix()
        tm.add_transition('A', 'B')
        tm.add_transition('B', 'A')
        tm.add_transition('C', 'D')
        tm.add_transition('D', 'C')
        
        classes = tm.get_communicating_classes()
        self.assertEqual(len(classes), 2)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_weather_prediction(self):
        """测试天气预测场景"""
        # 模拟天气序列：S=晴天, R=雨天
        weather_data = list('SSRSSRSSSSRSSRSSS')
        
        sp = SequencePredictor(order=2)
        sp.train(weather_data)
        
        # 预测
        pred, prob = sp.predict_with_probability(['S', 'S'])
        self.assertIn(pred, ['S', 'R'])
        self.assertGreater(prob, 0)
    
    def test_text_generation_quality(self):
        """测试文本生成质量"""
        gen = MarkovTextGenerator(order=2, mode='word')
        
        # 训练语料
        text = """
        The quick brown fox jumps over the lazy dog.
        The lazy dog sleeps all day long.
        The quick fox runs fast in the forest.
        A brown dog plays in the park.
        """
        
        gen.train(text)
        
        # 生成
        result = gen.generate(start="The quick", max_length=10)
        
        # 应该生成有意义的内容
        self.assertTrue(len(result) > 0)
        self.assertTrue(result.startswith("The quick"))
    
    def test_sequence_anomaly_detection(self):
        """测试序列异常检测"""
        # 正常模式
        sp = SequencePredictor(order=2)
        normal_sequences = [
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
        ]
        
        for seq in normal_sequences:
            sp.train(seq)
        
        # 异常序列
        test_sequence = [1, 2, 3, 5, 4]  # 顺序错误
        anomalies = sp.detect_anomaly(test_sequence, threshold=0.3)
        
        # 应该检测到异常
        self.assertTrue(len(anomalies) > 0)
    
    def test_chain_and_generator_together(self):
        """测试链和生成器配合使用"""
        # 使用马尔可夫链处理单词序列
        mc = MarkovChain(order=1)
        
        text = "hello world hello there world peace hello world"
        words = text.split()
        
        mc.train(words)
        
        # 应该能生成合理的序列
        result = mc.generate(start=('hello',), steps=5)
        self.assertTrue(len(result) >= 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)