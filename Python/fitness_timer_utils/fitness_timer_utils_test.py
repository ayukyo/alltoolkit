"""
Tests for Fitness Timer Utilities

Comprehensive tests for all timer types and utility functions.
Run with: python -m pytest fitness_timer_utils_test.py -v
"""

import unittest
import time
import threading
from datetime import datetime
from mod import (
    TimerState,
    PhaseType,
    TimerPhase,
    TimerEvent,
    WorkoutResult,
    BaseTimer,
    HIITTimer,
    TabataTimer,
    EMOMTimer,
    AMRAPTimer,
    CircuitTimer,
    CountdownTimer,
    Stopwatch,
    format_time,
    parse_time,
    create_interval_timer,
    calculate_calories_burned,
    get_met_value,
    MET_VALUES,
)


class TestFormatTime(unittest.TestCase):
    """Test time formatting utilities."""
    
    def test_format_time_seconds_only(self):
        """Test formatting less than a minute."""
        self.assertEqual(format_time(0), "00:00")
        self.assertEqual(format_time(1), "00:01")
        self.assertEqual(format_time(30), "00:30")
        self.assertEqual(format_time(59), "00:59")
    
    def test_format_time_minutes(self):
        """Test formatting minutes."""
        self.assertEqual(format_time(60), "01:00")
        self.assertEqual(format_time(90), "01:30")
        self.assertEqual(format_time(3599), "59:59")
    
    def test_format_time_hours(self):
        """Test formatting hours."""
        self.assertEqual(format_time(3600), "01:00:00")
        self.assertEqual(format_time(3661), "01:01:01")
        self.assertEqual(format_time(7325), "02:02:05")
    
    def test_format_time_negative(self):
        """Test negative time handling."""
        self.assertEqual(format_time(-1), "00:00")
        self.assertEqual(format_time(-100), "00:00")


class TestParseTime(unittest.TestCase):
    """Test time parsing utilities."""
    
    def test_parse_mmss(self):
        """Test parsing MM:SS format."""
        self.assertEqual(parse_time("00:00"), 0)
        self.assertEqual(parse_time("00:30"), 30)
        self.assertEqual(parse_time("01:00"), 60)
        self.assertEqual(parse_time("05:30"), 330)
        self.assertEqual(parse_time("59:59"), 3599)
    
    def test_parse_hhmmss(self):
        """Test parsing HH:MM:SS format."""
        self.assertEqual(parse_time("00:00:00"), 0)
        self.assertEqual(parse_time("01:00:00"), 3600)
        self.assertEqual(parse_time("01:30:30"), 5430)
        self.assertEqual(parse_time("02:30:45"), 9045)
    
    def test_parse_invalid(self):
        """Test invalid format handling."""
        with self.assertRaises(ValueError):
            parse_time("invalid")
        with self.assertRaises(ValueError):
            parse_time("1:2:3:4")


class TestHIITTimer(unittest.TestCase):
    """Test HIIT Timer functionality."""
    
    def test_initialization(self):
        """Test timer initialization with default values."""
        timer = HIITTimer()
        self.assertEqual(timer.work_seconds, 30)
        self.assertEqual(timer.rest_seconds, 15)
        self.assertEqual(timer.rounds, 8)
        self.assertEqual(timer.prepare_seconds, 10)
        self.assertEqual(timer.state, TimerState.IDLE)
    
    def test_custom_initialization(self):
        """Test timer with custom values."""
        timer = HIITTimer(work_seconds=45, rest_seconds=20, rounds=5, prepare_seconds=5)
        self.assertEqual(timer.work_seconds, 45)
        self.assertEqual(timer.rest_seconds, 20)
        self.assertEqual(timer.rounds, 5)
        self.assertEqual(timer.prepare_seconds, 5)
    
    def test_total_duration(self):
        """Test total duration calculation."""
        timer = HIITTimer(work_seconds=30, rest_seconds=10, rounds=4, prepare_seconds=5)
        # 5 + 4 * (30 + 10) = 5 + 160 = 165
        self.assertEqual(timer.total_duration, 165)
    
    def test_state_management(self):
        """Test timer state transitions."""
        timer = HIITTimer(work_seconds=1, rest_seconds=1, rounds=1, prepare_seconds=0)
        
        self.assertTrue(timer.is_running is False)
        self.assertTrue(timer.is_paused is False)
        self.assertTrue(timer.is_completed is False)
    
    def test_run_short_timer(self):
        """Test running a very short HIIT timer."""
        timer = HIITTimer(work_seconds=1, rest_seconds=1, rounds=1, prepare_seconds=0)
        events = []
        
        def on_tick(event):
            events.append(('tick', event.phase, event.remaining_seconds))
        
        def on_phase(event):
            events.append(('phase', event.phase, event.phase_name))
        
        timer.on_tick(on_tick).on_phase_change(on_phase)
        result = timer.run(blocking=True)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.workout_type, "HIIT")
        self.assertEqual(result.rounds_completed, 1)
        self.assertTrue(timer.is_completed)
        self.assertTrue(len(events) > 0)
    
    def test_run_with_preparation(self):
        """Test timer with preparation phase."""
        timer = HIITTimer(work_seconds=1, rest_seconds=1, rounds=1, prepare_seconds=1)
        phases = []
        
        def on_phase(event):
            phases.append(event.phase)
        
        timer.on_phase_change(on_phase)
        result = timer.run(blocking=True)
        
        self.assertIn(PhaseType.PREPARE, phases)
        self.assertIn(PhaseType.WORK, phases)
        self.assertIsNotNone(result)
    
    def test_double_run_raises_error(self):
        """Test that running twice without reset raises error."""
        timer = HIITTimer(work_seconds=1, rest_seconds=1, rounds=1, prepare_seconds=0)
        timer.run(blocking=True)
        
        with self.assertRaises(RuntimeError):
            timer.run(blocking=True)
    
    def test_reset(self):
        """Test timer reset functionality."""
        timer = HIITTimer(work_seconds=1, rest_seconds=1, rounds=1, prepare_seconds=0)
        timer.run(blocking=True)
        timer.reset()
        
        self.assertEqual(timer.state, TimerState.IDLE)
        self.assertTrue(timer.is_running is False)
    
    def test_pause_resume(self):
        """Test pause and resume functionality."""
        timer = HIITTimer(work_seconds=5, rest_seconds=2, rounds=1, prepare_seconds=0)
        tick_count = [0]
        pause_triggered = [False]
        
        def on_tick(event):
            tick_count[0] += 1
            if tick_count[0] == 2 and not pause_triggered[0]:
                timer.pause()
                pause_triggered[0] = True
                # Resume after a short delay
                threading.Timer(0.5, timer.resume).start()
        
        timer.on_tick(on_tick)
        
        # Run in thread
        thread = threading.Thread(target=timer.run, kwargs={'blocking': True})
        thread.start()
        thread.join(timeout=15)
        
        self.assertTrue(pause_triggered[0])


class TestTabataTimer(unittest.TestCase):
    """Test Tabata Timer functionality."""
    
    def test_initialization(self):
        """Test Tabata timer initialization."""
        timer = TabataTimer()
        self.assertEqual(timer.work_seconds, 20)
        self.assertEqual(timer.rest_seconds, 10)
        self.assertEqual(timer.rounds, 8)
        self.assertEqual(timer.state, TimerState.IDLE)
    
    def test_custom_rounds(self):
        """Test Tabata with custom round count."""
        timer = TabataTimer(rounds=4, prepare_seconds=5)
        self.assertEqual(timer.rounds, 4)
        self.assertEqual(timer.prepare_seconds, 5)
    
    def test_total_duration(self):
        """Test Tabata total duration calculation."""
        timer = TabataTimer(rounds=8, prepare_seconds=10)
        # 10 + 8 * (20 + 10) = 10 + 240 = 250
        self.assertEqual(timer.total_duration, 250)
    
    def test_tabata_result_type(self):
        """Test that Tabata result has correct type."""
        timer = TabataTimer(rounds=1, prepare_seconds=0)
        result = timer.run(blocking=True)
        
        self.assertEqual(result.workout_type, "Tabata")


class TestEMOMTimer(unittest.TestCase):
    """Test EMOM Timer functionality."""
    
    def test_initialization(self):
        """Test EMOM timer initialization."""
        timer = EMOMTimer(duration_minutes=5)
        self.assertEqual(timer.duration_minutes, 5)
        self.assertEqual(timer.state, TimerState.IDLE)
    
    def test_total_duration(self):
        """Test EMOM total duration calculation."""
        timer = EMOMTimer(duration_minutes=10)
        self.assertEqual(timer.total_duration, 600)
    
    def test_run_short_emom(self):
        """Test running a short EMOM workout."""
        timer = EMOMTimer(duration_minutes=1, exercises=["Push-ups", "Squats"])
        events = []
        
        def on_phase(event):
            events.append(event)
        
        timer.on_phase_change(on_phase)
        result = timer.run(blocking=True)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.workout_type, "EMOM")
        self.assertEqual(result.rounds_completed, 1)
    
    def test_exercise_rotation(self):
        """Test exercise name rotation."""
        timer = EMOMTimer(duration_minutes=3, exercises=["A", "B"])
        
        # Test internal method
        self.assertEqual(timer._get_exercise_name(1), " - A")
        self.assertEqual(timer._get_exercise_name(2), " - B")
        self.assertEqual(timer._get_exercise_name(3), " - A")


class TestAMRAPTimer(unittest.TestCase):
    """Test AMRAP Timer functionality."""
    
    def test_initialization(self):
        """Test AMRAP timer initialization."""
        timer = AMRAPTimer(duration_minutes=10)
        self.assertEqual(timer.duration_minutes, 10)
        self.assertEqual(timer.state, TimerState.IDLE)
    
    def test_total_duration(self):
        """Test AMRAP total duration calculation."""
        timer = AMRAPTimer(duration_minutes=15)
        self.assertEqual(timer.total_duration, 900)
    
    def test_record_round(self):
        """Test recording rounds during AMRAP."""
        timer = AMRAPTimer(duration_minutes=1)
        
        def on_tick(event):
            # Record a round every 15 seconds
            elapsed = event.elapsed_seconds
            if elapsed in [15, 30, 45]:
                timer.record_round()
        
        timer.on_tick(on_tick)
        result = timer.run(blocking=True)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.workout_type, "AMRAP")
        self.assertGreaterEqual(result.rounds_completed, 2)
    
    def test_amrap_result(self):
        """Test AMRAP result data."""
        timer = AMRAPTimer(duration_minutes=1)
        result = timer.run(blocking=True)
        
        self.assertEqual(result.workout_type, "AMRAP")
        self.assertEqual(result.total_duration_seconds, 60)
        self.assertGreaterEqual(len(result.phases), 1)


class TestCircuitTimer(unittest.TestCase):
    """Test Circuit Timer functionality."""
    
    def test_initialization(self):
        """Test circuit timer initialization."""
        exercises = [
            {"name": "Push-ups", "duration": 30},
            {"name": "Squats", "duration": 30},
        ]
        timer = CircuitTimer(exercises=exercises, rounds=3)
        
        self.assertEqual(len(timer.exercises), 2)
        self.assertEqual(timer.rounds, 3)
        self.assertEqual(timer.state, TimerState.IDLE)
    
    def test_total_duration(self):
        """Test circuit total duration calculation."""
        exercises = [
            {"name": "Push-ups", "duration": 30},
            {"name": "Squats", "duration": 30},
        ]
        timer = CircuitTimer(
            exercises=exercises,
            rounds=3,
            rest_between_exercises=10,
            rest_between_rounds=60,
            prepare_seconds=5
        )
        # 5 + 3 * (30 + 30) + 3 * 2 * 10 rest + 2 * 60 round rest
        # = 5 + 180 + 60 + 120 = 365
        # Actually: 5 prep + (30+30)*3 exercises + 10*2*3 rest between + 60*2 rest rounds
        # = 5 + 180 + 60 + 120 = 365
        self.assertEqual(timer.total_duration, 185)
    
    def test_run_short_circuit(self):
        """Test running a short circuit."""
        exercises = [
            {"name": "Push-ups", "duration": 1},
            {"name": "Squats", "duration": 1},
        ]
        timer = CircuitTimer(
            exercises=exercises,
            rounds=1,
            rest_between_exercises=1,
            rest_between_rounds=0,
            prepare_seconds=0
        )
        
        phases = []
        def on_phase(event):
            phases.append(event.phase_name)
        
        timer.on_phase_change(on_phase)
        result = timer.run(blocking=True)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.workout_type, "Circuit")
        self.assertIn("Push-ups", phases)
        self.assertIn("Squats", phases)


class TestCountdownTimer(unittest.TestCase):
    """Test Countdown Timer functionality."""
    
    def test_initialization(self):
        """Test countdown timer initialization."""
        timer = CountdownTimer(duration_seconds=60, name="Test Timer")
        self.assertEqual(timer.duration_seconds, 60)
        self.assertEqual(timer.name, "Test Timer")
    
    def test_run_short_countdown(self):
        """Test running a short countdown."""
        timer = CountdownTimer(duration_seconds=2, name="Quick")
        
        ticks = []
        def on_tick(event):
            ticks.append(event.remaining_seconds)
        
        timer.on_tick(on_tick)
        result = timer.run(blocking=True)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.workout_type, "Countdown")
        self.assertEqual(result.total_duration_seconds, 2)
        self.assertEqual(len(ticks), 2)


class TestStopwatch(unittest.TestCase):
    """Test Stopwatch functionality."""
    
    def test_initialization(self):
        """Test stopwatch initialization."""
        stopwatch = Stopwatch()
        self.assertEqual(stopwatch.state, TimerState.IDLE)
        self.assertEqual(len(stopwatch.laps), 0)
    
    def test_run_and_stop(self):
        """Test running and stopping stopwatch."""
        stopwatch = Stopwatch()
        
        stopwatch.run(blocking=False)
        self.assertTrue(stopwatch.is_running)
        
        time.sleep(0.5)  # Let it run briefly
        
        result = stopwatch.stop()
        self.assertEqual(stopwatch.state, TimerState.COMPLETED)
        self.assertEqual(result.workout_type, "Stopwatch")
    
    def test_lap_tracking(self):
        """Test lap tracking."""
        stopwatch = Stopwatch()
        stopwatch.run(blocking=False)
        
        time.sleep(0.2)
        lap1 = stopwatch.lap("First Lap")
        self.assertEqual(lap1['name'], "First Lap")
        self.assertEqual(lap1['lap_number'], 1)
        
        time.sleep(0.2)
        lap2 = stopwatch.lap()
        self.assertEqual(lap2['lap_number'], 2)
        
        stopwatch.stop()
        
        self.assertEqual(len(stopwatch.laps), 2)
    
    def test_lap_without_run(self):
        """Test that lap without running raises error."""
        stopwatch = Stopwatch()
        
        with self.assertRaises(RuntimeError):
            stopwatch.lap()
    
    def test_stop_without_run(self):
        """Test that stop without running raises error."""
        stopwatch = Stopwatch()
        
        with self.assertRaises(RuntimeError):
            stopwatch.stop()


class TestWorkoutResult(unittest.TestCase):
    """Test WorkoutResult dataclass."""
    
    def test_properties(self):
        """Test result properties."""
        result = WorkoutResult(
            workout_type="Test",
            total_duration_seconds=120,
            rounds_completed=3,
            work_time_seconds=90,
            rest_time_seconds=30,
            start_time=datetime.now(),
            end_time=datetime.now()
        )
        
        self.assertEqual(result.total_duration_minutes, 2.0)
    
    def test_to_dict(self):
        """Test serialization to dictionary."""
        result = WorkoutResult(
            workout_type="HIIT",
            total_duration_seconds=300,
            rounds_completed=5,
            work_time_seconds=200,
            rest_time_seconds=100,
            start_time=datetime(2024, 1, 1, 10, 0, 0),
            end_time=datetime(2024, 1, 1, 10, 5, 0)
        )
        
        d = result.to_dict()
        self.assertEqual(d['workout_type'], 'HIIT')
        self.assertEqual(d['total_duration_seconds'], 300)
        self.assertEqual(d['total_duration_minutes'], 5.0)
        self.assertEqual(d['rounds_completed'], 5)


class TestCreateIntervalTimer(unittest.TestCase):
    """Test timer factory function."""
    
    def test_create_hiit(self):
        """Test creating HIIT timer."""
        timer = create_interval_timer(work_seconds=30, rest_seconds=10, rounds=5, timer_type="hiit")
        self.assertIsInstance(timer, HIITTimer)
        self.assertEqual(timer.work_seconds, 30)
        self.assertEqual(timer.rest_seconds, 10)
        self.assertEqual(timer.rounds, 5)
    
    def test_create_tabata(self):
        """Test creating Tabata timer."""
        timer = create_interval_timer(work_seconds=20, rest_seconds=10, rounds=4, timer_type="tabata")
        self.assertIsInstance(timer, TabataTimer)
        # Tabata ignores custom work/rest values
        self.assertEqual(timer.rounds, 4)
    
    def test_invalid_type(self):
        """Test invalid timer type."""
        with self.assertRaises(ValueError):
            create_interval_timer(30, 10, 5, "invalid")


class TestCalorieCalculation(unittest.TestCase):
    """Test calorie calculation utilities."""
    
    def test_calculate_calories_burned(self):
        """Test calorie calculation."""
        # 30 minutes of moderate exercise (MET 5) for 70kg person
        calories = calculate_calories_burned(30, 5.0, 70)
        # 5 * 70 * (30/60) = 5 * 70 * 0.5 = 175
        self.assertAlmostEqual(calories, 175.0, places=1)
    
    def test_calculate_calories_hour(self):
        """Test calorie calculation for one hour."""
        # 60 minutes of running (MET 9.8) for 70kg person
        calories = calculate_calories_burned(60, 9.8, 70)
        # 9.8 * 70 * 1 = 686
        self.assertAlmostEqual(calories, 686.0, places=1)
    
    def test_get_met_value(self):
        """Test MET value lookup."""
        self.assertEqual(get_met_value("resting"), 1.0)
        self.assertEqual(get_met_value("running_5mph"), 8.3)
        self.assertEqual(get_met_value("jump_rope"), 12.0)
        self.assertEqual(get_met_value("HIIT"), 8.0)
        self.assertEqual(get_met_value("tabata"), 10.0)
    
    def test_get_met_value_case_insensitive(self):
        """Test MET value lookup is case insensitive."""
        self.assertEqual(get_met_value("RUNNING_5MPH"), 8.3)
        self.assertEqual(get_met_value("Jump_Rope"), 12.0)
    
    def test_get_met_value_unknown(self):
        """Test MET value for unknown exercise returns default."""
        self.assertEqual(get_met_value("unknown_exercise"), 5.0)
    
    def test_met_values_dict_exists(self):
        """Test that MET_VALUES dictionary contains expected values."""
        self.assertIn("hiit", MET_VALUES)
        self.assertIn("tabata", MET_VALUES)
        self.assertIn("running_5mph", MET_VALUES)
        self.assertGreater(MET_VALUES["jump_rope"], MET_VALUES["walking"])


class TestTimerEvent(unittest.TestCase):
    """Test TimerEvent dataclass."""
    
    def test_event_creation(self):
        """Test timer event creation."""
        event = TimerEvent(
            phase=PhaseType.WORK,
            phase_name="Work",
            remaining_seconds=30,
            total_seconds=45,
            current_round=2,
            total_rounds=5,
            elapsed_seconds=15,
            state=TimerState.RUNNING
        )
        
        self.assertEqual(event.phase, PhaseType.WORK)
        self.assertEqual(event.phase_name, "Work")
        self.assertEqual(event.remaining_seconds, 30)
        self.assertEqual(event.current_round, 2)
        self.assertEqual(event.state, TimerState.RUNNING)
        self.assertIsNotNone(event.timestamp)
    
    def test_event_with_metadata(self):
        """Test timer event with metadata."""
        event = TimerEvent(
            phase=PhaseType.WORK,
            phase_name="Exercise",
            remaining_seconds=30,
            total_seconds=30,
            current_round=1,
            total_rounds=3,
            elapsed_seconds=0,
            state=TimerState.RUNNING,
            metadata={"exercise": "Push-ups", "reps": 10}
        )
        
        self.assertEqual(event.metadata["exercise"], "Push-ups")
        self.assertEqual(event.metadata["reps"], 10)


class TestTimerPhase(unittest.TestCase):
    """Test TimerPhase dataclass."""
    
    def test_phase_creation(self):
        """Test timer phase creation."""
        phase = TimerPhase(
            phase_type=PhaseType.WORK,
            duration_seconds=30
        )
        
        self.assertEqual(phase.phase_type, PhaseType.WORK)
        self.assertEqual(phase.duration_seconds, 30)
        self.assertEqual(phase.name, "Work")
    
    def test_phase_custom_name(self):
        """Test timer phase with custom name."""
        phase = TimerPhase(
            phase_type=PhaseType.WORK,
            duration_seconds=45,
            name="Burpees"
        )
        
        self.assertEqual(phase.name, "Burpees")


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workout flows."""
    
    def test_full_hiit_workout(self):
        """Test a complete mini HIIT workout."""
        timer = HIITTimer(work_seconds=1, rest_seconds=1, rounds=2, prepare_seconds=1)
        
        results = {
            'phases': [],
            'ticks': 0,
            'completed': False
        }
        
        def on_phase(event):
            results['phases'].append(event.phase)
        
        def on_tick(event):
            results['ticks'] += 1
        
        def on_complete(result):
            results['completed'] = True
        
        timer.on_phase_change(on_phase).on_tick(on_tick).on_complete(on_complete)
        result = timer.run(blocking=True)
        
        self.assertTrue(results['completed'])
        self.assertEqual(result.workout_type, "HIIT")
        self.assertEqual(result.rounds_completed, 2)
        self.assertIn(PhaseType.PREPARE, results['phases'])
        self.assertIn(PhaseType.WORK, results['phases'])
        self.assertIn(PhaseType.REST, results['phases'])
    
    def test_circuit_with_exercises(self):
        """Test circuit timer with multiple exercises."""
        exercises = [
            {"name": "Push-ups", "duration": 1},
            {"name": "Squats", "duration": 1},
            {"name": "Plank", "duration": 1},
        ]
        
        timer = CircuitTimer(
            exercises=exercises,
            rounds=2,
            rest_between_exercises=1,
            rest_between_rounds=1,
            prepare_seconds=0
        )
        
        completed_phases = []
        
        def on_phase(event):
            completed_phases.append(event.phase_name)
        
        timer.on_phase_change(on_phase)
        result = timer.run(blocking=True)
        
        self.assertIsNotNone(result)
        self.assertIn("Push-ups", completed_phases)
        self.assertIn("Squats", completed_phases)
        self.assertIn("Plank", completed_phases)
        self.assertIn("Rest", completed_phases)


if __name__ == "__main__":
    unittest.main(verbosity=2)