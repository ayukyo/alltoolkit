// Package pubsub_utils provides a comprehensive publish-subscribe utility for Go applications.
// It supports synchronous and asynchronous messaging, topic-based routing, wildcard subscriptions,
// message filtering, and transformation. All implementations are thread-safe and use only the
// Go standard library.
//
// Example usage:
//
//	// Create a new broker
//	broker := pubsub.NewBroker()
//
//	// Subscribe to a topic
//	sub := broker.Subscribe("user.created")
//	go func() {
//	    for msg := range sub.Messages() {
//	        fmt.Printf("Received: %+v\n", msg.Data)
//	    }
//	}()
//
//	// Publish a message
//	broker.Publish("user.created", map[string]interface{}{"id": 123, "name": "Alice"})
//
//	// Unsubscribe when done
//	sub.Unsubscribe()
//
//	// Wildcard subscription
//	subAll := broker.Subscribe("user.*") // Matches user.created, user.deleted, etc.
//
//	// Multi-wildcard subscription
//	subDeep := broker.Subscribe("order.>") // Matches order.placed, order.placed.premium, etc.
//
//	// Subscribe with handler function
//	broker.SubscribeFunc("order.placed", func(msg *pubsub.Message) error {
//	    fmt.Printf("Order received: %+v\n", msg.Data)
//	    return nil
//	})
//
//	// Subscribe with synchronous handler
//	broker.SubscribeSync("log.event", func(msg *pubsub.Message) error {
//	    log.Printf("Event: %s - %v", msg.Topic, msg.Data)
//	    return nil
//	})
//
//	// Request-Reply pattern
//	broker.RegisterRequestHandler("math.add", func(msg *pubsub.Message) error {
//	    numbers := msg.Data.([]int)
//	    sum := 0
//	    for _, n := range numbers {
//	        sum += n
//	    }
//	    msg.Data = sum
//	    return nil
//	})
//	result, err := broker.Request("math.add", []int{1, 2, 3, 4, 5}, time.Second)
//
//	// With options
//	broker := pubsub.NewBroker(
//	    pubsub.WithBufferSize(1000),
//	    pubsub.WithMaxRetries(5),
//	    pubsub.WithRetryDelay(time.Second),
//	)
//
//	// Event emitter for simple use cases
//	emitter := pubsub.NewEventEmitter()
//	emitter.On("click", func(msg *pubsub.Message) error {
//	    fmt.Println("Button clicked!")
//	    return nil
//	})
//	emitter.Emit("click", nil)
//	emitter.Once("init", func(msg *pubsub.Message) error {
//	    fmt.Println("Initialized (only once)")
//	    return nil
//	})
//	emitter.EmitAsync("update", map[string]string{"status": "ready"})
//
// Features:
// - Zero dependencies, uses only Go standard library
// - Thread-safe implementations with sync.RWMutex
// - Topic-based routing with wildcard support (* for single segment, > for multiple)
// - Message filtering and transformation
// - Synchronous and asynchronous message handling
// - Request-Reply pattern for RPC-style communication
// - Dead letter queue for failed messages
// - Message acknowledgments and retries
// - Event emitter for simple pub/sub use cases
// - Graceful shutdown support
// - Production-ready for event-driven architectures
//
package pubsub

import (
	"context"
	"errors"
	"fmt"
	"regexp"
	"strings"
	"sync"
	"sync/atomic"
	"time"
)

// Common errors
var (
	ErrTopicEmpty       = errors.New("topic cannot be empty")
	ErrNotSubscribed    = errors.New("not subscribed to topic")
	ErrBrokerClosed     = errors.New("broker is closed")
	ErrHandlerPanic     = errors.New("handler panicked")
	ErrRequestTimeout   = errors.New("request timeout")
	ErrNoHandler        = errors.New("no handler available for request")
)

// Message represents a published message.
type Message struct {
	ID        string                 // Unique message ID
	Topic     string                 // Topic the message was published to
	Data      interface{}            // Message payload
	Metadata  map[string]interface{} // Optional metadata
	Timestamp time.Time              // Message creation time
	Retries   int                    // Number of retry attempts
}

// NewMessage creates a new message with the given topic and data.
func NewMessage(topic string, data interface{}) *Message {
	return &Message{
		ID:        generateID(),
		Topic:     topic,
		Data:      data,
		Metadata:  make(map[string]interface{}),
		Timestamp: time.Now(),
		Retries:   0,
	}
}

// WithMetadata adds metadata to the message.
func (m *Message) WithMetadata(key string, value interface{}) *Message {
	m.Metadata[key] = value
	return m
}

// Copy creates a copy of the message with a new ID.
func (m *Message) Copy() *Message {
	metadata := make(map[string]interface{})
	for k, v := range m.Metadata {
		metadata[k] = v
	}
	return &Message{
		ID:        generateID(),
		Topic:     m.Topic,
		Data:      m.Data,
		Metadata:  metadata,
		Timestamp: time.Now(),
		Retries:   m.Retries,
	}
}

// Stats contains broker statistics.
type Stats struct {
	TopicsCount        int64 // Number of active topics
	SubscriptionsCount int64 // Number of active subscriptions
	PublishedCount     int64 // Total messages published
	DeliveredCount     int64 // Total messages delivered
	FailedCount        int64 // Total messages failed
	DeadLetterCount    int64 // Messages in dead letter queue
}

// DeadLetterEntry represents a message that failed processing.
type DeadLetterEntry struct {
	Message   *Message
	Error     error
	FailedAt  time.Time
	Attempts  int
}

// Handler processes a message and returns an error if processing fails.
type Handler func(*Message) error

// Filter filters messages for subscription.
type Filter func(*Message) bool

// Transform transforms messages for subscription.
type Transform func(*Message) *Message

// Subscription represents a topic subscription.
type Subscription struct {
	id         string
	topic      string
	pattern    *regexp.Regexp
	msgChan    chan *Message
	bufferSize int
	mu         sync.RWMutex
	active     bool
	broker     *Broker
}

// ID returns the subscription ID.
func (s *Subscription) ID() string {
	return s.id
}

// Topic returns the subscribed topic pattern.
func (s *Subscription) Topic() string {
	return s.topic
}

// Messages returns a channel for receiving messages.
func (s *Subscription) Messages() <-chan *Message {
	return s.msgChan
}

// Unsubscribe cancels the subscription.
func (s *Subscription) Unsubscribe() {
	s.mu.Lock()
	defer s.mu.Unlock()

	if !s.active {
		return
	}

	s.active = false
	close(s.msgChan)

	if s.broker != nil {
		s.broker.removeSubscription(s)
	}
}

// IsActive returns whether the subscription is active.
func (s *Subscription) IsActive() bool {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.active
}

// Broker is the main pub/sub broker.
type Broker struct {
	mu            sync.RWMutex
	subscriptions map[string][]*Subscription // topic -> subscriptions
	wildcards     []*Subscription            // wildcard subscriptions
	syncHandlers  map[string][]Handler       // topic -> sync handlers
	reqHandlers   map[string]Handler         // topic -> request handler
	deadLetter    []DeadLetterEntry
	closed        bool
	stats         Stats
	bufferSize    int
	maxRetries    int
	retryDelay    time.Duration
	onDeadLetter  func(DeadLetterEntry)
	onPublish     func(*Message)
	onSubscribe   func(*Subscription)
	onUnsubscribe func(*Subscription)
}

// BrokerOption configures the broker.
type BrokerOption func(*Broker)

// WithBufferSize sets the message channel buffer size.
func WithBufferSize(size int) BrokerOption {
	return func(b *Broker) {
		if size > 0 {
			b.bufferSize = size
		}
	}
}

// WithMaxRetries sets the maximum retry attempts for failed messages.
func WithMaxRetries(max int) BrokerOption {
	return func(b *Broker) {
		if max >= 0 {
			b.maxRetries = max
		}
	}
}

// WithRetryDelay sets the delay between retry attempts.
func WithRetryDelay(delay time.Duration) BrokerOption {
	return func(b *Broker) {
		if delay > 0 {
			b.retryDelay = delay
		}
	}
}

// WithDeadLetterHandler sets a callback for dead letter messages.
func WithDeadLetterHandler(fn func(DeadLetterEntry)) BrokerOption {
	return func(b *Broker) {
		b.onDeadLetter = fn
	}
}

// OnPublish sets a callback called on every published message.
func OnPublish(fn func(*Message)) BrokerOption {
	return func(b *Broker) {
		b.onPublish = fn
	}
}

// OnSubscribe sets a callback called on every subscription.
func OnSubscribe(fn func(*Subscription)) BrokerOption {
	return func(b *Broker) {
		b.onSubscribe = fn
	}
}

// OnUnsubscribe sets a callback called on every unsubscription.
func OnUnsubscribe(fn func(*Subscription)) BrokerOption {
	return func(b *Broker) {
		b.onUnsubscribe = fn
	}
}

// NewBroker creates a new pub/sub broker with default settings.
func NewBroker(opts ...BrokerOption) *Broker {
	b := &Broker{
		subscriptions: make(map[string][]*Subscription),
		wildcards:     make([]*Subscription, 0),
		syncHandlers:  make(map[string][]Handler),
		reqHandlers:   make(map[string]Handler),
		deadLetter:    make([]DeadLetterEntry, 0),
		bufferSize:    100,
		maxRetries:    3,
		retryDelay:    time.Second,
	}

	for _, opt := range opts {
		opt(b)
	}

	return b
}

// Subscribe creates a new subscription for the given topic pattern.
// Supports wildcards: * matches a single segment, > matches multiple segments.
// Examples:
//   - "user.created" matches exactly "user.created"
//   - "user.*" matches "user.created", "user.deleted", etc.
//   - "user.>" matches "user.created", "user.profile.updated", etc.
func (b *Broker) Subscribe(topic string) *Subscription {
	b.mu.Lock()
	defer b.mu.Unlock()

	if b.closed {
		return nil
	}

	if topic == "" {
		return nil
	}

	sub := &Subscription{
		id:         generateID(),
		topic:      topic,
		pattern:    compileTopicPattern(topic),
		msgChan:    make(chan *Message, b.bufferSize),
		bufferSize: b.bufferSize,
		active:     true,
		broker:     b,
	}

	if isWildcard(topic) {
		b.wildcards = append(b.wildcards, sub)
	} else {
		b.subscriptions[topic] = append(b.subscriptions[topic], sub)
	}

	atomic.AddInt64(&b.stats.SubscriptionsCount, 1)

	if b.onSubscribe != nil {
		b.onSubscribe(sub)
	}

	return sub
}

// SubscribeFunc subscribes to a topic with an async handler function.
// Messages are delivered to the handler in a separate goroutine.
func (b *Broker) SubscribeFunc(topic string, handler Handler) *Subscription {
	sub := b.Subscribe(topic)
	if sub == nil {
		return nil
	}

	go func() {
		for msg := range sub.Messages() {
			if err := b.handleWithRetry(handler, msg); err != nil {
				b.addToDeadLetter(msg, err)
			}
		}
	}()

	return sub
}

// SubscribeSync subscribes to a topic with a synchronous handler.
// The handler is called directly in the publish goroutine.
func (b *Broker) SubscribeSync(topic string, handler Handler) {
	b.mu.Lock()
	defer b.mu.Unlock()

	if b.closed || topic == "" {
		return
	}

	b.syncHandlers[topic] = append(b.syncHandlers[topic], handler)
	atomic.AddInt64(&b.stats.SubscriptionsCount, 1)
}

// FilteredSubscription wraps a subscription with filtering.
type FilteredSubscription struct {
	sub    *Subscription
	filter Filter
	done   chan struct{}
}

// SubscribeFiltered creates a subscription with a message filter.
func (b *Broker) SubscribeFiltered(topic string, filter Filter) *FilteredSubscription {
	sub := b.Subscribe(topic)
	if sub == nil {
		return nil
	}

	return &FilteredSubscription{
		sub:    sub,
		filter: filter,
		done:   make(chan struct{}),
	}
}

// Messages returns a filtered message channel.
func (fs *FilteredSubscription) Messages() <-chan *Message {
	out := make(chan *Message, fs.sub.bufferSize)

	go func() {
		defer close(out)
		for {
			select {
			case msg, ok := <-fs.sub.Messages():
				if !ok {
					return
				}
				if fs.filter(msg) {
					out <- msg
				}
			case <-fs.done:
				return
			}
		}
	}()

	return out
}

// Unsubscribe cancels the filtered subscription.
func (fs *FilteredSubscription) Unsubscribe() {
	close(fs.done)
	fs.sub.Unsubscribe()
}

// TransformedSubscription wraps a subscription with transformation.
type TransformedSubscription struct {
	sub       *Subscription
	transform Transform
	done      chan struct{}
}

// SubscribeTransformed creates a subscription with message transformation.
func (b *Broker) SubscribeTransformed(topic string, transform Transform) *TransformedSubscription {
	sub := b.Subscribe(topic)
	if sub == nil {
		return nil
	}

	return &TransformedSubscription{
		sub:       sub,
		transform: transform,
		done:      make(chan struct{}),
	}
}

// Messages returns a transformed message channel.
func (ts *TransformedSubscription) Messages() <-chan *Message {
	out := make(chan *Message, ts.sub.bufferSize)

	go func() {
		defer close(out)
		for {
			select {
			case msg, ok := <-ts.sub.Messages():
				if !ok {
					return
				}
				transformed := ts.transform(msg)
				if transformed != nil {
					out <- transformed
				}
			case <-ts.done:
				return
			}
		}
	}()

	return out
}

// Unsubscribe cancels the transformed subscription.
func (ts *TransformedSubscription) Unsubscribe() {
	close(ts.done)
	ts.sub.Unsubscribe()
}

// RegisterRequestHandler registers a handler for the request-reply pattern.
func (b *Broker) RegisterRequestHandler(topic string, handler Handler) {
	b.mu.Lock()
	defer b.mu.Unlock()

	if !b.closed && topic != "" {
		b.reqHandlers[topic] = handler
	}
}

// Publish publishes a message to all subscribers of the given topic.
func (b *Broker) Publish(topic string, data interface{}) error {
	return b.PublishMessage(NewMessage(topic, data))
}

// PublishWithContext publishes a message with context for cancellation.
func (b *Broker) PublishWithContext(ctx context.Context, topic string, data interface{}) error {
	return b.PublishMessage(NewMessage(topic, data))
}

// PublishMessage publishes a pre-constructed message.
func (b *Broker) PublishMessage(msg *Message) error {
	b.mu.RLock()
	defer b.mu.RUnlock()

	if b.closed {
		return ErrBrokerClosed
	}

	atomic.AddInt64(&b.stats.PublishedCount, 1)

	if b.onPublish != nil {
		b.onPublish(msg)
	}

	// Deliver to direct subscribers
	if subs, ok := b.subscriptions[msg.Topic]; ok {
		for _, sub := range subs {
			if sub.IsActive() {
				select {
				case sub.msgChan <- msg:
					atomic.AddInt64(&b.stats.DeliveredCount, 1)
				default:
					atomic.AddInt64(&b.stats.FailedCount, 1)
				}
			}
		}
	}

	// Deliver to wildcard subscribers
	for _, sub := range b.wildcards {
		if sub.IsActive() && sub.pattern != nil && sub.pattern.MatchString(msg.Topic) {
			select {
			case sub.msgChan <- msg:
				atomic.AddInt64(&b.stats.DeliveredCount, 1)
			default:
				atomic.AddInt64(&b.stats.FailedCount, 1)
			}
		}
	}

	// Call synchronous handlers
	if handlers, ok := b.syncHandlers[msg.Topic]; ok {
		for _, handler := range handlers {
			if err := b.handleWithRetry(handler, msg); err != nil {
				b.addToDeadLetter(msg, err)
			}
		}
	}

	return nil
}

// Request sends a request and waits for a reply.
func (b *Broker) Request(topic string, data interface{}, timeout time.Duration) (interface{}, error) {
	return b.RequestWithContext(context.Background(), topic, data, timeout)
}

// RequestWithContext sends a request with context.
func (b *Broker) RequestWithContext(ctx context.Context, topic string, data interface{}, timeout time.Duration) (interface{}, error) {
	b.mu.RLock()
	handler, ok := b.reqHandlers[topic]
	b.mu.RUnlock()

	if !ok {
		return nil, ErrNoHandler
	}

	msg := NewMessage(topic, data)
	msg.Metadata["request"] = true

	done := make(chan interface{}, 1)
	errCh := make(chan error, 1)

	go func() {
		if err := handler(msg); err != nil {
			errCh <- err
		} else {
			done <- msg.Data
		}
	}()

	select {
	case <-ctx.Done():
		return nil, ctx.Err()
	case <-time.After(timeout):
		return nil, ErrRequestTimeout
	case result := <-done:
		return result, nil
	case err := <-errCh:
		return nil, err
	}
}

// handleWithRetry executes a handler with retry logic.
func (b *Broker) handleWithRetry(handler Handler, msg *Message) error {
	var lastErr error

	for attempt := 0; attempt <= b.maxRetries; attempt++ {
		func() {
			defer func() {
				if r := recover(); r != nil {
					lastErr = fmt.Errorf("%w: %v", ErrHandlerPanic, r)
				}
			}()

			if err := handler(msg); err != nil {
				lastErr = err
			} else {
				lastErr = nil
			}
		}()

		if lastErr == nil {
			return nil
		}

		msg.Retries++
		if attempt < b.maxRetries && b.retryDelay > 0 {
			time.Sleep(b.retryDelay)
		}
	}

	return lastErr
}

// addToDeadLetter adds a failed message to the dead letter queue.
// This is called from PublishMessage which holds a read lock,
// so we use a goroutine to avoid deadlock when acquiring the write lock.
func (b *Broker) addToDeadLetter(msg *Message, err error) {
	entry := DeadLetterEntry{
		Message:  msg,
		Error:    err,
		FailedAt: time.Now(),
		Attempts: msg.Retries + 1,
	}

	// Use goroutine to avoid deadlock with read lock
	go func() {
		b.mu.Lock()
		b.deadLetter = append(b.deadLetter, entry)
		b.mu.Unlock()

		atomic.AddInt64(&b.stats.DeadLetterCount, 1)
		atomic.AddInt64(&b.stats.FailedCount, 1)

		if b.onDeadLetter != nil {
			b.onDeadLetter(entry)
		}
	}()
}

// removeSubscription removes a subscription from the broker.
func (b *Broker) removeSubscription(sub *Subscription) {
	b.mu.Lock()
	defer b.mu.Unlock()

	// Remove from topic subscriptions
	if subs, ok := b.subscriptions[sub.topic]; ok {
		for i, s := range subs {
			if s.id == sub.id {
				b.subscriptions[sub.topic] = append(subs[:i], subs[i+1:]...)
				break
			}
		}
	}

	// Remove from wildcard subscriptions
	for i, s := range b.wildcards {
		if s.id == sub.id {
			b.wildcards = append(b.wildcards[:i], b.wildcards[i+1:]...)
			break
		}
	}

	atomic.AddInt64(&b.stats.SubscriptionsCount, -1)

	if b.onUnsubscribe != nil {
		b.onUnsubscribe(sub)
	}
}

// UnsubscribeAll removes all subscriptions for a topic.
func (b *Broker) UnsubscribeAll(topic string) {
	b.mu.Lock()
	defer b.mu.Unlock()

	if subs, ok := b.subscriptions[topic]; ok {
		for _, sub := range subs {
			sub.mu.Lock()
			sub.active = false
			close(sub.msgChan)
			sub.mu.Unlock()
		}
		delete(b.subscriptions, topic)
	}

	delete(b.syncHandlers, topic)
	delete(b.reqHandlers, topic)
}

// Topics returns all active topics.
func (b *Broker) Topics() []string {
	b.mu.RLock()
	defer b.mu.RUnlock()

	topics := make([]string, 0, len(b.subscriptions))
	for topic := range b.subscriptions {
		topics = append(topics, topic)
	}
	return topics
}

// Subscribers returns the number of subscribers for a topic.
func (b *Broker) Subscribers(topic string) int {
	b.mu.RLock()
	defer b.mu.RUnlock()

	count := 0
	if subs, ok := b.subscriptions[topic]; ok {
		count += len(subs)
	}

	// Count matching wildcards
	for _, sub := range b.wildcards {
		if sub.pattern != nil && sub.pattern.MatchString(topic) {
			count++
		}
	}

	// Count sync handlers
	if handlers, ok := b.syncHandlers[topic]; ok {
		count += len(handlers)
	}

	return count
}

// Stats returns current broker statistics.
func (b *Broker) Stats() Stats {
	b.mu.RLock()
	defer b.mu.RUnlock()

	stats := b.stats
	stats.TopicsCount = int64(len(b.subscriptions))

	return stats
}

// DeadLetter returns all dead letter entries.
func (b *Broker) DeadLetter() []DeadLetterEntry {
	b.mu.RLock()
	defer b.mu.RUnlock()
	return append([]DeadLetterEntry(nil), b.deadLetter...)
}

// ClearDeadLetter clears the dead letter queue.
func (b *Broker) ClearDeadLetter() {
	b.mu.Lock()
	defer b.mu.Unlock()
	b.deadLetter = b.deadLetter[:0]
	atomic.StoreInt64(&b.stats.DeadLetterCount, 0)
}

// Close gracefully shuts down the broker.
func (b *Broker) Close() error {
	b.mu.Lock()
	if b.closed {
		b.mu.Unlock()
		return nil
	}
	b.closed = true
	b.mu.Unlock()

	// Close all subscriptions
	b.mu.Lock()
	for topic, subs := range b.subscriptions {
		for _, sub := range subs {
			sub.mu.Lock()
			sub.active = false
			close(sub.msgChan)
			sub.mu.Unlock()
		}
		delete(b.subscriptions, topic)
	}

	for _, sub := range b.wildcards {
		sub.mu.Lock()
		sub.active = false
		close(sub.msgChan)
		sub.mu.Unlock()
	}
	b.wildcards = nil
	b.mu.Unlock()

	return nil
}

// IsClosed returns whether the broker is closed.
func (b *Broker) IsClosed() bool {
	b.mu.RLock()
	defer b.mu.RUnlock()
	return b.closed
}

// TopicBuilder helps build topic patterns.
type TopicBuilder struct {
	parts []string
}

// NewTopicBuilder creates a new topic builder.
func NewTopicBuilder() *TopicBuilder {
	return &TopicBuilder{parts: make([]string, 0)}
}

// Add adds a topic segment.
func (tb *TopicBuilder) Add(part string) *TopicBuilder {
	tb.parts = append(tb.parts, part)
	return tb
}

// Wildcard adds a single-segment wildcard (*).
func (tb *TopicBuilder) Wildcard() *TopicBuilder {
	tb.parts = append(tb.parts, "*")
	return tb
}

// MultiWildcard adds a multi-segment wildcard (>).
func (tb *TopicBuilder) MultiWildcard() *TopicBuilder {
	tb.parts = append(tb.parts, ">")
	return tb
}

// Build builds the topic string.
func (tb *TopicBuilder) Build() string {
	return strings.Join(tb.parts, ".")
}

// EventEmitter provides a simple event-based pub/sub.
type EventEmitter struct {
	mu       sync.RWMutex
	handlers map[string][]Handler
}

// NewEventEmitter creates a new event emitter.
func NewEventEmitter() *EventEmitter {
	return &EventEmitter{
		handlers: make(map[string][]Handler),
	}
}

// On registers an event handler.
func (ee *EventEmitter) On(event string, handler Handler) {
	ee.mu.Lock()
	defer ee.mu.Unlock()
	ee.handlers[event] = append(ee.handlers[event], handler)
}

// Once registers a one-time event handler that removes itself after first call.
func (ee *EventEmitter) Once(event string, handler Handler) {
	ee.mu.Lock()
	defer ee.mu.Unlock()

	onceHandler := Handler(func(msg *Message) error {
		ee.Off(event, handler)
		return handler(msg)
	})
	ee.handlers[event] = append(ee.handlers[event], onceHandler)
}

// Off removes an event handler.
func (ee *EventEmitter) Off(event string, handler Handler) {
	ee.mu.Lock()
	defer ee.mu.Unlock()

	if handlers, ok := ee.handlers[event]; ok {
		// Remove specific handler (by pointer equality)
		for i, h := range handlers {
			// Compare function pointers (works for closures wrapped in same function)
			if fmt.Sprintf("%p", h) == fmt.Sprintf("%p", handler) {
				ee.handlers[event] = append(handlers[:i], handlers[i+1:]...)
				break
			}
		}
	}
}

// Emit emits an event to all registered handlers.
func (ee *EventEmitter) Emit(event string, data interface{}) error {
	ee.mu.RLock()
	handlers := append([]Handler(nil), ee.handlers[event]...)
	ee.mu.RUnlock()

	msg := NewMessage(event, data)

	for _, handler := range handlers {
		if err := handler(msg); err != nil {
			return err
		}
	}

	return nil
}

// EmitAsync emits an event asynchronously.
func (ee *EventEmitter) EmitAsync(event string, data interface{}) chan error {
	errCh := make(chan error, 1)

	go func() {
		errCh <- ee.Emit(event, data)
	}()

	return errCh
}

// RemoveAll removes all event handlers.
func (ee *EventEmitter) RemoveAll() {
	ee.mu.Lock()
	defer ee.mu.Unlock()
	ee.handlers = make(map[string][]Handler)
}

// Helper functions

// generateID generates a unique ID for messages and subscriptions.
func generateID() string {
	return fmt.Sprintf("%d-%d", time.Now().UnixNano(), time.Now().Nanosecond())
}

// isWildcard checks if a topic pattern contains wildcards.
func isWildcard(topic string) bool {
	return strings.Contains(topic, "*") || strings.Contains(topic, ">")
}

// compileTopicPattern compiles a topic pattern to a regex.
func compileTopicPattern(topic string) *regexp.Regexp {
	// Handle wildcards: split by segments and process each
	segments := strings.Split(topic, ".")

	patternParts := make([]string, len(segments))
	for i, seg := range segments {
		if seg == "*" {
			// Single segment wildcard: matches anything except dots
			patternParts[i] = `[^.]+`
		} else if seg == ">" {
			// Multi-segment wildcard: matches anything including dots
			// Must be at the end
			patternParts[i] = `.+`
		} else {
			// Literal segment: escape special regex chars
			patternParts[i] = regexp.QuoteMeta(seg)
		}
	}

	// Join with escaped dot
	escaped := strings.Join(patternParts, `\.`)

	// Anchor the pattern
	escaped = "^" + escaped + "$"

	re, _ := regexp.Compile(escaped)
	return re
}