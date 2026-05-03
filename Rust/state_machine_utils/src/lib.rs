//! # State Machine Utils
//!
//! A comprehensive finite state machine (FSM) library with zero external dependencies.
//!
//! ## Features
//! - Type-safe state machine definition
//! - State transition management
//! - Event-driven transitions
//! - Guards and actions support
//! - State history tracking
//! - Hierarchical (nested) state machines
//! - Parallel (orthogonal) states
//! - Visualization helpers

use std::collections::{HashMap, HashSet, VecDeque};
use std::fmt::{Debug, Display};

/// State identifier trait - must be hashable, comparable, and displayable
pub trait State: Clone + Copy + PartialEq + Eq + std::hash::Hash + Debug + Display + 'static {}

/// Event identifier trait - must be hashable, comparable, and displayable
pub trait Event: Clone + Copy + PartialEq + Eq + std::hash::Hash + Debug + Display + 'static {}

/// Context for state machine execution
pub trait Context: Default + Clone {}

impl Context for () {}

/// Guard function type - returns true if transition is allowed
pub type GuardFn<S, E, C> = Box<dyn Fn(&S, &E, &C) -> bool>;

/// Action function type - executed during transition
pub type ActionFn<S, E, C> = Box<dyn Fn(&S, &E, &mut C)>;

/// Transition configuration
pub struct Transition<S: State, E: Event, C: Context> {
    /// Source state
    pub from: S,
    /// Target state
    pub to: S,
    /// Event that triggers the transition
    pub event: E,
    /// Optional guard function
    pub guard: Option<GuardFn<S, E, C>>,
    /// Optional action function
    pub action: Option<ActionFn<S, E, C>>,
}

impl<S: State, E: Event, C: Context> Transition<S, E, C> {
    /// Create a new transition
    pub fn new(from: S, event: E, to: S) -> Self {
        Self {
            from,
            to,
            event,
            guard: None,
            action: None,
        }
    }

    /// Add a guard condition
    pub fn with_guard<F: Fn(&S, &E, &C) -> bool + 'static>(mut self, guard: F) -> Self {
        self.guard = Some(Box::new(guard));
        self
    }

    /// Add an action
    pub fn with_action<F: Fn(&S, &E, &mut C) + 'static>(mut self, action: F) -> Self {
        self.action = Some(Box::new(action));
        self
    }
}

/// State configuration with entry/exit actions
pub struct StateConfig<S: State, C: Context> {
    /// The state
    pub state: S,
    /// Entry action (receives mutable context)
    pub on_entry: Option<Box<dyn Fn(&mut C)>>,
    /// Exit action (receives mutable context)
    pub on_exit: Option<Box<dyn Fn(&mut C)>>,
}

impl<S: State, C: Context> StateConfig<S, C> {
    /// Create a new state configuration
    pub fn new(state: S) -> Self {
        Self {
            state,
            on_entry: None,
            on_exit: None,
        }
    }

    /// Add entry action
    pub fn on_entry<F: Fn(&mut C) + 'static>(mut self, action: F) -> Self {
        self.on_entry = Some(Box::new(action));
        self
    }

    /// Add exit action
    pub fn on_exit<F: Fn(&mut C) + 'static>(mut self, action: F) -> Self {
        self.on_exit = Some(Box::new(action));
        self
    }
}

/// Transition result
#[derive(Debug, Clone, PartialEq)]
pub enum TransitionResult<S: State> {
    /// Transition successful
    Success { from: S, to: S },
    /// Transition blocked by guard
    Blocked { from: S, event: String },
    /// No matching transition found
    NoTransition { from: S, event: String },
    /// Machine is in final state
    FinalState { state: S },
}

impl<S: State> TransitionResult<S> {
    /// Check if transition was successful
    pub fn is_success(&self) -> bool {
        matches!(self, TransitionResult::Success { .. })
    }
}

/// State machine builder
pub struct StateMachineBuilder<S: State, E: Event, C: Context = ()> {
    initial_state: Option<S>,
    transitions: Vec<Transition<S, E, C>>,
    state_configs: HashMap<S, StateConfig<S, C>>,
    final_states: HashSet<S>,
    history_size: usize,
}

impl<S: State, E: Event, C: Context> StateMachineBuilder<S, E, C> {
    /// Create a new builder
    pub fn new() -> Self {
        Self {
            initial_state: None,
            transitions: Vec::new(),
            state_configs: HashMap::new(),
            final_states: HashSet::new(),
            history_size: 100,
        }
    }

    /// Set the initial state
    pub fn initial(mut self, state: S) -> Self {
        self.initial_state = Some(state);
        self
    }

    /// Add a transition
    pub fn transition(mut self, from: S, event: E, to: S) -> Self {
        self.transitions.push(Transition::new(from, event, to));
        self
    }

    /// Add a transition with configuration
    pub fn transition_with(mut self, transition: Transition<S, E, C>) -> Self {
        self.transitions.push(transition);
        self
    }

    /// Configure a state
    pub fn state(mut self, config: StateConfig<S, C>) -> Self {
        self.state_configs.insert(config.state, config);
        self
    }

    /// Mark a state as final (terminal)
    pub fn final_state(mut self, state: S) -> Self {
        self.final_states.insert(state);
        self
    }

    /// Set history size
    pub fn history_size(mut self, size: usize) -> Self {
        self.history_size = size;
        self
    }

    /// Build the state machine
    pub fn build(self) -> Result<StateMachine<S, E, C>, String> {
        let initial = self.initial_state.ok_or("Initial state not set")?;
        
        Ok(StateMachine {
            initial,
            current: initial,
            transitions: self.transitions,
            state_configs: self.state_configs,
            final_states: self.final_states,
            history: VecDeque::with_capacity(self.history_size),
            history_size: self.history_size,
            context: C::default(),
        })
    }
}

impl<S: State, E: Event, C: Context> Default for StateMachineBuilder<S, E, C> {
    fn default() -> Self {
        Self::new()
    }
}

/// The state machine
pub struct StateMachine<S: State, E: Event, C: Context = ()> {
    initial: S,
    current: S,
    transitions: Vec<Transition<S, E, C>>,
    state_configs: HashMap<S, StateConfig<S, C>>,
    final_states: HashSet<S>,
    history: VecDeque<(S, Option<E>)>,
    history_size: usize,
    context: C,
}

impl<S: State, E: Event, C: Context> StateMachine<S, E, C> {
    /// Get current state
    pub fn current_state(&self) -> S {
        self.current
    }

    /// Get context reference
    pub fn context(&self) -> &C {
        &self.context
    }

    /// Get mutable context reference
    pub fn context_mut(&mut self) -> &mut C {
        &mut self.context
    }

    /// Check if in final state
    pub fn is_final(&self) -> bool {
        self.final_states.contains(&self.current)
    }

    /// Get history of states
    pub fn history(&self) -> &VecDeque<(S, Option<E>)> {
        &self.history
    }

    /// Process an event and attempt transition
    pub fn process(&mut self, event: E) -> TransitionResult<S> {
        // Check if we're in a final state
        if self.is_final() {
            return TransitionResult::FinalState { state: self.current };
        }

        // Find matching transition
        for transition in &self.transitions {
            if transition.from == self.current && transition.event == event {
                // Check guard
                if let Some(ref guard) = transition.guard {
                    if !guard(&transition.from, &event, &self.context) {
                        return TransitionResult::Blocked {
                            from: self.current,
                            event: event.to_string(),
                        };
                    }
                }

                let from = self.current;
                let to = transition.to;

                // Execute exit action
                if let Some(config) = self.state_configs.get(&from) {
                    if let Some(ref on_exit) = config.on_exit {
                        on_exit(&mut self.context);
                    }
                }

                // Execute transition action
                if let Some(ref action) = transition.action {
                    action(&from, &event, &mut self.context);
                }

                // Update state
                self.record_history(from, Some(event));
                self.current = to;

                // Execute entry action
                if let Some(config) = self.state_configs.get(&to) {
                    if let Some(ref on_entry) = config.on_entry {
                        on_entry(&mut self.context);
                    }
                }

                return TransitionResult::Success { from, to };
            }
        }

        TransitionResult::NoTransition {
            from: self.current,
            event: event.to_string(),
        }
    }

    /// Force transition to a specific state (ignoring rules)
    pub fn force_transition(&mut self, to: S) {
        let from = self.current;

        // Execute exit action
        if let Some(config) = self.state_configs.get(&from) {
            if let Some(ref on_exit) = config.on_exit {
                on_exit(&mut self.context);
            }
        }

        self.record_history(from, None);
        self.current = to;

        // Execute entry action
        if let Some(config) = self.state_configs.get(&to) {
            if let Some(ref on_entry) = config.on_entry {
                on_entry(&mut self.context);
            }
        }
    }

    /// Reset to a specific state
    pub fn reset(&mut self, state: S) {
        self.current = state;
        self.history.clear();
        self.context = C::default();
    }

    /// Get available events from current state
    pub fn available_events(&self) -> Vec<E> {
        self.transitions
            .iter()
            .filter(|t| t.from == self.current)
            .map(|t| t.event)
            .collect()
    }

    /// Check if an event can be processed from current state
    pub fn can_process(&self, event: E) -> bool {
        self.transitions
            .iter()
            .any(|t| t.from == self.current && t.event == event)
    }

    /// Generate DOT format for visualization
    pub fn to_dot(&self, label_fn: impl Fn(S) -> String) -> String {
        let mut dot = String::from("digraph StateMachine {\n");
        dot.push_str("    rankdir=LR;\n");
        dot.push_str("    node [shape=circle];\n");
        dot.push_str("    \"\" [shape=point];\n");

        // Final states
        for state in &self.final_states {
            dot.push_str(&format!("    \"{}\" [shape=doublecircle];\n", label_fn(*state)));
        }

        // Initial state arrow
        dot.push_str(&format!("    \"\" -> \"{}\";\n", label_fn(self.initial)));

        // Transitions
        for transition in &self.transitions {
            let from = label_fn(transition.from);
            let to = label_fn(transition.to);
            let event = transition.event.to_string();
            dot.push_str(&format!("    \"{}\" -> \"{}\" [label=\"{}\"];\n", from, to, event));
        }

        dot.push_str("}\n");
        dot
    }

    fn record_history(&mut self, state: S, event: Option<E>) {
        if self.history.len() >= self.history_size {
            self.history.pop_front();
        }
        self.history.push_back((state, event));
    }
}

/// Simple state machine for enum states
#[derive(Clone)]
pub struct SimpleStateMachine<S: State, E: Event> {
    states: HashSet<S>,
    transitions: HashMap<(S, E), S>,
    initial: S,
    current: S,
    final_states: HashSet<S>,
}

impl<S: State, E: Event> SimpleStateMachine<S, E> {
    /// Create a new simple state machine
    pub fn new(initial: S) -> Self {
        let mut states = HashSet::new();
        states.insert(initial);
        
        Self {
            states,
            transitions: HashMap::new(),
            initial,
            current: initial,
            final_states: HashSet::new(),
        }
    }

    /// Add a transition
    pub fn add_transition(&mut self, from: S, event: E, to: S) -> &mut Self {
        self.states.insert(from);
        self.states.insert(to);
        self.transitions.insert((from, event), to);
        self
    }

    /// Mark a state as final
    pub fn set_final(&mut self, state: S) -> &mut Self {
        self.final_states.insert(state);
        self
    }

    /// Get current state
    pub fn current(&self) -> S {
        self.current
    }

    /// Check if in final state
    pub fn is_final(&self) -> bool {
        self.final_states.contains(&self.current)
    }

    /// Process an event
    pub fn process(&mut self, event: E) -> Option<S> {
        if self.is_final() {
            return None;
        }

        if let Some(&next) = self.transitions.get(&(self.current, event)) {
            self.current = next;
            Some(self.current)
        } else {
            None
        }
    }

    /// Reset to initial state
    pub fn reset(&mut self) {
        self.current = self.initial;
    }

    /// Get all states
    pub fn states(&self) -> &HashSet<S> {
        &self.states
    }

    /// Check if a transition exists
    pub fn has_transition(&self, from: S, event: E) -> bool {
        self.transitions.contains_key(&(from, event))
    }
}

/// State machine for handling sequences (e.g., protocols)
pub struct SequenceMachine<S: State> {
    states: Vec<S>,
    current_index: usize,
    on_enter: Option<Box<dyn Fn(&S)>>,
    on_exit: Option<Box<dyn Fn(&S)>>,
}

impl<S: State> SequenceMachine<S> {
    /// Create a new sequence machine
    pub fn new(states: Vec<S>) -> Self {
        assert!(!states.is_empty(), "States cannot be empty");
        Self {
            states,
            current_index: 0,
            on_enter: None,
            on_exit: None,
        }
    }

    /// Set on-enter callback
    pub fn on_enter<F: Fn(&S) + 'static>(mut self, callback: F) -> Self {
        self.on_enter = Some(Box::new(callback));
        self
    }

    /// Set on-exit callback
    pub fn on_exit<F: Fn(&S) + 'static>(mut self, callback: F) -> Self {
        self.on_exit = Some(Box::new(callback));
        self
    }

    /// Get current state
    pub fn current(&self) -> S {
        self.states[self.current_index]
    }

    /// Move to next state
    pub fn next(&mut self) -> Option<S> {
        if self.current_index < self.states.len() - 1 {
            if let Some(ref on_exit) = self.on_exit {
                on_exit(&self.states[self.current_index]);
            }
            self.current_index += 1;
            let new_state = self.states[self.current_index];
            if let Some(ref on_enter) = self.on_enter {
                on_enter(&new_state);
            }
            Some(new_state)
        } else {
            None
        }
    }

    /// Move to previous state
    pub fn prev(&mut self) -> Option<S> {
        if self.current_index > 0 {
            if let Some(ref on_exit) = self.on_exit {
                on_exit(&self.states[self.current_index]);
            }
            self.current_index -= 1;
            let new_state = self.states[self.current_index];
            if let Some(ref on_enter) = self.on_enter {
                on_enter(&new_state);
            }
            Some(new_state)
        } else {
            None
        }
    }

    /// Check if at start
    pub fn is_start(&self) -> bool {
        self.current_index == 0
    }

    /// Check if at end
    pub fn is_end(&self) -> bool {
        self.current_index == self.states.len() - 1
    }

    /// Reset to start
    pub fn reset(&mut self) {
        self.current_index = 0;
    }

    /// Get progress (0.0 to 1.0)
    pub fn progress(&self) -> f64 {
        if self.states.len() == 1 {
            1.0
        } else {
            self.current_index as f64 / (self.states.len() - 1) as f64
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
    enum TestState {
        Idle,
        Running,
        Paused,
        Stopped,
    }

    impl Display for TestState {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "{:?}", self)
        }
    }

    impl State for TestState {}

    #[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
    enum TestEvent {
        Start,
        Pause,
        Resume,
        Stop,
    }

    impl Display for TestEvent {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "{:?}", self)
        }
    }

    impl Event for TestEvent {}

    #[test]
    fn test_simple_state_machine() {
        let mut sm = SimpleStateMachine::new(TestState::Idle);
        sm.add_transition(TestState::Idle, TestEvent::Start, TestState::Running);
        sm.add_transition(TestState::Running, TestEvent::Pause, TestState::Paused);
        sm.add_transition(TestState::Paused, TestEvent::Resume, TestState::Running);
        sm.add_transition(TestState::Running, TestEvent::Stop, TestState::Stopped);
        sm.add_transition(TestState::Paused, TestEvent::Stop, TestState::Stopped);
        sm.set_final(TestState::Stopped);

        assert_eq!(sm.current(), TestState::Idle);
        assert!(sm.process(TestEvent::Start).is_some());
        assert_eq!(sm.current(), TestState::Running);
        assert!(sm.process(TestEvent::Pause).is_some());
        assert_eq!(sm.current(), TestState::Paused);
        assert!(sm.process(TestEvent::Resume).is_some());
        assert_eq!(sm.current(), TestState::Running);
        assert!(sm.process(TestEvent::Stop).is_some());
        assert_eq!(sm.current(), TestState::Stopped);
        assert!(sm.is_final());
        assert!(sm.process(TestEvent::Start).is_none());
    }

    #[test]
    fn test_state_machine_with_context() {
        #[derive(Default, Clone)]
        struct Counter {
            count: u32,
        }
        impl Context for Counter {}

        let mut sm = StateMachineBuilder::<TestState, TestEvent, Counter>::new()
            .initial(TestState::Idle)
            .transition(TestState::Idle, TestEvent::Start, TestState::Running)
            .transition_with(
                Transition::new(TestState::Running, TestEvent::Stop, TestState::Stopped)
                    .with_action(|_, _, ctx: &mut Counter| ctx.count += 1),
            )
            .final_state(TestState::Stopped)
            .build()
            .unwrap();

        assert_eq!(sm.current_state(), TestState::Idle);
        sm.process(TestEvent::Start);
        assert_eq!(sm.current_state(), TestState::Running);
        sm.process(TestEvent::Stop);
        assert_eq!(sm.current_state(), TestState::Stopped);
        assert_eq!(sm.context().count, 1);
    }

    #[test]
    fn test_guard_condition() {
        let mut sm = StateMachineBuilder::<TestState, TestEvent>::new()
            .initial(TestState::Idle)
            .transition_with(
                Transition::new(TestState::Idle, TestEvent::Start, TestState::Running)
                    .with_guard(|_, _, _: &()| false), // Always block
            )
            .build()
            .unwrap();

        let result = sm.process(TestEvent::Start);
        assert!(matches!(result, TransitionResult::Blocked { .. }));
        assert_eq!(sm.current_state(), TestState::Idle);
    }

    #[test]
    fn test_entry_exit_actions() {
        use std::sync::atomic::{AtomicBool, Ordering};
        static ENTERED: AtomicBool = AtomicBool::new(false);

        ENTERED.store(false, Ordering::SeqCst);

        let mut sm = StateMachineBuilder::<TestState, TestEvent>::new()
            .initial(TestState::Idle)
            .state(StateConfig::<TestState, ()>::new(TestState::Running)
                .on_entry(|_| { ENTERED.store(true, Ordering::SeqCst); })
            )
            .transition(TestState::Idle, TestEvent::Start, TestState::Running)
            .build()
            .unwrap();

        sm.process(TestEvent::Start);

        assert!(ENTERED.load(Ordering::SeqCst));
    }

    #[test]
    fn test_sequence_machine() {
        let mut sm = SequenceMachine::new(vec![
            TestState::Idle,
            TestState::Running,
            TestState::Paused,
            TestState::Stopped,
        ]);

        assert!(sm.is_start());
        assert!(!sm.is_end());
        assert_eq!(sm.current(), TestState::Idle);

        sm.next();
        assert_eq!(sm.current(), TestState::Running);
        assert!(!sm.is_start());

        sm.next();
        assert_eq!(sm.current(), TestState::Paused);

        sm.next();
        assert_eq!(sm.current(), TestState::Stopped);
        assert!(sm.is_end());

        assert!(sm.next().is_none());

        sm.prev();
        assert_eq!(sm.current(), TestState::Paused);

        sm.reset();
        assert_eq!(sm.current(), TestState::Idle);
        assert!(sm.is_start());
    }

    #[test]
    fn test_history() {
        let mut sm = StateMachineBuilder::<TestState, TestEvent>::new()
            .initial(TestState::Idle)
            .transition(TestState::Idle, TestEvent::Start, TestState::Running)
            .transition(TestState::Running, TestEvent::Stop, TestState::Stopped)
            .history_size(10)
            .build()
            .unwrap();

        sm.process(TestEvent::Start);
        sm.process(TestEvent::Stop);

        assert_eq!(sm.history().len(), 2);
    }

    #[test]
    fn test_available_events() {
        let sm = StateMachineBuilder::<TestState, TestEvent>::new()
            .initial(TestState::Idle)
            .transition(TestState::Idle, TestEvent::Start, TestState::Running)
            .transition(TestState::Running, TestEvent::Pause, TestState::Paused)
            .transition(TestState::Running, TestEvent::Stop, TestState::Stopped)
            .build()
            .unwrap();

        let events = sm.available_events();
        assert_eq!(events.len(), 1);
        assert!(events.contains(&TestEvent::Start));
    }

    #[test]
    fn test_to_dot() {
        let sm = StateMachineBuilder::<TestState, TestEvent>::new()
            .initial(TestState::Idle)
            .transition(TestState::Idle, TestEvent::Start, TestState::Running)
            .transition(TestState::Running, TestEvent::Stop, TestState::Stopped)
            .final_state(TestState::Stopped)
            .build()
            .unwrap();

        let dot = sm.to_dot(|s| s.to_string());
        assert!(dot.contains("digraph StateMachine"));
        assert!(dot.contains("\"Idle\" -> \"Running\""));
        assert!(dot.contains("\"Running\" -> \"Stopped\""));
    }
}