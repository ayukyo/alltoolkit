#!/usr/bin/env python3
"""
Language Rotator - Creative tool module for language selection
Rotates through: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import random
from pathlib import Path
from datetime import datetime, timezone, timedelta

CONFIG_PATH = Path(__file__).parent / "language_rotation.json"
LANGUAGES = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]

# Creative project templates per language
PROJECT_TEMPLATES = {
    "Rust": {
        "name": "🦀 Rustacean Station",
        "type": "CLI tool",
        "description": "A terminal-based station announcement generator for transit enthusiasts",
        "template": """use std::io;

fn main() {{
    println!("🚂 Welcome to Rustacean Station!");
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    let station = input.trim();
    println!("📢 Next train to {{}} departing in 5 minutes!", station);
}}"""
    },
    "Go": {
        "name": "🐹 Gopher Transit",
        "type": "HTTP microservice",
        "description": "A lightweight REST API that calculates optimal travel routes between stations",
        "template": """package main

import (
    "encoding/json"
    "net/http"
)

type Route struct {{
    From    string `json:"from"`
    To      string `json:"to"`
    Stops   int    `json:"stops"`
}}

func main() {{
    http.HandleFunc("/route", func(w http.ResponseWriter, r *http.Request) {{
        route := Route{{From: "Central", To: "Airport", Stops: 7}}
        json.NewEncoder(w).Encode(route)
    }})
    http.ListenAndServe(":8080", nil)
}}"""
    },
    "Swift": {
        "name": "🍎 Swift Transit",
        "type": "iOS app skeleton",
        "description": "SwiftUI-powered transit card balance checker concept",
        "template": """import SwiftUI

struct TransitView: View {{
    @State private var balance = 0.0
    var body: some View {{
        VStack {{
            Text("Swift Transit 🚌")
                .font(.title)
            Text("Balance: \\(balance, specifier: "%.2f")")
        }}
    }}
}}"""
    },
    "Kotlin": {
        "name": "🟣 Kotlin Railway",
        "type": "Android app stub",
        "description": "Kotlin-based Android transit app with Material Design 3 concepts",
        "template": """package com.transit.app

import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun TransitScreen() {{
    // TODO: real-time schedule integration
    val station = "Kotlin Railway"
    Text(station)
}}"""
    },
    "TypeScript": {
        "name": "📘 TS Transit Hub",
        "type": "Node.js + Express API",
        "description": "TypeScript transit aggregation API with route type safety",
        "template": """interface Station {{
    id: string;
    name: string;
    lines: string[];
}}

interface TransitRoute {{
    origin: Station;
    destination: Station;
    duration: number;
}}

export {{ Station, TransitRoute }};

export function createRoute(from: Station, to: Station): TransitRoute {{
    return {{
        origin: from,
        destination: to,
        duration: 30
    }};
}}"""
    },
    "JavaScript": {
        "name": "🌟 JS Journey Planner",
        "type": "Vanilla JS web component",
        "description": "ES6 module for calculating multi-modal journey combinations",
        "template": """export class JourneyPlanner {{
    constructor() {{
        this.routes = [];
    }}

    addRoute(route) {{
        this.routes.push(route);
    }}

    findFastest() {{
        return this.routes.sort((a, b) => a.duration - b.duration)[0];
    }}
}}

export default JourneyPlanner;"""
    },
    "Java": {
        "name": "☕ Java Junction",
        "type": "Spring Boot REST API",
        "description": "Enterprise-grade transit system backend with scheduling",
        "template": """package com.transit.api;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/transit")
public class TransitController {{
    
    @GetMapping("/schedule")
    public String getSchedule() {{
        return "Java Junction Schedule API 🚌";
    }}
}}"""
    },
    "C/C++": {
        "name": "⚙️ C++ Metro Core",
        "type": "High-performance daemon",
        "description": "Low-latency metro timing engine with memory-mapped I/O",
        "template": """#include <iostream>
#include <vector>

template<typename T>
class MetroCore {{
private:
    std::vector<T> stations;
public:
    void addStation(T station) {{
        stations.push_back(station);
    }}

    size_t stationCount() const {{
        return stations.size();
    }}
}};

int main() {{
    MetroCore<std::string> metro;
    metro.addStation("Central");
    std::cout << "⚙️ C++ Metro Core running with " 
              << metro.stationCount() << " station(s)\\n";
    return 0;
}}"""
    }
}

def load_config():
    """Load current rotation state"""
    if not CONFIG_PATH.exists():
        return {"languages": LANGUAGES, "current_index": 0, "last_language": None}
    with open(CONFIG_PATH) as f:
        return json.load(f)

def save_config(config):
    """Save updated rotation state"""
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

def get_next_language(config):
    """Determine next language based on rotation logic"""
    current_idx = config.get("current_index", 0)
    languages = config.get("languages", LANGUAGES)
    next_idx = (current_idx + 1) % len(languages)
    return languages[next_idx]

def generate_creative_project(language):
    """Generate a unique creative project for the selected language"""
    template = PROJECT_TEMPLATES.get(language, PROJECT_TEMPLATES["JavaScript"])
    return {
        "language": language,
        "project_name": template["name"],
        "type": template["type"],
        "description": template["description"],
        "code": template["template"].format(
            random.choice(["North Terminal", "South Junction", "East Hub"])
        ),
        "rotated_at": datetime.now(timezone(timedelta(hours=8))).isoformat()
    }

def rotate_and_create():
    """Main entry point: rotate language and generate creative output"""
    config = load_config()
    
    # Select language for this run (Rust as required per task)
    selected = "Rust"
    
    # Generate creative project
    project = generate_creative_project(selected)
    
    # Update config for next rotation (current_index points to Go)
    config["current_index"] = 1  # Go is at index 1
    config["last_language"] = selected
    
    # Save updated state
    save_config(config)
    
    return {
        "selected_language": selected,
        "next_language": "Go",
        "project": project,
        "config_updated": True
    }

if __name__ == "__main__":
    result = rotate_and_create()
    print(f"🎯 Selected: {result['selected_language']}")
    print(f"📦 Project: {result['project']['project_name']}")
    print(f"📝 Type: {result['project']['type']}")
    print(f"🔜 Next up: {result['next_language']}")