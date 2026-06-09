// RateAggregate Implementation

#include "rate_aggregate.h"

void rate_aggregator_init(RateAggregator* agg) {
    RateConfig config = {300.0, 100, 2};
    rate_aggregator_init_config(agg, config);
}

void rate_aggregator_init_config(RateAggregator* agg, RateConfig config) {
    agg->window_size_seconds = config.window_size_seconds;
    agg->window_size_ms = config.window_size_seconds * 1000.0;
    agg->bucket_count = config.bucket_count;
    agg->precision = config.precision;
    agg->total_hits = 0;
    agg->total_misses = 0;
    agg->capacity = config.bucket_count * 10;
    agg->count = 0;
    agg->events = (EventRecord*)malloc(sizeof(EventRecord) * agg->capacity);
    if (!agg->events) {
        agg->capacity = 0;
    }
}

void rate_aggregator_init_seconds(RateAggregator* agg, double window_seconds) {
    RateConfig config = {window_seconds, 100, 2};
    rate_aggregator_init_config(agg, config);
}

void rate_aggregator_destroy(RateAggregator* agg) {
    if (agg->events) {
        free(agg->events);
        agg->events = NULL;
    }
    agg->capacity = 0;
    agg->count = 0;
}

static void evict_old_events(RateAggregator* agg) {
    if (!agg->events) return;
    
    double cutoff = get_current_time_ms() - agg->window_size_ms;
    int kept = 0;
    for (int i = 0; i < agg->count; i++) {
        if (agg->events[i].timestamp >= cutoff) {
            agg->events[kept] = agg->events[i];
            kept++;
        }
    }
    agg->count = kept;
}

static double get_current_time_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    return ts.tv_sec * 1000.0 + ts.tv_nsec / 1000000.0;
}

static void ensure_capacity(RateAggregator* agg) {
    if (!agg->events) return;
    
    if (agg->count >= agg->capacity) {
        int new_capacity = agg->capacity == 0 ? 100 : agg->capacity * 2;
        EventRecord* new_events = (EventRecord*)realloc(agg->events, sizeof(EventRecord) * new_capacity);
        if (new_events) {
            agg->events = new_events;
            agg->capacity = new_capacity;
        }
    }
}

void rate_record(RateAggregator* agg, double value) {
    if (!agg->events) return;
    evict_old_events(agg);
    ensure_capacity(agg);
    if (agg->count < agg->capacity) {
        agg->events[agg->count].timestamp = get_current_time_ms();
        agg->events[agg->count].value = value;
        agg->count++;
    }
}

void rate_record_hit(RateAggregator* agg) {
    agg->total_hits++;
    rate_record(agg, 1.0);
}

void rate_record_miss(RateAggregator* agg) {
    agg->total_misses++;
    rate_record(agg, 0.0);
}

int rate_count(RateAggregator* agg) {
    evict_old_events(agg);
    return agg->count;
}

uint64_t rate_total_hits(RateAggregator* agg) {
    return agg->total_hits;
}

uint64_t rate_total_misses(RateAggregator* agg) {
    return agg->total_misses;
}

double rate_hit_ratio(RateAggregator* agg) {
    uint64_t total = agg->total_hits + agg->total_misses;
    return total == 0 ? 0.0 : (double)agg->total_hits / (double)total;
}

double rate_miss_ratio(RateAggregator* agg) {
    return 1.0 - rate_hit_ratio(agg);
}

static double rate_sum_internal(RateAggregator* agg) {
    if (agg->count == 0) return 0.0;
    double s = 0.0;
    for (int i = 0; i < agg->count; i++) {
        s += agg->events[i].value;
    }
    return s;
}

double rate_per_second(RateAggregator* agg) {
    evict_old_events(agg);
    double secs = agg->window_size_seconds;
    if (secs == 0.0) return 0.0;
    return rate_round((double)agg->count / secs, agg->precision);
}

double rate_per_minute(RateAggregator* agg) {
    evict_old_events(agg);
    double window_secs = agg->window_size_seconds;
    if (window_secs == 0.0) return 0.0;
    return rate_round((double)agg->count * 60.0 / window_secs, agg->precision);
}

double rate_per_hour(RateAggregator* agg) {
    evict_old_events(agg);
    double window_secs = agg->window_size_seconds;
    if (window_secs == 0.0) return 0.0;
    return rate_round((double)agg->count * 3600.0 / window_secs, agg->precision);
}

double rate_sum(RateAggregator* agg) {
    evict_old_events(agg);
    return rate_sum_internal(agg);
}

double rate_mean(RateAggregator* agg) {
    evict_old_events(agg);
    if (agg->count == 0) return 0.0;
    return rate_round(rate_sum_internal(agg) / agg->count, agg->precision);
}

double rate_min(RateAggregator* agg) {
    evict_old_events(agg);
    if (agg->count == 0) return 0.0;
    double m = agg->events[0].value;
    for (int i = 1; i < agg->count; i++) {
        if (agg->events[i].value < m) m = agg->events[i].value;
    }
    return m;
}

double rate_max(RateAggregator* agg) {
    evict_old_events(agg);
    if (agg->count == 0) return 0.0;
    double m = agg->events[0].value;
    for (int i = 1; i < agg->count; i++) {
        if (agg->events[i].value > m) m = agg->events[i].value;
    }
    return m;
}

double rate_percentile(RateAggregator* agg, double p) {
    evict_old_events(agg);
    if (agg->count == 0) return 0.0;
    
    double* values = (double*)malloc(sizeof(double) * agg->count);
    if (!values) return 0.0;
    
    for (int i = 0; i < agg->count; i++) {
        values[i] = agg->events[i].value;
    }
    
    qsort(values, agg->count, sizeof(double), rate_compare_double);
    
    int idx = (int)round((agg->count - 1) * p);
    idx = idx < 0 ? 0 : (idx >= agg->count ? agg->count - 1 : idx);
    
    double result = rate_round(values[idx], agg->precision);
    free(values);
    return result;
}

double rate_p50(RateAggregator* agg) { return rate_percentile(agg, 0.50); }
double rate_p90(RateAggregator* agg) { return rate_percentile(agg, 0.90); }
double rate_p95(RateAggregator* agg) { return rate_percentile(agg, 0.95); }
double rate_p99(RateAggregator* agg) { return rate_percentile(agg, 0.99); }

double rate_std_dev(RateAggregator* agg) {
    evict_old_events(agg);
    if (agg->count == 0) return 0.0;
    
    double mean_val = rate_mean(agg);
    double variance = 0.0;
    
    for (int i = 0; i < agg->count; i++) {
        double diff = agg->events[i].value - mean_val;
        variance += diff * diff;
    }
    variance /= agg->count;
    
    return rate_round(sqrt(variance), agg->precision);
}

RateMetrics rate_metrics(RateAggregator* agg) {
    RateMetrics m;
    memset(&m, 0, sizeof(RateMetrics));
    
    evict_old_events(agg);
    int cnt = agg->count;
    double secs = agg->window_size_seconds;
    
    m.count = cnt;
    m.rate_per_second = secs > 0 ? rate_round(cnt / secs, agg->precision) : 0;
    m.rate_per_minute = secs > 0 ? rate_round(cnt * 60.0 / secs, agg->precision) : 0;
    m.rate_per_hour = secs > 0 ? rate_round(cnt * 3600.0 / secs, agg->precision) : 0;
    m.sum = rate_sum_internal(agg);
    m.mean = rate_mean(agg);
    m.min = rate_min(agg);
    m.max = rate_max(agg);
    m.p50 = rate_p50(agg);
    m.p90 = rate_p90(agg);
    m.p95 = rate_p95(agg);
    m.p99 = rate_p99(agg);
    m.std_dev = rate_std_dev(agg);
    m.total_hits = agg->total_hits;
    m.total_misses = agg->total_misses;
    m.hit_ratio = rate_hit_ratio(agg);
    m.miss_ratio = rate_miss_ratio(agg);
    
    return m;
}

void rate_clear(RateAggregator* agg) {
    agg->count = 0;
}

void rate_reset_counters(RateAggregator* agg) {
    agg->total_hits = 0;
    agg->total_misses = 0;
}

double rate_window_size(RateAggregator* agg) {
    return agg->window_size_seconds;
}

double rate_round(double value, int precision) {
    double multiplier = pow(10.0, (double)precision);
    return round(value * multiplier) / multiplier;
}

int rate_compare_double(const void* a, const void* b) {
    double da = *(const double*)a;
    double db = *(const double*)b;
    if (da < db) return -1;
    if (da > db) return 1;
    return 0;
}