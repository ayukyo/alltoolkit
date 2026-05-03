//! # State Machine Utils - Usage Examples
//!
//! This example demonstrates various use cases for the state machine library.

use state_machine_utils::*;

// Example 1: Traffic Light Controller
#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
enum TrafficLight {
    Red,
    Yellow,
    Green,
}

impl std::fmt::Display for TrafficLight {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}

impl State for TrafficLight {}

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
enum TrafficEvent {
    Timer,
    Emergency,
}

impl std::fmt::Display for TrafficEvent {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}

impl Event for TrafficEvent {}

fn traffic_light_example() {
    println!("=== Traffic Light Controller ===\n");

    let mut traffic_light = SimpleStateMachine::new(TrafficLight::Red);

    // Define transitions: Red -> Green -> Yellow -> Red
    traffic_light
        .add_transition(TrafficLight::Red, TrafficEvent::Timer, TrafficLight::Green)
        .add_transition(TrafficLight::Green, TrafficEvent::Timer, TrafficLight::Yellow)
        .add_transition(TrafficLight::Yellow, TrafficEvent::Timer, TrafficLight::Red)
        .add_transition(TrafficLight::Red, TrafficEvent::Emergency, TrafficLight::Yellow);

    println!("Initial state: {:?}", traffic_light.current());

    // Simulate traffic light cycles
    for i in 1..=6 {
        let event = if i == 3 {
            println!("\nEmergency vehicle detected!");
            TrafficEvent::Emergency
        } else {
            TrafficEvent::Timer
        };

        if let Some(new_state) = traffic_light.process(event) {
            println!("Event: {:?} -> New state: {:?}", event, new_state);
        }
    }
}

// Example 2: Order Processing System
#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
enum OrderState {
    Created,
    Paid,
    Processing,
    Shipped,
    Delivered,
    Cancelled,
}

impl std::fmt::Display for OrderState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}

impl State for OrderState {}

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
enum OrderEvent {
    Pay,
    Process,
    Ship,
    Deliver,
    Cancel,
}

impl std::fmt::Display for OrderEvent {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}

impl Event for OrderEvent {}

#[derive(Default, Clone)]
struct OrderContext {
    tracking_number: String,
    total_amount: f64,
}

impl Context for OrderContext {}

fn order_processing_example() {
    println!("\n=== Order Processing System ===\n");

    let mut order = StateMachineBuilder::<OrderState, OrderEvent, OrderContext>::new()
        .initial(OrderState::Created)
        // Created -> Paid
        .transition_with(
            Transition::new(OrderState::Created, OrderEvent::Pay, OrderState::Paid)
                .with_action(|_, _, ctx: &mut OrderContext| {
                    ctx.total_amount = 99.99;
                    println!("  💳 Payment processed: ${}", ctx.total_amount);
                }),
        )
        // Paid -> Processing
        .transition(OrderState::Paid, OrderEvent::Process, OrderState::Processing)
        // Processing -> Shipped
        .transition_with(
            Transition::new(OrderState::Processing, OrderEvent::Ship, OrderState::Shipped)
                .with_action(|_, _, ctx: &mut OrderContext| {
                    ctx.tracking_number = format!("TRK-{}", rand_tracking());
                    println!("  📦 Order shipped! Tracking: {}", ctx.tracking_number);
                }),
        )
        // Shipped -> Delivered
        .transition(OrderState::Shipped, OrderEvent::Deliver, OrderState::Delivered)
        // Any state -> Cancelled (simplified)
        .transition(OrderState::Created, OrderEvent::Cancel, OrderState::Cancelled)
        .transition(OrderState::Paid, OrderEvent::Cancel, OrderState::Cancelled)
        // Configure state actions
        .state(StateConfig::<OrderState, OrderContext>::new(OrderState::Processing).on_entry(|_| {
            println!("  ⚙️  Order is being processed...");
        }))
        .state(StateConfig::<OrderState, OrderContext>::new(OrderState::Delivered).on_entry(|_| {
            println!("  ✅ Order delivered successfully!");
        }))
        .final_state(OrderState::Delivered)
        .final_state(OrderState::Cancelled)
        .build()
        .unwrap();

    println!("Order state: {:?}", order.current_state());

    println!("\nProcessing order flow:");
    order.process(OrderEvent::Pay);
    println!("  State: {:?}", order.current_state());

    order.process(OrderEvent::Process);
    println!("  State: {:?}", order.current_state());

    order.process(OrderEvent::Ship);
    println!("  State: {:?}", order.current_state());

    order.process(OrderEvent::Deliver);
    println!("  State: {:?}", order.current_state());

    println!("\nOrder is final: {}", order.is_final());
}

fn rand_tracking() -> u32 {
    // Simple pseudo-random for demo
    123456
}

// Example 3: Document Approval Workflow
#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
enum DocState {
    Draft,
    Submitted,
    UnderReview,
    Approved,
    Rejected,
    Archived,
}

impl std::fmt::Display for DocState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}

impl State for DocState {}

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
enum DocEvent {
    Submit,
    RequestChanges,
    Approve,
    Reject,
    Archive,
    Resubmit,
}

impl std::fmt::Display for DocEvent {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}

impl Event for DocEvent {}

#[derive(Default, Clone)]
struct ApprovalContext {
    approval_count: u32,
    min_approvals: u32,
}

impl Context for ApprovalContext {}

fn document_approval_example() {
    println!("\n=== Document Approval Workflow ===\n");

    let mut doc = StateMachineBuilder::<DocState, DocEvent, ApprovalContext>::new()
        .initial(DocState::Draft)
        .transition(DocState::Draft, DocEvent::Submit, DocState::Submitted)
        .transition(DocState::Submitted, DocEvent::RequestChanges, DocState::Draft)
        .transition(DocState::Submitted, DocEvent::Approve, DocState::UnderReview)
        .transition_with(
            Transition::new(DocState::UnderReview, DocEvent::Approve, DocState::Approved)
                .with_guard(|_, _, ctx: &ApprovalContext| ctx.approval_count >= ctx.min_approvals),
        )
        .transition_with(
            Transition::new(DocState::UnderReview, DocEvent::Approve, DocState::UnderReview)
                .with_action(|_, _, ctx: &mut ApprovalContext| {
                    ctx.approval_count += 1;
                    println!("  👍 Approval received ({}/{})", ctx.approval_count, ctx.min_approvals);
                }),
        )
        .transition(DocState::UnderReview, DocEvent::Reject, DocState::Rejected)
        .transition(DocState::Rejected, DocEvent::Resubmit, DocState::Draft)
        .transition(DocState::Approved, DocEvent::Archive, DocState::Archived)
        .final_state(DocState::Archived)
        .build()
        .unwrap();

    // Set minimum approvals
    doc.context_mut().min_approvals = 3;

    println!("Document state: {:?}", doc.current_state());

    // Submit document
    println!("\nSubmitting document...");
    doc.process(DocEvent::Submit);
    println!("State: {:?}", doc.current_state());

    // Initial review
    println!("\nStarting review...");
    doc.process(DocEvent::Approve);
    println!("State: {:?}", doc.current_state());

    // Collect approvals (need 3)
    println!("\nCollecting approvals:");
    for i in 1..=3 {
        println!("\nApproval {}:", i);
        let result = doc.process(DocEvent::Approve);
        println!("Result: {:?}", result);
        println!("State: {:?}", doc.current_state());
    }

    // Archive
    println!("\nArchiving document...");
    doc.process(DocEvent::Archive);
    println!("Final state: {:?}", doc.current_state());
}

// Example 4: Sequence Machine for Wizard/Form
#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
enum WizardStep {
    PersonalInfo,
    ContactDetails,
    Preferences,
    Review,
    Complete,
}

impl std::fmt::Display for WizardStep {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            WizardStep::PersonalInfo => write!(f, "Personal Info"),
            WizardStep::ContactDetails => write!(f, "Contact Details"),
            WizardStep::Preferences => write!(f, "Preferences"),
            WizardStep::Review => write!(f, "Review"),
            WizardStep::Complete => write!(f, "Complete"),
        }
    }
}

impl State for WizardStep {}

fn wizard_example() {
    println!("\n=== Form Wizard (Sequence Machine) ===\n");

    let mut wizard = SequenceMachine::new(vec![
        WizardStep::PersonalInfo,
        WizardStep::ContactDetails,
        WizardStep::Preferences,
        WizardStep::Review,
        WizardStep::Complete,
    ]);

    while !wizard.is_end() {
        println!("📋 Current step: {} ({:.0}%)", wizard.current(), wizard.progress() * 100.0);
        wizard.next();
    }

    println!("📋 Current step: {} ({:.0}%)", wizard.current(), wizard.progress() * 100.0);
    println!("\n✅ Wizard complete!");

    // Go back
    println!("\nGoing back...");
    wizard.prev();
    println!("📋 Current step: {}", wizard.current());
}

// Example 5: Generate DOT visualization
fn visualization_example() {
    println!("\n=== State Machine Visualization (DOT) ===\n");

    let sm = StateMachineBuilder::<OrderState, OrderEvent>::new()
        .initial(OrderState::Created)
        .transition(OrderState::Created, OrderEvent::Pay, OrderState::Paid)
        .transition(OrderState::Paid, OrderEvent::Process, OrderState::Processing)
        .transition(OrderState::Processing, OrderEvent::Ship, OrderState::Shipped)
        .transition(OrderState::Shipped, OrderEvent::Deliver, OrderState::Delivered)
        .transition(OrderState::Created, OrderEvent::Cancel, OrderState::Cancelled)
        .final_state(OrderState::Delivered)
        .final_state(OrderState::Cancelled)
        .build()
        .unwrap();

    let dot = sm.to_dot(|s| s.to_string());
    println!("DOT Graph:");
    println!("{}", dot);
    println!("Tip: Use Graphviz (dot -Tpng) to visualize this graph");
}

fn main() {
    println!("╔═══════════════════════════════════════════════════════════╗");
    println!("║        State Machine Utils - Examples                     ║");
    println!("╚═══════════════════════════════════════════════════════════╝\n");

    traffic_light_example();
    order_processing_example();
    document_approval_example();
    wizard_example();
    visualization_example();

    println!("\n✅ All examples completed!");
}