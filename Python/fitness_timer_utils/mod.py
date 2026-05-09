"""
Fitness Timer Utilities

A comprehensive fitness timer module supporting various workout styles:
- HIIT (High-Intensity Interval Training)
- Tabata (20s work / 10s rest)
- EMOM (Every Minute on the Minute)
- AMRAP (As Many Rounds As Possible)
- Circuit Training
- Countdown Timer
- Stopwatch

Zero external dependencies - uses only Python standard library.
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional, List, Dict, Any
from datetime import datetime, timedelta


class TimerState(Enum):
    """Timer state enumeration."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"


class PhaseType(Enum):
    """Workout phase types."""
    PREPARE = "prepare"
    WORK = "work"
    REST = "rest"
    TRANSITION = "transition"
    COMPLETED = "completed"


@dataclass
class TimerPhase:
    """Represents a single phase in a workout timer."""
    phase_type: PhaseType
    duration_seconds: int
    name: str = ""
    
    def __post_init__(self):
        if not self.name:
            self.name = self.phase_type.value.capitalize()


@dataclass
class TimerEvent:
    """Event data passed to callbacks during timer execution."""
    phase: PhaseType
    phase_name: str
    remaining_seconds: int
    total_seconds: int
    current_round: int
    total_rounds: int
    elapsed_seconds: int
    state: TimerState
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkoutResult:
    """Result of a completed workout session."""
    workout_type: str
    total_duration_seconds: int
    rounds_completed: int
    work_time_seconds: int
    rest_time_seconds: int
    start_time: datetime
    end_time: datetime
    phases: List[Dict[str, Any]] = field(default_factory=list)
    
    @property
    def total_duration_minutes(self) -> float:
        return self.total_duration_seconds / 60
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "workout_type": self.workout_type,
            "total_duration_seconds": self.total_duration_seconds,
            "total_duration_minutes": round(self.total_duration_minutes, 2),
            "rounds_completed": self.rounds_completed,
            "work_time_seconds": self.work_time_seconds,
            "rest_time_seconds": self.rest_time_seconds,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "phases": self.phases
        }


class BaseTimer:
    """Base class for all fitness timers."""
    
    def __init__(self):
        self.state: TimerState = TimerState.IDLE
        self._start_time: Optional[float] = None
        self._pause_time: Optional[float] = None
        self._elapsed_before_pause: int = 0
        self._current_phase: Optional[PhaseType] = None
        self._current_round: int = 0
        self._on_tick: Optional[Callable[[TimerEvent], None]] = None
        self._on_phase_change: Optional[Callable[[TimerEvent], None]] = None
        self._on_complete: Optional[Callable[[WorkoutResult], None]] = None
        self._event_log: List[Dict[str, Any]] = []
    
    def on_tick(self, callback: Callable[[TimerEvent], None]) -> 'BaseTimer':
        """Set callback for each second tick."""
        self._on_tick = callback
        return self
    
    def on_phase_change(self, callback: Callable[[TimerEvent], None]) -> 'BaseTimer':
        """Set callback for phase changes."""
        self._on_phase_change = callback
        return self
    
    def on_complete(self, callback: Callable[[WorkoutResult], None]) -> 'BaseTimer':
        """Set callback for workout completion."""
        self._on_complete = callback
        return self
    
    def _emit_tick(self, event: TimerEvent) -> None:
        """Emit tick event."""
        if self._on_tick:
            self._on_tick(event)
    
    def _emit_phase_change(self, event: TimerEvent) -> None:
        """Emit phase change event."""
        self._event_log.append({
            "phase": event.phase.value,
            "round": event.current_round,
            "timestamp": event.timestamp.isoformat()
        })
        if self._on_phase_change:
            self._on_phase_change(event)
    
    def _emit_complete(self, result: WorkoutResult) -> None:
        """Emit completion event."""
        result.phases = self._event_log
        if self._on_complete:
            self._on_complete(result)
    
    def pause(self) -> None:
        """Pause the timer."""
        if self.state == TimerState.RUNNING:
            self.state = TimerState.PAUSED
            self._pause_time = time.time()
    
    def resume(self) -> None:
        """Resume a paused timer."""
        if self.state == TimerState.PAUSED:
            self.state = TimerState.RUNNING
            if self._pause_time:
                pause_duration = time.time() - self._pause_time
                self._start_time += pause_duration
                self._pause_time = None
    
    def reset(self) -> None:
        """Reset the timer to initial state."""
        self.state = TimerState.IDLE
        self._start_time = None
        self._pause_time = None
        self._elapsed_before_pause = 0
        self._current_phase = None
        self._current_round = 0
        self._event_log = []
    
    @property
    def is_running(self) -> bool:
        return self.state == TimerState.RUNNING
    
    @property
    def is_paused(self) -> bool:
        return self.state == TimerState.PAUSED
    
    @property
    def is_completed(self) -> bool:
        return self.state == TimerState.COMPLETED


class HIITTimer(BaseTimer):
    """
    High-Intensity Interval Training Timer.
    
    Supports custom work/rest intervals with configurable rounds.
    """
    
    def __init__(
        self,
        work_seconds: int = 30,
        rest_seconds: int = 15,
        rounds: int = 8,
        prepare_seconds: int = 10
    ):
        super().__init__()
        self.work_seconds = work_seconds
        self.rest_seconds = rest_seconds
        self.rounds = rounds
        self.prepare_seconds = prepare_seconds
        self._work_elapsed: int = 0
        self._rest_elapsed: int = 0
    
    @property
    def total_duration(self) -> int:
        """Calculate total workout duration in seconds."""
        return (
            self.prepare_seconds +
            (self.work_seconds + self.rest_seconds) * self.rounds
        )
    
    def run(self, blocking: bool = True) -> Optional[WorkoutResult]:
        """
        Start the HIIT timer.
        
        Args:
            blocking: If True, blocks until complete. If False, runs in background.
        
        Returns:
            WorkoutResult if blocking, None otherwise.
        """
        if self.state != TimerState.IDLE:
            raise RuntimeError("Timer already started. Call reset() first.")
        
        self.state = TimerState.RUNNING
        self._start_time = time.time()
        result = None
        
        try:
            # Prepare phase
            if self.prepare_seconds > 0:
                self._run_phase(PhaseType.PREPARE, self.prepare_seconds, 0)
            
            # Work/Rest rounds
            for round_num in range(1, self.rounds + 1):
                if self.state != TimerState.RUNNING:
                    break
                self._current_round = round_num
                self._run_phase(PhaseType.WORK, self.work_seconds, round_num)
                self._work_elapsed += self.work_seconds
                
                if round_num < self.rounds and self.state == TimerState.RUNNING:
                    self._run_phase(PhaseType.REST, self.rest_seconds, round_num)
                    self._rest_elapsed += self.rest_seconds
            
            if self.state == TimerState.RUNNING:
                self.state = TimerState.COMPLETED
                result = self._create_result()
                self._emit_complete(result)
        
        except Exception as e:
            self.state = TimerState.IDLE
            raise e
        
        return result if blocking else None
    
    def _run_phase(self, phase_type: PhaseType, duration: int, round_num: int) -> None:
        """Run a single phase of the workout."""
        self._current_phase = phase_type
        
        event = TimerEvent(
            phase=phase_type,
            phase_name=phase_type.value.capitalize(),
            remaining_seconds=duration,
            total_seconds=duration,
            current_round=round_num,
            total_rounds=self.rounds,
            elapsed_seconds=int(time.time() - self._start_time),
            state=self.state
        )
        self._emit_phase_change(event)
        
        for remaining in range(duration, 0, -1):
            if self.state != TimerState.RUNNING:
                break
            
            while self.state == TimerState.PAUSED:
                time.sleep(0.1)
            
            if self.state != TimerState.RUNNING:
                break
            
            event = TimerEvent(
                phase=phase_type,
                phase_name=phase_type.value.capitalize(),
                remaining_seconds=remaining,
                total_seconds=duration,
                current_round=round_num,
                total_rounds=self.rounds,
                elapsed_seconds=int(time.time() - self._start_time),
                state=self.state
            )
            self._emit_tick(event)
            
            if remaining > 1:
                time.sleep(1)
    
    def _create_result(self) -> WorkoutResult:
        """Create workout result."""
        end_time = datetime.now()
        start_time = datetime.fromtimestamp(self._start_time)
        
        return WorkoutResult(
            workout_type="HIIT",
            total_duration_seconds=int(time.time() - self._start_time),
            rounds_completed=self._current_round,
            work_time_seconds=self._work_elapsed,
            rest_time_seconds=self._rest_elapsed,
            start_time=start_time,
            end_time=end_time
        )


class TabataTimer(HIITTimer):
    """
    Tabata Timer - Standard 20/10 interval training.
    
    Tabata protocol: 8 rounds of 20 seconds work + 10 seconds rest.
    Total: 4 minutes.
    """
    
    def __self_init__(self):
        self._work_elapsed: int = 0
        self._rest_elapsed: int = 0
    
    def __init__(self, rounds: int = 8, prepare_seconds: int = 10):
        """
        Initialize Tabata timer.
        
        Args:
            rounds: Number of rounds (default 8 for standard Tabata)
            prepare_seconds: Preparation time before starting
        """
        super().__init__(
            work_seconds=20,
            rest_seconds=10,
            rounds=rounds,
            prepare_seconds=prepare_seconds
        )
        self._work_elapsed: int = 0
        self._rest_elapsed: int = 0
    
    def _create_result(self) -> WorkoutResult:
        """Create workout result with Tabata type."""
        result = super()._create_result()
        result.workout_type = "Tabata"
        return result


class EMOMTimer(BaseTimer):
    """
    EMOM (Every Minute on the Minute) Timer.
    
    Perform a set of exercises at the start of every minute.
    Remaining time in the minute is your rest period.
    """
    
    def __init__(
        self,
        duration_minutes: int = 10,
        exercises: Optional[List[str]] = None
    ):
        super().__init__()
        self.duration_minutes = duration_minutes
        self.exercises = exercises or []
        self._current_exercise_idx: int = 0
        self._total_work_seconds: int = 0
    
    @property
    def total_duration(self) -> int:
        """Total duration in seconds."""
        return self.duration_minutes * 60
    
    def run(self, blocking: bool = True) -> Optional[WorkoutResult]:
        """Start the EMOM timer."""
        if self.state != TimerState.IDLE:
            raise RuntimeError("Timer already started. Call reset() first.")
        
        self.state = TimerState.RUNNING
        self._start_time = time.time()
        result = None
        
        try:
            for minute in range(1, self.duration_minutes + 1):
                if self.state != TimerState.RUNNING:
                    break
                
                self._current_round = minute
                exercise_name = self._get_exercise_name(minute)
                
                # New minute event
                event = TimerEvent(
                    phase=PhaseType.WORK,
                    phase_name=f"Minute {minute}{exercise_name}",
                    remaining_seconds=60,
                    total_seconds=60,
                    current_round=minute,
                    total_rounds=self.duration_minutes,
                    elapsed_seconds=(minute - 1) * 60,
                    state=self.state,
                    metadata={"exercise": exercise_name.strip(" - ")} if exercise_name else {}
                )
                self._emit_phase_change(event)
                
                # Count down the minute
                for second in range(60, 0, -1):
                    if self.state != TimerState.RUNNING:
                        break
                    
                    while self.state == TimerState.PAUSED:
                        time.sleep(0.1)
                    
                    if self.state != TimerState.RUNNING:
                        break
                    
                    event = TimerEvent(
                        phase=PhaseType.WORK if second > 30 else PhaseType.REST,
                        phase_name=f"Minute {minute}{exercise_name}",
                        remaining_seconds=second,
                        total_seconds=60,
                        current_round=minute,
                        total_rounds=self.duration_minutes,
                        elapsed_seconds=(minute - 1) * 60 + (60 - second),
                        state=self.state,
                        metadata={"exercise": exercise_name.strip(" - ")} if exercise_name else {}
                    )
                    self._emit_tick(event)
                    
                    if second > 1:
                        time.sleep(1)
            
            if self.state == TimerState.RUNNING:
                self.state = TimerState.COMPLETED
                result = self._create_result()
                self._emit_complete(result)
        
        except Exception as e:
            self.state = TimerState.IDLE
            raise e
        
        return result if blocking else None
    
    def _get_exercise_name(self, minute: int) -> str:
        """Get exercise name for current minute."""
        if not self.exercises:
            return ""
        exercise = self.exercises[(minute - 1) % len(self.exercises)]
        return f" - {exercise}"
    
    def _create_result(self) -> WorkoutResult:
        """Create workout result."""
        end_time = datetime.now()
        start_time = datetime.fromtimestamp(self._start_time)
        
        return WorkoutResult(
            workout_type="EMOM",
            total_duration_seconds=self.duration_minutes * 60,
            rounds_completed=self._current_round,
            work_time_seconds=self._current_round * 30,  # Estimated
            rest_time_seconds=self._current_round * 30,  # Estimated
            start_time=start_time,
            end_time=end_time
        )


class AMRAPTimer(BaseTimer):
    """
    AMRAP (As Many Rounds As Possible) Timer.
    
    Complete as many rounds of exercises as possible in the given time.
    """
    
    def __init__(
        self,
        duration_minutes: int = 20,
        round_exercises: Optional[List[str]] = None
    ):
        super().__init__()
        self.duration_minutes = duration_minutes
        self.round_exercises = round_exercises or []
        self._rounds_completed: int = 0
        self._last_round_time: Optional[float] = None
        self._round_times: List[float] = []
    
    @property
    def total_duration(self) -> int:
        """Total duration in seconds."""
        return self.duration_minutes * 60
    
    def record_round(self) -> None:
        """Record completion of one round."""
        if self.state == TimerState.RUNNING:
            self._rounds_completed += 1
            current_time = time.time()
            if self._last_round_time:
                self._round_times.append(current_time - self._last_round_time)
            self._last_round_time = current_time
    
    def run(self, blocking: bool = True) -> Optional[WorkoutResult]:
        """Start the AMRAP timer."""
        if self.state != TimerState.IDLE:
            raise RuntimeError("Timer already started. Call reset() first.")
        
        self.state = TimerState.RUNNING
        self._start_time = time.time()
        self._last_round_time = self._start_time
        result = None
        
        try:
            total_seconds = self.duration_minutes * 60
            
            # Initial phase event
            event = TimerEvent(
                phase=PhaseType.WORK,
                phase_name="AMRAP",
                remaining_seconds=total_seconds,
                total_seconds=total_seconds,
                current_round=0,
                total_rounds=0,  # Unknown in AMRAP
                elapsed_seconds=0,
                state=self.state
            )
            self._emit_phase_change(event)
            
            for remaining in range(total_seconds, 0, -1):
                if self.state != TimerState.RUNNING:
                    break
                
                while self.state == TimerState.PAUSED:
                    time.sleep(0.1)
                
                if self.state != TimerState.RUNNING:
                    break
                
                self._current_round = self._rounds_completed
                
                event = TimerEvent(
                    phase=PhaseType.WORK,
                    phase_name="AMRAP",
                    remaining_seconds=remaining,
                    total_seconds=total_seconds,
                    current_round=self._rounds_completed,
                    total_rounds=self._rounds_completed,
                    elapsed_seconds=total_seconds - remaining,
                    state=self.state
                )
                self._emit_tick(event)
                
                if remaining > 1:
                    time.sleep(1)
            
            if self.state == TimerState.RUNNING:
                self.state = TimerState.COMPLETED
                result = self._create_result()
                self._emit_complete(result)
        
        except Exception as e:
            self.state = TimerState.IDLE
            raise e
        
        return result if blocking else None
    
    def _create_result(self) -> WorkoutResult:
        """Create workout result."""
        end_time = datetime.now()
        start_time = datetime.fromtimestamp(self._start_time)
        
        avg_round_time = (
            sum(self._round_times) / len(self._round_times)
            if self._round_times else 0
        )
        
        return WorkoutResult(
            workout_type="AMRAP",
            total_duration_seconds=self.duration_minutes * 60,
            rounds_completed=self._rounds_completed,
            work_time_seconds=self.duration_minutes * 60,
            rest_time_seconds=0,
            start_time=start_time,
            end_time=end_time,
            phases=[{
                "rounds_completed": self._rounds_completed,
                "average_round_time": round(avg_round_time, 2),
                "round_times": [round(t, 2) for t in self._round_times]
            }]
        )


class CircuitTimer(BaseTimer):
    """
    Circuit Training Timer.
    
    Customizable circuit with multiple exercises, each with specific duration.
    Supports rest between exercises and between rounds.
    """
    
    def __init__(
        self,
        exercises: List[Dict[str, Any]],
        rounds: int = 3,
        rest_between_exercises: int = 15,
        rest_between_rounds: int = 60,
        prepare_seconds: int = 10
    ):
        """
        Initialize circuit timer.
        
        Args:
            exercises: List of exercise configs with 'name' and 'duration' keys
            rounds: Number of circuit rounds
            rest_between_exercises: Rest time between exercises (seconds)
            rest_between_rounds: Rest time between rounds (seconds)
            prepare_seconds: Preparation time before starting
        """
        super().__init__()
        self.exercises = exercises
        self.rounds = rounds
        self.rest_between_exercises = rest_between_exercises
        self.rest_between_rounds = rest_between_rounds
        self.prepare_seconds = prepare_seconds
        self._current_exercise_idx: int = 0
        self._work_time: int = 0
        self._rest_time: int = 0
    
    @property
    def total_duration(self) -> int:
        """Calculate total workout duration."""
        exercise_time = sum(e.get('duration', 30) for e in self.exercises)
        total_exercise_time = exercise_time * self.rounds
        total_rest = (
            self.rest_between_exercises * (len(self.exercises) - 1) * self.rounds +
            self.rest_between_rounds * (self.rounds - 1)
        )
        return self.prepare_seconds + total_exercise_time + total_rest
    
    def run(self, blocking: bool = True) -> Optional[WorkoutResult]:
        """Start the circuit timer."""
        if self.state != TimerState.IDLE:
            raise RuntimeError("Timer already started. Call reset() first.")
        
        self.state = TimerState.RUNNING
        self._start_time = time.time()
        result = None
        
        try:
            # Prepare phase
            if self.prepare_seconds > 0:
                self._run_phase(PhaseType.PREPARE, self.prepare_seconds, 0, "Prepare")
            
            # Circuit rounds
            for round_num in range(1, self.rounds + 1):
                if self.state != TimerState.RUNNING:
                    break
                
                self._current_round = round_num
                
                # Exercises in this round
                for idx, exercise in enumerate(self.exercises):
                    if self.state != TimerState.RUNNING:
                        break
                    
                    self._current_exercise_idx = idx
                    exercise_name = exercise.get('name', f'Exercise {idx + 1}')
                    duration = exercise.get('duration', 30)
                    
                    # Work phase
                    self._run_phase(PhaseType.WORK, duration, round_num, exercise_name)
                    self._work_time += duration
                    
                    # Rest between exercises (not after last exercise of round)
                    if idx < len(self.exercises) - 1 and self.state == TimerState.RUNNING:
                        self._run_phase(
                            PhaseType.REST,
                            self.rest_between_exercises,
                            round_num,
                            "Rest"
                        )
                        self._rest_time += self.rest_between_exercises
                
                # Rest between rounds (not after last round)
                if round_num < self.rounds and self.state == TimerState.RUNNING:
                    self._run_phase(
                        PhaseType.REST,
                        self.rest_between_rounds,
                        round_num,
                        "Round Rest"
                    )
                    self._rest_time += self.rest_between_rounds
            
            if self.state == TimerState.RUNNING:
                self.state = TimerState.COMPLETED
                result = self._create_result()
                self._emit_complete(result)
        
        except Exception as e:
            self.state = TimerState.IDLE
            raise e
        
        return result if blocking else None
    
    def _run_phase(
        self,
        phase_type: PhaseType,
        duration: int,
        round_num: int,
        phase_name: str
    ) -> None:
        """Run a single phase."""
        self._current_phase = phase_type
        
        event = TimerEvent(
            phase=phase_type,
            phase_name=phase_name,
            remaining_seconds=duration,
            total_seconds=duration,
            current_round=round_num,
            total_rounds=self.rounds,
            elapsed_seconds=int(time.time() - self._start_time),
            state=self.state
        )
        self._emit_phase_change(event)
        
        for remaining in range(duration, 0, -1):
            if self.state != TimerState.RUNNING:
                break
            
            while self.state == TimerState.PAUSED:
                time.sleep(0.1)
            
            if self.state != TimerState.RUNNING:
                break
            
            event = TimerEvent(
                phase=phase_type,
                phase_name=phase_name,
                remaining_seconds=remaining,
                total_seconds=duration,
                current_round=round_num,
                total_rounds=self.rounds,
                elapsed_seconds=int(time.time() - self._start_time),
                state=self.state
            )
            self._emit_tick(event)
            
            if remaining > 1:
                time.sleep(1)
    
    def _create_result(self) -> WorkoutResult:
        """Create workout result."""
        end_time = datetime.now()
        start_time = datetime.fromtimestamp(self._start_time)
        
        return WorkoutResult(
            workout_type="Circuit",
            total_duration_seconds=int(time.time() - self._start_time),
            rounds_completed=self._current_round,
            work_time_seconds=self._work_time,
            rest_time_seconds=self._rest_time,
            start_time=start_time,
            end_time=end_time,
            phases=[{
                "exercises": [e.get('name', f'Exercise {i+1}') 
                              for i, e in enumerate(self.exercises)]
            }]
        )


class CountdownTimer(BaseTimer):
    """Simple countdown timer with customizable duration."""
    
    def __init__(self, duration_seconds: int, name: str = "Countdown"):
        super().__init__()
        self.duration_seconds = duration_seconds
        self.name = name
    
    @property
    def total_duration(self) -> int:
        return self.duration_seconds
    
    def run(self, blocking: bool = True) -> Optional[WorkoutResult]:
        """Start the countdown timer."""
        if self.state != TimerState.IDLE:
            raise RuntimeError("Timer already started. Call reset() first.")
        
        self.state = TimerState.RUNNING
        self._start_time = time.time()
        result = None
        
        try:
            event = TimerEvent(
                phase=PhaseType.WORK,
                phase_name=self.name,
                remaining_seconds=self.duration_seconds,
                total_seconds=self.duration_seconds,
                current_round=1,
                total_rounds=1,
                elapsed_seconds=0,
                state=self.state
            )
            self._emit_phase_change(event)
            
            for remaining in range(self.duration_seconds, 0, -1):
                if self.state != TimerState.RUNNING:
                    break
                
                while self.state == TimerState.PAUSED:
                    time.sleep(0.1)
                
                if self.state != TimerState.RUNNING:
                    break
                
                event = TimerEvent(
                    phase=PhaseType.WORK,
                    phase_name=self.name,
                    remaining_seconds=remaining,
                    total_seconds=self.duration_seconds,
                    current_round=1,
                    total_rounds=1,
                    elapsed_seconds=self.duration_seconds - remaining,
                    state=self.state
                )
                self._emit_tick(event)
                
                if remaining > 1:
                    time.sleep(1)
            
            if self.state == TimerState.RUNNING:
                self.state = TimerState.COMPLETED
                result = self._create_result()
                self._emit_complete(result)
        
        except Exception as e:
            self.state = TimerState.IDLE
            raise e
        
        return result if blocking else None
    
    def _create_result(self) -> WorkoutResult:
        """Create workout result."""
        end_time = datetime.now()
        start_time = datetime.fromtimestamp(self._start_time)
        
        return WorkoutResult(
            workout_type="Countdown",
            total_duration_seconds=self.duration_seconds,
            rounds_completed=1,
            work_time_seconds=self.duration_seconds,
            rest_time_seconds=0,
            start_time=start_time,
            end_time=end_time
        )


class Stopwatch(BaseTimer):
    """Stopwatch with lap tracking."""
    
    def __init__(self):
        super().__init__()
        self._laps: List[Dict[str, Any]] = []
        self._last_lap_time: float = 0
    
    @property
    def elapsed_seconds(self) -> int:
        """Get elapsed seconds."""
        if self._start_time is None:
            return 0
        return int(time.time() - self._start_time)
    
    @property
    def laps(self) -> List[Dict[str, Any]]:
        """Get lap times."""
        return self._laps.copy()
    
    def lap(self, name: Optional[str] = None) -> Dict[str, Any]:
        """Record a lap time."""
        if self.state != TimerState.RUNNING:
            raise RuntimeError("Stopwatch not running")
        
        current_time = time.time()
        lap_time = current_time - self._last_lap_time
        total_time = current_time - self._start_time
        
        lap_data = {
            "lap_number": len(self._laps) + 1,
            "lap_time": round(lap_time, 3),
            "total_time": round(total_time, 3),
            "name": name or f"Lap {len(self._laps) + 1}"
        }
        
        self._laps.append(lap_data)
        self._last_lap_time = current_time
        
        return lap_data
    
    def run(self, blocking: bool = True) -> Optional[WorkoutResult]:
        """Start the stopwatch."""
        if self.state != TimerState.IDLE:
            raise RuntimeError("Stopwatch already started. Call reset() first.")
        
        self.state = TimerState.RUNNING
        self._start_time = time.time()
        self._last_lap_time = self._start_time
        
        if blocking:
            # For non-blocking use, start and return
            return None
        
        return None
    
    def stop(self) -> WorkoutResult:
        """Stop the stopwatch and get result."""
        if self.state != TimerState.RUNNING:
            raise RuntimeError("Stopwatch not running")
        
        self.state = TimerState.COMPLETED
        end_time = datetime.now()
        start_time = datetime.fromtimestamp(self._start_time)
        
        result = WorkoutResult(
            workout_type="Stopwatch",
            total_duration_seconds=self.elapsed_seconds,
            rounds_completed=len(self._laps),
            work_time_seconds=self.elapsed_seconds,
            rest_time_seconds=0,
            start_time=start_time,
            end_time=end_time,
            phases=self._laps
        )
        
        self._emit_complete(result)
        return result


# Utility functions
def format_time(seconds: int) -> str:
    """Format seconds to MM:SS or HH:MM:SS string."""
    if seconds < 0:
        return "00:00"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def parse_time(time_str: str) -> int:
    """Parse time string (MM:SS or HH:MM:SS) to seconds."""
    parts = time_str.split(':')
    
    if len(parts) == 2:
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    elif len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError(f"Invalid time format: {time_str}")


def create_interval_timer(
    work_seconds: int,
    rest_seconds: int,
    rounds: int,
    timer_type: str = "hiit"
) -> BaseTimer:
    """
    Factory function to create interval timers.
    
    Args:
        work_seconds: Work interval duration
        rest_seconds: Rest interval duration
        rounds: Number of rounds
        timer_type: Type of timer ("hiit", "tabata")
    
    Returns:
        Configured timer instance
    """
    timer_type = timer_type.lower()
    
    if timer_type == "tabata":
        return TabataTimer(rounds=rounds)
    elif timer_type == "hiit":
        return HIITTimer(
            work_seconds=work_seconds,
            rest_seconds=rest_seconds,
            rounds=rounds
        )
    else:
        raise ValueError(f"Unknown timer type: {timer_type}")


def calculate_calories_burned(
    duration_minutes: float,
    met_value: float,
    weight_kg: float
) -> float:
    """
    Estimate calories burned during exercise.
    
    Args:
        duration_minutes: Exercise duration in minutes
        met_value: Metabolic Equivalent of Task (MET) value
        weight_kg: Body weight in kilograms
    
    Returns:
        Estimated calories burned
    """
    # Formula: Calories = MET × Weight (kg) × Duration (hours)
    duration_hours = duration_minutes / 60
    return met_value * weight_kg * duration_hours


# MET values for common exercises
MET_VALUES = {
    "resting": 1.0,
    "walking": 3.5,
    "light_calisthenics": 3.5,
    "moderate_calisthenics": 5.0,
    "vigorous_calisthenics": 8.0,
    "running_5mph": 8.3,
    "running_6mph": 9.8,
    "running_7mph": 11.0,
    "running_8mph": 11.8,
    "cycling_moderate": 5.0,
    "cycling_vigorous": 7.5,
    "swimming_moderate": 6.0,
    "swimming_vigorous": 10.0,
    "jump_rope": 12.0,
    "burpees": 8.0,
    "pushups": 3.8,
    "pullups": 4.8,
    "squats": 5.0,
    "lunges": 4.0,
    "plank": 3.0,
    "mountain_climbers": 8.0,
    "hiit": 8.0,
    "tabata": 10.0,
    "yoga": 2.5,
    "pilates": 3.0,
    "jumping_jacks": 8.0,
    "boxing_bag": 5.5,
    "boxing_sparring": 9.0,
    "crossfit": 8.0,
    "rowing_moderate": 4.8,
    "rowing_vigorous": 7.0,
    "stair_climbing": 9.0,
    "kettlebell": 6.0,
    "battle_ropes": 8.5,
}


def get_met_value(exercise: str) -> float:
    """Get MET value for an exercise."""
    exercise_lower = exercise.lower().replace(" ", "_")
    return MET_VALUES.get(exercise_lower, 5.0)  # Default to moderate exercise