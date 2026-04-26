//! Comprehensive tests for text_distance_utils
//!
//! Tests all distance and similarity algorithms.

use text_distance_utils::*;

#[cfg(test)]
mod hamming_tests {
    use super::*;

    #[test]
    fn test_equal_strings() {
        assert_eq!(hamming_distance("hello", "hello"), Ok(0));
        assert_eq!(hamming_distance("", ""), Ok(0));
        assert_eq!(hamming_distance("abc", "abc"), Ok(0));
    }

    #[test]
    fn test_one_difference() {
        assert_eq!(hamming_distance("hello", "hallo"), Ok(1));
        assert_eq!(hamming_distance("cat", "bat"), Ok(1));
        assert_eq!(hamming_distance("dog", "dig"), Ok(1));
    }

    #[test]
    fn test_multiple_differences() {
        assert_eq!(hamming_distance("karolin", "kathrin"), Ok(3));
        assert_eq!(hamming_distance("0000", "1111"), Ok(4));
        assert_eq!(hamming_distance("abcdef", "fedcba"), Ok(6));
    }

    #[test]
    fn test_unicode_strings() {
        assert_eq!(hamming_distance("你好世界", "你好世异"), Ok(1));
        assert_eq!(hamming_distance("日本語", "日本国"), Ok(1));
    }

    #[test]
    fn test_different_lengths() {
        assert!(hamming_distance("hello", "hi").is_err());
        assert!(hamming_distance("short", "verylongstring").is_err());
        assert!(hamming_distance("", "a").is_err());
    }

    #[test]
    fn test_similarity() {
        assert_eq!(hamming_similarity("hello", "hello"), Ok(1.0));
        assert_eq!(hamming_similarity("karolin", "kathrin"), Ok(4.0 / 7.0));
    }
}

#[cfg(test)]
mod levenshtein_tests {
    use super::*;

    #[test]
    fn test_empty_strings() {
        assert_eq!(levenshtein_distance("", ""), 0);
        assert_eq!(levenshtein_distance("", "hello"), 5);
        assert_eq!(levenshtein_distance("hello", ""), 5);
    }

    #[test]
    fn test_identical_strings() {
        assert_eq!(levenshtein_distance("hello", "hello"), 0);
        assert_eq!(levenshtein_distance("abc", "abc"), 0);
    }

    #[test]
    fn test_single_operations() {
        // Single substitution
        assert_eq!(levenshtein_distance("cat", "bat"), 1);
        assert_eq!(levenshtein_distance("hello", "hallo"), 1);

        // Single insertion
        assert_eq!(levenshtein_distance("cat", "cats"), 1);
        assert_eq!(levenshtein_distance("abc", "abcd"), 1);

        // Single deletion
        assert_eq!(levenshtein_distance("cats", "cat"), 1);
        assert_eq!(levenshtein_distance("abcd", "abc"), 1);
    }

    #[test]
    fn test_multiple_operations() {
        assert_eq!(levenshtein_distance("kitten", "sitting"), 3);
        assert_eq!(levenshtein_distance("book", "back"), 2);
        assert_eq!(levenshtein_distance("saturday", "sunday"), 3);
    }

    #[test]
    fn test_unicode_strings() {
        assert_eq!(levenshtein_distance("你好世界", "你好世异"), 1);
        assert_eq!(levenshtein_distance("日本語", "日本国"), 1);
    }

    #[test]
    fn test_similarity() {
        assert_eq!(levenshtein_similarity("hello", "hello"), 1.0);
        assert_eq!(levenshtein_similarity("", ""), 1.0);

        let sim = levenshtein_similarity("kitten", "sitting");
        assert!(sim > 0.4 && sim < 0.6);
    }
}

#[cfg(test)]
mod damerau_levenshtein_tests {
    use super::*;

    #[test]
    fn test_transposition() {
        // Transposition counts as 1 edit
        assert_eq!(damerau_levenshtein_distance("ca", "ac"), 1);
        assert_eq!(damerau_levenshtein_distance("abcd", "acbd"), 1);
        assert_eq!(damerau_levenshtein_distance("ab", "ba"), 1);
    }

    #[test]
    fn test_multiple_transpositions() {
        assert_eq!(damerau_levenshtein_distance("abc", "cba"), 2);
    }

    #[test]
    fn test_combined_operations() {
        assert_eq!(damerau_levenshtein_distance("ca", "abc"), 2);
    }

    #[test]
    fn test_empty_strings() {
        assert_eq!(damerau_levenshtein_distance("", ""), 0);
        assert_eq!(damerau_levenshtein_distance("", "abc"), 3);
        assert_eq!(damerau_levenshtein_distance("abc", ""), 3);
    }

    #[test]
    fn test_identical_strings() {
        assert_eq!(damerau_levenshtein_distance("hello", "hello"), 0);
    }
}

#[cfg(test)]
mod jaro_tests {
    use super::*;

    #[test]
    fn test_identical_strings() {
        assert_eq!(jaro_similarity("hello", "hello"), 1.0);
        assert_eq!(jaro_similarity("", ""), 1.0);
        assert_eq!(jaro_similarity("abc", "abc"), 1.0);
    }

    #[test]
    fn test_empty_strings() {
        assert_eq!(jaro_similarity("", "hello"), 0.0);
        assert_eq!(jaro_similarity("hello", ""), 0.0);
    }

    #[test]
    fn test_no_common_chars() {
        assert_eq!(jaro_similarity("abc", "xyz"), 0.0);
    }

    #[test]
    fn test_known_values() {
        // MARTHA vs MARHTA: known to be ~0.944
        let sim = jaro_similarity("MARTHA", "MARHTA");
        assert!((sim - 0.944).abs() < 0.01);

        // DWAYNE vs DUANE: known to be ~0.82
        let sim = jaro_similarity("DWAYNE", "DUANE");
        assert!((sim - 0.82).abs() < 0.02);
    }

    #[test]
    fn test_unicode_strings() {
        assert!(jaro_similarity("你好世界", "你好世异") > 0.9);
    }
}

#[cfg(test)]
mod jaro_winkler_tests {
    use super::*;

    #[test]
    fn test_identical_strings() {
        assert_eq!(jaro_winkler_similarity("hello", "hello"), 1.0);
        assert_eq!(jaro_winkler_similarity("", ""), 1.0);
    }

    #[test]
    fn test_empty_strings() {
        assert_eq!(jaro_winkler_similarity("", "hello"), 0.0);
        assert_eq!(jaro_winkler_similarity("hello", ""), 0.0);
    }

    #[test]
    fn test_prefix_bonus() {
        // Jaro-Winkler should give higher score than Jaro for matching prefixes
        let jaro_sim = jaro_similarity("MARTHA", "MARHTA");
        let jw_sim = jaro_winkler_similarity("MARTHA", "MARHTA");
        assert!(jw_sim > jaro_sim);

        // Known value for MARTHA vs MARHTA: ~0.961
        assert!((jw_sim - 0.961).abs() < 0.01);
    }

    #[test]
    fn test_no_prefix_match() {
        // When there's no common prefix, Jaro-Winkler equals Jaro
        let jaro_sim = jaro_similarity("abc", "xyz");
        let jw_sim = jaro_winkler_similarity("abc", "xyz");
        assert_eq!(jaro_sim, jw_sim);
    }
}

#[cfg(test)]
mod ngram_tests {
    use super::*;

    #[test]
    fn test_generate_ngrams() {
        let ngrams = generate_ngrams("hello", 2);
        assert!(ngrams.contains("he"));
        assert!(ngrams.contains("el"));
        assert!(ngrams.contains("ll"));
        assert!(ngrams.contains("lo"));
        assert_eq!(ngrams.len(), 4);

        let ngrams = generate_ngrams("hello", 3);
        assert!(ngrams.contains("hel"));
        assert!(ngrams.contains("ell"));
        assert!(ngrams.contains("llo"));
        assert_eq!(ngrams.len(), 3);
    }

    #[test]
    fn test_empty_string_ngrams() {
        assert!(generate_ngrams("", 2).is_empty());
        assert!(generate_ngrams("a", 2).is_empty());
    }

    #[test]
    fn test_ngram_similarity() {
        assert_eq!(ngram_similarity("hello", "hello", 2), 1.0);
        assert!(ngram_similarity("hello", "hella", 2) > 0.5);
        assert!(ngram_similarity("hello", "xyz", 2) < 0.2);
    }
}

#[cfg(test)]
mod dice_tests {
    use super::*;

    #[test]
    fn test_identical_strings() {
        assert_eq!(dice_coefficient("hello", "hello"), 1.0);
    }

    #[test]
    fn test_empty_strings() {
        assert_eq!(dice_coefficient("", ""), 1.0);
        assert_eq!(dice_coefficient("", "hello"), 0.0);
        assert_eq!(dice_coefficient("hello", ""), 0.0);
    }

    #[test]
    fn test_known_values() {
        // night vs nacht: known to be ~0.25
        let coef = dice_coefficient("night", "nacht");
        assert!((coef - 0.25).abs() < 0.1);
    }

    #[test]
    fn test_no_common_bigrams() {
        assert_eq!(dice_coefficient("abc", "xyz"), 0.0);
    }
}

#[cfg(test)]
mod cosine_tests {
    use super::*;

    #[test]
    fn test_identical_strings() {
        assert_eq!(cosine_similarity("hello world", "hello world"), 1.0);
        assert_eq!(cosine_similarity("", ""), 1.0);
    }

    #[test]
    fn test_no_common_words() {
        assert_eq!(cosine_similarity("hello world", "foo bar"), 0.0);
    }

    #[test]
    fn test_same_words_different_order() {
        // Bag of words approach - order doesn't matter
        assert_eq!(cosine_similarity("hello world", "world hello"), 1.0);
    }

    #[test]
    fn test_partial_overlap() {
        let sim = cosine_similarity("the quick brown fox", "the quick blue cat");
        assert!(sim > 0.0 && sim < 1.0);
        assert!((sim - 0.5).abs() < 0.1); // 2 of 4 unique words overlap
    }

    #[test]
    fn test_case_insensitive() {
        assert_eq!(cosine_similarity("Hello World", "hello world"), 1.0);
    }

    #[test]
    fn test_cosine_ngram_similarity() {
        assert_eq!(cosine_ngram_similarity("hello", "hello", 2), 1.0);
        assert!(cosine_ngram_similarity("hello", "hella", 2) > 0.0);
    }
}

#[cfg(test)]
mod overlap_tests {
    use super::*;

    #[test]
    fn test_identical_strings() {
        assert_eq!(overlap_coefficient("hello world", "hello world"), 1.0);
    }

    #[test]
    fn test_empty_strings() {
        assert_eq!(overlap_coefficient("", ""), 1.0);
        assert_eq!(overlap_coefficient("", "hello"), 0.0);
    }

    #[test]
    fn test_subset() {
        // One string's words are subset of other's
        assert_eq!(overlap_coefficient("hello world", "hello"), 1.0);
        assert_eq!(overlap_coefficient("hello", "hello world"), 1.0);
    }

    #[test]
    fn test_partial_overlap() {
        let coef = overlap_coefficient("hello world test", "hello foo");
        assert!((coef - 0.5).abs() < 0.1);
    }
}

#[cfg(test)]
mod qgram_tests {
    use super::*;

    #[test]
    fn test_identical_strings() {
        assert_eq!(qgram_distance("hello", "hello", 2), 0);
        assert_eq!(qgram_distance("hello", "hello", 3), 0);
    }

    #[test]
    fn test_different_strings() {
        assert!(qgram_distance("hello", "world", 2) > 0);
        assert!(qgram_distance("hello", "world", 3) > 0);
    }
}

#[cfg(test)]
mod matching_tests {
    use super::*;

    #[test]
    fn test_best_match() {
        let candidates = vec!["hello", "hallo", "hola", "hi"];
        let result = best_match("hell", &candidates);
        assert!(result.is_some());

        let (idx, score) = result.unwrap();
        assert_eq!(idx, 0); // "hello" should be best match
        assert!(score > 0.7);
    }

    #[test]
    fn test_best_match_empty() {
        let candidates: Vec<&str> = vec![];
        assert!(best_match("test", &candidates).is_none());
    }

    #[test]
    fn test_find_matches() {
        let candidates = vec!["hello", "hallo", "world", "help"];
        let matches = find_matches("hell", &candidates, 0.5);
        assert!(!matches.is_empty());

        // Should match "hello", "hallo", and possibly "help"
        let matched_indices: Vec<usize> = matches.iter().map(|(i, _)| *i).collect();
        assert!(matched_indices.contains(&0));
        assert!(matched_indices.contains(&1));
    }

    #[test]
    fn test_find_matches_no_matches() {
        let candidates = vec!["xyz", "abc"];
        let matches = find_matches("hello", &candidates, 0.5);
        assert!(matches.is_empty());
    }
}

#[cfg(test)]
mod compare_tests {
    use super::*;

    #[test]
    fn test_compare_strings() {
        let metrics = compare_strings("kitten", "sitting");

        // Check that all expected metrics are present
        assert!(metrics.contains_key("levenshtein_distance"));
        assert!(metrics.contains_key("jaro_similarity"));
        assert!(metrics.contains_key("jaro_winkler_similarity"));
        assert!(metrics.contains_key("dice_coefficient"));
        assert!(metrics.contains_key("cosine_similarity"));

        // Check known values
        assert_eq!(metrics.get("levenshtein_distance").unwrap(), 3.0);
        assert!(metrics.get("jaro_similarity").unwrap() > 0.0);
    }

    #[test]
    fn test_compare_identical_strings() {
        let metrics = compare_strings("hello", "hello");

        // All distances should be 0
        assert_eq!(metrics.get("levenshtein_distance").unwrap(), 0.0);

        // All similarities should be 1.0
        assert_eq!(metrics.get("levenshtein_similarity").unwrap(), 1.0);
        assert_eq!(metrics.get("jaro_similarity").unwrap(), 1.0);
        assert_eq!(metrics.get("jaro_winkler_similarity").unwrap(), 1.0);
        assert_eq!(metrics.get("dice_coefficient").unwrap(), 1.0);
        assert_eq!(metrics.get("cosine_similarity").unwrap(), 1.0);
    }
}

#[cfg(test)]
mod osa_tests {
    use super::*;

    #[test]
    fn test_transposition() {
        // Single transposition
        assert_eq!(osa_distance("ab", "ba"), 1);
        assert_eq!(osa_distance("abcd", "acbd"), 1);
    }

    #[test]
    fn test_combined_operations() {
        assert_eq!(osa_distance("ca", "abc"), 3);
    }

    #[test]
    fn test_empty_strings() {
        assert_eq!(osa_distance("", ""), 0);
        assert_eq!(osa_distance("", "abc"), 3);
        assert_eq!(osa_distance("abc", ""), 3);
    }
}

#[cfg(test)]
mod integration_tests {
    use super::*;

    #[test]
    fn test_typo_detection() {
        let candidates = vec![
            "hello",
            "help",
            "held",
            "helicopter",
            "helix",
            "helmet",
            "helper",
        ];

        // Common typos should match closest word
        let (idx, score) = best_match("helo", &candidates).unwrap();
        assert_eq!(idx, 0); // Should match "hello"
        assert!(score > 0.8);

        let (idx, score) = best_match("helpp", &candidates).unwrap();
        assert_eq!(idx, 1); // Should match "help"
        assert!(score > 0.8);
    }

    #[test]
    fn test_fuzzy_search() {
        let dictionary = vec![
            "apple",
            "banana",
            "cherry",
            "date",
            "elderberry",
            "fig",
            "grape",
        ];

        // Search for fruit with typos
        let matches = find_matches("appl", &dictionary, 0.6);
        assert!(!matches.is_empty());
        assert!(matches.iter().any(|(i, _)| *i == 0)); // Should find "apple"

        let matches = find_matches("bnana", &dictionary, 0.6);
        assert!(!matches.is_empty());
        assert!(matches.iter().any(|(i, _)| *i == 1)); // Should find "banana"
    }

    #[test]
    fn test_name_matching() {
        let names = vec!["John Smith", "John Smyth", "Jon Smith", "Jane Smith"];

        // Find all John Smith variations
        let matches = find_matches("John Smith", &names, 0.85);
        assert!(matches.len() >= 2); // Should match at least "John Smith" and "John Smyth"
    }
}