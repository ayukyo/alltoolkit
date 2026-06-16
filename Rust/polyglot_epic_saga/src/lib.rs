//! # Polyglot Epic Saga
//!
//! Epic Narrative Generator — treats each programming language as an epic hero
//! on an odyssey, generating narrative poetry about legendary battles,
//! mythological companions, and prophetic destiny.
//!
//! ## Creative Concept
//!
//! **"Every language is a hero. Every feature is a legend."**
//!
//! This module treats programming languages as characters in an epic mythological
//! narrative — Rust is the scarred warrior who mastered the Ownership Blade after
//! being exiled from the C/C++ highlands. Go is the pragmatic seafarer who built
//! the Goroutine Armada. Each language's traits become epic attributes, their
//! evolution becomes a hero's journey, and their ecosystem becomes a cast of
//! mythological companions.
//!
//! ## Rotation Integration
//!
//! - Reads `language_rotation.json` → `current_index` → selects "hero" language
//! - Generates an epic saga with: hero intro, legendary deeds, companions, battles, prophecy
//! - After generation, `current_index` advances by 1 (mod 8) and `updated_at` is refreshed
//! - A log of all saga runs is kept in `polyglot_epic_saga_log.json`
//!
//! ## Saga Structure (per run)
//!
//! Each saga consists of 6 chapters:
//! 1. **The Summoning** — How the hero first answered the call (birth/history)
//! 2. **The Legendary Deeds** — Three heroic feats that defined the language
//! 3. **The Companion Council** — Three key tools/frameworks as allies
//! 4. **The Antagonist Alliance** — Three rivals/challenges
//! 5. **The Omens & Prophecy** — What the future holds for this hero
//! 6. **The Epic Closure** — A closing couplet summarizing the hero's essence
//!
//! ## Rotation Order
//!
//! Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust

use rand::seq::SliceRandom;
use rand::Rng;
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

// ─────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum Language {
    Rust,
    Go,
    Swift,
    Kotlin,
    TypeScript,
    JavaScript,
    Java,
    #[serde(rename = "C/C++")]
    Cpp,
}

impl Language {
    pub fn from_str(s: &str) -> Option<Self> {
        match s {
            "Rust" => Some(Language::Rust),
            "Go" => Some(Language::Go),
            "Swift" => Some(Language::Swift),
            "Kotlin" => Some(Language::Kotlin),
            "TypeScript" => Some(Language::TypeScript),
            "JavaScript" => Some(Language::JavaScript),
            "Java" => Some(Language::Java),
            "C/C++" => Some(Language::Cpp),
            _ => None,
        }
    }

    pub fn as_str(&self) -> &'static str {
        match self {
            Language::Rust => "Rust",
            Language::Go => "Go",
            Language::Swift => "Swift",
            Language::Kotlin => "Kotlin",
            Language::TypeScript => "TypeScript",
            Language::JavaScript => "JavaScript",
            Language::Java => "Java",
            Language::Cpp => "C/C++",
        }
    }

    pub fn all() -> [Language; 8] {
        [
            Language::Rust,
            Language::Go,
            Language::Swift,
            Language::Kotlin,
            Language::TypeScript,
            Language::JavaScript,
            Language::Java,
            Language::Cpp,
        ]
    }

    pub fn file_ext(&self) -> &'static str {
        match self {
            Language::Rust => "rs",
            Language::Go => "go",
            Language::Swift => "swift",
            Language::Kotlin => "kt",
            Language::TypeScript => "ts",
            Language::JavaScript => "js",
            Language::Java => "java",
            Language::Cpp => "cpp",
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HeroArchetype {
    pub archetype: String,
    pub epithet: String,
    pub weapon: String,
    pub armor: String,
    pub home: String,
}

impl HeroArchetype {
    pub fn for_language(lang: Language) -> Self {
        match lang {
            Language::Rust => HeroArchetype {
                archetype: "The Scarred Warrior".into(),
                epithet: "Fearless in the Ownership Storm".into(),
                weapon: "The Ownership Blade (zero-cost abstractions)".into(),
                armor: "Lifetime Forged Platemail".into(),
                home: "The Highlands of Memory Safety".into(),
            },
            Language::Go => HeroArchetype {
                archetype: "The Pragmatic Seafarer".into(),
                epithet: "Who Built Harbors Where All Could Dock".into(),
                weapon: "The Goroutine Trident".into(),
                armor: "Simplicity Woven Tunic".into(),
                home: "The Harbor City-State".into(),
            },
            Language::Swift => HeroArchetype {
                archetype: "The Elegant Sorcerer".into(),
                epithet: "Master of Protocol Spells".into(),
                weapon: "The Optional Wand (safe nil dispersal)".into(),
                armor: "Value-Type Mage Robes".into(),
                home: "The Valley of Apple".into(),
            },
            Language::Kotlin => HeroArchetype {
                archetype: "The JVM Alchemist".into(),
                epithet: "Who Transmuted Java into Gold".into(),
                weapon: "The Coroutine Serpent Staff".into(),
                armor: "Extension Enchanted Cloak".into(),
                home: "The JetBrains Forge".into(),
            },
            Language::TypeScript => HeroArchetype {
                archetype: "The Typed Prophet".into(),
                epithet: "Who Sang Types into the Scripting Wilds".into(),
                weapon: "The Type Oracle Scroll".into(),
                armor: "Structural Record Mail".into(),
                home: "The Microsoft Spire".into(),
            },
            Language::JavaScript => HeroArchetype {
                archetype: "The Prototypal Trickster".into(),
                epithet: "Shape-Shifter of Ten Thousand Frameworks".into(),
                weapon: "The Event Loop Boomerang".into(),
                armor: "Prototype Chain Shroud".into(),
                home: "The Everyweb — Found Everywhere".into(),
            },
            Language::Java => HeroArchetype {
                archetype: "The Enterprise Paladin".into(),
                epithet: "Who Swore the Sacred Virtual Oath".into(),
                weapon: "The Object-Oriented Longsword".into(),
                armor: "JVM Sanctified Platemail".into(),
                home: "The Kingdom of Write Once, Run Anywhere".into(),
            },
            Language::Cpp => HeroArchetype {
                archetype: "The Ancient Highlander".into(),
                epithet: "Master of the Raw Machine".into(),
                weapon: "The Template Sorcery Staff".into(),
                armor: "Undefined Behavior Shroud (dangerous but mighty)".into(),
                home: "The C/C++ Highlands — Where It All Began".into(),
            },
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LegendaryDeed {
    pub title: String,
    pub epic_verse: String,
    pub significance: String,
}

impl LegendaryDeed {
    pub fn for_language<R: Rng>(lang: Language, rng: &mut R) -> Self {
        let deeds = Self::all_deeds(lang);
        deeds.choose(rng).unwrap().clone()
    }

    fn all_deeds(lang: Language) -> Vec<Self> {
        match lang {
            Language::Rust => vec![
                LegendaryDeed {
                    title: "The Battle of the Borrow Gate".into(),
                    epic_verse: "At the gates of segmentation, Rust stood alone. \
'None shall pass with aliased mutability!' And the compiler thundered YEA, \
and the ownership blade sang, and the highlands were safe forever.".into(),
                    significance: "The moment Rust proved memory safety without GC was possible".into(),
                },
                LegendaryDeed {
                    title: "The Raising of the Zero-Cost Cathedral".into(),
                    epic_verse: "With abstractions that bent not the machine, \
Rust raised a cathedral in the sky. 'What you don't use, you don't pay,' \
sang the priests, and LLVM forge-blessed every stone.".into(),
                    significance: "Zero-cost abstractions became the foundation of Rust's identity".into(),
                },
                LegendaryDeed {
                    title: "The Fearless Concurrency Crusade".into(),
                    epic_verse: "When the thread-daemons of data-races threatened the realm, \
Rust sent forth the Send and Sync crusaders. 'By the ledger of ownership, \
ye shall not corrupt!' And the concurrency was fearlessly achieved.".into(),
                    significance: "Compile-time concurrency safety became Rust's defining feature".into(),
                },
                LegendaryDeed {
                    title: "The Match of Exhaustive Truths".into(),
                    epic_verse: "In the arena of pattern matching, no stone was left unturned. \
Rust stood before the enum of all possibilities and VANQUISHED the unhandled case. \
'None shall escape my match!' And it was so — every truth was known.".into(),
                    significance: "Exhaustive pattern matching eliminated entire categories of bugs".into(),
                },
                LegendaryDeed {
                    title: "The Great Lifetime Expedition".into(),
                    epic_verse: "When references wandered lost through the stack, \
Rust charted the lifetime — 'Prove thy scope, or be EXILED!' And the \
borrow checker mapped every reference's journey, and dangling pointers \
were no more.".into(),
                    significance: "Lifetime annotations solved the dangling reference problem".into(),
                },
            ],
            Language::Go => vec![
                LegendaryDeed {
                    title: "The Launching of the Goroutine Armada".into(),
                    epic_verse: "Go summoned ten thousand goroutines with a single 'go', \
and the channels sang between them like harbors in the night. \
'Fear not the concurrency,' quoth Go, 'for my goroutines weigh but little!'".into(),
                    significance: "Goroutines revolutionized concurrent programming with minimal overhead".into(),
                },
                LegendaryDeed {
                    title: "The Cleansing of the Complexity Temple".into(),
                    epic_verse: "When the inheritance towers grew too tall and the \
generic shrines too cryptic, Go smote them with simplicity's axe. \
'No more shall ye suffer twenty layers of abstraction!' And the \
code was clean, and the gopher rejoiced.".into(),
                    significance: "Go's minimalism was a deliberate rebellion against complexity".into(),
                },
                LegendaryDeed {
                    title: "The Compiling of the Swift Fleet".into(),
                    epic_verse: "Before Go, compilation took an age. Go forged the Swift Fleet \
of incremental compilation, and builds that once took hours were done in heartbeats. \
'Wait not for thy code,' sang Go, 'ship it NOW!'".into(),
                    significance: "Fast compilation became a core Go philosophy and competitive advantage".into(),
                },
                LegendaryDeed {
                    title: "The Deferral of the Temple Cleaners".into(),
                    epic_verse: "At the gates of every function's end, Go placed the defer. \
'Clean what thou openest,' commanded Go, 'and it shall be so in fire or in return.' \
And the resource handlers wept with relief.".into(),
                    significance: "The defer statement revolutionized resource management patterns".into(),
                },
            ],
            Language::Swift => vec![
                LegendaryDeed {
                    title: "The Binding of the Protocol Covenant".into(),
                    epic_verse: "Swift forged the Protocol — a covenant not of inheritance \
but of capability. 'THOU SHALT implement what thou proclaimest,' \
and the types knelt before the protocol's authority, and polymorphism \
was achieved without the chains of class.".into(),
                    significance: "Protocol-oriented programming became Swift's defining paradigm".into(),
                },
                LegendaryDeed {
                    title: "The Great Optional Dispersal".into(),
                    epic_verse: "When nil crept through the valleys of code causing ruin, \
Swift spoke: 'Let optionals be — Some or None, but NEVER unspecified!' \
And the unwrapping rituals were established, and nil crashes became legend.".into(),
                    significance: "Optionals made nil handling explicit and safe".into(),
                },
                LegendaryDeed {
                    title: "The Value-Type March".into(),
                    epic_verse: "Swift's armies marched not with references but with values. \
'Carry thy struct, own thy copy!' declared Swift, and the performance \
of array operations was swift indeed, and the copies multiplied without fear.".into(),
                    significance: "Value types (structs) by default provided performance predictability".into(),
                },
                LegendaryDeed {
                    title: "The Apple Valley Founding".into(),
                    epic_verse: "From the halls of Objective-C, Swift rose — young, bold, \
and unafraid of the sugar-coated syntax. 'I shall run on thy devices, \
in thy IDE, and bring joy to the Apple faithful!' And it was so.".into(),
                    significance: "Swift's creation by Apple to replace Objective-C".into(),
                },
            ],
            Language::Kotlin => vec![
                LegendaryDeed {
                    title: "The Null Safety Reformation".into(),
                    epic_verse: "Kotlin marched upon the Java kingdom and declared: \
'Let null be a TYPE, not a default!' And the safe-call operator bloomed \
like a flower, and the !! came as a warning, and null pointer \
exceptions retreated to legend.".into(),
                    significance: "Kotlin's null safety influenced the entire JVM ecosystem".into(),
                },
                LegendaryDeed {
                    title: "The Coroutine Convergence".into(),
                    epic_verse: "When async dragons plagued the land, Kotlin summoned \
coroutines — lighter than threads, more graceful than callbacks. \
'Suspend,' spoke Kotlin, 'and the world shall await.' And the callback \
pyramids crumbled.".into(),
                    significance: "Kotlin coroutines provided the best async story on the JVM".into(),
                },
                LegendaryDeed {
                    title: "The Extension Spell".into(),
                    epic_verse: "With a wave of the extension wand, Kotlin added methods \
to classes without altering their bloodline. 'Fear not the final class!' \
cried Kotlin, 'I shall extend ALL.' And String gained new powers.".into(),
                    significance: "Extension functions allowed open-closed principle without inheritance".into(),
                },
                LegendaryDeed {
                    title: "The Google I/O Benediction".into(),
                    epic_verse: "At the great Google summit, Kotlin was named Android's \
chosen tongue. 'Go forth,' spake Google, 'and be the language of \
three billion devices!' And Kotlin's star ascended to the heavens.".into(),
                    significance: "Google's endorsement made Kotlin the preferred Android language".into(),
                },
            ],
            Language::TypeScript => vec![
                LegendaryDeed {
                    title: "The Type Oracle Ascension".into(),
                    epic_verse: "JavaScript, the untyped wanderer, was confronted by \
TypeScript: 'Thou shalt NOT pass without declaring thy shape!' \
And the any-type was cursed, and strict mode bloomed, and \
entire categories of runtime errors retreated.".into(),
                    significance: "TypeScript brought static types to JavaScript at scale".into(),
                },
                LegendaryDeed {
                    title: "The Structural Type Decree".into(),
                    epic_verse: "'NAME MEANS NOTHING,' declared TypeScript's structural oracle. \
'Only SHAPE MATTERS!' And the nominal type wars ended, and \
duck-typed code found its kingdom, and interface compatibility \
was proven by form alone.".into(),
                    significance: "Structural typing made TypeScript flexible and pragmatic".into(),
                },
                LegendaryDeed {
                    title: "The Erasure Prophecy".into(),
                    epic_verse: "At runtime, TypeScript's annotations vanish like morning mist. \
'Compile-time thy truth, runtime thy freedom,' prophesied the type oracle, \
'and JS shall run unchanged.' And the JavaScript faithful rejoiced.".into(),
                    significance: "TypeScript erases types at runtime — no runtime overhead".into(),
                },
                LegendaryDeed {
                    title: "The Microsoft Benediction".into(),
                    epic_verse: "Microsoft, the great empire of tooling, looked upon \
TypeScript and said: 'THOU SHALT BE OURS.' And VS Code was forged \
in TypeScript's image, and the intellisense spirits answered every keystroke.".into(),
                    significance: "Microsoft's backing and VS Code integration made TypeScript dominant".into(),
                },
            ],
            Language::JavaScript => vec![
                LegendaryDeed {
                    title: "The Great Event Loop Race".into(),
                    epic_verse: "In the single-threaded arena, JavaScript orchestrated \
the great event loop race. 'Hitherto async tasks! Hitherto promises!' \
And the callback queue was managed, and the call stack never overflowed, \
and the web was powered by one champion's tireless beat.".into(),
                    significance: "JavaScript's event loop made async programming possible in a single thread".into(),
                },
                LegendaryDeed {
                    title: "The Prototype Chain Ritual".into(),
                    epic_verse: "JavaScript stood apart from the class-bound kingdoms \
and declared: 'I SHALL INHERIT FROM THE ACTUAL!' And the prototype \
chain was forged, and objects begat objects in an unbroken lineage, \
and class syntax was but sugar upon the prototype shrine.".into(),
                    significance: "Prototypal inheritance was JavaScript's unique object model".into(),
                },
                LegendaryDeed {
                    title: "The Everywhere March".into(),
                    epic_verse: "'I SHALL RUN ON EVERY DEVICE IN THE KNOWN WORLD!' \
declared JavaScript, and the browsers bowed, and Node rose to \
challenge the server, and now even the smallest IoT device \
knows the JavaScript name.".into(),
                    significance: "JavaScript runs everywhere — browsers, servers, mobile, IoT".into(),
                },
                LegendaryDeed {
                    title: "The NPM Library Immensity".into(),
                    epic_verse: "JavaScript summoned the greatest library army ever assembled. \
npm install this, npm install that. A million packages, and still growing. \
'No task,' spake JavaScript, 'but what my packages have not already solved.'".into(),
                    significance: "npm became the largest package ecosystem in the world".into(),
                },
            ],
            Language::Java => vec![
                LegendaryDeed {
                    title: "The Write Once Oath".into(),
                    epic_verse: "In the valley of platform wars, Java swore the sacred oath: \
'WHAT I WRITE UPON MY VIRTUAL MACHINE, ALL MACHINES SHALL RUN!' \
And the JVM spirit entered every device, and the bytecode scrolls \
were carried to every shore.".into(),
                    significance: "Java's WORA promise revolutionized portable software".into(),
                },
                LegendaryDeed {
                    title: "The Garbage Collection Truce".into(),
                    epic_verse: "When memory demons haunted every allocation, Java \
summoned the Garbage Collector — an ever-vigilant spirit. \
'FEAR NOT THE FREE,' proclaimed Java, 'for my GC shall reclaim what is done.' \
And manual memory management retired to legend.".into(),
                    significance: "Java's GC made memory management accessible to mere mortals".into(),
                },
                LegendaryDeed {
                    title: "The Enterprise Army Mustering".into(),
                    epic_verse: "Java rallied the great enterprise armies. 'To me, ye \
corporate knights!' cried Java, and Spring arose, and Hibernate \
tamed the database beasts, and the enterprise citadel was built \
upon Java's foundations.".into(),
                    significance: "Java became the backbone of enterprise computing".into(),
                },
                LegendaryDeed {
                    title: "The Android Conquest".into(),
                    epic_verse: "When mobile devices rose from the digital seas, Java \
marched upon them. 'THESE DEVICES SHALL BE MINE,' declared Java, \
and Android's heart beat with Java's rhythm. For a decade, \
Java WAS the mobile language, until Kotlin came with its reformation.".into(),
                    significance: "Java was the original Android language for a decade".into(),
                },
            ],
            Language::Cpp => vec![
                LegendaryDeed {
                    title: "The First Light of the C/C++ Highlands".into(),
                    epic_verse: "In the beginning, there was C. And C saw the machine, \
and C spoke unto it in its own tongue. And from C's loins rose C++, \
the augmenting warrior. 'I SHALL ADD CLASSES TO C,' declared C++, \
'WITHOUT ABANDONING THE RAW POWER!' And lo, it was good.".into(),
                    significance: "C/C++ created the foundation for all modern systems programming".into(),
                },
                LegendaryDeed {
                    title: "The Template Metaprogramming Incantation".into(),
                    epic_verse: "When developers sought to conjure code that writes code, \
C++ whispered the Template Spell. 'INSTANTIATE ME AT COMPILE TIME!' \
And the TMP dragons were tamed, and constexpr became an oracle of \
everlasting computation.".into(),
                    significance: "C++ templates enabled powerful compile-time computation".into(),
                },
                LegendaryDeed {
                    title: "The RAII Fortress".into(),
                    epic_verse: "C++ raised the fortress of RAII — Resource Acquisition \
Is Initialization. 'What thou openest, close thou shalt,' commanded C++, \
'and the destructor shall be thy guarantee!' And the resource leaks \
were not vanquished — but bounded.".into(),
                    significance: "RAII became C++'s signature resource management technique".into(),
                },
                LegendaryDeed {
                    title: "The Performance Vow".into(),
                    epic_verse: "'I SHALL GIVE THEE THE MACHINE,' vowed C++ to its followers. \
'No runtime, no interpreter — PURE NATIVE EXECUTION.' \
And the game engines knelt, and the operating systems bowed. \
For in raw performance, none could match the C++ vow.".into(),
                    significance: "C++ became the gold standard for performance-critical applications".into(),
                },
            ],
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Companion {
    pub name: String,
    pub role: String,
    pub epic_description: String,
}

impl Companion {
    pub fn for_language<R: Rng>(lang: Language, rng: &mut R) -> [Self; 3] {
        let companions = Self::all_companions(lang);
        companions
            .choose_multiple(rng, 3)
            .cloned()
            .collect::<Vec<_>>()
            .try_into()
            .unwrap()
    }

    fn all_companions(lang: Language) -> Vec<Self> {
        match lang {
            Language::Rust => vec![
                Companion {
                    name: "Cargo".into(),
                    role: "The Quartermaster".into(),
                    epic_description: "Cargo leads the provisioning of dependencies, wielding the manifest as a map to all known crates. The Rust lands would starve without Cargo's meticulous supply lines.".into(),
                },
                Companion {
                    name: "rustfmt".into(),
                    role: "The Style Arbiter".into(),
                    epic_description: "With ironclad formatting rules, rustfmt ensures the Rust warrior always presents in impeccable rank. Inconsistency is banned; beauty is enforced.".into(),
                },
                Companion {
                    name: "Clippy".into(),
                    role: "The Wisdom Keeper".into(),
                    epic_description: "Clippy dispenses ancient lint wisdom — 'Are ye sure ye wish to .clone() that which could be borrowed?' The compiler's conscience speaks through Clippy.".into(),
                },
                Companion {
                    name: "rust-analyzer".into(),
                    role: "The Oracle's Eye".into(),
                    epic_description: "In the VS Code court, rust-analyzer sees all — type shadows, completion spirits, the full IDE radiance. It is the Oracle's Eye in the Rust lands.".into(),
                },
                Companion {
                    name: "Miri".into(),
                    role: "The Undefined Behavior Hunter".into(),
                    epic_description: "Miri stalks the shadows of undefined behavior, ever vigilant. When unsafe code strays into UB territory, Miri sounds the alarm before the field is lost.".into(),
                },
                Companion {
                    name: "The Borrow Checker".into(),
                    role: "The Eternal Guardian".into(),
                    epic_description: "Standing since the first Rust dawn, the Borrow Checker verifies every reference. It permits no alias with mutability, and no use-after-free survives its gaze.".into(),
                },
            ],
            Language::Go => vec![
                Companion {
                    name: "gofmt".into(),
                    role: "The Style Enforcer".into(),
                    epic_description: "gofmt inscribes the law of formatting upon all Go code. Arguments about braces end forever — gofmt is the final arbiter of Go style.".into(),
                },
                Companion {
                    name: "go mod".into(),
                    role: "The Dependency Shepherd".into(),
                    epic_description: "Gone are the days of GOPATH wandering. go mod summons dependencies from the great beyond and binds them in the go.mod covenant, and versions are respected.".into(),
                },
                Companion {
                    name: "delve".into(),
                    role: "The Depth Delver".into(),
                    epic_description: "When bugs burrow deep, delve descends into the runtime trenches. It reads goroutines like scrolls and traces stacks like ancient maps of the underworld.".into(),
                },
                Companion {
                    name: "gofake".into(),
                    role: "The Test Illusionist".into(),
                    epic_description: "gofake conjures fake names, addresses, credit cards, and entire fictitious corporations for the testing realm — all legal tender in the world of tests.".into(),
                },
                Companion {
                    name: "testify".into(),
                    role: "The Assertion Champion".into(),
                    epic_description: "/testify's assertions ring with authority — require, assert, suite. Where testing was once verbose, testify makes it succinct, and failures are dramatic.".into(),
                },
            ],
            Language::Swift => vec![
                Companion {
                    name: "Xcode".into(),
                    role: "The IDE Citadel".into(),
                    epic_description: "Within Xcode's walls, Swift code is written, debugged, and born as apps. The Interface Builder hangs its canvas, and the simulator runs within its gates.".into(),
                },
                Companion {
                    name: "Swift Package Manager".into(),
                    role: "The Dependency Forge".into(),
                    epic_description: "SPM forges dependencies with a swift package init and package add. No CocoaPods treasury needed — SPM is the official summoner of external code.".into(),
                },
                Companion {
                    name: "Combine".into(),
                    role: "The Reactive Stream Sage".into(),
                    epic_description: "Combine teaches publishers to speak and subscribers to listen. The reactive streams flow through Swift's veins, and async events are processed in elegant pipelines.".into(),
                },
                Companion {
                    name: "SwiftUI".into(),
                    role: "The Declarative Cartographer".into(),
                    epic_description: "SwiftUI maps UI with declarations: 'A button here, a list there.' State flows downhill like water, and SwiftUI renders the landscape of interfaces.".into(),
                },
            ],
            Language::Kotlin => vec![
                Companion {
                    name: "IntelliJ IDEA".into(),
                    role: "The IDE Oracle".into(),
                    epic_description: "JetBrains forged IntelliJ as Kotlin's sacred vessel. Every feature, every refactoring, every ktlint correction — IntelliJ is the hammer and anvil of Kotlin craft.".into(),
                },
                Companion {
                    name: "Gradle".into(),
                    role: "The Build Daemon".into(),
                    epic_description: "Gradle Kotlin DSL speaks Kotlin to Gradle itself. 'Build scripts are code,' declared Gradle, and the Kotlin DSL was born, and builds became typed.".into(),
                },
                Companion {
                    name: "Kotlin Coroutines".into(),
                    role: "The Async Summoner".into(),
                    epic_description: "Under the JVM, the coroutine serpents coil. launch, async, await — Kotlin calls forth async warriors without the thread legions, and the JVM rests easier.".into(),
                },
                Companion {
                    name: "Koin".into(),
                    role: "The Lightweight Dependency Injector".into(),
                    epic_description: "Not Spring's bureaucracy — Koin is the functional's dagger. No XML, no annotation processing, just modules and by definitions, and the DI is achieved.".into(),
                },
            ],
            Language::TypeScript => vec![
                Companion {
                    name: "VS Code".into(),
                    role: "The IDE of the People".into(),
                    epic_description: "Microsoft forged VS Code from TypeScript's own spirit. The editor that conquered the world runs on TypeScript, serves TypeScript, and loves TypeScript with IntelliSense burning bright.".into(),
                },
                Companion {
                    name: "tsc".into(),
                    role: "The Type Oracle".into(),
                    epic_description: "The TypeScript compiler tsc reads the sacred .ts scrolls and either approves with a green BUILD SUCCESS or unleashes a scroll of type errors upon the developer.".into(),
                },
                Companion {
                    name: "ts-node".into(),
                    role: "The Immediate Executor".into(),
                    epic_description: "ts-node runs TypeScript without prior compilation — the script is transcribed on the fly. 'WHY WAIT FOR TSC?' cries ts-node, and the REPL is born.".into(),
                },
                Companion {
                    name: "ESLint".into(),
                    role: "The Lint Warden".into(),
                    epic_description: "ESLint sets the lint wardens upon TypeScript's shores. No unused variable escapes, no any-type slips unquestioned. The code quality guardians are relentless.".into(),
                },
            ],
            Language::JavaScript => vec![
                Companion {
                    name: "Node.js".into(),
                    role: "The Server Challenger".into(),
                    epic_description: "From the browser's prison, JavaScript escaped to the server. 'I SHALL POWER THE SERVER TOO!' declared Node, and npm followed, and the full-stack prophecy was fulfilled.".into(),
                },
                Companion {
                    name: "V8".into(),
                    role: "The Speeding Engine".into(),
                    epic_description: "V8 devours JavaScript and excretes pure machine code at astonishing speed. Chrome's heart, Node's soul — V8 is the fastest horse in the JavaScript cavalry.".into(),
                },
                Companion {
                    name: "npm".into(),
                    role: "The Treasury Master".into(),
                    epic_description: "The world's largest software registry, with over a million packages. npm install is the incantation that summons any library the JavaScript hero might need.".into(),
                },
                Companion {
                    name: "React".into(),
                    role: "The Component Sorcerer".into(),
                    epic_description: "React conjured the virtual DOM, a phantom reflection of the true UI. 'DIFF ME THIS,' commanded React, and the UI updated with surgical precision.".into(),
                },
                Companion {
                    name: "Webpack".into(),
                    role: "The Bundler General".into(),
                    epic_description: "When a thousand modules threatened to overwhelm the browser, Webpack marched forth and bundled them all into one deployable artifact.".into(),
                },
            ],
            Language::Java => vec![
                Companion {
                    name: "Spring".into(),
                    role: "The Enterprise Framework Titan".into(),
                    epic_description: "Spring rose to dominate the enterprise — dependency injection, web servers, microservices, reactive streams. One annotation at a time, Spring conquered the corporate kingdom.".into(),
                },
                Companion {
                    name: "Maven".into(),
                    role: "The Dependency Admiral".into(),
                    epic_description: "Maven organizes the JAR archives with a pom.xml command. Repositories are searched, dependencies descend, and the build is managed with convention over configuration.".into(),
                },
                Companion {
                    name: "JUnit".into(),
                    role: "The Test Champion".into(),
                    epic_description: "JUnit, the elder of testing frameworks, bestows @Test annotations upon methods. @Before and @After prepare and clean, and assertions prove truth upon the field.".into(),
                },
                Companion {
                    name: "Hibernate".into(),
                    role: "The ORM Sage".into(),
                    epic_description: "Hibernate translates Java objects into relational database whispers. Tables are mapped to classes, SQL is generated from intent, and the DAO layer is simplified to legend.".into(),
                },
            ],
            Language::Cpp => vec![
                Companion {
                    name: "STL".into(),
                    role: "The Standard Library Citadel".into(),
                    epic_description: "The Standard Template Library stands as a fortress of containers, algorithms, and iterators. vector, map, sort — the STL weapons are sharp and battle-tested.".into(),
                },
                Companion {
                    name: "Boost".into(),
                    role: "The Extended Library Pantheon".into(),
                    epic_description: "Beyond the STL, Boost houses libraries deemed too advanced for standardization. shared_ptr, lambda, regex, thread — Boost is the proving ground for future STL.".into(),
                },
                Companion {
                    name: "CMake".into(),
                    role: "The Build System Oracle".into(),
                    epic_description: "CMake speaks the cmake tongue and conjures makefiles and IDE projects. Cross-platform builds are CMake's domain — Visual Studio, Unix make, Ninja — all bow to its script.".into(),
                },
                Companion {
                    name: "Valgrind".into(),
                    role: "The Memory Spirit Hunter".into(),
                    epic_description: "Valgrind stalks the memory of C++ programs — leaks, undefined reads, invalid frees. Its memcheck tool is the bane of memory bug villains everywhere.".into(),
                },
                Companion {
                    name: "fmt".into(),
                    role: "The String Formatting Scribe".into(),
                    epic_description: "fmtlib writes formatted strings with compile-time safety and printf-like brevity. 'fmt::format is my song,' writes the modern C++ scribe, and the output is perfectly formed.".into(),
                },
            ],
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Antagonist {
    pub name: String,
    pub nature: String,
    pub epic_description: String,
}

impl Antagonist {
    pub fn for_language<R: Rng>(lang: Language, rng: &mut R) -> [Self; 3] {
        let antagonists = Self::all_antagonists(lang);
        antagonists
            .choose_multiple(rng, 3)
            .cloned()
            .collect::<Vec<_>>()
            .try_into()
            .unwrap()
    }

    fn all_antagonists(lang: Language) -> Vec<Self> {
        match lang {
            Language::Rust => vec![
                Antagonist {
                    name: "The Undefined Behavior Specter".into(),
                    nature: "Ancient malevolence from the C/C++ realms".into(),
                    epic_description: "It haunts the unsafe corridors of Rust, whispering use-after-free and data-race incantations. Only the borrow checker stands between Rust and this specter's corruption.".into(),
                },
                Antagonist {
                    name: "The Compile Time Dragon".into(),
                    nature: "Excessive compile times on large codebases".into(),
                    epic_description: "When the Rust project grows to a million lines, the compile time dragon awakens. Incremental compilation is the current tamer, but the dragon is patient.".into(),
                },
                Antagonist {
                    name: "The Learning Cliff".into(),
                    nature: "The steep ownership/borrow learning curve".into(),
                    epic_description: "Many warriors fall at the Borrow Checker's gate. The lifetime annotations are cryptic runes that defeat the uninitiated.".into(),
                },
                Antagonist {
                    name: "The async/await Immaturity".into(),
                    nature: "The async ecosystem is still maturing".into(),
                    epic_description: "The async草原 is not yet fully settled. Tokio dominates, but pinning, futures, and the Waker are arcane arts that test even seasoned Rust heroes.".into(),
                },
            ],
            Language::Go => vec![
                Antagonist {
                    name: "The Generics Void".into(),
                    nature: "Go's delayed arrival of generics".into(),
                    epic_description: "For years, Go warriors lacked generic types. 'WRITE THE SAME CODE FOR INT AND STRING!' they cried, until generics arrived in Go 1.18 — late but welcomed.".into(),
                },
                Antagonist {
                    name: "The Error Handling Verbosity".into(),
                    nature: "if err != nil repetition".into(),
                    epic_description: "Every function call that might fail demands: 'if err != nil { return err }'. The error handling is explicit but verbose, and the Go hero tires of the repetition.".into(),
                },
                Antagonist {
                    name: "The nil Pointer Phantom".into(),
                    nature: "Interfaces can be nil but look initialized".into(),
                    epic_description: "When an interface holds nil, it still looks like a valid value — until you call a method and the nil pointer dereference crashes the goroutine.".into(),
                },
                Antagonist {
                    name: "The Dependency Version Chasm".into(),
                    nature: "No lockfile was the original curse".into(),
                    epic_description: "Early Go had no go.sum, no lockfile. Different machines built with different versions, and reproducible builds were a legend. go.mod solved this — eventually.".into(),
                },
            ],
            Language::Swift => vec![
                Antagonist {
                    name: "The Apple Platform Tyranny".into(),
                    nature: "Swift's destiny is tied to Apple's platforms".into(),
                    epic_description: "Swift rose under Apple's wing, and the Apple platform ceiling limits its reach. Linux support exists, Windows is nascent — Swift is still finding its other homes.".into(),
                },
                Antagonist {
                    name: "The ABI Stability Wars".into(),
                    nature: "Binary compatibility across Swift versions".into(),
                    epic_description: "Swift's ABI was unstable for years — each Swift version broke binary compatibility. The ABI stability promise was a hard-won battle in the Swift chronicles.".into(),
                },
                Antagonist {
                    name: "The Weakly Typed String API Past".into(),
                    nature: "String's historical API inconsistencies".into(),
                    epic_description: "In early Swift, String was too index-based and cryptic. The modern String API improved, but the legacy scars of index distances remain.".into(),
                },
            ],
            Language::Kotlin => vec![
                Antagonist {
                    name: "The JVM Inheritance Chain".into(),
                    nature: "Limited by Java's class-based legacy".into(),
                    epic_description: "Kotlin rides upon the JVM, and the JVM demands Java's class-file format. Some Kotlin dreams are limited by what the JVM bytecode can express.".into(),
                },
                Antagonist {
                    name: "The Gradle Build Sloth".into(),
                    nature: "Even with Kotlin DSL, Gradle can be slow".into(),
                    epic_description: "The Android build times are legendary. Even with Kotlin DSL's improvements, the Gradle daemon's startup and configuration evaluation can test the hero's patience.".into(),
                },
                Antagonist {
                    name: "The Java Interop Tax".into(),
                    nature: "Kotlin-Java interop has edge cases".into(),
                    epic_description: "nullability mismatches between Kotlin's non-null types and Java's null-happy APIs create a constant null-check burden. @Nullable annotations help, but the tax remains.".into(),
                },
            ],
            Language::TypeScript => vec![
                Antagonist {
                    name: "The any-type Shadow".into(),
                    nature: "any opting out of type safety".into(),
                    epic_description: "The 'any' type is TypeScript's escape hatch — 'I DON'T KNOW WHAT THIS IS, BUT TRUST ME.' It shuts off type checking where it is used, a dangerous shadow.".into(),
                },
                Antagonist {
                    name: "The Type-erasure Prophecy".into(),
                    nature: "Runtime type information is absent".into(),
                    epic_description: "Type annotations vanish at runtime. 'I declared this as string,' says TypeScript at compile time, but at runtime it is still JavaScript, and instanceof knows no TypeScript.".into(),
                },
                Antagonist {
                    name: "The Third-party Declaration Drought".into(),
                    nature: "Missing .d.ts files for npm packages".into(),
                    epic_description: "Not all npm packages ship TypeScript declarations. When @types is missing, the hero must write declarations by hand or cast to any.".into(),
                },
                Antagonist {
                    name: "The Deep Type Inference Chasm".into(),
                    nature: "Complex generic types strain inference".into(),
                    epic_description: "Deeply nested generics sometimes stump TypeScript's inference engine. 'I GIVE UP,' it declares, and demands explicit type annotations on pain of error.".into(),
                },
            ],
            Language::JavaScript => vec![
                Antagonist {
                    name: "The typeof null Fool".into(),
                    nature: "typeof null === 'object' — historical JavaScript folly".into(),
                    epic_description: "In JavaScript's original design, typeof null returned 'object'. This error has persisted for decades — a comedy of nulls that haunts every hero's debug sessions.".into(),
                },
                Antagonist {
                    name: "The Scope Chain Confusion".into(),
                    nature: "var hoisting and closure surprises".into(),
                    epic_description: "var hoisted variables and the classic for-loop-closure trap await the unwary hero. 'let and const were forged to slay this dragon,' JavaScript now declares, 'but var's legacy remains.'".into(),
                },
                Antagonist {
                    name: "The NaN !== NaN Paradox".into(),
                    nature: "NaN is not equal to itself".into(),
                    epic_description: "NaN — Not a Number — is not equal to itself, not even to itself. 'IS THIS NAN?' the hero asks, and JavaScript answers: 'NaN !== NaN. Use isNaN().' And the hero weeps.".into(),
                },
                Antagonist {
                    name: "The Callback Pyramid of Doom".into(),
                    nature: "Nested callbacks beyond readability".into(),
                    epic_description: "Before promises and async/await, callback pyramids rose endlessly. 'DO THIS, THEN THAT, THEN IF THAT SUCCEEDED, DO THE OTHER,' and the indentation reached the sky.".into(),
                },
            ],
            Language::Java => vec![
                Antagonist {
                    name: "The Generics Erasure Curse".into(),
                    nature: "Type erasure at runtime loses generic info".into(),
                    epic_description: "Java generics are compile-time only — at runtime, all is raw Object. 'I thought this was List<String>!' cries the hero at runtime reflection, but Java only sees raw List.".into(),
                },
                Antagonist {
                    name: "The Checked Exception Overload".into(),
                    nature: "Checked exceptions clutter method signatures".into(),
                    epic_description: "Java forces IOException, SQLException, ClassNotFoundException upon every method that might throw. The method signatures become scrolls of exception obligations.".into(),
                },
                Antagonist {
                    name: "The NullPointerException Hydra".into(),
                    nature: "The null dragon has many heads".into(),
                    epic_description: "Despite Java's maturity, NPE still slays warriors. Every object access could be null, and Java never solved the billion-dollar mistake it helped popularize.".into(),
                },
                Antagonist {
                    name: "The JVM Memory Appetite".into(),
                    nature: "GC pauses and memory overhead".into(),
                    epic_description: "The Garbage Collector, while helpful, demands its tithe in memory and pause time. For low-latency heroes, the GC's world-stopping collections are a recurring nightmare.".into(),
                },
            ],
            Language::Cpp => vec![
                Antagonist {
                    name: "The Undefined Behavior Labyrinth".into(),
                    nature: "UB is C++'s most dangerous labyrinth".into(),
                    epic_description: "Dangling pointers, out-of-bounds access, use-after-free — C++ permits these, and the compiler may optimize based on the assumption they never happen. UB is the dragon within the dragon.".into(),
                },
                Antagonist {
                    name: "The Header Dependency Maze".into(),
                    nature: "Compilation hell from header includes".into(),
                    epic_description: "Every change to a header recompiles everything that transitively includes it. Template instantiation in headers multiplies this pain exponentially.".into(),
                },
                Antagonist {
                    name: "The Segmentation Fault Specter".into(),
                    nature: "Memory access violations haunt C++ warriors".into(),
                    epic_description: "C++ gives raw pointers to the machine, and the machine is unforgiving. Segfaults lurk in the shadows of every pointer arithmetic — the warrior must be ever vigilant.".into(),
                },
                Antagonist {
                    name: "The Macro Preprocessor Crypt".into(),
                    nature: "#define macros are untyped, undebuggable text substitution".into(),
                    epic_description: "Before the compiler proper, the preprocessor runs — a text substitution ghost. #define MAX(a,b) ((a)>(b)?(a):(b)) has subtleties that bite, and debuggers see only the expanded result.".into(),
                },
            ],
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Omen {
    pub title: String,
    pub verse: String,
}

impl Omen {
    pub fn for_language<R: Rng>(lang: Language, rng: &mut R) -> [Self; 2] {
        let omens = Self::all_omens(lang);
        omens.choose_multiple(rng, 2).cloned().collect::<Vec<_>>().try_into().unwrap()
    }

    fn all_omens(lang: Language) -> Vec<Self> {
        match lang {
            Language::Rust => vec![
                Omen {
                    title: "The Async草原 Prophecy".into(),
                    verse: "In time, the async/await steppe shall be settled with standardized libraries, and the Rust hero shall ride across it without fearing Tokio's dominance.".into(),
                },
                Omen {
                    title: "The Ownership Renaissance".into(),
                    verse: "Other tongues shall look upon Rust's ownership model and see its wisdom. The C/C++ successor, whoever emerges, shall wear Rust's armor of proof.".into(),
                },
                Omen {
                    title: "The WASM Alliance".into(),
                    verse: "Rust and WebAssembly shall forge an alliance, and Rust shall run in the browser's heart, and systems programming shall come to every webpage.".into(),
                },
                Omen {
                    title: "The Embedded Expansion".into(),
                    verse: "Rust shall descend into the embedded realm — microcontrollers, firmwares, kernels. The ownership model shall keep the smallest devices safe.".into(),
                },
            ],
            Language::Go => vec![
                Omen {
                    title: "The Genericsmatio".into(),
                    verse: "With generics now part of Go's canon, the language shall attract warriors from theMLand, and code duplication shall diminish across the Go kingdom.".into(),
                },
                Omen {
                    title: "The FaaS Dominion".into(),
                    verse: "Functions as a Service shall be Go's greatest domain. The goroutine economy scales perfectly to zero and spikes to a million, and Go remains the serverless champion.".into(),
                },
                Omen {
                    title: "The Go 2 Ascension".into(),
                    verse: "Error handling improvements shall come in Go 2, and the verbosity dragon shall be vanquished. The ? operator shall spread its blessing to all Go functions.".into(),
                },
            ],
            Language::Swift => vec![
                Omen {
                    title: "The Server-side Swift Rise".into(),
                    verse: "Swift shall expand beyond Apple Valley. Server-side Swift — Vapor, Hummingbird — shall challenge Node and Go in the backend arena.".into(),
                },
                Omen {
                    title: "The Swift 6 Concurrency Dawn".into(),
                    verse: "Swift 6's strict concurrency checking shall vanquish data races forever. The Sendable protocol shall be the new ownership ledger.".into(),
                },
                Omen {
                    title: "The Cross-Platform Quest".into(),
                    verse: "Swift shall spread to Windows and Linux, and the Apple Tyranny shall weaken. One day, Swift may rival Java in platform reach.".into(),
                },
            ],
            Language::Kotlin => vec![
                Omen {
                    title: "The Multiplatform Odyssey".into(),
                    verse: "Kotlin Multiplatform shall enable code-sharing between Android, iOS, web, and native. 'Write once, run on every platform' shall be Kotlin's new oath.".into(),
                },
                Omen {
                    title: "The Compose Revolution".into(),
                    verse: "Jetpack Compose shall replace the XML layouts, and declarative UI shall reign in Android. Kotlin's future is written in composable functions.".into(),
                },
                Omen {
                    title: "The K2 Compiler Ascension".into(),
                    verse: "The K2 compiler, with its rewritten frontend, shall compile Kotlin twice as fast, and developers shall weep tears of joy at the reduced build times.".into(),
                },
            ],
            Language::TypeScript => vec![
                Omen {
                    title: "The Type-level Magic Proliferation".into(),
                    verse: "TypeScript's type-level programming shall grow ever more arcane. Template literal types, conditional types — TypeScript shall become its own type language.".into(),
                },
                Omen {
                    title: "The ts-pattern Revolution".into(),
                    verse: "Pattern matching shall come to TypeScript, and exhaustiveness checking shall reach new heights. The switch statement shall be reborn.".into(),
                },
                Omen {
                    title: "The JavaScript Convergence".into(),
                    verse: "As TypeScript's stricter modes grow, JavaScript itself shall evolve to meet TypeScript halfway. The gap between TS and JS shall narrow with each ECMAScript edition.".into(),
                },
            ],
            Language::JavaScript => vec![
                Omen {
                    title: "The WebAssembly Challenger".into(),
                    verse: "WebAssembly shall challenge JavaScript in the browser — but JavaScript shall form alliances with WASM, loading it seamlessly and profiting from its speed.".into(),
                },
                Omen {
                    title: "The Node.js Succession".into(),
                    verse: "Bun and Deno rise as Node challengers, but Node's ecosystem depth shall resist for years. Eventually, a convergence may emerge — or three ecosystems shall persist.".into(),
                },
                Omen {
                    title: "The ES20XX Editions".into(),
                    verse: "Each ECMAScript edition brings new syntax — optional chaining, nullish coalescing, regex improvements. JavaScript grows more ergonomic with every year.".into(),
                },
            ],
            Language::Java => vec![
                Omen {
                    title: "The Virtual Threads Elevation".into(),
                    verse: "Project Loom's virtual threads shall free Java from the thread-per-request burden. 'A million virtual threads, consuming little,' the prophecy speaks, and Java's concurrency fearlessness shall return.".into(),
                },
                Omen {
                    title: "The JVM Renaissance".into(),
                    verse: "The JVM shall attract new languages — Kotlin, Scala, Clojure, JRuby — the JVM dream lives on. Java the language may fade, but Java the platform shall endure.".into(),
                },
                Omen {
                    title: "The Cloud Native Adoption".into(),
                    verse: "Java shall be reforged for the cloud native age — GraalVM for AOT compilation, smaller images, faster startup. The old paladin learns new tricks.".into(),
                },
            ],
            Language::Cpp => vec![
                Omen {
                    title: "The Modules Arrival".into(),
                    verse: "C++ Modules shall finally replace the preprocessor-based header inclusion model. Compilation times shall plummet, and the dependency maze shall begin to clear.".into(),
                },
                Omen {
                    title: "The Safety Reform".into(),
                    verse: "C++ shall embrace memory safety — through profile annotations, through std::expected, through bounds-checking libraries. The unsafe corridor shall narrow.".into(),
                },
                Omen {
                    title: "The Embedded Crown".into(),
                    verse: "In embedded systems and game engines, C++ shall remain supreme. The performance vow shall never be broken, and the raw machine shall answer to C++ alone.".into(),
                },
            ],
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SagaCompanion {
    pub name: String,
    pub role: String,
    pub description: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EpicSaga {
    pub language: String,
    pub archetype: HeroArchetype,
    pub deeds: Vec<LegendaryDeed>,
    pub companions: Vec<SagaCompanion>,
    pub antagonists: Vec<Antagonist>,
    pub omens: Vec<Omen>,
    pub closure: String,
    pub generated_at: String,
}

impl EpicSaga {
    pub fn generate<R: Rng>(lang: Language, rng: &mut R) -> Self {
        let closures = Self::closures(lang);
        let closure = closures.choose(rng).unwrap().clone();

        let companions = Companion::for_language(lang, rng);
        let companions: Vec<SagaCompanion> = companions
            .into_iter()
            .map(|c| SagaCompanion {
                name: c.name,
                role: c.role,
                description: c.epic_description,
            })
            .collect();

        let deeds: Vec<LegendaryDeed> = (0..3)
            .map(|_| LegendaryDeed::for_language(lang, rng))
            .collect();

        let antagonists = Antagonist::for_language(lang, rng).to_vec();
        let omens: Vec<Omen> = Omen::for_language(lang, rng).to_vec();

        Self {
            archetype: HeroArchetype::for_language(lang),
            language: lang.as_str().to_string(),
            deeds,
            companions,
            antagonists,
            omens,
            closure,
            generated_at: chrono::Utc::now().to_rfc3339(),
        }
    }

    fn closures(lang: Language) -> Vec<String> {
        match lang {
            Language::Rust => vec![
                "Thus ends the saga of Rust — Fearless, Proven, Forever Secure.".into(),
                "Let it be remembered: Rust writes what none dare promise. Memory safe. Concurrency fearless. Forever.".into(),
                "The Ownership Republic endures. Its blade is sharp, its ledger is exact, and its highlands shall never fall to memory's chaos.".into(),
            ],
            Language::Go => vec![
                "And so the saga of Go closes — Simple, Shipped, Always Building.".into(),
                "The Goroutine Harbor remains open. Come one, come all — the channel gates never close, and the gopher's welcome is eternal.".into(),
                "Let it be known: Go came, Go compiled, Go shipped. Simplicity was its oath, and simplicity endures.".into(),
            ],
            Language::Swift => vec![
                "Thus the Swift saga closes — Elegant, Safe, Apple-Blessed.".into(),
                "The Protocol Covenant stands. Swift's warriors abide by capability, not inheritance. The optionals are safe, and the types are true.".into(),
                "From Apple's valley, Swift rose to touch every platform. Its elegance is its oath; its safety, its eternal promise.".into(),
            ],
            Language::Kotlin => vec![
                "Thus the Kotlin saga closes — Transmuted, Null-Safe, JVM-Eternal.".into(),
                "The Alchemist's work is never done. Kotlin transforms the JVM, transmutes nulls to safety, and forges coroutines in the fire of asynchrony.".into(),
                "Kotlin proved that the JVM could evolve. Null-safe, extension-wielding, coroutine-summoning — the JVM knight rides eternal.".into(),
            ],
            Language::TypeScript => vec![
                "Thus the TypeScript saga closes — Prophetic, Typed, Erasure-Blessed.".into(),
                "The Type Oracle speaks: 'WHAT THOU DECLAREST, I SHALL PROVE.' And the JavaScript realms tremble with newfound certainty.".into(),
                "TypeScript brought order to the scripting wilds. The types are known, the shapes are clear, and the runtime remains untouched by compile-time's hand.".into(),
            ],
            Language::JavaScript => vec![
                "Thus the JavaScript saga closes — Everywhere, Prototypal, Eternal.".into(),
                "JavaScript said: 'I SHALL RUN,' and it ran — on servers, browsers, phones, and in the smallest IoT toaster's soul. Nowhere is JavaScript absent.".into(),
                "The event loop never sleeps. The prototype chain extends forever. JavaScript is the trickster that conquered the world without asking permission.".into(),
            ],
            Language::Java => vec![
                "Thus the Java saga closes — Oath-Bound, Virtual, Enterprise-Forged.".into(),
                "'WRITE ONCE, RUN ANYWHERE' — the vow was spoken, and the JVM carried Java's bytecode to every shore. The enterprise kingdom stands.".into(),
                "Java, the paladin of the corporate realm, endures. The garbage collector keeps its vigil, and the JVM's oath shall not be broken in our lifetime.".into(),
            ],
            Language::Cpp => vec![
                "Thus the C/C++ saga closes — Ancient, Powerful, Uncompromising.".into(),
                "The raw machine answers to C++. No runtime, no interpreter — only the metal speaks to metal. The performance vow is C++'s eternal contract.".into(),
                "From C's first light to C++'s template sorcery, the highlands have stood. C/C++ is the root of all systems, and the root does not forget its children.".into(),
            ],
        }
    }

    pub fn render_text(&self) -> String {
        let mut out = String::new();

        out.push_str("╔══════════════════════════════════════════════════════════════════╗\n");
        out.push_str("║          ⚔️  POLYGLOT EPIC SAGA  ⚔️                                  ║\n");
        out.push_str("╠══════════════════════════════════════════════════════════════════╣\n");
        out.push_str("║   The Heroic Chronicle of a Programming Language                 ║\n");
        out.push_str("╚══════════════════════════════════════════════════════════════════╝\n\n");

        out.push_str(&format!(
            "🐾 HERO: {} — {}\n",
            self.language, self.archetype.epithet
        ));
        out.push_str(&format!("   Archetype: {}\n", self.archetype.archetype));
        out.push_str(&format!("   Weapon:    {}\n", self.archetype.weapon));
        out.push_str(&format!("   Armor:     {}\n", self.archetype.armor));
        out.push_str(&format!("   Home:      {}\n", self.archetype.home));
        out.push('\n');

        // Chapter I
        out.push_str("═══════════════════════════════════════════════════════════════════\n");
        out.push_str("📜 CHAPTER I: THE SUMMONING\n");
        out.push_str("═══════════════════════════════════════════════════════════════════\n");
        out.push_str(&format!(
            "In the age before memory safety, {} arose upon the digital stage.\n",
            self.language
        ));
        out.push_str(&format!(
            "This hero, bearing the epithet '{}', took up the {} and\n",
            self.archetype.epithet, self.archetype.weapon
        ));
        out.push_str(&format!(
            "donned the {}. From {} did this champion emerge,\n",
            self.archetype.armor, self.archetype.home
        ));
        out.push_str("answering the developer's call to build, to ship, to endure.\n\n");

        // Chapter II
        out.push_str("═══════════════════════════════════════════════════════════════════\n");
        out.push_str("⚔️  CHAPTER II: THE LEGENDARY DEEDS\n");
        out.push_str("═══════════════════════════════════════════════════════════════════\n");
        for (i, deed) in self.deeds.iter().enumerate() {
            out.push_str(&format!("\n◆ DEED {}: « {} »\n", i + 1, deed.title));
            let verses: Vec<&str> = deed.epic_verse.split(". ").collect();
            for verse in verses {
                out.push_str(&format!("  {}.\n", verse.trim()));
            }
            out.push_str(&format!("\n  Significance: {}\n", deed.significance));
        }
        out.push('\n');

        // Chapter III
        out.push_str("═══════════════════════════════════════════════════════════════════\n");
        out.push_str("🛡️  CHAPTER III: THE COMPANION COUNCIL\n");
        out.push_str("═══════════════════════════════════════════════════════════════════\n");
        out.push_str("No hero walks alone. The Companions of the Epic Stand:\n\n");
        for (i, companion) in self.companions.iter().enumerate() {
            out.push_str(&format!(
                "  ⚔ COMPANION {}: {} — « {} »\n",
                i + 1, companion.name, companion.role
            ));
            out.push_str(&format!("  {}\n\n", companion.description));
        }

        // Chapter IV
        out.push_str("═══════════════════════════════════════════════════════════════════\n");
        out.push_str("👹 CHAPTER IV: THE ANTAGONIST ALLIANCE\n");
        out.push_str("═══════════════════════════════════════════════════════════════════\n");
        out.push_str("Every hero faces darkness. The Perils of the Epic:\n\n");
        for (i, antagonist) in self.antagonists.iter().enumerate() {
            out.push_str(&format!(
                "  ⛔ FOE {}: {} ({})\n",
                i + 1, antagonist.name, antagonist.nature
            ));
            out.push_str(&format!("  {}\n\n", antagonist.epic_description));
        }

        // Chapter V
        out.push_str("═══════════════════════════════════════════════════════════════════\n");
        out.push_str("🔮 CHAPTER V: OMENS & PROPHECY\n");
        out.push_str("═══════════════════════════════════════════════════════════════════\n");
        out.push_str("The Seers of the Epic have spoken:\n\n");
        for (i, omen) in self.omens.iter().enumerate() {
            out.push_str(&format!("  ✦ PROPHECY {}: « {} »\n", i + 1, omen.title));
            out.push_str(&format!("  {}\n\n", omen.verse));
        }

        // Chapter VI
        out.push_str("═══════════════════════════════════════════════════════════════════\n");
        out.push_str("🎭 CHAPTER VI: THE EPIC CLOSURE\n");
        out.push_str("═══════════════════════════════════════════════════════════════════\n\n");
        out.push_str(&format!("  {}\n\n", self.closure));

        out.push_str("═══════════════════════════════════════════════════════════════════\n");
        out.push_str(&format!(
            "  Generated for: {} | {}",
            self.language, self.generated_at
        ));
        out.push_str("\n═══════════════════════════════════════════════════════════════════\n");

        out
    }

    pub fn to_json(&self) -> Result<String, serde_json::Error> {
        serde_json::to_string_pretty(self)
    }
}

// ─────────────────────────────────────────────────────────────────
// Rotation
// ─────────────────────────────────────────────────────────────────

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RotationState {
    pub languages: Vec<String>,
    pub current_index: usize,
    pub last_language: Option<String>,
    pub updated_at: String,
}

pub fn load_rotation(path: impl AsRef<Path>) -> Result<RotationState, String> {
    let content =
        fs::read_to_string(path.as_ref()).map_err(|e| format!("IO error: {}", e))?;
    serde_json::from_str(&content).map_err(|e| format!("Parse error: {}", e))
}

pub fn save_rotation(path: impl AsRef<Path>, state: &RotationState) -> Result<(), String> {
    let json =
        serde_json::to_string_pretty(state).map_err(|e| format!("Encode error: {}", e))?;
    let tmp = format!("{}.tmp", path.as_ref().display());
    fs::write(&tmp, &json).map_err(|e| format!("IO error: {}", e))?;
    fs::rename(&tmp, path.as_ref()).map_err(|e| format!("Rename error: {}", e))?;
    Ok(())
}

pub fn advance_rotation(state: &mut RotationState) {
    let lang = state.languages.get(state.current_index).cloned();
    state.last_language = lang;
    if !state.languages.is_empty() {
        state.current_index = (state.current_index + 1) % state.languages.len();
    }
    state.updated_at = chrono::Utc::now().to_rfc3339();
}

pub fn run_cycle<R: Rng>(
    rotation_path: impl AsRef<Path>,
    rng: &mut R,
) -> Result<EpicSaga, String> {
    let mut state = load_rotation(rotation_path.as_ref())?;
    let lang = state
        .languages
        .get(state.current_index)
        .ok_or("Empty language list")?;
    let lang_enum = Language::from_str(lang).ok_or(format!("Unknown language: {}", lang))?;
    let saga = EpicSaga::generate(lang_enum, rng);
    advance_rotation(&mut state);
    save_rotation(rotation_path.as_ref(), &state)?;
    Ok(saga)
}

// ─────────────────────────────────────────────────────────────────
// Saga Log
// ─────────────────────────────────────────────────────────────────

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SagaRun {
    pub language: String,
    pub generated_at: String,
    pub archetype: String,
    pub deed_titles: Vec<String>,
}

#[derive(Debug, Default, Serialize, Deserialize)]
pub struct SagaLog {
    pub runs: Vec<SagaRun>,
}

impl SagaLog {
    pub fn add_run(&mut self, saga: &EpicSaga) {
        self.runs.push(SagaRun {
            language: saga.language.clone(),
            generated_at: saga.generated_at.clone(),
            archetype: saga.archetype.archetype.clone(),
            deed_titles: saga.deeds.iter().map(|d| d.title.clone()).collect(),
        });
        if self.runs.len() > 100 {
            self.runs.remove(0);
        }
    }

    pub fn load(path: impl AsRef<Path>) -> Self {
        fs::read_to_string(path.as_ref())
            .ok()
            .and_then(|c| serde_json::from_str(&c).ok())
            .unwrap_or_default()
    }

    pub fn save(&self, path: impl AsRef<Path>) -> Result<(), String> {
        let json =
            serde_json::to_string_pretty(self).map_err(|e| format!("Encode error: {}", e))?;
        fs::write(path.as_ref(), json).map_err(|e| format!("IO error: {}", e))?;
        Ok(())
    }
}

pub fn run_cycle_with_log<R: Rng>(
    rotation_path: impl AsRef<Path>,
    log_path: impl AsRef<Path>,
    rng: &mut R,
) -> Result<EpicSaga, String> {
    let saga = run_cycle(rotation_path.as_ref(), rng)?;
    let mut log = SagaLog::load(log_path.as_ref());
    log.add_run(&saga);
    log.save(log_path.as_ref())?;
    Ok(saga)
}

// ─────────────────────────────────────────────────────────────────
// Tests
// ─────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use rand::SeedableRng;

    fn test_rng() -> impl rand::RngCore {
        rand::rngs::StdRng::seed_from_u64(42)
    }

    #[test]
    fn test_language_from_str_roundtrip() {
        for lang in Language::all() {
            assert_eq!(Language::from_str(lang.as_str()), Some(lang));
        }
        assert_eq!(Language::from_str("Python"), None);
    }

    #[test]
    fn test_saga_generation_all_languages() {
        let mut rng = test_rng();
        for lang in Language::all() {
            let saga = EpicSaga::generate(lang, &mut rng);
            assert_eq!(saga.language, lang.as_str());
            assert!(!saga.archetype.archetype.is_empty());
            assert_eq!(saga.deeds.len(), 3);
            assert_eq!(saga.companions.len(), 3);
            assert_eq!(saga.antagonists.len(), 3);
            assert_eq!(saga.omens.len(), 2);
            assert!(!saga.closure.is_empty());
            assert!(!saga.generated_at.is_empty());
        }
    }

    #[test]
    fn test_saga_render_text_all_languages() {
        let mut rng = test_rng();
        for lang in Language::all() {
            let saga = EpicSaga::generate(lang, &mut rng);
            let text = saga.render_text();
            assert!(text.contains(lang.as_str()));
            assert!(text.contains("CHAPTER"));
            assert!(text.contains("DEED"));
            assert!(text.contains("COMPANION"));
            assert!(text.contains("FOE"));
            assert!(text.contains("PROPHECY"));
            assert!(text.contains("CLOSURE"));
        }
    }

    #[test]
    fn test_saga_json_serialization_roundtrip() {
        let mut rng = test_rng();
        let saga = EpicSaga::generate(Language::Rust, &mut rng);
        let json = saga.to_json().unwrap();
        let parsed: EpicSaga = serde_json::from_str(&json).unwrap();
        assert_eq!(parsed.language, saga.language);
        assert_eq!(parsed.archetype.archetype, saga.archetype.archetype);
    }

    #[test]
    fn test_saga_deeds_are_unique() {
        let mut rng = test_rng();
        let mut titles: std::collections::HashSet<String> = std::collections::HashSet::new();
        for _ in 0..10 {
            let saga = EpicSaga::generate(Language::Rust, &mut rng);
            for deed in &saga.deeds {
                titles.insert(deed.title.clone());
            }
        }
        assert!(titles.len() > 3);
    }

    #[test]
    fn test_heroes_are_distinct_per_language() {
        let mut rng = test_rng();
        let archetypes: Vec<_> = Language::all()
            .iter()
            .map(|lang| {
                let saga = EpicSaga::generate(*lang, &mut rng);
                saga.archetype.archetype.clone()
            })
            .collect();
        let unique: std::collections::HashSet<_> = archetypes.iter().collect();
        assert_eq!(unique.len(), archetypes.len());
    }

    #[test]
    fn test_closure_non_empty_for_all_languages() {
        let mut rng = test_rng();
        for lang in Language::all() {
            let saga = EpicSaga::generate(lang, &mut rng);
            assert!(!saga.closure.is_empty());
            assert!(!saga.generated_at.is_empty());
        }
    }

    #[test]
    fn test_render_text_contains_all_chapters() {
        let mut rng = test_rng();
        let saga = EpicSaga::generate(Language::Go, &mut rng);
        let text = saga.render_text();
        for chapter in [
            "I: THE SUMMONING",
            "II: THE LEGENDARY DEEDS",
            "III: THE COMPANION COUNCIL",
            "IV: THE ANTAGONIST ALLIANCE",
            "V: OMENS & PROPHECY",
            "VI: THE EPIC CLOSURE",
        ] {
            assert!(
                text.contains(chapter),
                "Missing chapter: {}",
                chapter
            );
        }
    }

    #[test]
    fn test_language_as_str() {
        assert_eq!(Language::Rust.as_str(), "Rust");
        assert_eq!(Language::Cpp.as_str(), "C/C++");
        assert_eq!(Language::Go.as_str(), "Go");
    }

    #[test]
    fn test_language_file_ext() {
        assert_eq!(Language::Rust.file_ext(), "rs");
        assert_eq!(Language::Go.file_ext(), "go");
        assert_eq!(Language::Cpp.file_ext(), "cpp");
        assert_eq!(Language::Swift.file_ext(), "swift");
        assert_eq!(Language::Kotlin.file_ext(), "kt");
        assert_eq!(Language::TypeScript.file_ext(), "ts");
        assert_eq!(Language::JavaScript.file_ext(), "js");
        assert_eq!(Language::Java.file_ext(), "java");
    }

    #[test]
    fn test_rotation_state_roundtrip() {
            let temp_dir = std::env::temp_dir();
        let path = temp_dir.join("test_rotation.json");

        {
            let state = RotationState {
                languages: vec!["Rust".into(), "Go".into(), "Swift".into()],
                current_index: 1,
                last_language: Some("Rust".into()),
                updated_at: "2026-01-01T00:00:00Z".into(),
            };
            save_rotation(&path, &state).unwrap();
        }

        let loaded = load_rotation(&path).unwrap();
        assert_eq!(loaded.languages.len(), 3);
        assert_eq!(loaded.current_index, 1);
        assert_eq!(loaded.last_language, Some("Rust".into()));

        std::fs::remove_file(&path).ok();
    }

    #[test]
    fn test_advance_rotation() {
        let mut state = RotationState {
            languages: vec!["Rust".into(), "Go".into(), "Swift".into()],
            current_index: 0,
            last_language: None,
            updated_at: "2026-01-01T00:00:00Z".into(),
        };

        advance_rotation(&mut state);
        assert_eq!(state.current_index, 1);
        assert_eq!(state.last_language, Some("Rust".into()));

        advance_rotation(&mut state);
        assert_eq!(state.current_index, 2);

        advance_rotation(&mut state);
        assert_eq!(state.current_index, 0); // wraps

        advance_rotation(&mut state);
        assert_eq!(state.current_index, 1);
    }

    #[test]
    fn test_saga_log_roundtrip() {
            let temp_dir = std::env::temp_dir();
        let path = temp_dir.join("test_saga_log.json");

        let mut rng = test_rng();
        let saga = EpicSaga::generate(Language::Rust, &mut rng);

        let mut log = SagaLog::default();
        log.add_run(&saga);
        log.save(&path).unwrap();

        let loaded = SagaLog::load(&path);
        assert_eq!(loaded.runs.len(), 1);
        assert_eq!(loaded.runs[0].language, "Rust");

        std::fs::remove_file(&path).ok();
    }
}
