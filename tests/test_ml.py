"""머신러닝 엔진 테스트"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engine.ml_matcher import MLMatcher
from src.data.training_data_generator import TrainingDataGenerator


class TestMLMatcher(unittest.TestCase):
    """ML 매칭 엔진 테스트"""

    def setUp(self):
        """각 테스트 전에 실행"""
        self.generator = TrainingDataGenerator(seed=42)
        self.facilities = self.generator.generate_facilities()

    def test_ml_matcher_creation(self):
        """ML 매처 생성 테스트"""
        matcher = MLMatcher(n_estimators=10, random_state=42)
        self.assertIsNotNone(matcher)
        self.assertFalse(matcher._is_trained)

    def test_training(self):
        """모델 학습 테스트"""
        orders, labels = self.generator.generate_training_data(50)

        matcher = MLMatcher(n_estimators=10, random_state=42)
        result = matcher.train(orders, labels)

        self.assertTrue(matcher._is_trained)
        self.assertIn('train_accuracy', result)
        self.assertGreater(result['train_accuracy'], 0.5)  # 50% 이상 정확도

    def test_prediction(self):
        """예측 테스트"""
        orders, labels = self.generator.generate_training_data(50)

        matcher = MLMatcher(n_estimators=10, random_state=42)
        matcher.train(orders, labels)

        # 새로운 주문으로 예측
        test_order = self.generator.generate_random_order("TEST-001")
        result = matcher.predict(test_order, self.facilities)

        # 결과가 있으면 튜플이어야 함
        if result:
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
            facility, confidence = result
            self.assertGreaterEqual(confidence, 0.0)
            self.assertLessEqual(confidence, 1.0)

    def test_predict_before_training(self):
        """학습 전 예측 시 오류 테스트"""
        matcher = MLMatcher(n_estimators=10, random_state=42)
        test_order = self.generator.generate_random_order("TEST-002")

        with self.assertRaises(RuntimeError):
            matcher.predict(test_order, self.facilities)

    def test_feature_extraction(self):
        """특성 추출 테스트"""
        matcher = MLMatcher(n_estimators=10, random_state=42)
        order = self.generator.generate_random_order("TEST-003")

        features = matcher._extract_features(order)

        self.assertEqual(len(features), 10)  # 10개 특성
        self.assertTrue(all(isinstance(f, (int, float)) for f in features))

    def test_top_k_predictions(self):
        """상위 k개 예측 테스트"""
        orders, labels = self.generator.generate_training_data(50)

        matcher = MLMatcher(n_estimators=10, random_state=42)
        matcher.train(orders, labels)

        test_order = self.generator.generate_random_order("TEST-004")
        top_k = matcher.predict_top_k(test_order, self.facilities, k=3)

        self.assertLessEqual(len(top_k), 3)

        # 확률이 내림차순으로 정렬되어 있는지 확인
        if len(top_k) > 1:
            for i in range(len(top_k) - 1):
                self.assertGreaterEqual(top_k[i][1], top_k[i+1][1])

    def test_model_save_load(self):
        """모델 저장/로드 테스트"""
        import tempfile

        orders, labels = self.generator.generate_training_data(30)

        # 학습 및 저장
        matcher1 = MLMatcher(n_estimators=10, random_state=42)
        matcher1.train(orders, labels)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as f:
            temp_path = f.name

        try:
            matcher1.save_model(temp_path)

            # 로드
            matcher2 = MLMatcher()
            matcher2.load_model(temp_path)

            self.assertTrue(matcher2._is_trained)

            # 같은 예측 결과를 내는지 확인
            test_order = self.generator.generate_random_order("TEST-005")

            result1 = matcher1.predict(test_order, self.facilities)
            result2 = matcher2.predict(test_order, self.facilities)

            if result1 and result2:
                self.assertEqual(result1[0].facility_id, result2[0].facility_id)

        finally:
            # 임시 파일 삭제
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_evaluation(self):
        """모델 평가 테스트"""
        train_orders, train_labels = self.generator.generate_training_data(50)
        test_orders, test_labels = self.generator.generate_test_data(20)

        matcher = MLMatcher(n_estimators=10, random_state=42)
        matcher.train(train_orders, train_labels)

        eval_result = matcher.evaluate(test_orders, test_labels)

        self.assertIn('accuracy', eval_result)
        self.assertIn('correct', eval_result)
        self.assertIn('total', eval_result)

        self.assertGreaterEqual(eval_result['accuracy'], 0.0)
        self.assertLessEqual(eval_result['accuracy'], 1.0)


class TestTrainingDataGenerator(unittest.TestCase):
    """학습 데이터 생성기 테스트"""

    def test_generator_creation(self):
        """생성기 생성 테스트"""
        generator = TrainingDataGenerator(seed=42)
        self.assertIsNotNone(generator)

    def test_random_order_generation(self):
        """랜덤 주문 생성 테스트"""
        generator = TrainingDataGenerator(seed=42)
        order = generator.generate_random_order("TEST-001")

        self.assertIsNotNone(order)
        self.assertEqual(order.order_id, "TEST-001")
        self.assertGreater(order.weight, 0)
        self.assertGreater(order.volume, 0)

    def test_facility_generation(self):
        """설비 생성 테스트"""
        generator = TrainingDataGenerator(seed=42)
        facilities = generator.generate_facilities()

        self.assertGreater(len(facilities), 0)
        self.assertTrue(all(f.facility_id.startswith("FAC-") for f in facilities))

    def test_training_data_generation(self):
        """학습 데이터 생성 테스트"""
        generator = TrainingDataGenerator(seed=42)
        orders, labels = generator.generate_training_data(20)

        self.assertGreater(len(orders), 0)
        self.assertEqual(len(orders), len(labels))
        self.assertTrue(all(isinstance(label, str) for label in labels))

    def test_reproducibility(self):
        """재현성 테스트 (같은 시드 = 같은 결과)"""
        gen1 = TrainingDataGenerator(seed=42)
        orders1 = [gen1.generate_random_order(f"TEST-{i}") for i in range(10)]

        gen2 = TrainingDataGenerator(seed=42)
        orders2 = [gen2.generate_random_order(f"TEST-{i}") for i in range(10)]

        self.assertEqual(len(orders1), len(orders2))

        # 첫 번째 주문이 같은지 확인
        self.assertAlmostEqual(orders1[0].weight, orders2[0].weight, places=2)
        self.assertAlmostEqual(orders1[0].volume, orders2[0].volume, places=2)


def run_tests():
    """테스트 실행"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestMLMatcher))
    suite.addTests(loader.loadTestsFromTestCase(TestTrainingDataGenerator))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "="*70)
    print("테스트 결과 요약")
    print("="*70)
    print(f"실행된 테스트: {result.testsRun}개")
    print(f"성공: {result.testsRun - len(result.failures) - len(result.errors)}개")
    print(f"실패: {len(result.failures)}개")
    print(f"오류: {len(result.errors)}개")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
