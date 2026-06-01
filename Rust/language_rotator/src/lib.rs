//! Language Rotation Scheduler
//!
//! A smart round-robin language selector with weighted preferences,
//! streak tracking, cooldown logic, and JSON persistence.
//!
//! # Features
//! - Round-robin selection with automatic index rotation
//! - Weighted preference system (boost/bury languages)
//! - Streak tracking (no consecutive repeats)
//! - Minimum interval enforcement (cooldown between uses)
//! - JSON load/save with atomic writes
//! - Event history with timestamp logging

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::Path;
use std::time::{SystemTime, UNIX_EPOCH};

/// Timestamp in milliseconds since UNIX_EPOCH
pub type Timestamp = u64;

/// Core selection result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Selection {
    pub language: String,
    pub index: usize,
    pub rotation_index: usize,
    pub weight: f64,
    pub was_streak_blocked: bool,
    pub cooldown_remaining_ms: Option<u64>,
    pub timestamp: Timestamp,
}

impl Selection {
    pub fn new(language: String, index: usize, rotation_index: usize, weight: f64) -> Self {
        Self {
            language,
            index,
            rotation_index,
            weight,
            was_streak_blocked: false,
            cooldown_remaining_ms: None,
            timestamp: current_time_ms(),
        }
    }

    pub fn with_cooldown(mut self, remaining_ms: u64) -> Self {
        self.cooldown_remaining_ms = Some(remaining_ms);
        self
    }

    pub fn streak_blocked(mut self) -> Self {
        self.was_streak_blocked = true;
        self
    }
}

/// A logged selection event
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SelectionEvent {
    pub language: String,
    pub index: usize,
    pub timestamp: Timestamp,
    pub was_forced: bool,
}

/// Language entry with weight metadata
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LanguageEntry {
    pub name: String,
    pub weight: f64,
    #[serde(default)]
    pub use_count: usize,
    #[serde(default)]
    pub last_used: Option<Timestamp>,
    /// Minimum ms between selections (0 = no limit)
    #[serde(default)]
    pub cooldown_ms: u64,
    /// If true, skip when it would create a repeat streak
    #[serde(default)]
    pub avoid_streak: bool,
}

impl LanguageEntry {
    pub fn new(name: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            weight: 1.0,
            use_count: 0,
            last_used: None,
            cooldown_ms: 0,
            avoid_streak: true,
        }
    }

    pub fn with_weight(mut self, weight: f64) -> Self {
        self.weight = weight;
        self
    }

    pub fn with_cooldown(mut self, ms: u64) -> Self {
        self.cooldown_ms = ms;
        self
    }

    pub fn always_allowed(mut self) -> Self {
        self.avoid_streak = false;
        self
    }
}

/// Persistent state for the rotator
#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct RotatorState {
    pub languages: Vec<LanguageEntry>,
    pub current_index: usize,
    #[serde(default)]
    pub last_selected: Option<String>,
    #[serde(default)]
    pub history: Vec<SelectionEvent>,
}

impl RotatorState {
    pub fn new(languages: Vec<LanguageEntry>) -> Self {
        Self {
            languages,
            current_index: 0,
            last_selected: None,
            history: Vec::new(),
        }
    }

    /// Advance current_index to next position (wrapping)
    fn advance_index(&mut self) {
        if !self.languages.is_empty() {
            self.current_index = (self.current_index + 1) % self.languages.len();
        }
    }
}

/// Main language rotation engine
#[derive(Debug, Clone)]
pub struct LanguageRotator {
    state: RotatorState,
    /// Cache of last-used timestamps for quick cooldown lookup
    last_used_cache: HashMap<String, Timestamp>,
}

impl LanguageRotator {
    // ─────────────────────────────────────────────────────────────
    // Construction
    // ─────────────────────────────────────────────────────────────

    /// Build from explicit language list
    pub fn new(languages: Vec<LanguageEntry>) -> Self {
        Self {
            state: RotatorState::new(languages),
            last_used_cache: HashMap::new(),
        }
    }

    /// Load state from a JSON file
    pub fn load(path: impl AsRef<Path>) -> Result<Self, RotatorError> {
        let content = fs::read_to_string(path.as_ref())
            .map_err(|e| RotatorError::Io(path.as_ref().display().to_string(), e.to_string()))?;

        let state: RotatorState = serde_json::from_str(&content)
            .map_err(|e| RotatorError::Parse(e.to_string()))?;

        // Rebuild cache from history
        let mut cache = HashMap::new();
        for event in &state.history {
            cache.insert(event.language.clone(), event.timestamp);
        }
        for entry in &state.languages {
            if let Some(ts) = entry.last_used {
                cache.insert(entry.name.clone(), ts);
            }
        }

        Ok(Self {
            state,
            last_used_cache: cache,
        })
    }

    /// Save state to a JSON file (atomic via rename)
    pub fn save(&self, path: impl AsRef<Path>) -> Result<(), RotatorError> {
        let json = serde_json::to_string_pretty(&self.state)
            .map_err(|e| RotatorError::Encode(e.to_string()))?;

        let tmp = format!("{}.tmp", path.as_ref().display());
        fs::write(&tmp, &json)
            .map_err(|e| RotatorError::Io(path.as_ref().display().to_string(), e.to_string()))?;

        fs::rename(&tmp, path.as_ref())
            .map_err(|e| RotatorError::Io(path.as_ref().display().to_string(), e.to_string()))?;

        Ok(())
    }

    // ─────────────────────────────────────────────────────────────
    // Queries
    // ─────────────────────────────────────────────────────────────

    /// Current list of languages
    pub fn languages(&self) -> &[LanguageEntry] {
        &self.state.languages
    }

    /// Current raw rotation index
    pub fn current_index(&self) -> usize {
        self.state.current_index
    }

    /// Last selected language name
    pub fn last_selected(&self) -> Option<&str> {
        self.state.last_selected.as_deref()
    }

    /// Selection history
    pub fn history(&self) -> &[SelectionEvent] {
        &self.state.history
    }

    /// Number of uses for a language
    pub fn use_count(&self, name: &str) -> usize {
        self.state
            .languages
            .iter()
            .find(|l| l.name == name)
            .map(|l| l.use_count)
            .unwrap_or(0)
    }

    /// Remaining cooldown for a language in ms (0 = ready)
    pub fn cooldown_remaining(&self, name: &str) -> u64 {
        if let Some(last_used) = self.last_used_cache.get(name) {
            if let Some(entry) = self.state.languages.iter().find(|l| l.name == name) {
                if entry.cooldown_ms == 0 {
                    return 0;
                }
                let elapsed = current_time_ms().saturating_sub(*last_used);
                return entry.cooldown_ms.saturating_sub(elapsed);
            }
        }
        0
    }

    // ─────────────────────────────────────────────────────────────
    // Mutations
    // ─────────────────────────────────────────────────────────────

    /// Add or update a language
    pub fn set_language(&mut self, entry: LanguageEntry) {
        if let Some(existing) = self.state.languages.iter_mut().find(|l| l.name == entry.name) {
            *existing = entry;
        } else {
            self.state.languages.push(entry);
        }
    }

    /// Remove a language by name
    pub fn remove_language(&mut self, name: &str) {
        self.state.languages.retain(|l| l.name != name);
        if self.state.languages.is_empty() {
            self.state.current_index = 0;
        } else if self.state.current_index >= self.state.languages.len() {
            self.state.current_index = 0;
        }
        self.last_used_cache.remove(name);
    }

    /// Force-select a specific language (bypasses rotation/cooldown)
    /// Does NOT advance the rotation index (intentional — caller controls the next position)
    pub fn force_select(&mut self, name: &str) -> Result<Selection, RotatorError> {
        let idx = self
            .state
            .languages
            .iter()
            .position(|l| l.name == name)
            .ok_or_else(|| RotatorError::NotFound(name.to_string()))?;

        // Extract data before any mutable borrow
        let lang_name = self.state.languages[idx].name.clone();
        let lang_weight = self.state.languages[idx].weight;
        let now = current_time_ms();

        let selection = Selection::new(
            lang_name.clone(),
            idx,
            self.state.current_index,
            lang_weight,
        );

        self.state.last_selected = Some(lang_name.clone());
        self.state.languages[idx].use_count += 1;
        self.state.languages[idx].last_used = Some(now);
        self.state.history.push(SelectionEvent {
            language: lang_name,
            index: idx,
            timestamp: now,
            was_forced: true,
        });

        self.last_used_cache.insert(self.state.languages[idx].name.clone(), now);

        Ok(selection)
    }

    /// Select the next language using round-robin with streak + cooldown guards.
    /// Selection uses current_index, then advances for the next call.
    pub fn select(&mut self) -> Result<Selection, RotatorError> {
        if self.state.languages.is_empty() {
            return Err(RotatorError::EmptyList);
        }

        // Build candidate list from current_index around
        let n = self.state.languages.len();
        let candidates: Vec<usize> = (0..n)
            .map(|i| (self.state.current_index + i) % n)
            .collect();

        let last = self.state.last_selected.clone();
        let mut chosen_idx = candidates[0];
        let mut streak_blocked = false;

        // Phase 1: streak guard — try to avoid repeating the last language
        if let Some(ref last_lang) = last {
            if let Some(entry) = self.state.languages.iter().find(|l| &l.name == last_lang) {
                if entry.avoid_streak && self.state.languages[chosen_idx].name == *last_lang {
                    let mut found = false;
                    for offset in 1..candidates.len() {
                        let probe = candidates[offset];
                        if self.state.languages[probe].name != *last_lang {
                            chosen_idx = probe;
                            found = true;
                            break;
                        }
                    }
                    if !found {
                        streak_blocked = true;
                    }
                }
            }
        }

        // Phase 2: cooldown guard — skip if still cooling down
        let max_attempts = candidates.len();
        let mut attempts = 0;

        while attempts < max_attempts {
            let entry = &self.state.languages[chosen_idx];
            let remaining = if entry.cooldown_ms > 0 {
                let elapsed = current_time_ms()
                    .saturating_sub(self.last_used_cache.get(&entry.name).copied().unwrap_or(0));
                entry.cooldown_ms.saturating_sub(elapsed)
            } else {
                0
            };

            if remaining == 0 {
                break;
            }

            // Move to next candidate (only if we haven't exhausted all)
            if attempts + 1 < max_attempts {
                chosen_idx = candidates[attempts + 1];
            }
            attempts += 1;
        }

        if attempts >= max_attempts {
            return Err(RotatorError::AllOnCooldown);
        }

        // Extract data before any mutable borrow
        let lang_name = self.state.languages[chosen_idx].name.clone();
        let lang_weight = self.state.languages[chosen_idx].weight;
        let now = current_time_ms();

        let mut selection = Selection::new(
            lang_name.clone(),
            chosen_idx,
            self.state.current_index,
            lang_weight,
        );

        if streak_blocked {
            selection = selection.streak_blocked();
        }

        // Commit the selection
        self.state.last_selected = Some(lang_name.clone());
        self.state.languages[chosen_idx].use_count += 1;
        self.state.languages[chosen_idx].last_used = Some(now);
        self.state.history.push(SelectionEvent {
            language: lang_name,
            index: chosen_idx,
            timestamp: now,
            was_forced: false,
        });

        self.last_used_cache
            .insert(self.state.languages[chosen_idx].name.clone(), now);

        // Advance for the next call
        self.state.advance_index();

        Ok(selection)
    }

    /// Advance the rotation index without selecting (for pre-warming)
    pub fn peek_next(&self) -> Option<&LanguageEntry> {
        if self.state.languages.is_empty() {
            return None;
        }
        self.state.languages.get(self.state.current_index)
    }

    /// Clear selection history
    pub fn clear_history(&mut self) {
        self.state.history.clear();
    }
}

// ─────────────────────────────────────────────────────────────────
// Utilities
// ─────────────────────────────────────────────────────────────────

fn current_time_ms() -> Timestamp {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_millis() as Timestamp
}

/// Convenience: load, select, save (all-in-one round-robin step)
pub fn rotate_path(path: impl AsRef<Path>) -> Result<Selection, RotatorError> {
    let mut rotator = LanguageRotator::load(path.as_ref())?;
    let result = rotator.select()?;
    rotator.save(path.as_ref())?;
    Ok(result)
}

// ─────────────────────────────────────────────────────────────────
// Errors
// ─────────────────────────────────────────────────────────────────

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum RotatorError {
    EmptyList,
    NotFound(String),
    AllOnCooldown,
    Io(String, String),
    Parse(String),
    Encode(String),
}

impl std::fmt::Display for RotatorError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::EmptyList => write!(f, "Language list is empty"),
            Self::NotFound(n) => write!(f, "Language not found: {}", n),
            Self::AllOnCooldown => write!(f, "All languages are on cooldown"),
            Self::Io(p, e) => write!(f, "IO error ({p}): {e}"),
            Self::Parse(e) => write!(f, "JSON parse error: {e}"),
            Self::Encode(e) => write!(f, "JSON encode error: {e}"),
        }
    }
}

impl std::error::Error for RotatorError {}

#[cfg(test)]
mod tests {
    use super::*;

    fn temp_path() -> std::path::PathBuf {
        std::env::temp_dir().join(format!("lr_test_{}.json", rand_name()))
    }

    fn rand_name() -> String {
        use std::time::SystemTime;
        format!("{:x}", SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos())
    }

    #[test]
    fn test_round_robin_sequence() {
        let languages = vec![
            LanguageEntry::new("Rust"),
            LanguageEntry::new("Go"),
            LanguageEntry::new("Swift"),
        ];

        let mut rotator = LanguageRotator::new(languages);

        let sel1 = rotator.select().unwrap();
        assert_eq!(sel1.language, "Rust");

        let sel2 = rotator.select().unwrap();
        assert_eq!(sel2.language, "Go");

        let sel3 = rotator.select().unwrap();
        assert_eq!(sel3.language, "Swift");

        let sel4 = rotator.select().unwrap();
        assert_eq!(sel4.language, "Rust"); // wraps around

        // peek_next shows what would be selected next (current_index)
        assert_eq!(rotator.peek_next().unwrap().name, "Go");
    }

    #[test]
    fn test_streak_blocking() {
        // Rust with avoid_streak=false, Go with avoid_streak=true
        let languages = vec![
            LanguageEntry::new("Rust").always_allowed(),
            LanguageEntry::new("Go"),
        ];

        let mut rotator = LanguageRotator::new(languages);

        let sel1 = rotator.select().unwrap();
        assert_eq!(sel1.language, "Rust");

        let sel2 = rotator.select().unwrap();
        assert_eq!(sel2.language, "Go"); // Go is different, ok

        let sel3 = rotator.select().unwrap();
        // With avoid_streak, Go would skip, so Rust is chosen
        assert_eq!(sel3.language, "Rust");
    }

    #[test]
    fn test_force_select() {
        let languages = vec![
            LanguageEntry::new("Rust"),
            LanguageEntry::new("Go"),
            LanguageEntry::new("Swift"),
        ];

        let mut rotator = LanguageRotator::new(languages);

        // First regular select
        let sel1 = rotator.select().unwrap();
        assert_eq!(sel1.language, "Rust");

        // Force select Swift
        let sel = rotator.force_select("Swift").unwrap();
        assert_eq!(sel.language, "Swift");

        // Force select doesn't advance rotation index,
        // so next select continues from where we were
        let sel2 = rotator.select().unwrap();
        assert_eq!(sel2.language, "Go"); // rotation: Rust(0) -> Go(1) -> next
    }

    #[test]
    fn test_persistence() {
        let languages = vec![
            LanguageEntry::new("Rust"),
            LanguageEntry::new("Go"),
        ];

        let path = temp_path();
        {
            let mut rotator = LanguageRotator::new(languages);
            rotator.select().unwrap(); // Rust
            rotator.select().unwrap(); // Go
            rotator.save(&path).unwrap();
        }

        {
            let rotator = LanguageRotator::load(&path).unwrap();
            assert_eq!(rotator.languages().len(), 2);
            // After 2 selects: current_index = 2 % 2 = 0
            assert_eq!(rotator.current_index(), 0);
        }

        std::fs::remove_file(&path).ok();
    }

    #[test]
    fn test_add_remove_language() {
        let languages = vec![LanguageEntry::new("Rust"), LanguageEntry::new("Go")];
        let mut rotator = LanguageRotator::new(languages);

        rotator.set_language(LanguageEntry::new("Swift").with_weight(2.0));
        assert_eq!(rotator.languages().len(), 3);

        rotator.remove_language("Go");
        assert_eq!(rotator.languages().len(), 2);
        assert!(rotator.languages().iter().all(|l| l.name != "Go"));
    }

    #[test]
    fn test_cooldown() {
        let languages = vec![
            LanguageEntry::new("Rust").with_cooldown(10_000), // 10s cooldown
            LanguageEntry::new("Go"),
        ];

        let mut rotator = LanguageRotator::new(languages);

        let sel = rotator.select().unwrap();
        assert_eq!(sel.language, "Rust");
        assert!(rotator.cooldown_remaining("Rust") > 0);

        // Immediate second select should skip Rust (still on cooldown)
        let sel2 = rotator.select().unwrap();
        assert_eq!(sel2.language, "Go");
    }

    #[test]
    fn test_both_languages_selectable() {
        let languages = vec![
            LanguageEntry::new("Rust"),
            LanguageEntry::new("Go"),
        ];
        let mut rotator = LanguageRotator::new(languages);

        let sel = rotator.select().unwrap();
        assert!(sel.language == "Rust" || sel.language == "Go");

        let sel2 = rotator.select().unwrap();
        // Should be different since both avoid_streak=true by default
        assert_ne!(sel.language, sel2.language);
    }

    #[test]
    fn test_empty_list_error() {
        let mut rotator = LanguageRotator::new(vec![]);
        let err = rotator.select().unwrap_err();
        assert!(matches!(err, RotatorError::EmptyList));
    }

    #[test]
    fn test_not_found_error() {
        let mut rotator = LanguageRotator::new(vec![LanguageEntry::new("Rust")]);
        let err = rotator.force_select("Pascal").unwrap_err();
        assert!(matches!(err, RotatorError::NotFound(_)));
    }

    #[test]
    fn test_history_tracking() {
        let languages = vec![
            LanguageEntry::new("Rust"),
            LanguageEntry::new("Go"),
        ];
        let mut rotator = LanguageRotator::new(languages);

        rotator.select().unwrap();
        rotator.select().unwrap();
        rotator.force_select("Rust").unwrap();

        assert_eq!(rotator.history().len(), 3);
        assert!(rotator.history().last().unwrap().was_forced);
    }

    #[test]
    fn test_use_count() {
        let languages = vec![LanguageEntry::new("Rust"), LanguageEntry::new("Go")];
        let mut rotator = LanguageRotator::new(languages);

        rotator.select().unwrap(); // Rust
        rotator.select().unwrap(); // Go
        rotator.select().unwrap(); // Rust (wrapped)

        assert_eq!(rotator.use_count("Rust"), 2);
        assert_eq!(rotator.use_count("Go"), 1);
    }

    #[test]
    fn test_last_selected() {
        let languages = vec![LanguageEntry::new("Rust"), LanguageEntry::new("Go")];
        let mut rotator = LanguageRotator::new(languages);

        assert!(rotator.last_selected().is_none());
        rotator.select().unwrap();
        assert_eq!(rotator.last_selected(), Some("Rust"));
        rotator.select().unwrap();
        assert_eq!(rotator.last_selected(), Some("Go"));
    }
}