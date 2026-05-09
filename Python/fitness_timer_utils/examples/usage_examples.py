"""
Fitness Timer Utilities - Usage Examples

This file demonstrates various ways to use the fitness timer module.
"""

import time
from mod import (
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
)


def basic_hiit_timer():
    """Example: Basic HIIT timer with callbacks."""
    print("\n" + "="*50)
    print("BASIC HIIT TIMER")
    print("="*50)
    
    # Create a 30/15 HIIT timer with 4 rounds
    timer = HIITTimer(
        work_seconds=30,
        rest_seconds=15,
        rounds=4,
        prepare_seconds=5
    )
    
    def on_phase_change(event):
        print(f"\n>>> Phase: {event.phase_name}")
        print(f"    Round: {event.current_round}/{event.total_rounds}")
    
    def on_tick(event):
        # Show countdown for last 5 seconds
        if event.remaining_seconds <= 5:
            print(f"    {event.phase_name}: {event.remaining_seconds}s")
    
    def on_complete(result):
        print(f"\n✅ Workout Complete!")
        print(f"   Type: {result.workout_type}")
        print(f"   Duration: {format_time(result.total_duration_seconds)}")
        print(f"   Rounds: {result.rounds_completed}")
        print(f"   Work time: {format_time(result.work_time_seconds)}")
        print(f"   Rest time: {format_time(result.rest_time_seconds)}")
    
    timer.on_phase_change(on_phase_change)
    timer.on_tick(on_tick)
    timer.on_complete(on_complete)
    
    print(f"\nTotal duration: {format_time(timer.total_duration)}")
    print("\nStarting HIIT workout...")
    
    # Run the timer (blocking)
    result = timer.run(blocking=True)
    
    return result


def quick_tabata():
    """Example: Quick Tabata workout (standard 20/10 x 8)."""
    print("\n" + "="*50)
    print("TABATA TIMER")
    print("="*50)
    
    # Standard Tabata: 20s work, 10s rest, 8 rounds
    timer = TabataTimer(rounds=8, prepare_seconds=10)
    
    def on_phase(event):
        if event.phase.value == "work":
            print(f"💪 WORK HARD! Round {event.current_round}/8")
        elif event.phase.value == "rest":
            print(f"😮‍💨 Rest... Round {event.current_round}/8")
        elif event.phase.value == "prepare":
            print(f"⏱️  Get ready! {event.remaining_seconds}s")
    
    def on_tick(event):
        if event.remaining_seconds in [5, 4, 3, 2, 1]:
            phase_emoji = "💪" if event.phase.value == "work" else "😮‍💨"
            print(f"   {phase_emoji} {event.remaining_seconds}s")
    
    timer.on_phase_change(on_phase).on_tick(on_tick)
    
    print(f"\nStandard Tabata Protocol")
    print(f"20s work / 10s rest x 8 rounds")
    print(f"Total: {format_time(timer.total_duration)}")
    print("\nStarting in...")
    
    result = timer.run(blocking=True)
    
    # Calculate estimated calories burned
    calories = calculate_calories_burned(
        duration_minutes=result.total_duration_minutes,
        met_value=get_met_value("tabata"),
        weight_kg=70
    )
    print(f"\n🔥 Estimated calories burned: {calories:.1f} kcal (for 70kg person)")
    
    return result


def emom_workout():
    """Example: EMOM (Every Minute on the Minute) workout."""
    print("\n" + "="*50)
    print("EMOM TIMER")
    print("="*50)
    
    # 10-minute EMOM with alternating exercises
    exercises = [
        "Burpees",
        "Pull-ups",
        "Push-ups",
        "Squats",
        "Box Jumps"
    ]
    
    timer = EMOMTimer(duration_minutes=10, exercises=exercises)
    
    def on_phase(event):
        exercise = event.metadata.get("exercise", "")
        if exercise:
            print(f"\n⏰ Minute {event.current_round}: {exercise}")
        else:
            print(f"\n⏰ Minute {event.current_round}")
    
    def on_tick(event):
        if event.remaining_seconds == 30:
            print("   🔔 Halfway point - push harder!")
        elif event.remaining_seconds <= 5:
            print(f"   ⏳ {event.remaining_seconds}s remaining")
    
    timer.on_phase_change(on_phase).on_tick(on_tick)
    
    print(f"\nExercises cycle: {', '.join(exercises)}")
    print(f"Duration: {timer.duration_minutes} minutes")
    print("\nStarting EMOM...")
    
    result = timer.run(blocking=True)
    
    print(f"\n✅ EMOM Complete! {result.rounds_completed} minutes")
    
    return result


def amrap_workout():
    """Example: AMRAP (As Many Rounds As Possible) workout."""
    print("\n" + "="*50)
    print("AMRAP TIMER")
    print("="*50)
    
    # 5-minute AMRAP
    timer = AMRAPTimer(duration_minutes=5)
    
    round_count = [0]
    last_tick = [0]
    
    def on_tick(event):
        # Prompt user to record rounds
        if event.elapsed_seconds > 0 and event.elapsed_seconds % 60 == 0 and last_tick[0] != event.elapsed_seconds:
            last_tick[0] = event.elapsed_seconds
            print(f"\n⏱️  {event.elapsed_seconds // 60} minute(s) elapsed")
            print(f"   Rounds completed so far: {round_count[0]}")
    
    timer.on_tick(on_tick)
    
    print(f"\nAMRAP Duration: {timer.duration_minutes} minutes")
    print("Complete as many rounds as possible!")
    print("The timer will track your total time.")
    print("\nStarting AMRAP...")
    
    # Start timer
    timer.run(blocking=False)
    
    # Simulate recording rounds (in real use, user would call timer.record_round())
    time.sleep(2)  # Simulate some work
    timer.record_round()
    print("   ✅ Round 1 recorded!")
    
    time.sleep(1)
    timer.record_round()
    print("   ✅ Round 2 recorded!")
    
    # Wait for timer to complete
    while timer.state.value == "running":
        time.sleep(0.5)
    
    result = timer.stop()
    
    print(f"\n✅ AMRAP Complete!")
    print(f"   Total rounds: {result.rounds_completed}")
    print(f"   Average round time: {result.phases[0].get('average_round_time', 0):.2f}s")
    
    return result


def circuit_training():
    """Example: Circuit training timer."""
    print("\n" + "="*50)
    print("CIRCUIT TIMER")
    print("="*50)
    
    # Define circuit exercises
    exercises = [
        {"name": "Push-ups", "duration": 45},
        {"name": "Squats", "duration": 45},
        {"name": "Mountain Climbers", "duration": 30},
        {"name": "Plank", "duration": 30},
        {"name": "Burpees", "duration": 30},
    ]
    
    timer = CircuitTimer(
        exercises=exercises,
        rounds=3,
        rest_between_exercises=15,
        rest_between_rounds=60,
        prepare_seconds=10
    )
    
    def on_phase(event):
        if event.phase.value == "work":
            print(f"\n💪 {event.phase_name} - GO!")
        elif event.phase.value == "rest":
            if "Round Rest" in event.phase_name:
                print(f"\n☕ Round {event.current_round} complete! Rest 60s")
            else:
                print(f"\n😮‍💨 Rest {timer.rest_between_exercises}s")
        elif event.phase.value == "prepare":
            print(f"\n⏱️  Prepare: {event.remaining_seconds}s")
    
    def on_tick(event):
        # Show countdown for last 5 seconds of each phase
        if event.remaining_seconds <= 5 and event.remaining_seconds > 0:
            if event.phase.value == "work":
                print(f"   ⚡ {event.phase_name}: {event.remaining_seconds}s")
            elif event.phase.value == "rest":
                print(f"   ⏳ {event.remaining_seconds}s")
    
    timer.on_phase_change(on_phase).on_tick(on_tick)
    
    print(f"\nCircuit: {len(exercises)} exercises x {timer.rounds} rounds")
    print(f"Total duration: {format_time(timer.total_duration)}")
    print(f"\nExercises:")
    for i, ex in enumerate(exercises, 1):
        print(f"   {i}. {ex['name']} ({ex['duration']}s)")
    
    print("\nStarting circuit...")
    
    result = timer.run(blocking=True)
    
    print(f"\n✅ Circuit Complete!")
    print(f"   Total time: {format_time(result.total_duration_seconds)}")
    print(f"   Work time: {format_time(result.work_time_seconds)}")
    print(f"   Rest time: {format_time(result.rest_time_seconds)}")
    
    return result


def countdown_timer_example():
    """Example: Simple countdown timer."""
    print("\n" + "="*50)
    print("COUNTDOWN TIMER")
    print("="*50)
    
    # 5-minute plank timer
    timer = CountdownTimer(duration_seconds=300, name="Plank Challenge")
    
    def on_tick(event):
        remaining = event.remaining_seconds
        # Show time at intervals
        if remaining == 300:
            print("💪 Plank started! Hold it!")
        elif remaining == 180:
            print("💪 3 minutes down, 2 to go!")
        elif remaining == 60:
            print("💪 Last minute!")
        elif remaining <= 10:
            print(f"💪 {remaining}!")
    
    def on_complete(result):
        print("\n🎉 Congratulations! You held the plank for 5 minutes!")
    
    timer.on_tick(on_tick).on_complete(on_complete)
    
    print(f"\n{timer.name}: {format_time(timer.duration_seconds)}")
    print("\nStarting...")
    
    result = timer.run(blocking=True)
    
    return result


def stopwatch_example():
    """Example: Stopwatch with lap tracking."""
    print("\n" + "="*50)
    print("STOPWATCH")
    print("="*50)
    
    stopwatch = Stopwatch()
    
    print("\nStarting stopwatch...")
    stopwatch.run(blocking=False)
    
    # Simulate recording laps
    time.sleep(1)
    lap1 = stopwatch.lap("First 100m")
    print(f"   Lap 1 ({lap1['name']}): {lap1['lap_time']:.3f}s")
    
    time.sleep(1)
    lap2 = stopwatch.lap("Second 100m")
    print(f"   Lap 2 ({lap2['name']}): {lap2['lap_time']:.3f}s")
    
    time.sleep(1)
    lap3 = stopwatch.lap("Third 100m")
    print(f"   Lap 3 ({lap3['name']}): {lap3['lap_time']:.3f}s")
    
    time.sleep(1)
    result = stopwatch.stop()
    
    print(f"\n✅ Stopwatch stopped!")
    print(f"   Total time: {format_time(result.total_duration_seconds)}")
    print(f"   Laps recorded: {result.rounds_completed}")
    
    print("\n   Lap times:")
    for lap in stopwatch.laps:
        print(f"   - {lap['name']}: {lap['lap_time']:.3f}s (total: {lap['total_time']:.3f}s)")
    
    return result


def calorie_estimation():
    """Example: Calculate calories burned for different exercises."""
    print("\n" + "="*50)
    print("CALORIE ESTIMATION")
    print("="*50)
    
    weight_kg = 70
    
    exercises = [
        ("HIIT Workout", 30, "hiit"),
        ("Tabata Session", 20, "tabata"),
        ("Running 6mph", 30, "running_6mph"),
        ("Jump Rope", 15, "jump_rope"),
        ("Swimming (Vigorous)", 45, "swimming_vigorous"),
        ("Yoga", 60, "yoga"),
        ("Weight Training", 45, "vigorous_calisthenics"),
    ]
    
    print(f"\nCalories burned for {weight_kg}kg person:\n")
    print(f"{'Exercise':<25} {'Duration':<12} {'MET':<6} {'Calories'}")
    print("-" * 55)
    
    for name, duration, exercise_key in exercises:
        met = get_met_value(exercise_key)
        calories = calculate_calories_burned(duration, met, weight_kg)
        print(f"{name:<25} {duration}min{'':<6} {met:<6.1f} {calories:.0f} kcal")


def timer_factory_example():
    """Example: Using the timer factory function."""
    print("\n" + "="*50)
    print("TIMER FACTORY")
    print("="*50)
    
    # Create HIIT timer
    hiit = create_interval_timer(
        work_seconds=40,
        rest_seconds=20,
        rounds=6,
        timer_type="hiit"
    )
    print(f"\nCreated HIIT timer: {hiit.work_seconds}s work / {hiit.rest_seconds}s rest x {hiit.rounds}")
    
    # Create Tabata timer
    tabata = create_interval_timer(
        work_seconds=20,
        rest_seconds=10,
        rounds=4,
        timer_type="tabata"
    )
    print(f"Created Tabata timer: {tabata.rounds} rounds")


def pause_resume_example():
    """Example: Pause and resume functionality."""
    print("\n" + "="*50)
    print("PAUSE & RESUME")
    print("="*50)
    
    timer = HIITTimer(work_seconds=3, rest_seconds=2, rounds=1, prepare_seconds=2)
    
    paused = [False]
    
    def on_tick(event):
        if event.remaining_seconds == 2 and event.phase.value == "work" and not paused[0]:
            print(f"\n⏸️  Pausing at {event.remaining_seconds}s remaining...")
            timer.pause()
            paused[0] = True
            # Resume after 2 seconds
            time.sleep(2)
            print("▶️  Resuming...")
            timer.resume()
    
    timer.on_tick(on_tick)
    
    print("\nTimer will pause during work phase...")
    result = timer.run(blocking=True)
    
    print("\n✅ Timer completed with pause/resume demo!")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("FITNESS TIMER UTILITIES - USAGE EXAMPLES")
    print("="*60)
    
    print("\n⚠️  Note: These examples use very short durations for demonstration.")
    print("    Adjust durations for real workouts!\n")
    
    # Quick examples (uncomment to run full versions)
    
    # 1. Basic HIIT (shortened for demo)
    print("\n1. Running quick HIIT demo (3s work / 2s rest x 2 rounds)...")
    quick_timer = HIITTimer(work_seconds=3, rest_seconds=2, rounds=2, prepare_seconds=2)
    
    def on_phase(event):
        print(f"  Phase: {event.phase_name} (Round {event.current_round}/{event.total_rounds})")
    
    quick_timer.on_phase_change(on_phase)
    quick_timer.run(blocking=True)
    
    # 2. Show calorie estimation
    calorie_estimation()
    
    # 3. Time formatting utilities
    print("\n" + "="*50)
    print("TIME FORMATTING UTILITIES")
    print("="*50)
    
    print(f"\nformat_time(90) = {format_time(90)}")
    print(f"format_time(3661) = {format_time(3661)}")
    print(f"parse_time('05:30') = {parse_time('05:30')} seconds")
    print(f"parse_time('01:30:00') = {parse_time('01:30:00')} seconds")
    
    print("\n" + "="*60)
    print("Demo complete! See individual example functions for full usage.")
    print("="*60 + "\n")
    
    # Full examples (commented out - run individually as needed)
    # basic_hiit_timer()
    # quick_tabata()
    # emom_workout()
    # amrap_workout()
    # circuit_training()
    # countdown_timer_example()
    # stopwatch_example()
    # pause_resume_example()


if __name__ == "__main__":
    main()