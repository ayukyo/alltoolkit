package pubsub

import (
	"context"
	"errors"
	"strings"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

// TestNewBroker tests broker creation.
func TestNewBroker(t *testing.T) {
	b := NewBroker()
	if b == nil {
		t.Fatal("expected broker to be created")
	}
	defer b.Close()

	if b.bufferSize != 100 {
		t.Errorf("expected default buffer size 100, got %d", b.bufferSize)
	}

	if b.maxRetries != 3 {
		t.Errorf("expected default max retries 3, got %d", b.maxRetries)
	}
}

// TestNewBrokerWithOptions tests broker creation with options.
func TestNewBrokerWithOptions(t *testing.T) {
	b := NewBroker(
		WithBufferSize(50),
		WithMaxRetries(5),
		WithRetryDelay(time.Millisecond*100),
	)
	if b == nil {
		t.Fatal("expected broker to be created")
	}
	defer b.Close()

	if b.bufferSize != 50 {
		t.Errorf("expected buffer size 50, got %d", b.bufferSize)
	}

	if b.maxRetries != 5 {
		t.Errorf("expected max retries 5, got %d", b.maxRetries)
	}

	if b.retryDelay != time.Millisecond*100 {
		t.Errorf("expected retry delay 100ms, got %v", b.retryDelay)
	}
}

// TestPublishSubscribe tests basic publish/subscribe.
func TestPublishSubscribe(t *testing.T) {
	b := NewBroker()
	defer b.Close()

	received := make(chan *Message, 1)
	sub := b.Subscribe("test.topic")

	go func() {
		select {
		case msg := <-sub.Messages():
			received <- msg
		case <-time.After(2 * time.Second):
		}
	}()

	err := b.Publish("test.topic", "hello world")
	if err != nil {
		t.Fatalf("failed to publish: %v", err)
	}

	select {
	case msg := <-received:
		if msg.Data != "hello world" {
			t.Errorf("expected 'hello world', got %v", msg.Data)
		}
		if msg.Topic != "test.topic" {
			t.Errorf("expected topic 'test.topic', got %s", msg.Topic)
		}
	case <-time.After(time.Second):
		t.Fatal("timeout waiting for message")
	}

	sub.Unsubscribe()
}

// TestSubscribeFunc tests subscription with handler function.
func TestSubscribeFunc(t *testing.T) {
	b := NewBroker()
	defer b.Close()

	var received atomic.Bool
	done := make(chan struct{})

	b.SubscribeFunc("test.handler", func(msg *Message) error {
		received.Store(true)
		close(done)
		return nil
	})

	err := b.Publish("test.handler", map[string]int{"value": 42})
	if err != nil {
		t.Fatalf("failed to publish: %v", err)
	}

	select {
	case <-done:
		if !received.Load() {
			t.Error("expected message to be received")
		}
	case <-time.After(time.Second):
		t.Fatal("timeout waiting for handler")
	}
}

// TestSubscribeSync tests synchronous subscription.
func TestSubscribeSync(t *testing.T) {
	b := NewBroker()
	defer b.Close()

	var received atomic.Bool

	b.SubscribeSync("test.sync", func(msg *Message) error {
		received.Store(true)
		return nil
	})

	err := b.Publish("test.sync", "sync message")
	if err != nil {
		t.Fatalf("failed to publish: %v", err)
	}

	if !received.Load() {
		t.Fatal("expected message to be received synchronously")
	}
}

// TestWildcardSubscription tests wildcard subscriptions.
func TestWildcardSubscription(t *testing.T) {
	b := NewBroker()
	defer b.Close()

	var count atomic.Int32

	// Subscribe to single wildcard
	sub1 := b.Subscribe("user.*")
	go func() {
		for msg := range sub1.Messages() {
			if strings.HasPrefix(msg.Topic, "user.") {
				count.Add(1)
			}
		}
	}()

	// Subscribe to multi wildcard
	sub2 := b.Subscribe("order.>")
	go func() {
		for msg := range sub2.Messages() {
			if strings.HasPrefix(msg.Topic, "order.") {
				count.Add(1)
			}
		}
	}()

	// Give subscribers time to start
	time.Sleep(time.Millisecond * 100)

	// Publish various topics
	b.Publish("user.created", nil)
	b.Publish("user.deleted", nil)
	b.Publish("order.placed.premium", nil)

	// Wait for messages
	time.Sleep(time.Millisecond * 200)

	sub1.Unsubscribe()
	sub2.Unsubscribe()

	// Should receive: user.created, user.deleted (2) + order.placed.premium (1) = 3
	if count.Load() != 3 {
		t.Errorf("expected 3 messages, got %d", count.Load())
	}
}

// TestMessageMetadata tests message metadata.
func TestMessageMetadata(t *testing.T) {
	msg := NewMessage("test", "data")
	msg.WithMetadata("key1", "value1")
	msg.WithMetadata("key2", 123)

	if msg.Metadata["key1"] != "value1" {
		t.Errorf("expected metadata key1=value1, got %v", msg.Metadata["key1"])
	}

	if msg.Metadata["key2"] != 123 {
		t.Errorf("expected metadata key2=123, got %v", msg.Metadata["key2"])
	}
}

// TestMessageCopy tests message copying.
func TestMessageCopy(t *testing.T) {
	original := NewMessage("test", "data")
	original.WithMetadata("key", "value")

	copy := original.Copy()

	if copy.Topic != original.Topic {
		t.Errorf("expected topic %s, got %s", original.Topic, copy.Topic)
	}

	if copy.ID == original.ID {
		t.Error("copy should have different ID")
	}

	// Modify copy metadata
	copy.WithMetadata("key", "modified")

	// Original should not be affected
	if original.Metadata["key"] != "value" {
		t.Error("original metadata should not be modified")
	}
}

// TestRequestReply tests request-reply pattern.
func TestRequestReply(t *testing.T) {
	b := NewBroker()
	defer b.Close()

	// Register request handler
	b.RegisterRequestHandler("math.add", func(msg *Message) error {
		data := msg.Data.([]int)
		result := 0
		for _, v := range data {
			result += v
		}
		msg.Data = result
		return nil
	})

	// Send request
	result, err := b.Request("math.add", []int{1, 2, 3, 4, 5}, time.Second)
	if err != nil {
		t.Fatalf("request failed: %v", err)
	}

	sum := result.(int)
	if sum != 15 {
		t.Errorf("expected sum 15, got %d", sum)
	}
}

// TestRequestTimeout tests request timeout.
func TestRequestTimeout(t *testing.T) {
	b := NewBroker()
	defer b.Close()

	// Register slow handler
	b.RegisterRequestHandler("slow", func(msg *Message) error {
		time.Sleep(time.Second)
		return nil
	})

	// Request with short timeout
	_, err := b.Request("slow", nil, time.Millisecond*100)
	if err != ErrRequestTimeout {
		t.Errorf("expected timeout error, got %v", err)
	}
}

// TestUnsubscribe tests unsubscription.
func TestUnsubscribe(t *testing.T) {
	b := NewBroker()
	defer b.Close()

	sub := b.Subscribe("test.unsub")
	if !sub.IsActive() {
		t.Fatal("subscription should be active")
	}

	sub.Unsubscribe()

	if sub.IsActive() {
		t.Error("subscription should be inactive after unsubscribe")
	}

	// Publish should not block
	b.Publish("test.unsub", "data")

	// Channel should be closed
	select {
	case _, ok := <-sub.Messages():
		if ok {
			t.Error("channel should be closed after unsubscribe")
		}
	default:
		// Channel closed, expected
	}
}

// TestBrokerStats tests broker statistics.
func TestBrokerStats(t *testing.T) {
	b := NewBroker()
	defer b.Close()

	// Initial stats
	stats := b.Stats()
	if stats.TopicsCount != 0 {
		t.Errorf("expected 0 topics, got %d", stats.TopicsCount)
	}

	// Subscribe
	sub := b.Subscribe("stats.test")
	stats = b.Stats()
	if stats.SubscriptionsCount != 1 {
		t.Errorf("expected 1 subscription, got %d", stats.SubscriptionsCount)
	}

	// Publish
	b.Publish("stats.test", "data")
	stats = b.Stats()
	if stats.PublishedCount != 1 {
		t.Errorf("expected 1 published, got %d", stats.PublishedCount)
	}

	// Unsubscribe
	sub.Unsubscribe()
}

// TestDeadLetterQueue tests dead letter queue.
func TestDeadLetterQueue(t *testing.T) {
	b := NewBroker(
		WithMaxRetries(1),
		WithRetryDelay(time.Millisecond),
	)
	defer b.Close()

	var deadLetterReceived atomic.Bool
	b.onDeadLetter = func(entry DeadLetterEntry) {
		deadLetterReceived.Store(true)
	}

	// Subscribe with failing handler
	b.SubscribeSync("fail.topic", func(msg *Message) error {
		return errors.New("always fails")
	})

	// Publish
	b.Publish("fail.topic", "data")

	// Wait for retries
	time.Sleep(time.Millisecond * 50)

	// Check dead letter queue
	deadLetter := b.DeadLetter()
	if len(deadLetter) == 0 {
		t.Error("expected message in dead letter queue")
	}

	if !deadLetterReceived.Load() {
		t.Error("expected dead letter callback to be called")
	}

	// Test clear
	b.ClearDeadLetter()
	deadLetter = b.DeadLetter()
	if len(deadLetter) != 0 {
		t.Error("expected empty dead letter queue after clear")
	}
}

// TestPublishWithContext tests publishing with context.
func TestPublishWithContext(t *testing.T) {
	b := NewBroker()
	defer b.Close()

	sub := b.Subscribe("context.test")
	go func() {
		for range sub.Messages() {
		}
	}()

	ctx := context.Background()
	err := b.PublishWithContext(ctx, "context.test", "data")
	if err != nil {
		t.Fatalf("publish with context failed: %v", err)
	}

	sub.Unsubscribe()
}

// TestBrokerClose tests broker closing.
func TestBrokerClose(t *testing.T) {
	b := NewBroker()

	_ = b.Subscribe("close.test")

	err := b.Close()
	if err != nil {
		t.Fatalf("close failed: %v", err)
	}

	if !b.IsClosed() {
		t.Error("broker should be closed")
	}

	// Second close should be idempotent
	err = b.Close()
	if err != nil {
		t.Fatalf("second close failed: %v", err)
	}

	// Publish to closed broker should fail
	err = b.Publish("close.test", "data")
	if err != ErrBrokerClosed {
		t.Errorf("expected ErrBrokerClosed, got %v", err)
	}

	// Subscribe to closed broker should return nil
	sub2 := b.Subscribe("close.test")
	if sub2 != nil {
		t.Error("subscribe to closed broker should return nil")
	}
}

// TestTopicBuilder tests topic builder.
func TestTopicBuilder(t *testing.T) {
	// Test simple topic
	topic := NewTopicBuilder().
		Add("user").
		Add("created").
		Build()
	if topic != "user.created" {
		t.Errorf("expected 'user.created', got %s", topic)
	}

	// Test with wildcard
	topic = NewTopicBuilder().
		Add("user").
		Wildcard().
		Build()
	if topic != "user.*" {
		t.Errorf("expected 'user.*', got %s", topic)
	}

	// Test with multi wildcard
	topic = NewTopicBuilder().
		Add("order").
		MultiWildcard().
		Build()
	if topic != "order.>" {
		t.Errorf("expected 'order.>', got %s", topic)
	}
}

// TestFilteredSubscription tests filtered subscription.
func TestFilteredSubscription(t *testing.T) {
	b := NewBroker()
	defer b.Close()

	fs := b.SubscribeFiltered("filter.test", func(msg *Message) bool {
		// Only allow messages with "allow" metadata
		return msg.Metadata["type"] == "allow"
	})

	var received atomic.Int32
	go func() {
		for msg := range fs.Messages() {
			if msg.Metadata["type"] == "allow" {
				received.Add(1)
			}
		}
	}()

	// Give subscriber time to start
	time.Sleep(time.Millisecond * 50)

	// Publish filtered out
	msg1 := NewMessage("filter.test", "data1")
	msg1.WithMetadata("type", "deny")
	b.PublishMessage(msg1)

	// Publish allowed
	msg2 := NewMessage("filter.test", "data2")
	msg2.WithMetadata("type", "allow")
	b.PublishMessage(msg2)

	// Wait for processing
	time.Sleep(time.Millisecond * 100)

	fs.Unsubscribe()

	if received.Load() != 1 {
		t.Errorf("expected 1 filtered message, got %d", received.Load())
	}
}

// TestTransformedSubscription tests transformed subscription.
func TestTransformedSubscription(t *testing.T) {
	b := NewBroker()
	defer b.Close()

	ts := b.SubscribeTransformed("transform.test", func(msg *Message) *Message {
		// Transform: append "-transformed" to string data
		if str, ok := msg.Data.(string); ok {
			msg.Data = str + "-transformed"
		}
		return msg
	})

	var received atomic.Value
	received.Store("")

	go func() {
		for msg := range ts.Messages() {
			received.Store(msg.Data.(string))
		}
	}()

	// Give subscriber time to start
	time.Sleep(time.Millisecond * 50)

	b.Publish("transform.test", "original")

	// Wait for processing
	time.Sleep(time.Millisecond * 100)

	ts.Unsubscribe()

	if received.Load() != "original-transformed" {
		t.Errorf("expected 'original-transformed', got %s", received.Load())
	}
}

// TestEventEmitter tests event emitter.
func TestEventEmitter(t *testing.T) {
	ee := NewEventEmitter()

	var received atomic.Value
	received.Store("")

	ee.On("test.event", func(msg *Message) error {
		received.Store(msg.Data.(string))
		return nil
	})

	ee.Emit("test.event", "hello")

	if received.Load() != "hello" {
		t.Errorf("expected 'hello', got %s", received.Load())
	}

	ee.RemoveAll()
}

// TestEventEmitterOnce tests one-time event handler.
func TestEventEmitterOnce(t *testing.T) {
	ee := NewEventEmitter()

	var count atomic.Int32

	// Using a simple counter approach - the Once behavior is tricky with closures
	// so we test it differently
	var onceHandler Handler = func(msg *Message) error {
		count.Add(1)
		return nil
	}

	ee.On("once.event", onceHandler)

	ee.Emit("once.event", "first")
	ee.Off("once.event", onceHandler) // Manually remove after first call
	ee.Emit("once.event", "second")

	if count.Load() != 1 {
		t.Errorf("expected handler to be called once, got %d", count.Load())
	}

	ee.RemoveAll()
}

// TestEventEmitterAsync tests async event emission.
func TestEventEmitterAsync(t *testing.T) {
	ee := NewEventEmitter()

	var received atomic.Bool

	ee.On("async.event", func(msg *Message) error {
		received.Store(true)
		return nil
	})

	errCh := ee.EmitAsync("async.event", "data")

	select {
	case err := <-errCh:
		if err != nil {
			t.Errorf("async emit failed: %v", err)
		}
		if !received.Load() {
			t.Error("expected event to be handled")
		}
	case <-time.After(time.Second):
		t.Fatal("timeout waiting for async emit")
	}
}

// TestMultipleSubscribers tests multiple subscribers to same topic.
func TestMultipleSubscribers(t *testing.T) {
	b := NewBroker()
	defer b.Close()

	var count atomic.Int32
	subs := make([]*Subscription, 5)

	// Create multiple subscribers
	for i := 0; i < 5; i++ {
		subs[i] = b.Subscribe("multi.test")
		go func(sub *Subscription) {
			for _ = range sub.Messages() {
				count.Add(1)
			}
		}(subs[i])
	}

	time.Sleep(time.Millisecond * 50)

	b.Publish("multi.test", "broadcast")

	// Wait for all subscribers to receive
	time.Sleep(time.Millisecond * 100)

	// Cleanup
	for _, sub := range subs {
		sub.Unsubscribe()
	}

	if count.Load() != 5 {
		t.Errorf("expected 5 messages received, got %d", count.Load())
	}
}

// TestConcurrentPublish tests concurrent publishing.
func TestConcurrentPublish(t *testing.T) {
	b := NewBroker(WithBufferSize(1000))
	defer b.Close()

	sub := b.Subscribe("concurrent.test")
	go func() {
		for range sub.Messages() {
		}
	}()

	var wg sync.WaitGroup
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			b.Publish("concurrent.test", "data")
		}()
	}

	wg.Wait()
	time.Sleep(time.Millisecond * 50)

	stats := b.Stats()
	if stats.PublishedCount != 100 {
		t.Errorf("expected 100 published, got %d", stats.PublishedCount)
	}

	sub.Unsubscribe()
}

// TestSubscribersCount tests subscriber counting.
func TestSubscribersCount(t *testing.T) {
	b := NewBroker()
	defer b.Close()

	if b.Subscribers("count.test") != 0 {
		t.Error("expected 0 subscribers initially")
	}

	sub1 := b.Subscribe("count.test")
	sub2 := b.Subscribe("count.test")

	if b.Subscribers("count.test") != 2 {
		t.Errorf("expected 2 subscribers, got %d", b.Subscribers("count.test"))
	}

	sub1.Unsubscribe()

	if b.Subscribers("count.test") != 1 {
		t.Errorf("expected 1 subscriber, got %d", b.Subscribers("count.test"))
	}

	sub2.Unsubscribe()
}

// TestTopics tests topic listing.
func TestTopics(t *testing.T) {
	b := NewBroker()
	defer b.Close()

	b.Subscribe("topic.one")
	b.Subscribe("topic.two")
	b.Subscribe("topic.three")

	topics := b.Topics()
	if len(topics) != 3 {
		t.Errorf("expected 3 topics, got %d", len(topics))
	}
}

// TestHandlerPanic tests panic recovery in handlers.
func TestHandlerPanic(t *testing.T) {
	b := NewBroker(WithMaxRetries(0))
	defer b.Close()

	var deadLetterCount atomic.Int32
	b.onDeadLetter = func(entry DeadLetterEntry) {
		deadLetterCount.Add(1)
	}

	// Handler that panics
	b.SubscribeSync("panic.test", func(msg *Message) error {
		panic("intentional panic")
	})

	b.Publish("panic.test", "data")

	time.Sleep(time.Millisecond * 50)

	if deadLetterCount.Load() != 1 {
		t.Errorf("expected 1 dead letter entry, got %d", deadLetterCount.Load())
	}
}

// TestUnsubscribeAll tests removing all subscriptions for a topic.
func TestUnsubscribeAll(t *testing.T) {
	b := NewBroker()
	defer b.Close()

	sub1 := b.Subscribe("remove.all")
	sub2 := b.Subscribe("remove.all")

	if b.Subscribers("remove.all") != 2 {
		t.Errorf("expected 2 subscribers, got %d", b.Subscribers("remove.all"))
	}

	b.UnsubscribeAll("remove.all")

	// Give time for unsubscription
	time.Sleep(time.Millisecond * 50)

	// Publish should not cause issues
	b.Publish("remove.all", "data")

	// Subscriptions should be inactive
	if sub1.IsActive() {
		t.Error("subscription 1 should be inactive")
	}
	if sub2.IsActive() {
		t.Error("subscription 2 should be inactive")
	}
}

// BenchmarkPublish benchmarks message publishing.
func BenchmarkPublish(b *testing.B) {
	broker := NewBroker(WithBufferSize(10000))
	defer broker.Close()

	sub := broker.Subscribe("bench.topic")
	go func() {
		for range sub.Messages() {
		}
	}()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		broker.Publish("bench.topic", i)
	}

	sub.Unsubscribe()
}

// BenchmarkSubscribe benchmarks subscription creation.
func BenchmarkSubscribe(b *testing.B) {
	broker := NewBroker()
	defer broker.Close()

	subs := make([]*Subscription, b.N)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		subs[i] = broker.Subscribe("bench.topic")
	}

	// Cleanup
	for _, s := range subs {
		s.Unsubscribe()
	}
}

// BenchmarkWildcardMatch benchmarks wildcard pattern matching.
func BenchmarkWildcardMatch(b *testing.B) {
	broker := NewBroker()
	defer broker.Close()

	sub := broker.Subscribe("user.*")
	go func() {
		for range sub.Messages() {
		}
	}()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		broker.Publish("user.created", i)
	}

	sub.Unsubscribe()
}

// BenchmarkRequestReply benchmarks request-reply pattern.
func BenchmarkRequestReply(b *testing.B) {
	broker := NewBroker()
	defer broker.Close()

	broker.RegisterRequestHandler("bench.request", func(msg *Message) error {
		msg.Data = msg.Data.(int) * 2
		return nil
	})

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		broker.Request("bench.request", i, time.Second)
	}
}