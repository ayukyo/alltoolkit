# music_utils - Music Theory Utilities for Go

Zero external dependencies - pure Go standard library implementation.

## Features

- **Note Frequency Calculations**: Convert between note names, MIDI numbers, and frequencies
- **Scale Generation**: Major, minor, modes, pentatonic, blues, chromatic, whole tone
- **Chord Generation**: Major, minor, diminished, augmented, seventh chords, and more
- **Chord Identification**: Identify chords from a set of notes
- **Interval Calculations**: Calculate intervals between notes
- **MIDI Conversions**: MIDI note numbers ↔ note names ↔ frequencies
- **Key Signatures**: Circle of fifths, relative keys
- **Tempo Utilities**: BPM ↔ milliseconds conversions
- **Note Values**: Whole, half, quarter, eighth notes with dotted support
- **Harmonic Series**: Generate harmonic frequencies
- **Just Intonation**: Common just intonation ratios
- **Equal Temperament**: Frequency calculations using standard tuning

## Installation

```go
import music "github.com/ayukyo/alltoolkit/Go/music_utils"
```

## Quick Examples

### Note Frequency

```go
note := music.Note{Name: music.A, Octave: 4}
fmt.Println(note.Frequency()) // 440 Hz
fmt.Println(note.MIDI())       // 69
```

### Parse Note

```go
note, err := music.ParseNote("C#5")
// note.Name == music.CSharp, note.Octave == 5
```

### Frequency to Note

```go
note := music.FrequencyToNote(440.0) // A4
cents := music.CentsDeviation(441.0) // ~+4 cents
```

### Scales

```go
cMajor := music.NewScale(music.C, music.MajorScale)
fmt.Println(cMajor.Notes()) // [C, D, E, F, G, A, B]
fmt.Println(cMajor.Frequencies(4, 1)) // Frequencies starting from C4
```

### Chords

```go
cMajor := music.NewChord(music.C, music.Major)
fmt.Println(cMajor.Notes())       // [C, E, G]
fmt.Println(cMajor.Frequencies(4)) // [261.63, 329.63, 392.00]

// Identify chord from notes
chord, err := music.IdentifyChord([]music.NoteName{music.C, music.E, music.G})
// chord.Type == music.Major
```

### Intervals

```go
c4 := music.Note{Name: music.C, Octave: 4}
g4 := music.Note{Name: music.G, Octave: 4}
interval := music.GetInterval(c4, g4) // Perfect Fifth
```

### Transposition

```go
c4 := music.Note{Name: music.C, Octave: 4}
g4 := c4.Transpose(7) // Perfect fifth up
c5 := c4.Transpose(12) // One octave up
```

### BPM Conversions

```go
ms := music.BPMtoMilliseconds(120) // 500 ms per beat
sec := music.BPMtoSeconds(60)     // 1 second per beat
```

### Note Values

```go
ms := music.QuarterNote.DurationMs(120) // 500 ms at 120 BPM
dotted := music.QuarterNote.DurationWithDots(1) // 1.5 beats
```

### Circle of Fifths

```go
cof := music.CircleOfFifths() // [C, G, D, A, E, B, F#, C#, G#, D#, A#, F]
minor := music.RelativeMinor(music.C) // A
```

### Harmonic Series

```go
harmonics := music.HarmonicSeries(220.0, 8) // First 8 harmonics of A3
```

### Just Intonation

```go
fifth := music.JustIntervals["fifth"]
freq := fifth.Frequency(440.0) // 660 Hz (3:2 ratio)
```

## API Reference

### Note Types

- `NoteName`: C, CSharp, D, DSharp, E, F, FSharp, G, GSharp, A, ASharp, B
- `Note`: {Name NoteName, Octave int}

### Scale Types

- `MajorScale`, `MinorScale`, `HarmonicMinor`, `MelodicMinor`
- `Dorian`, `Phrygian`, `Lydian`, `Mixolydian`, `Locrian`
- `PentatonicMajor`, `PentatonicMinor`, `BluesScale`
- `Chromatic`, `WholeTone`

### Chord Types

- `Major`, `Minor`, `Diminished`, `Augmented`
- `MajorSeventh`, `MinorSeventh`, `DominantSeventh`, `DiminishedSeventh`
- `SuspendedSecond`, `SuspendedFourth`
- `Ninth`, `Eleventh`, `Thirteenth` variants
- `Power` (root + fifth)

### Interval Types

- `Unison`, `MinorSecond`, `MajorSecond`
- `MinorThird`, `MajorThird`, `PerfectFourth`, `AugmentedFourth`
- `PerfectFifth`, `MinorSixth`, `MajorSixth`
- `MinorSeventh`, `MajorSeventh`, `Octave`

## Running Tests

```bash
cd Go/music_utils
go test -v
```

## Running Examples

```bash
cd Go/music_utils/examples
go run main.go
```

## License

MIT License - Part of AllToolkit

## Author

AllToolkit Automated Development System
Date: 2026-04-20