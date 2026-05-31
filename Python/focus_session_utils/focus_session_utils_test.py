"""
Focus Session Utils - 测试用例
"""

import unittest
from datetime import datetime, timedelta, date
from focus_session_utils.mod import (
    FocusSessionManager,
    FocusSession,
    SessionStatus,
    DistractionCategory,
    Distraction,
    DailyFocusReport,
)


class TestFocusSessionManager(unittest.TestCase):

    def setUp(self):
        self.manager = FocusSessionManager(daily_goal_minutes=120)

    def test_create_session(self):
        session = self.manager.create_session(25, "写报告")
        self.assertEqual(session.planned_duration_minutes, 25)
        self.assertEqual(session.task_name, "写报告")
        self.assertEqual(session.status, SessionStatus.IDLE)
        self.assertIsNotNone(session.id)

    def test_start_session(self):
        session = self.manager.create_session(25)
        self.manager.start_session(session)
        self.assertEqual(session.status, SessionStatus.RUNNING)
        self.assertIsNotNone(session.start_time)

    def test_end_session(self):
        session = self.manager.create_session(25)
        self.manager.start_session(session)
        self.manager.end_session(session)
        self.assertEqual(session.status, SessionStatus.COMPLETED)
        self.assertIsNotNone(session.end_time)

    def test_abandoned_session(self):
        session = self.manager.create_session(25)
        self.manager.start_session(session)
        self.manager.end_session(session, abandoned=True)
        self.assertEqual(session.status, SessionStatus.ABANDONED)

    def test_distraction_logging(self):
        session = self.manager.create_session(25)
        self.manager.start_session(session)
        self.manager.log_distraction(session, DistractionCategory.WEIXIN, note="群消息")
        self.assertEqual(session.distraction_count, 1)
        self.assertEqual(session.distractions[0].category, DistractionCategory.WEIXIN)

    def test_pause_and_resume(self):
        session = self.manager.create_session(25)
        self.manager.start_session(session)
        d = self.manager.pause_session(session)
        self.assertIsNotNone(d)
        self.assertEqual(session.status, SessionStatus.PAUSED)
        self.manager.resume_session(session, d, DistractionCategory.PHONE_CALL, "快递电话")
        self.assertEqual(session.status, SessionStatus.RUNNING)
        self.assertEqual(session.distractions[0].category, DistractionCategory.PHONE_CALL)
        self.assertGreaterEqual(len(session.distractions), 1)

    def test_quality_score_no_distraction(self):
        session = self.manager.create_session(25)
        self.manager.start_session(session)
        # 模拟已完成会话
        session.end_time = session.start_time + timedelta(minutes=25)
        session.status = SessionStatus.COMPLETED
        score = session.quality_score
        self.assertGreaterEqual(score, 90)

    def test_quality_score_with_distractions(self):
        session = self.manager.create_session(25)
        self.manager.start_session(session)
        session.end_time = session.start_time + timedelta(minutes=25)
        session.status = SessionStatus.COMPLETED
        session.distractions.append(Distraction(
            timestamp=session.start_time + timedelta(minutes=5),
            category=DistractionCategory.WEIXIN,
            duration_seconds=300
        ))
        score = session.distraction_free_seconds
        self.assertLess(score, 25 * 60)

    def test_completion_rate(self):
        session = FocusSession(id="test", planned_duration_minutes=30)
        session.start_time = datetime.now()
        session.end_time = session.start_time + timedelta(minutes=15)
        session.status = SessionStatus.COMPLETED
        self.assertAlmostEqual(session.completion_rate, 50.0, places=1)

    def test_daily_report(self):
        session = self.manager.create_session(60, "代码评审")
        self.manager.start_session(session)
        session.end_time = session.start_time + timedelta(minutes=60)
        session.status = SessionStatus.COMPLETED

        report = self.manager.get_daily_report()
        self.assertEqual(report.date, date.today())
        self.assertEqual(report.total_sessions, 1)
        self.assertEqual(report.completed_sessions, 1)
        self.assertEqual(report.total_focus_minutes, 60.0)

    def test_best_focus_hours(self):
        for i in range(3):
            s = self.manager.create_session(30, f"任务{i}")
            s.start_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) - timedelta(days=i)
            s.end_time = s.start_time + timedelta(minutes=30)
            s.status = SessionStatus.COMPLETED

        best = self.manager.get_best_focus_hours(days_back=7)
        self.assertTrue(len(best) > 0)

    def test_export_to_csv(self):
        session = self.manager.create_session(25, "测试任务")
        self.manager.start_session(session)
        self.manager.end_session(session)
        csv_str = self.manager.export_to_csv()
        self.assertIn("id", csv_str)
        self.assertIn("测试任务", csv_str)

    def test_session_id_provided(self):
        session = self.manager.create_session(25, session_id="custom-id-123")
        self.assertEqual(session.id, "custom-id-123")

    def test_empty_manager_report(self):
        report = self.manager.get_daily_report()
        self.assertEqual(report.total_sessions, 0)
        self.assertEqual(report.completed_sessions, 0)


if __name__ == "__main__":
    unittest.main()
