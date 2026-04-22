/**
 * @file example_priority_queue.c
 * @brief Usage Examples for Priority Queue (Min-Heap)
 * 
 * @author AllToolkit
 * @date 2026-04-23
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "priority_queue.h"

/* ========== Example 1: Task Scheduler ========== */

typedef struct {
    char name[32];
    int id;
} Task;

void example_task_scheduler(void) {
    printf("\n=== Example 1: Task Scheduler ===\n\n");
    
    PriorityQueue *scheduler = pq_create(sizeof(Task), 0);
    
    /* Add tasks with priorities (lower = more urgent) */
    Task t1 = {"Backup Database", 1};
    Task t2 = {"Send Email", 2};
    Task t3 = {"Fix Critical Bug", 3};
    Task t4 = {"Update Docs", 4};
    Task t5 = {"Review Code", 5};
    
    pq_insert(scheduler, &t3, 1.0);  /* Most urgent */
    pq_insert(scheduler, &t1, 3.0);
    pq_insert(scheduler, &t5, 5.0);
    pq_insert(scheduler, &t2, 2.0);
    pq_insert(scheduler, &t4, 4.0);
    
    printf("Tasks in execution order:\n");
    while (!pq_is_empty(scheduler)) {
        Task task;
        double priority;
        pq_extract_min(scheduler, &task, &priority);
        printf("  Priority %.1f: %s (ID: %d)\n", priority, task.name, task.id);
    }
    
    pq_free(&scheduler);
}

/* ========== Example 2: Dijkstra's Algorithm Demo ========== */

typedef struct {
    int node;
    int distance;
} PathNode;

void example_shortest_path(void) {
    printf("\n=== Example 2: Shortest Path (Dijkstra-style) ===\n\n");
    
    PriorityQueue *pq = pq_create(sizeof(PathNode), 0);
    
    /* Simulate distance updates in path finding */
    PathNode nodes[] = {
        {0, 0},    /* Start node */
        {1, 4},    /* Node 1 at distance 4 */
        {2, 2},    /* Node 2 at distance 2 */
        {3, 7},    /* Node 3 at distance 7 */
        {4, 1},    /* Node 4 at distance 1 */
        {5, 5},    /* Node 5 at distance 5 */
    };
    
    /* Insert in random order */
    for (int i = 5; i >= 0; i--) {
        pq_insert(pq, &nodes[i], (double)nodes[i].distance);
    }
    
    printf("Processing nodes by shortest distance:\n");
    while (!pq_is_empty(pq)) {
        PathNode node;
        pq_extract_min(pq, &node, NULL);
        printf("  Node %d (distance: %d)\n", node.node, node.distance);
    }
    
    pq_free(&pq);
}

/* ========== Example 3: Number Sorting ========== */

void example_sort_numbers(void) {
    printf("\n=== Example 3: Sorting Numbers with Priority Queue ===\n\n");
    
    PriorityQueue *pq = pq_create_int();
    
    int numbers[] = {42, 17, 89, 3, 56, 23, 71, 8};
    int n = sizeof(numbers) / sizeof(numbers[0]);
    
    printf("Original array: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", numbers[i]);
        pq_insert_int(pq, numbers[i], (double)numbers[i]);
    }
    printf("\n");
    
    printf("Sorted (ascending): ");
    while (!pq_is_empty(pq)) {
        int val;
        pq_extract_int(pq, &val, NULL);
        printf("%d ", val);
    }
    printf("\n");
    
    pq_free(&pq);
}

/* ========== Example 4: Event Simulation ========== */

typedef struct {
    double time;
    char description[64];
} Event;

void example_event_simulation(void) {
    printf("\n=== Example 4: Event Simulation ===\n\n");
    
    PriorityQueue *events = pq_create(sizeof(Event), 0);
    
    /* Schedule events at different times */
    Event e1 = {5.0, "User Login"};
    Event e2 = {2.0, "System Check"};
    Event e3 = {10.0, "Backup"};
    Event e4 = {7.5, "Report Generation"};
    Event e5 = {3.0, "Email Notification"};
    
    pq_insert(events, &e1, e1.time);
    pq_insert(events, &e3, e3.time);
    pq_insert(events, &e5, e5.time);
    pq_insert(events, &e2, e2.time);
    pq_insert(events, &e4, e4.time);
    
    printf("Simulating events in chronological order:\n");
    double current_time = 0.0;
    while (!pq_is_empty(events)) {
        Event event;
        double time;
        pq_extract_min(events, &event, &time);
        printf("  Time %.1f: %s (elapsed: %.1f)\n", 
               event.time, event.description, event.time - current_time);
        current_time = event.time;
    }
    
    pq_free(&events);
}

/* ========== Example 5: Patient Queue (ER Triage) ========== */

typedef struct {
    char name[32];
    int severity;  /* 1-10, lower = more severe */
} Patient;

void example_er_triage(void) {
    printf("\n=== Example 5: ER Triage System ===\n\n");
    
    PriorityQueue *er = pq_create(sizeof(Patient), 0);
    
    /* Patients arrive with different severity */
    Patient patients[] = {
        {"John", 8},     /* Minor injury */
        {"Alice", 2},    /* Critical */
        {"Bob", 5},      /* Moderate */
        {"Carol", 1},    /* Life-threatening */
        {"David", 6},    /* Moderate-severe */
    };
    
    printf("Patients arriving:\n");
    for (int i = 0; i < 5; i++) {
        printf("  %s (severity: %d)\n", patients[i].name, patients[i].severity);
        /* Priority = severity (lower severity treated first) */
        pq_insert(er, &patients[i], (double)patients[i].severity);
    }
    
    printf("\nTreatment order (most critical first):\n");
    while (!pq_is_empty(er)) {
        Patient patient;
        double severity;
        pq_extract_min(er, &patient, &severity);
        printf("  %s (severity: %.0f)\n", patient.name, severity);
    }
    
    pq_free(&er);
}

/* ========== Example 6: Priority Update Demo ========== */

int cmp_task(const void *a, const void *b) {
    const Task *ta = (const Task *)a;
    const Task *tb = (const Task *)b;
    return ta->id - tb->id;
}

void example_priority_update(void) {
    printf("\n=== Example 6: Dynamic Priority Update ===\n\n");
    
    PriorityQueue *pq = pq_create(sizeof(Task), 0);
    
    Task tasks[] = {
        {"Task A", 1},
        {"Task B", 2},
        {"Task C", 3},
    };
    
    pq_insert(pq, &tasks[0], 3.0);
    pq_insert(pq, &tasks[1], 2.0);
    pq_insert(pq, &tasks[2], 1.0);
    
    printf("Initial order:\n");
    Task t;
    pq_peek_min(pq, &t, NULL);
    printf("  Next: %s (ID: %d)\n", t.name, t.id);
    
    /* Make Task A urgent */
    printf("\nUpdating Task A priority to 0.5 (urgent):\n");
    pq_update_priority(pq, &tasks[0], 0.5, cmp_task);
    
    pq_peek_min(pq, &t, NULL);
    printf("  Next: %s (ID: %d)\n", t.name, t.id);
    
    /* Extract all to show new order */
    printf("\nFinal execution order:\n");
    while (!pq_is_empty(pq)) {
        double pri;
        pq_extract_min(pq, &t, &pri);
        printf("  Priority %.1f: %s (ID: %d)\n", pri, t.name, t.id);
    }
    
    pq_free(&pq);
}

/* ========== Example 7: Get Sorted Without Extraction ========== */

void example_get_sorted(void) {
    printf("\n=== Example 7: Get Sorted Data (Non-destructive) ===\n\n");
    
    PriorityQueue *pq = pq_create_int();
    
    pq_insert_int(pq, 50, 5.0);
    pq_insert_int(pq, 10, 1.0);
    pq_insert_int(pq, 30, 3.0);
    pq_insert_int(pq, 20, 2.0);
    pq_insert_int(pq, 40, 4.0);
    
    int sorted[5];
    double priorities[5];
    
    pq_get_sorted(pq, sorted, priorities);
    
    printf("Sorted view (without extraction):\n");
    for (int i = 0; i < 5; i++) {
        printf("  Value %d (priority %.1f)\n", sorted[i], priorities[i]);
    }
    
    printf("\nQueue still contains %zu elements\n", pq_size(pq));
    
    pq_free(&pq);
}

/* ========== Main ========== */

int main(void) {
    printf("\n========================================\n");
    printf("  Priority Queue Usage Examples\n");
    printf("========================================\n");
    
    example_task_scheduler();
    example_shortest_path();
    example_sort_numbers();
    example_event_simulation();
    example_er_triage();
    example_priority_update();
    example_get_sorted();
    
    printf("\n========================================\n");
    printf("  All examples completed!\n");
    printf("========================================\n\n");
    
    return 0;
}