using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using AllToolkit;

public class EventBusTest
{
    private static int _passed = 0;
    private static int _failed = 0;

    public static void Main()
    {
        Console.WriteLine("=== EventBus Test Suite ===\n");

        TestBasicSubscribeAndPublish();
        TestAsyncSubscription();
        TestSubscribeOnce();
        TestSubscribeWithFilter();
        TestPriority();
        TestUnsubscribe();
        TestEventHistory();
        TestMultipleSubscribers();
        TestThreadSafety();
        TestSubscriberCount();

        Console.WriteLine($"\n=== Results ===");
        Console.WriteLine($"Passed: {_passed}");
        Console.WriteLine($"Failed: {_failed}");
        Console.WriteLine($"Total: {_passed + _failed}");

        Environment.Exit(_failed > 0 ? 1 : 0);
    }

    private static void Assert(bool condition, string message)
    {
        if (condition) { _passed++; Console.WriteLine($"  ✓ {message}"); }
        else { _failed++; Console.WriteLine($"  ✗ {message}"); }
    }

    private static void TestBasicSubscribeAndPublish()
    {
        Console.WriteLine("Test: Basic Subscribe and Publish");
        var bus = new EventBus();
        var received = false;
        var token = bus.Subscribe<TestEvent>(e => { received = true; });
        bus.Publish(new TestEvent { Message = "Hello" });
        Assert(received, "Event was received");
        token.Unsubscribe();
    }

    private static void TestAsyncSubscription()
    {
        Console.WriteLine("\nTest: Async Subscription");
        var bus = new EventBus();
        var received = false;
        var token = bus.SubscribeAsync<TestEvent>(async e =>
        {
            await Task.Delay(10);
            received = true;
        });
        bus.Publish(new TestEvent { Message = "Async" });
        Assert(received, "Async event was received");
        token.Unsubscribe();
    }

    private static void TestSubscribeOnce()
    {
        Console.WriteLine("\nTest: Subscribe Once");
        var bus = new EventBus();
        var count = 0;
        var token = bus.SubscribeOnce<TestEvent>(e => { count++; });
        bus.Publish(new TestEvent { Message = "First" });
        bus.Publish(new TestEvent { Message = "Second" });
        Assert(count == 1, $"Once subscription fired exactly once (count={count})");
    }

    private static void TestSubscribeWithFilter()
    {
        Console.WriteLine("\nTest: Subscribe with Filter");
        var bus = new EventBus();
        var highPriorityReceived = false;
        var token = bus.SubscribeWithFilter<PriorityEvent>(
            e => { highPriorityReceived = true; },
            e => e.Priority > 5);
        bus.Publish(new PriorityEvent { Priority = 3 });
        Assert(!highPriorityReceived, "Low priority event filtered out");
        bus.Publish(new PriorityEvent { Priority = 8 });
        Assert(highPriorityReceived, "High priority event received");
        token.Unsubscribe();
    }

    private static void TestPriority()
    {
        Console.WriteLine("\nTest: Priority Ordering");
        var bus = new EventBus();
        var order = new List<int>();
        var t1 = bus.Subscribe<TestEvent>(e => { order.Add(1); }, priority: 1);
        var t2 = bus.Subscribe<TestEvent>(e => { order.Add(2); }, priority: 5);
        var t3 = bus.Subscribe<TestEvent>(e => { order.Add(3); }, priority: 3);
        bus.Publish(new TestEvent());
        Assert(order[0] == 2 && order[1] == 3 && order[2] == 1, "Priority order correct (high to low)");
        t1.Unsubscribe(); t2.Unsubscribe(); t3.Unsubscribe();
    }

    private static void TestUnsubscribe()
    {
        Console.WriteLine("\nTest: Unsubscribe");
        var bus = new EventBus();
        var count = 0;
        var token = bus.Subscribe<TestEvent>(e => { count++; });
        bus.Publish(new TestEvent());
        var unsubscribed = token.Unsubscribe();
        Assert(unsubscribed, "Unsubscribe returned true");
        bus.Publish(new TestEvent());
        Assert(count == 1, "Unsubscribed handler not called");
    }

    private static void TestEventHistory()
    {
        Console.WriteLine("\nTest: Event History");
        var bus = new EventBus();
        bus.Publish(new TestEvent { Message = "First" });
        bus.Publish(new TestEvent { Message = "Second" });
        var history = bus.GetHistory<TestEvent>();
        Assert(history.Count == 2, "History contains 2 events");
        var last = bus.GetLastEvent<TestEvent>();
        Assert(last?.Message == "Second", "Last event is correct");
        bus.ClearHistory<TestEvent>();
        Assert(bus.GetHistory<TestEvent>().Count == 0, "History cleared");
    }

    private static void TestMultipleSubscribers()
    {
        Console.WriteLine("\nTest: Multiple Subscribers");
        var bus = new EventBus();
        var count = 0;
        var t1 = bus.Subscribe<TestEvent>(e => { Interlocked.Increment(ref count); });
        var t2 = bus.Subscribe<TestEvent>(e => { Interlocked.Increment(ref count); });
        var t3 = bus.Subscribe<TestEvent>(e => { Interlocked.Increment(ref count); });
        bus.Publish(new TestEvent());
        Assert(count == 3, "All 3 subscribers received event");
        t1.Unsubscribe(); t2.Unsubscribe(); t3.Unsubscribe();
    }

    private static void TestThreadSafety()
    {
        Console.WriteLine("\nTest: Thread Safety");
        var bus = new EventBus();
        var count = 0;
        var tokens = new List<SubscriptionToken>();
        for (int i = 0; i < 10; i++)
            tokens.Add(bus.Subscribe<TestEvent>(e => { Interlocked.Increment(ref count); }));
        Parallel.For(0, 100, _ => bus.Publish(new TestEvent()));
        Assert(count == 1000, "Thread-safe publish (100 events x 10 subscribers)");
        foreach (var t in tokens) t.Unsubscribe();
    }

    private static void TestSubscriberCount()
    {
        Console.WriteLine("\nTest: Subscriber Count");
        var bus = new EventBus();
        Assert(bus.GetSubscriberCount<TestEvent>() == 0, "Initial count is 0");
        var t1 = bus.Subscribe<TestEvent>(e => { });
        var t2 = bus.Subscribe<TestEvent>(e => { });
        Assert(bus.GetSubscriberCount<TestEvent>() == 2, "Count is 2 after subscriptions");
        Assert(bus.HasSubscribers<TestEvent>(), "HasSubscribers returns true");
        t1.Unsubscribe();
        Assert(bus.GetSubscriberCount<TestEvent>() == 1, "Count is 1 after unsubscribe");
        t2.Unsubscribe();
        Assert(!bus.HasSubscribers<TestEvent>(), "HasSubscribers returns false after all unsubscribed");
    }
}

public class TestEvent
{
    public string Message { get; set; }
}

public class PriorityEvent
{
    public int Priority { get; set; }
}
