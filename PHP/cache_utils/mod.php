<?php
/**
 * AllToolkit - PHP Cache Utilities
 *
 * A comprehensive file-based caching utility module providing TTL support,
 * cache tags, statistics, and various caching strategies with zero dependencies.
 *
 * @package AllToolkit
 * @author AllToolkit Team
 * @license MIT
 */

namespace AllToolkit;

/**
 * Cache entry metadata structure
 */
class CacheEntry {
    public $key;
    public $value;
    public $expires;
    public $created;
    public $tags;
    public $hits;

    public function __construct(string $key, $value, int $expires, array $tags = []) {
        $this->key = $key;
        $this->value = $value;
        $this->expires = $expires;
        $this->created = time();
        $this->tags = $tags;
        $this->hits = 0;
    }

    public function isExpired(): bool {
        return $this->expires > 0 && time() > $this->expires;
    }

    public function getAge(): int {
        return time() - $this->created;
    }

    public function getTtl(): ?int {
        if ($this->expires <= 0) {
            return null;
        }
        $remaining = $this->expires - time();
        return max(0, $remaining);
    }
}

class CacheStats {
    public $entries = 0;
    public $expired = 0;
    public $hits = 0;
    public $misses = 0;
    public $size = 0;

    public function getHitRate(): float {
        $total = $this->hits + $this->misses;
        return $total > 0 ? ($this->hits / $total) * 100 : 0;
    }

    public function getMissRate(): float {
        return 100 - $this->getHitRate();
    }
}

class CacheOptions {
    public $directory;
    public $defaultTtl = 3600;
    public $maxSize = 0;
    public $maxEntries = 0;
    public $autoClean = true;
    public $extension = '.cache';

    public function __construct(array $options = []) {
        $this->directory = $options['directory'] ?? sys_get_temp_dir() . '/alltoolkit_cache';
        $this->defaultTtl = $options['defaultTtl'] ?? 3600;
        $this->maxSize = $options['maxSize'] ?? 0;
        $this->maxEntries = $options['maxEntries'] ?? 0;
        $this->autoClean = $options['autoClean'] ?? true;
        $this->extension = $options['extension'] ?? '.cache';
    }
}

class Cache {
    private $options;
    private $directory;
    private $currentSize = 0;
    private $entryCount = 0;

    public function __construct($options = []) {
        if ($options instanceof CacheOptions) {
            $this->options = $options;
        } else {
            $this->options = new CacheOptions($options);
        }
        $this->directory = rtrim($this->options->directory, '/\\');
        $this->ensureDirectory();
        $this->initializeStats();
    }

    private function ensureDirectory(): void {
        if (!is_dir($this->directory)) {
            @mkdir($this->directory, 0755, true);
        }
    }

    private function initializeStats(): void {
        $this->currentSize = 0;
        $this->entryCount = 0;
        if (is_dir($this->directory)) {
            $files = glob($this->directory . '/*' . $this->options->extension);
            if ($files) {
                foreach ($files as $file) {
                    $this->currentSize += filesize($file);
                    $this->entryCount++;
                }
            }
        }
    }

    private function getFilePath(string $key): string {
        $safeKey = preg_replace('/[^a-zA-Z0-9_-]/', '_', $key);
        return $this->directory . '/' . $safeKey . $this->options->extension;
    }

    private function normalizeTtl(?int $ttl = null): int {
        if ($ttl === null) {
            $ttl = $this->options->defaultTtl;
        }
        return $ttl > 0 ? time() + $ttl : 0;
    }

    public function set(string $key, $value, ?int $ttl = null, array $tags = []): bool {
        $this->ensureDirectory();
        if ($this->options->maxEntries > 0 && $this->entryCount >= $this->options->maxEntries) {
            if (!$this->evictOldest()) {
                return false;
            }
        }
        $entry = new CacheEntry($key, $value, $this->normalizeTtl($ttl), $tags);
        $data = serialize($entry);
        $dataSize = strlen($data);
        if ($this->options->maxSize > 0 && ($this->currentSize + $dataSize) > $this->options->maxSize) {
            if (!$this->evictBySize($dataSize)) {
                return false;
            }
        }
        $filePath = $this->getFilePath($key);
        $result = file_put_contents($filePath, $data, LOCK_EX);
        if ($result !== false) {
            $this->currentSize += $dataSize;
            $this->entryCount++;
            return true;
        }
        return false;
    }

    public function get(string $key, $default = null) {
        $filePath = $this->getFilePath($key);
        if (!file_exists($filePath)) {
            return $default;
        }
        $data = file_get_contents($filePath);
        if ($data === false) {
            return $default;
        }
        $entry = unserialize($data);
        if (!($entry instanceof CacheEntry)) {
            return $default;
        }
        if ($entry->isExpired()) {
            if ($this->options->autoClean) {
                $this->delete($key);
            }
            return $default;
        }
        $entry->hits++;
        file_put_contents($filePath, serialize($entry), LOCK_EX);
        return $entry->value;
    }

    public function has(string $key): bool {
        $filePath = $this->getFilePath($key);
        if (!file_exists($filePath)) {
            return false;
        }
        $data = file_get_contents($filePath);
        if ($data === false) {
            return false;
        }
        $entry = unserialize($data);
        if (!($entry instanceof CacheEntry)) {
            return false;
        }
        if ($entry->isExpired()) {
            if ($this->options->autoClean) {
                $this->delete($key);
            }
            return false;
        }
        return true;
    }

    public function delete(string $key): bool {
        $filePath = $this->getFilePath($key);
        if (file_exists($filePath)) {
            $size = filesize($filePath);
            if (unlink($filePath)) {
                $this->currentSize -= $size;
                $this->entryCount--;
                return true;
            }
        }
        return false;
    }

    public function getEntry(string $key): ?CacheEntry {
        $filePath = $this->getFilePath($key);
        if (!file_exists($filePath)) {
            return null;
        }
        $data = file_get_contents($filePath);
        if ($data === false) {
            return null;
        }
        $entry = unserialize($data);
        if (!($entry instanceof CacheEntry)) {
            return null;
        }
        if ($entry->isExpired()) {
            if ($this->options->autoClean) {
                $this->delete($key);
            }
            return null;
        }
        return $entry;
    }

    public function getOrSet(string $key, callable $callback, ?int $ttl = null, array $tags = []) {
        $value = $this->get($key);
        if ($value !== null) {
            return $value;
        }
        $value = $callback();
        $this->set($key, $value, $ttl, $tags);
        return $value;
    }

    public function remember(string $key, callable $callback, ?int $ttl = null, array $tags = []) {
        return $this->getOrSet($key, $callback, $ttl, $tags);
    }

    public function increment(string $key, int $step = 1, ?int $ttl = null): int {
        $value = $this->get($key, 0);
        if (!is_numeric($value)) {
            $value = 0;
        }
        $newValue = $value + $step;
        $this->set($key, $newValue, $ttl);
        return $newValue;
    }

    public function decrement(string $key, int $step = 1, ?int $ttl = null): int {
        return $this->increment($key, -$step, $ttl);
    }

    public function flush(): bool {
        if (!is_dir($this->directory)) {
            return true;
        }
        $files = glob($this->directory . '/*' . $this->options->extension);
        if ($files) {
            foreach ($files as $file) {
                @unlink($file);
            }
        }
        $this->currentSize = 0;
        $this->entryCount = 0;
        return true;
    }

    public function flushExpired(): int {
        $count = 0;
        if (!is_dir($this->directory)) {
            return $count;
        }
        $files = glob($this->directory . '/*' . $this->options->extension);
        if ($files) {
            foreach ($files as $file) {
                $data = @file_get_contents($file);
                if ($data !== false) {
                    $entry = @unserialize($data);
                    if ($entry instanceof CacheEntry && $entry->isExpired()) {
                        if (@unlink($file)) {
                            $count++;
                            $this->currentSize -= strlen($data);
                            $this->entryCount--;
                        }
                    }
                }
            }
        }
        return $count;
    }

    public function flushByTag(string $tag): int {
        $count = 0;
        if (!is_dir($this->directory)) {
            return $count;
        }
        $files = glob($this->directory . '/*' . $this->options->extension);
        if ($files) {
            foreach ($files as $file) {
                $data = @file_get_contents($file);
                if ($data !== false) {
                    $entry = @unserialize($data);
                    if ($entry instanceof CacheEntry && in_array($tag, $entry->tags)) {
                        if (@unlink($file)) {
                            $count++;
                            $this->currentSize -= strlen($data);
                            $this->entryCount--;
                        }
                    }
                }
            }
        }
        return $count;
    }

    public function flushByTags(array $tags): int {
        $count = 0;
        if (!is_dir($this->directory) || empty($tags)) {
            return $count;
        }
        $files = glob($this->directory . '/*' . $this->options->extension);
        if ($files) {
            foreach ($files as $file) {
                $data = @file_get_contents($file);
                if ($data !== false) {
                    $entry = @unserialize($data);
                    if ($entry instanceof CacheEntry) {
                        $hasTag = false;
                        foreach ($tags as $tag) {
                            if (in_array($tag, $entry->tags)) {
                                $hasTag = true;
                                break;
                            }
                        }
                        if ($hasTag) {
                            if (@unlink($file)) {
                                $count++;
                                $this->currentSize -= strlen($data);
                                $this->entryCount--;
                            }
                        }
                    }
                }
            }
        }
        return $count;
    }

    public function getKeys(): array {
        $keys = [];
        if (!is_dir($this->directory)) {
            return $keys;
        }
        $files = glob($this->directory . '/*' . $this->options->extension);
        if ($files) {
            foreach ($files as $file) {
                $data = @file_get_contents($file);
                if ($data !== false) {
                    $entry = @unserialize($data);
                    if ($entry instanceof CacheEntry && !$entry->isExpired()) {
                        $keys[] = $entry->key;
                    }
                }
            }
        }
        return $keys;
    }

    public function getKeysByTag(string $tag): array {
        $keys = [];
        if (!is_dir($this->directory)) {
            return $keys;
        }
        $files = glob($this->directory . '/*' . $this->options->extension);
        if ($files) {
            foreach ($files as $file) {
                $data = @file_get_contents($file);
                if ($data !== false) {
                    $entry = @unserialize($data);
                    if ($entry instanceof CacheEntry && !$entry->isExpired() && in_array($tag, $entry->tags)) {
                        $keys[] = $entry->key;
                    }
                }
            }
        }
        return $keys;
    }

    public function getTags(): array {
        $tags = [];
        if (!is_dir($this->directory)) {
            return $tags;
        }
        $files = glob($this->directory . '/*' . $this->options->extension);
        if ($files) {
            foreach ($files as $file) {
                $data = @file_get_contents($file);
                if ($data !== false) {
                    $entry = @unserialize($data);
                    if ($entry instanceof CacheEntry && !$entry->isExpired()) {
                        foreach ($entry->tags as $tag) {
                            if (!in_array($tag, $tags)) {
                                $tags[] = $tag;
                            }
                        }
                    }
                }
            }
        }
        return $tags;
    }

    public function stats(): CacheStats {
        $stats = new CacheStats();
        if (!is_dir($this->directory)) {
            return $stats;
        }
        $files = glob($this->directory . '/*' . $this->options->extension);
        if ($files) {
            foreach ($files as $file) {
                $data = @file_get_contents($file);
                if ($data !== false) {
                    $entry = @unserialize($data);
                    if ($entry instanceof CacheEntry) {
                        $stats->size += strlen($data);
                        if ($entry->isExpired()) {
                            $stats->expired++;
                        } else {
                            $stats->entries++;
                        }
                        $stats->hits += $entry->hits;
                    }
                }
            }
        }
        return $stats;
    }

    public function size(): int {
        return $this->currentSize;
    }

    public function count(): int {
        return $this->entryCount;
    }

    private function evictOldest(): bool {
        $oldestFile = null;
        $oldestTime = PHP_INT_MAX;
        if (!is_dir($this->directory)) {
            return false;
        }
        $files = glob($this->directory . '/*' . $this->options->extension);
        if ($files) {
            foreach ($files as $file) {
                $mtime = filemtime($file);
                if ($mtime < $oldestTime) {
                    $oldestTime = $mtime;
                    $oldestFile = $file;
                }
            }
        }
        if ($oldestFile !== null) {
            $size = filesize($oldestFile);
            if (@unlink($oldestFile)) {
                $this->currentSize -= $size;
                $this->entryCount--;
                return true;
            }
        }
        return false;
    }

    private function evictBySize(int $neededSize): bool {
        $freed = 0;
        $target = $neededSize + ($this->options->maxSize * 0.1);
        while ($freed < $target) {
            if (!$this->evictOldest()) {
                return false;
            }
            $freed += $this->currentSize;
        }
        return true;
    }

    public function touch(string $key): bool {
        $entry = $this->getEntry($key);
        if ($entry === null) {
            return false;
        }
        return $this->set($key, $entry->value, $this->options->defaultTtl, $entry->tags);
    }

    public function ttl(string $key): ?int {
        $entry = $this->getEntry($key);
        return $entry !== null ? $entry->getTtl() : null;
    }

    public function expiresAt(string $key): ?int {
        $entry = $this->getEntry($key);
        return $entry !== null ? ($entry->expires > 0 ? $entry->expires : null) : null;
    }

    public function add(string $key, $value, ?int $ttl = null, array $tags = []): bool {
        if ($this->has($key)) {
            return false;
        }
        return $this->set($key, $value, $ttl, $tags);
    }

    public function forever(string $key, $value, array $tags = []): bool {
        return $this->set($key, $value, 0, $tags);
    }

    public function pull(string $key, $default = null) {
        $value = $this->get($key, $default);
        $this->delete($key);
        return $value;
    }

    public function many(array $keys): array {
        $result = [];
        foreach ($keys as $key) {
            $result[$key] = $this->get($key);
        }
        return $result;
    }

    public function putMany(array $values, ?int $ttl = null, array $tags = []): bool {
        $success = true;
        foreach ($values as $key => $value) {
            if (!$this->set($key, $value, $ttl, $tags)) {
                $success = false;
            }
        }
        return $success;
    }

    public function deleteMultiple(array $keys): int {
        $count = 0;
        foreach ($keys as $key) {
            if ($this->delete($key)) {
                $count++;
            }
        }
        return $count;
    }

    public function isEmpty(): bool {
        return $this->entryCount === 0;
    }

    public function isNotEmpty(): bool {
        return !$this->isEmpty();
    }
}
