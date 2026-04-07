using System;
using System.Threading.Tasks;
using AllToolkit;

namespace EventBusExample
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== EventBus Examples ===\n");
            Example1_BasicUsage();
            Example2_PrioritySubscription();
            Example3_FilteredSubscription();
            Example4_OneTimeSubscription();
            Example5_AsyncHandler().Wait();
            Example6_EventHistory();
            Example7_MultipleEventTypes();
            Example8_DelayedPublish().Wait();
            Console.WriteLine("\nAll examples completed!");
        }

        static void Example1_BasicUsage()
        {
            Console.WriteLine("1. Basic Usage");
            var bus = new EventBus();
            var token = bus.Subscribe<UserLoggedInEvent>(evt =>
            {
                Console.WriteLine($"   User logged in: {evt.Username} at {evt.LoginTime}");
            });
            bus.Publish(new UserLoggedInEvent { Username = "john_doe", LoginTime = DateTime.Now });
            token.Unsubscribe();
            Console.WriteLine();
        }

        static void Example2_PrioritySubscription()
        {
            Console.WriteLine("2. Priority Subscription");
            var bus = new EventBus();
            bus.Subscribe<OrderCreatedEvent>(evt => Console.WriteLine($"   [Low] Logging order: {evt.OrderId}"), priority: 1);
            bus.Subscribe<OrderCreatedEvent>(evt => Console.WriteLine($"   [High] Validating order: {evt.OrderId}"), priority: 10);
            bus.Subscribe<OrderCreatedEvent>(evt => Console.WriteLine($"   [Med] Processing order: {evt.OrderId}"), priority: 5);
            bus.Publish(new OrderCreatedEvent { OrderId = "ORD-12345" });
            bus.ClearAllSubscriptions();
            Console.WriteLine();
        }

        static void Example3_FilteredSubscription()
        {
            Console.WriteLine("3. Filtered Subscription");
            var bus = new EventBus();
            bus.SubscribeWithFilter<OrderEvent>(evt => Console.WriteLine($"   VIP Order: {evt.OrderId}, Amount: ${evt.Amount}"), filter: evt => evt.Amount > 1000);
            bus.Subscribe<OrderEvent>(evt => Console.WriteLine($"   All Orders: {evt.OrderId}, Amount: ${evt.Amount}"));
            bus.Publish(new OrderEvent { OrderId = "ORD-001", Amount = 500 });
            bus.Publish(new OrderEvent { OrderId = "ORD-002", Amount = 2000 });
            bus.ClearAllSubscriptions();
            Console.WriteLine();
        }

        static void Example4_OneTimeSubscription()
        {
            Console.WriteLine("4. One-Time Subscription");
            var bus = new EventBus();
            bus.SubscribeOnce<SystemAlertEvent>(evt => Console.WriteLine($"   [ONCE] Alert: {evt.Message}"));
            bus.Publish(new SystemAlertEvent { Message = "Server starting..." });
            bus.Publish(new SystemAlertEvent { Message = "Server running..." });
            bus.Publish(new SystemAlertEvent { Message = "Server stopped." });
            Console.WriteLine("   (Only first alert was processed)");
            Console.WriteLine();
        }

        static async Task Example5_AsyncHandler()
        {
            Console.WriteLine("5. Async Handler");
            var bus = new EventBus();
            bus.SubscribeAsync<DataReceivedEvent>(async evt =>
            {
                Console.WriteLine($"   Processing data: {evt.DataId}...");
                await Task.Delay(100);
                Console.WriteLine($"   Data {evt.DataId} processed!");
            });
            await bus.PublishAsync(new DataReceivedEvent { DataId = "DATA-001" });
            await bus.PublishAsync(new DataReceivedEvent { DataId = "DATA-002" });
            bus.ClearAllSubscriptions();
            Console.WriteLine();
        }

        static void Example6_EventHistory()
        {
            Console.WriteLine("6. Event History");
            var bus = new EventBus();
            bus.Publish(new ChatMessageEvent { User = "Alice", Message = "Hello!" });
            bus.Publish(new ChatMessageEvent { User = "Bob", Message = "Hi Alice!" });
            bus.Publish(new ChatMessageEvent { User = "Alice", Message = "How are you?" });
            var history = bus.GetHistory<ChatMessageEvent>();
            Console.WriteLine($"   Total messages: {history.Count}");
            var lastMessage = bus.GetLastEvent<ChatMessageEvent>();
            Console.WriteLine($"   Last: {lastMessage.User}: {lastMessage.Message}");
            Console.WriteLine("   History:");
            foreach (var msg in history) Console.WriteLine($"     - {msg.User}: {msg.Message}");
            Console.WriteLine();
        }

        static void Example7_MultipleEventTypes()
        {
            Console.WriteLine("7. Multiple Event Types");
            var bus = new EventBus();
            bus.Subscribe<UserLoggedInEvent>(evt => Console.WriteLine($"   [Auth] {evt.Username} logged in"));
            bus.Subscribe<UserLoggedOutEvent>(evt => Console.WriteLine($"   [Auth] {evt.Username} logged out"));
            bus.Subscribe<PageViewEvent>(evt => Console.WriteLine($"   [Analytics] Page viewed: {evt.PageUrl}"));
            bus.Publish(new UserLoggedInEvent { Username = "alice" });
            bus.Publish(new PageViewEvent { PageUrl = "/dashboard" });
            bus.Publish(new UserLoggedOutEvent { Username = "alice" });
            bus.ClearAllSubscriptions();
            Console.WriteLine();
        }

        static async Task Example8_DelayedPublish()
        {
            Console.WriteLine("8. Delayed Publish");
            var bus = new EventBus();
            bus.Subscribe<ReminderEvent>(evt => Console.WriteLine($"   [{DateTime.Now:HH:mm:ss}] Reminder: {evt.Message}"));
            Console.WriteLine($"   Setting reminder for 2 seconds... ({DateTime.Now:HH:mm:ss})");
            await bus.PublishDelayed(new ReminderEvent { Message = "Time's up!" }, TimeSpan.FromSeconds(2));
            Console.WriteLine($"   Done! ({DateTime.Now:HH:mm:ss})");
            Console.WriteLine();
        }
    }

    public class UserLoggedInEvent { public string Username { get; set; } public DateTime LoginTime { get; set; } }
    public class UserLoggedOutEvent { public string Username { get; set; } public DateTime LogoutTime { get; set; } }
    public class OrderCreatedEvent { public string OrderId { get; set; } public decimal TotalAmount { get; set; } }
    public class OrderEvent { public string OrderId { get; set; } public decimal Amount { get; set; } }
    public class SystemAlertEvent { public string Message { get; set; } public DateTime Timestamp { get; set; } }
    public class DataReceivedEvent { public string DataId { get; set; } public byte[] Data { get; set; } }
    public class ChatMessageEvent { public string User { get; set; } public string Message { get; set; } public DateTime Timestamp { get; set; } }
    public class PageViewEvent { public string PageUrl { get; set; } public string UserId { get; set; } public DateTime ViewTime { get; set; } }
    public class ReminderEvent { public string Message { get; set; } public DateTime ScheduledTime { get; set; } }
}
