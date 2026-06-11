#!/usr/bin/env python3
"""
🌦️ Polyglot Weather v1.0
A "language weather forecaster" — treats programming languages as atmospheric
pressure systems and forecasts their interactions, front collisions, and
seasonal patterns across the ecosystem.

Creative concept: "Languages are weather systems. High-pressure languages
bring stability; low-pressure zones bring disruption. When two language
fronts meet, expect turbulence — and opportunity."

The tool generates:
  1. A "weather report" for the current rotation language (its atmospheric pressure, temperature, humidity)
  2. Collision forecasts — what happens when this language meets another front
  3. Seasonal patterns — how the language's influence waxes and wanes
  4. Ecosystem barometric pressure — overall health of each language's ecosystem

Each run reads language_rotation.json, generates a weather report for the
current language, updates the index, and commits to git.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust

Distinct from existing tools:
  - polyglot_digest:      syntax-parallel snippets (static comparison)
  - polyglot_bridges:     problem→solution maps (conceptual)
  - polyglot_resonator:   harmonic relationships (frequency lens)
  - polyglot_dna:         genetic trait mapping (trait lens)
  - polyglot_chronicle:   daily history (temporal)
  - polyglot_flavor:      sensory tasting notes (sensory lens)
  - polyglot_code_printer: code postcard aesthetic (visual)
  - polyglot_meridian:    spectral positioning (coordinate lens)
  - polyglot_translation: cultural linguistics (cultural lens)
  - polyglot_cipher:      cryptographic puzzles (crypto lens)
  - polyglot_ecosystem_map: ecosystem graph (graph lens)

Weather is about ATMOSPHERIC DYNAMICS — how language "pressure systems"
interact, collide, and create opportunities in the ecosystem.
"""

import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-weather"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = str(
    Path(__file__).parent.parent.parent / "language_rotation.json"
)

# The 8-language rotation sequence
ROTATION_ORDER = [
    "Rust",
    "Go",
    "Swift",
    "Kotlin",
    "TypeScript",
    "JavaScript",
    "Java",
    "C/C++",
]


# ── Language atmospheric profiles ─────────────────────────────────────────────
# Each language has atmospheric characteristics:
#   pressure_index   — ecosystem stability (0.0=volatile, 1.0=stable)
#   temperature      — development activity/heat (0=cold/rare, 100=hot/ubiquitous)
#   humidity         — complexity of the language (0=minimalist, 100=massive/bloated)
#   wind_speed       — evolution/change velocity (0=slow/stable, 100=fast/churning)
#   visibility       — job market demand (0=obscure, 100=omnipresent)
#   forecast         — outlook for next 6 months

LANGUAGE_ATMOSPHERE: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "pressure_index": 0.85,
        "temperature": 78,
        "humidity": 55,
        "wind_speed": 65,
        "visibility": 55,
        "forecast": "Clearing — memory safety awareness driving adoption",
        "pressure_trend": "rising",
        "conditions": "Systems-level adoption accelerating in cloud and security sectors",
        "precipitation_risk": "low",
        "notable_fronts": [
            {"lang": "C/C++", "interaction": "Displacement pressure: Rust gaining ground in systems programming"},
            {"lang": "Go", "interaction": "Convergence zone: both targeting cloud infrastructure"},
        ],
    },
    "Go": {
        "pressure_index": 0.92,
        "temperature": 82,
        "humidity": 40,
        "wind_speed": 45,
        "visibility": 72,
        "forecast": "Fair — cloud-native adoption remains strong",
        "pressure_trend": "stable",
        "conditions": "Kubernetes and cloud backend ecosystem remains mature and stable",
        "precipitation_risk": "low",
        "notable_fronts": [
            {"lang": "Rust", "interaction": "Convergence zone: both targeting cloud infrastructure"},
            {"lang": "Java", "interaction": "Warm front collision: Go encroaching on Java backend territory"},
        ],
    },
    "Swift": {
        "pressure_index": 0.78,
        "temperature": 65,
        "humidity": 50,
        "wind_speed": 35,
        "visibility": 45,
        "forecast": "Partly cloudy — Apple ecosystem locked but steady",
        "pressure_trend": "stable",
        "conditions": "iOS/macOS development remains essential; server-side Swift gaining slowly",
        "precipitation_risk": "medium",
        "notable_fronts": [
            {"lang": "Kotlin", "interaction": "Parallel evolution: both modernizing mobile development"},
            {"lang": "Rust", "interaction": "Cross-pollination: Rust influence visible in Swift memory model"},
        ],
    },
    "Kotlin": {
        "pressure_index": 0.82,
        "temperature": 72,
        "humidity": 58,
        "wind_speed": 55,
        "visibility": 60,
        "forecast": "Fair — Android development remains strong",
        "pressure_trend": "rising",
        "conditions": "Android primary language status driving growth; JetBrains tooling excellent",
        "precipitation_risk": "low",
        "notable_fronts": [
            {"lang": "Java", "interaction": "Warm front: Kotlin and Java fully interoperable, smooth transition"},
            {"lang": "Swift", "interaction": "Parallel evolution: both modernizing mobile development"},
        ],
    },
    "TypeScript": {
        "pressure_index": 0.88,
        "temperature": 90,
        "humidity": 60,
        "wind_speed": 50,
        "visibility": 85,
        "forecast": "Hot — JavaScript superset dominance continues",
        "pressure_trend": "rising",
        "conditions": "Web development standard; Node.js and all major frameworks embrace TypeScript",
        "precipitation_risk": "low",
        "notable_fronts": [
            {"lang": "JavaScript", "interaction": "Absorption front: TypeScript progressively swallowing JavaScript"},
            {"lang": "Python", "interaction": "Cross-pollination: TypeScript types influencing Python type hints"},
        ],
    },
    "JavaScript": {
        "pressure_index": 0.95,
        "temperature": 95,
        "humidity": 70,
        "wind_speed": 30,
        "visibility": 98,
        "forecast": "Scorching — runs the web, still irreplaceable",
        "pressure_trend": "stable",
        "conditions": "Only browser language; Node.js ecosystem massive and mature",
        "precipitation_risk": "very_low",
        "notable_fronts": [
            {"lang": "TypeScript", "interaction": "Absorption front: TypeScript progressively swallowing JavaScript"},
        ],
    },
    "Java": {
        "pressure_index": 0.90,
        "temperature": 68,
        "humidity": 65,
        "wind_speed": 20,
        "visibility": 80,
        "forecast": "Cooling slightly — enterprise backbone but growth plateaued",
        "pressure_trend": "falling",
        "conditions": "Enterprise and Android (legacy) still massive; new projects declining",
        "precipitation_risk": "medium",
        "notable_fronts": [
            {"lang": "Go", "interaction": "Warm front collision: Go encroaching on Java backend territory"},
            {"lang": "Kotlin", "interaction": "Warm front: Kotlin and Java fully interoperable, smooth transition"},
        ],
    },
    "C/C++": {
        "pressure_index": 0.80,
        "temperature": 55,
        "humidity": 35,
        "wind_speed": 25,
        "visibility": 65,
        "forecast": "Stable — the bedrock beneath everything",
        "pressure_trend": "stable",
        "conditions": "Operating systems, embedded, game engines, high-performance computing",
        "precipitation_risk": "low",
        "notable_fronts": [
            {"lang": "Rust", "interaction": "Displacement pressure: Rust gaining ground in systems programming"},
        ],
    },
}


# ── Weather condition generators ──────────────────────────────────────────────

def _get_pressure_description(idx: float) -> str:
    """Convert pressure index to weather description."""
    if idx >= 0.90:
        return "High Pressure System — Extremely Stable"
    elif idx >= 0.80:
        return "Stable High Pressure — Calm Conditions"
    elif idx >= 0.70:
        return "Moderate Pressure — Normal Conditions"
    elif idx >= 0.60:
        return "Low Pressure Zone — Some Uncertainty"
    else:
        return "Very Low Pressure — Turbulent Conditions"


def _get_temperature_description(temp: int) -> str:
    """Convert temperature to descriptive weather."""
    if temp >= 90:
        return "Sultry Heat — Ubiquitous and Hot"
    elif temp >= 75:
        return "Warm — Active and Growing"
    elif temp >= 60:
        return "Mild — Steady Development"
    elif temp >= 40:
        return "Cool — Niche but Active"
    else:
        return "Cold Front — Specialized Use Only"


def _get_humidity_description(humidity: int) -> str:
    """Convert humidity to language complexity description."""
    if humidity >= 70:
        return "Heavy Atmosphere — Complex, Feature-Rich"
    elif humidity >= 55:
        return "Moderate Humidity — Moderate Complexity"
    elif humidity >= 40:
        return "Light Air — Lean and Focused"
    else:
        return "Dry Climate — Minimalist Design"


def _get_wind_description(wind: int) -> str:
    """Convert wind speed to evolution velocity description."""
    if wind >= 60:
        return "Blustery — Rapidly Evolving"
    elif wind >= 40:
        return "Breezy — Steady Evolution"
    elif wind >= 25:
        return "Light Breeze — Stable Core"
    else:
        return "Calm — Mature and Stable"


def _get_visibility_description(vis: int) -> str:
    """Convert visibility to market demand description."""
    if vis >= 85:
        return "Crystal Clear — Massively in Demand"
    elif vis >= 65:
        return "Good Visibility — Strong Demand"
    elif vis >= 45:
        return "Partial Visibility — Moderate Demand"
    else:
        return "Foggy — Niche Demand"


def _get_weather_icon(pressure_trend: str, forecast: str) -> str:
    """Get a weather icon based on conditions."""
    if "Scorching" in forecast or "Hot" in forecast or "Sultry" in forecast:
        return "🔥"
    elif "Cooling" in forecast or "Cold" in forecast:
        return "❄️"
    elif pressure_trend == "rising":
        return "☀️"
    elif pressure_trend == "falling":
        return "🌧️"
    else:
        return "⛅"


def _get_storm_risk(lang_a: str, lang_b: str) -> str:
    """Assess storm risk when two language fronts collide."""
    # High competition pairs
    high_storm = {
        ("Rust", "C/C++"): "Thunderstorm Watch — displacement battle in systems programming",
        ("Go", "Java"): "Severe Thunderstorm — backend territory dispute",
        ("TypeScript", "JavaScript"): "Warm Front — absorption in progress",
        ("Kotlin", "Java"): "Light Rain — gradual replacement underway",
        ("Rust", "Go"): "Squall Line — cloud infrastructure competition",
    }
    key = (lang_a, lang_b) if (lang_a, lang_b) in high_storm else (lang_b, lang_a)
    return high_storm.get(key, "Clearing — peaceful coexistence")


def _generate_barometric_reading(atmosphere: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a complete barometric reading for a language."""
    return {
        "pressure_index": atmosphere["pressure_index"],
        "pressure_mb": round(950 + atmosphere["pressure_index"] * 50, 1),
        "temperature_c": round(atmosphere["temperature"] * 0.3, 1),
        "humidity_pct": atmosphere["humidity"],
        "wind_speed_kmh": round(atmosphere["wind_speed"] * 1.5, 1),
        "visibility_km": round(atmosphere["visibility"] * 0.08, 1),
    }


def _generate_advisory(lang: str, atmosphere: Dict[str, Any]) -> List[str]:
    """Generate weather advisories for a language."""
    advisories = []
    if atmosphere["wind_speed"] >= 60:
        advisories.append("⚠️ High Wind Advisory: Language evolving rapidly — expect breaking changes")
    if atmosphere["humidity"] >= 70:
        advisories.append("🌫️ Heavy Complexity Advisory: Feature-rich — steep learning curve expected")
    if atmosphere["pressure_trend"] == "falling":
        advisories.append("📉 Falling Pressure Watch: Declining adoption — consider backup languages")
    if atmosphere["precipitation_risk"] == "high":
        advisories.append("🌧️ Precipitation Risk: Job market volatility expected")
    if atmosphere["visibility"] >= 85:
        advisories.append("🏆 Clear Skies Award: Massively in demand — excellent job prospects")
    if atmosphere["pressure_index"] >= 0.90:
        advisories.append("🛡️ Stable Weather Certificate: Mature ecosystem — low disruption risk")
    if not advisories:
        advisories.append("✅ Fair Conditions: No significant advisories")
    return advisories


# ── Core API ──────────────────────────────────────────────────────────────────

def load_rotation_data() -> Dict[str, Any]:
    """Load the language rotation configuration."""
    if not os.path.exists(ROTATION_FILE):
        return {
            "languages": ROTATION_ORDER.copy(),
            "current_index": 0,
            "last_language": None,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation_data(data: Dict[str, Any]) -> None:
    """Save updated language rotation configuration."""
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_rotation_language() -> str:
    """Get the current language from rotation without advancing index."""
    data = load_rotation_data()
    idx = data.get("current_index", 0)
    langs = data.get("languages", ROTATION_ORDER)
    return langs[idx % len(langs)]


def rotate_and_update() -> Dict[str, Any]:
    """
    Get the current language, advance the rotation index, save, and return report.

    Returns a full weather report for the current language.
    """
    data = load_rotation_data()
    idx = data.get("current_index", 0)
    langs = data.get("languages", ROTATION_ORDER)
    prev = data.get("last_language")

    current_lang = langs[idx % len(langs)]

    # Advance index
    next_idx = (idx + 1) % len(langs)
    data["current_index"] = next_idx
    data["last_language"] = current_lang
    save_rotation_data(data)

    # Build weather report
    atmosphere = LANGUAGE_ATMOSPHERE.get(current_lang, LANGUAGE_ATMOSPHERE["Rust"])
    barometric = _generate_barometric_reading(atmosphere)
    icon = _get_weather_icon(atmosphere["pressure_trend"], atmosphere["forecast"])

    report = {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "language": current_lang,
        "rotation_index": idx,
        "previous_language": prev,
        "weather": {
            "conditions": atmosphere["conditions"],
            "forecast": atmosphere["forecast"],
            "pressure_trend": atmosphere["pressure_trend"],
            "pressure_description": _get_pressure_description(atmosphere["pressure_index"]),
            "temperature_description": _get_temperature_description(atmosphere["temperature"]),
            "humidity_description": _get_humidity_description(atmosphere["humidity"]),
            "wind_description": _get_wind_description(atmosphere["wind_speed"]),
            "visibility_description": _get_visibility_description(atmosphere["visibility"]),
            "icon": icon,
        },
        "barometric_reading": barometric,
        "advisories": _generate_advisory(current_lang, atmosphere),
        "notable_fronts": atmosphere.get("notable_fronts", []),
    }

    return report


def collision_forecast(lang_a: str, lang_b: str) -> Dict[str, Any]:
    """
    Generate a collision forecast between two language fronts.

    Args:
        lang_a: First language
        lang_b: Second language

    Returns a collision report with storm risk and interaction details.
    """
    # Get both atmospheres
    atm_a = LANGUAGE_ATMOSPHERE.get(lang_a, {})
    atm_b = LANGUAGE_ATMOSPHERE.get(lang_b, {})

    # Calculate combined barometric pressure
    combined_pressure = (
        atm_a.get("pressure_index", 0.5) + atm_b.get("pressure_index", 0.5)
    ) / 2

    # Calculate temperature differential
    temp_diff = abs(
        atm_a.get("temperature", 50) - atm_b.get("temperature", 50)
    )

    storm_risk = _get_storm_risk(lang_a, lang_b)

    # Interaction description
    interactions = {
        ("Rust", "C/C++"): "Systems programmers face a choice: legacy stability vs. memory safety",
        ("Rust", "Go"): "Cloud infrastructure convergence: both targeting similar domains",
        ("Go", "Java"): "Backend battlefield: Go's simplicity vs. Java's ecosystem",
        ("Swift", "Kotlin"): "Mobile development parallels: modern, concise, safe",
        ("TypeScript", "JavaScript"): "Superset absorption: TypeScript expanding JavaScript's reach",
        ("Kotlin", "Java"): "Interoperable transition: Kotlin replacing Java incrementally",
        ("Java", "Go"): "Backend territory dispute: Go eating Java's lunch in new projects",
        ("Rust", "Swift"): "Systems meets mobile: cross-pollination of memory models",
    }
    key = (lang_a, lang_b) if (lang_a, lang_b) in interactions else (lang_b, lang_a)
    interaction = interactions.get(key, f"{lang_a} and {lang_b} coexist with moderate interaction")

    return {
        "front_a": lang_a,
        "front_b": lang_b,
        "storm_risk": storm_risk,
        "combined_barometric_pressure": round(combined_pressure, 3),
        "temperature_differential": temp_diff,
        "interaction": interaction,
        "recommendation": (
            "Watch for convergence opportunities"
            if combined_pressure > 0.85
            else "Monitor for displacement patterns"
        ),
    }


def generate_ecosystem_barometer() -> Dict[str, Any]:
    """
    Generate ecosystem-wide barometric pressure readings for all languages.

    Returns a ranked list of languages by ecosystem health.
    """
    readings = []
    for lang, atm in LANGUAGE_ATMOSPHERE.items():
        combined = (
            atm["pressure_index"] * 0.4
            + (atm["temperature"] / 100) * 0.2
            + (atm["visibility"] / 100) * 0.3
            + (1 - atm["wind_speed"] / 100) * 0.1
        )
        readings.append(
            {
                "language": lang,
                "ecosystem_score": round(combined, 3),
                "pressure_index": atm["pressure_index"],
                "temperature": atm["temperature"],
                "visibility": atm["visibility"],
                "trend": atm["pressure_trend"],
            }
        )

    readings.sort(key=lambda x: x["ecosystem_score"], reverse=True)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rankings": readings,
        "overall_ecosystem_health": round(
            sum(r["ecosystem_score"] for r in readings) / len(readings), 3
        ),
    }


def get_seasonal_pattern(lang: str) -> Dict[str, Any]:
    """
    Generate a seasonal pattern forecast for a language.

    Shows how adoption typically waxes and wanes throughout the year.
    """
    atm = LANGUAGE_ATMOSPHERE.get(lang, {})
    base_temp = atm.get("temperature", 50)

    # Seasonal modifiers (relative index into the year)
    seasons = [
        {"name": "Winter (Jan-Mar)", "modifier": -5, "note": "Post-holiday hiring surge"},
        {"name": "Spring (Apr-Jun)", "modifier": 8, "note": "Active hiring season begins"},
        {"name": "Summer (Jul-Sep)", "modifier": 3, "note": "Vacation slowdowns balanced by conferences"},
        {"name": "Autumn (Oct-Dec)", "modifier": 10, "note": "Hiring peaks; budgets releasing; new projects start"},
    ]

    seasonal_forecast = []
    for season in seasons:
        adjusted_temp = max(0, min(100, base_temp + season["modifier"]))
        if adjusted_temp >= 85:
            condition = "Hiring Boom"
        elif adjusted_temp >= 70:
            condition = "Active Season"
        elif adjusted_temp >= 50:
            condition = "Moderate Activity"
        else:
            condition = "Low Season"
        seasonal_forecast.append(
            {
                "season": season["name"],
                "adjusted_temperature": adjusted_temp,
                "condition": condition,
                "note": season["note"],
            }
        )

    return {
        "language": lang,
        "base_temperature": base_temp,
        "seasonal_forecast": seasonal_forecast,
    }


# ── Tests ──────────────────────────────────────────────────────────────────────

def run_tests() -> None:
    """Run all tests for polyglot_weather module."""
    import unittest
    import sys
    import os

    # Ensure the module directory is on the path
    sys.path.insert(0, os.path.dirname(__file__))

    # Re-import ourselves for testing
    import importlib
    import polyglot_weather as mod
    importlib.reload(mod)

    class TestRotationLogic(unittest.TestCase):
        def test_rotation_file_exists(self):
            self.assertTrue(os.path.exists(ROTATION_FILE))

        def test_rotation_order_loads(self):
            data = mod.load_rotation_data()
            self.assertIn("languages", data)
            self.assertEqual(len(data["languages"]), 8)

        def test_get_rotation_language(self):
            lang = mod.get_rotation_language()
            self.assertIn(lang, ROTATION_ORDER)

        def test_rotate_and_update(self):
            data_before = mod.load_rotation_data()
            idx_before = data_before["current_index"]
            result = mod.rotate_and_update()
            data_after = mod.load_rotation_data()
            idx_after = data_after["current_index"]

            self.assertIn(result["language"], ROTATION_ORDER)
            self.assertEqual(result["rotation_index"], idx_before)
            self.assertEqual(idx_after, (idx_before + 1) % 8)

        def test_rotate_wraps(self):
            data = mod.load_rotation_data()
            langs = data["languages"]
            n = len(langs)
            start_idx = data["current_index"]
            # Rotate through the full cycle
            for _ in range(n):
                mod.rotate_and_update()
            data = mod.load_rotation_data()
            self.assertEqual(data["current_index"], start_idx)  # Wrapped back to original

    class TestWeatherReport(unittest.TestCase):
        def test_report_structure(self):
            result = mod.rotate_and_update()
            self.assertIn("language", result)
            self.assertIn("weather", result)
            self.assertIn("barometric_reading", result)
            self.assertIn("advisories", result)
            self.assertIn("notable_fronts", result)

        def test_all_languages_have_atmosphere(self):
            for lang in ROTATION_ORDER:
                self.assertIn(lang, LANGUAGE_ATMOSPHERE)

        def test_barometric_reading_fields(self):
            result = mod.rotate_and_update()
            br = result["barometric_reading"]
            self.assertIn("pressure_mb", br)
            self.assertIn("temperature_c", br)
            self.assertIn("humidity_pct", br)
            self.assertIn("wind_speed_kmh", br)
            self.assertIn("visibility_km", br)

        def test_weather_fields(self):
            result = mod.rotate_and_update()
            w = result["weather"]
            self.assertIn("conditions", w)
            self.assertIn("forecast", w)
            self.assertIn("pressure_trend", w)
            self.assertIn("icon", w)

    class TestCollisionForecast(unittest.TestCase):
        def test_collision_between_rust_and_c(self):
            result = mod.collision_forecast("Rust", "C/C++")
            self.assertEqual(result["front_a"], "Rust")
            self.assertEqual(result["front_b"], "C/C++")
            self.assertIn("storm_risk", result)
            self.assertIn("interaction", result)

        def test_symmetric_collision(self):
            result_a = mod.collision_forecast("Rust", "Go")
            result_b = mod.collision_forecast("Go", "Rust")
            self.assertEqual(result_a["storm_risk"], result_b["storm_risk"])

    class TestEcosystemBarometer(unittest.TestCase):
        def test_barometer_structure(self):
            result = mod.generate_ecosystem_barometer()
            self.assertIn("rankings", result)
            self.assertIn("overall_ecosystem_health", result)
            self.assertEqual(len(result["rankings"]), 8)

        def test_rankings_sorted(self):
            result = mod.generate_ecosystem_barometer()
            scores = [r["ecosystem_score"] for r in result["rankings"]]
            self.assertEqual(scores, sorted(scores, reverse=True))

    class TestSeasonalPattern(unittest.TestCase):
        def test_seasonal_forecast_has_four_seasons(self):
            result = mod.get_seasonal_pattern("Rust")
            self.assertEqual(len(result["seasonal_forecast"]), 4)

        def test_all_languages_have_seasonal_pattern(self):
            for lang in ROTATION_ORDER:
                result = mod.get_seasonal_pattern(lang)
                self.assertEqual(result["language"], lang)

    # Run tests
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRotationLogic))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestWeatherReport))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCollisionForecast))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEcosystemBarometer))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSeasonalPattern))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
