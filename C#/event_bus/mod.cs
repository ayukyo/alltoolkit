using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace AllToolkit
{
    public class EventBus
    {
        private readonly Dictionary<Type, List<Subscription>> _subscriptions;
        private readonly Dictionary<Type, List<object>> _eventHistory;
        private readonly ReaderWriterLockSlim _lock;
        private readonly int _maxHistorySize;

        public static EventBus Default { get; } = new EventBus();

        public EventBus(int maxHistorySize = 100)
        {
            _subscriptions = new Dictionary<Type, List<Subscription>>();
            _eventHistory = new Dictionary<Type, List<object>>();
            _lock = new ReaderWriterLockSlim();
            _maxHistorySize = maxHistorySize;
        }

        public SubscriptionToken Subscribe<T>(Action<T> handler, int priority = 0) where T : class
        {
            return SubscribeInternal<T>(handler, priority, false, null);
        }

        public SubscriptionToken SubscribeAsync<T>(Func<T, Task> handler, int priority = 0) where T : class
        {
            return SubscribeInternal<T>(handler, priority, false, null);
        }

        public SubscriptionToken SubscribeOnce<T>(Action<T> handler, int priority = 0) where T : class
        {
            return SubscribeInternal<T>(handler, priority, true, null);
        }

        public SubscriptionToken SubscribeWithFilter<T>(Action<T> handler, Predicate<T> filter, int priority = 0) where T : class
        {
            return SubscribeInternal<T>(handler, priority, false, filter);
        }

        public bool Unsubscribe(SubscriptionToken token)
        {
            if (token == null) return false;
            _lock.EnterWriteLock();
            try
            {
                if (_subscriptions.TryGetValue(token.EventType, out var subs))
                {
                    var sub = subs.FirstOrDefault(s => s.Id == token.Id);
                    if (sub != null)
                    {
                        subs.Remove(sub);
                        return true;
                    }
                }
                return false;
            }
            finally { _lock.ExitWriteLock(); }
        }

        public void UnsubscribeAll<T>() where T : class { UnsubscribeAll(typeof(T)); }

        public void UnsubscribeAll(Type eventType)
        {
            _lock.EnterWriteLock();
            try { _subscriptions.Remove(eventType); }
            finally { _lock.ExitWriteLock(); }
        }

        public void ClearAllSubscriptions()
        {
            _lock.EnterWriteLock();
            try { _subscriptions.Clear(); }
            finally { _lock.ExitWriteLock(); }
        }

        public void Publish<T>(T eventData) where T : class { PublishInternal(eventData, false).Wait(); }

        public async Task PublishAsync<T>(T eventData) where T : class { await PublishInternal(eventData, true); }

        public async Task PublishDelayed<T>(T eventData, TimeSpan delay) where T : class
        {
            await Task.Delay(delay);
            await PublishAsync(eventData);
        }

        public List<T> GetHistory<T>() where T : class
        {
            _lock.EnterReadLock();
            try
            {
                if (_eventHistory.TryGetValue(typeof(T), out var history))
                    return history.Cast<T>().ToList();
                return new List<T>();
            }
            finally { _lock.ExitReadLock(); }
        }

        public T GetLastEvent<T>() where T : class
        {
            _lock.EnterReadLock();
            try
            {
                if (_eventHistory.TryGetValue(typeof(T), out var history) && history.Count > 0)
                    return history.Last() as T;
                return null;
            }
            finally { _lock.ExitReadLock(); }
        }

        public void ClearHistory<T>() where T : class { ClearHistory(typeof(T)); }

        public void ClearHistory(Type eventType)
        {
            _lock.EnterWriteLock();
            try { _eventHistory.Remove(eventType); }
            finally { _lock.ExitWriteLock(); }
        }

        public void ClearAllHistory()
        {
            _lock.EnterWriteLock();
            try { _eventHistory.Clear(); }
            finally { _lock.ExitWriteLock(); }
        }

        public bool HasSubscribers<T>() where T : class { return HasSubscribers(typeof(T)); }

        public bool HasSubscribers(Type eventType)
        {
            _lock.EnterReadLock();
            try { return _subscriptions.TryGetValue(eventType, out var subs) && subs.Count > 0; }
            finally { _lock.ExitReadLock(); }
        }

        public int GetSubscriberCount<T>() where T : class { return GetSubscriberCount(typeof(T)); }

        public int GetSubscriberCount(Type eventType)
        {
            _lock.EnterReadLock();
            try { return _subscriptions.TryGetValue(eventType, out var subs) ? subs.Count : 0; }
            finally { _lock.ExitReadLock(); }
        }

        private SubscriptionToken SubscribeInternal<T>(Delegate handler, int priority, bool once, Predicate<T> filter) where T : class
        {
            var eventType = typeof(T);
            var subscription = new Subscription
            {
                Id = Guid.NewGuid(),
                EventType = eventType,
                Handler = handler,
                Priority = priority,
                Once = once,
                Filter = filter != null ? (Predicate<object>)(obj => filter((T)obj)) : null
            };

            _lock.EnterWriteLock();
            try
            {
                if (!_subscriptions.TryGetValue(eventType, out var subs))
                {
                    subs = new List<Subscription>();
                    _subscriptions[eventType] = subs;
                }
                subs.Add(subscription);
                subs.Sort((a, b) => b.Priority.CompareTo(a.Priority));
            }
            finally { _lock.ExitWriteLock(); }

            return new SubscriptionToken(subscription.Id, eventType, this);
        }

        private async Task PublishInternal<T>(T eventData, bool async) where T : class
        {
            if (eventData == null) throw new ArgumentNullException(nameof(eventData));

            var eventType = typeof(T);
            List<Subscription> subscriptions;

            _lock.EnterReadLock();
            try
            {
                if (!_subscriptions.TryGetValue(eventType, out subscriptions))
                    subscriptions = new List<Subscription>();
                else
                    subscriptions = new List<Subscription>(subscriptions);
            }
            finally { _lock.ExitReadLock(); }

            var toRemove = new List<Subscription>();

            foreach (var sub in subscriptions)
            {
                if (sub.Filter != null && !sub.Filter(eventData))
                    continue;

                try
                {
                    if (sub.Handler is Action<T> syncHandler)
                    {
                        syncHandler(eventData);
                    }
                    else if (sub.Handler is Func<T, Task> asyncHandler)
                    {
                        if (async) await asyncHandler(eventData);
                        else asyncHandler(eventData).Wait();
                    }
                }
                catch { /* 处理器异常不应影响其他订阅者 */ }

                if (sub.Once)
                    toRemove.Add(sub);
            }

            if (toRemove.Count > 0)
            {
                _lock.EnterWriteLock();
                try
                {
                    if (_subscriptions.TryGetValue(eventType, out var subs))
                    {
                        foreach (var sub in toRemove)
                            subs.RemoveAll(s => s.Id == sub.Id);
                    }
                }
                finally { _lock.ExitWriteLock(); }
            }

            _lock.EnterWriteLock();
            try
            {
                if (!_eventHistory.TryGetValue(eventType, out var history))
                {
                    history = new List<object>();
                    _eventHistory[eventType] = history;
                }
                history.Add(eventData);
                if (history.Count > _maxHistorySize)
                    history.RemoveAt(0);
            }
            finally { _lock.ExitWriteLock(); }
        }
    }

    public class Subscription
    {
        public Guid Id { get; set; }
        public Type EventType { get; set; }
        public Delegate Handler { get; set; }
        public int Priority { get; set; }
        public bool Once { get; set; }
        public Predicate<object> Filter { get; set; }
    }

    public class SubscriptionToken
    {
        public Guid Id { get; }
        public Type EventType { get; }
        private readonly EventBus _eventBus;

        public SubscriptionToken(Guid id, Type eventType, EventBus eventBus)
        {
            Id = id;
            EventType = eventType;
            _eventBus = eventBus;
        }

        public bool Unsubscribe() => _eventBus.Unsubscribe(this);
    }
}
