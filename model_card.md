# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Goal / Task

VibeMatch suggests the 5 songs from a small catalog that best fit what a user says they like. It compares every song to the user's favorite genre, mood, and energy level, then shows the top matches with the reasons each one was picked.

---

## 3. Data Used

The catalog has 20 songs (the starter had 10, and I added 10) covering 17 genres and 16 moods. Each song has a genre, mood, energy, valence (happy vs. sad), and acousticness; tempo and danceability are in the file but not used. Most genres only have one song and only four songs are really loud, so the lists run out of good matches fast. There's no data on lyrics, language, or popularity.

---

## 4. Algorithm Summary

Every song gets points for how well it fits the user: genre is worth the most (2), then mood (1.5), then how close its energy is (1.5), plus small bonuses for valence and acousticness (0.5 each), for a max of 6. Close-but-not-exact matches get half credit, like "indie pop" for a pop fan or "relaxed" for someone who wants "chill." Then every song is sorted by points and the top 5 are shown.

---

## 5. Observed Behavior / Biases

The system trusts labels more than sound: a genre and mood match is worth 3.5 points, which is more than energy, valence, and acousticness combined (2.5). That's why my "Sad but High Energy" user got a quiet folk song (energy 0.30) at #1 even though they asked for 0.90. Since 15 of the 17 genres only have one song, the rest of each list is filled with whatever's loud, which is why "Gym Hero" showed up in 5 of 9 lists. Users who want very quiet music also lose out, because no song is quieter than 0.22 energy.

---

## 6. Evaluation Process

I tested 9 profiles: 3 normal ones (Pop / Happy, Lofi / Chill Study, Deep Intense Rock) and 6 made to trick the system (Sad but High Energy, Metal but Chill, Whitespace Genre, Substring Genre 'r', Unknown Mood, Out-of-Range Energy). I also tried halving the genre weight and doubling energy as a one-off experiment; the sad list got closer to right, but the rock list didn't change, so the small catalog is the bigger problem. Comparing pairs of profiles:

- **Pop / Happy vs. Lofi / Chill Study:** No songs in common. Pop got loud songs and lofi got quiet, acoustic ones, which makes sense.
- **Pop / Happy vs. Deep Intense Rock:** "Gym Hero" is in both. The pop fan gets it for being a loud pop song, and the rock fan gets it for its "intense" mood.
- **Deep Intense Rock vs. Out-of-Range Energy:** Same 5 songs in the same order, just lower scores, because an energy of 1.5 matches nothing.
- **Pop / Happy vs. Whitespace Genre:** Typing " Pop " with spaces dropped "Sunrise City" from 5.88 to 4.88, since it only counted as a half genre match.
- **Lofi / Chill Study vs. Metal but Chill:** Both got the same calm songs. The only metal song is too loud for someone who wants quiet music.
- **Deep Intense Rock vs. Sad but High Energy:** Both want 0.90 energy, but the sad list starts with a quiet folk song because matching "folk" and "sad" beats matching energy.

<details>
<summary>Full terminal output for every profile, plus the weight-shift results</summary>

Terminal output of `python3 -m src.main` (top 5 per profile). The first three are standard profiles; the rest are adversarial / edge-case profiles meant to trick the scoring.

**Pop / Happy**

```
============================================================
  Profile: Pop / Happy
  genre=pop | mood=happy | energy=0.80 | valence=0.80 | acoustic=no
============================================================

  #1  Sunrise City  by Neon Echo
      Score: 5.88 / 6.00
      Why:
        - genre match: pop (+2.00)
        - mood match: happy (+1.50)
        - energy 0.82 vs target 0.80 (+1.49)
        - valence 0.84 vs target 0.80 (+0.48)
        - non-acoustic fit (+0.41)

  #2  Rooftop Lights  by Indigo Parade
      Score: 4.77 / 6.00
      Why:
        - related genre: indie pop (+1.00)
        - mood match: happy (+1.50)
        - energy 0.76 vs target 0.80 (+1.45)
        - valence 0.81 vs target 0.80 (+0.50)
        - non-acoustic fit (+0.33)

  #3  Gym Hero  by Max Pulse
      Score: 4.00 / 6.00
      Why:
        - genre match: pop (+2.00)
        - energy 0.93 vs target 0.80 (+1.03)
        - valence 0.77 vs target 0.80 (+0.49)
        - non-acoustic fit (+0.47)

  #4  Fuego Lento  by Brisa Norte
      Score: 3.02 / 6.00
      Why:
        - related mood: playful (+0.75)
        - energy 0.78 vs target 0.80 (+1.49)
        - valence 0.88 vs target 0.80 (+0.43)
        - non-acoustic fit (+0.35)

  #5  Golden Hour Cypher  by Verse Theory
      Score: 2.69 / 6.00
      Why:
        - related mood: confident (+0.75)
        - energy 0.71 vs target 0.80 (+1.25)
        - valence 0.62 vs target 0.80 (+0.24)
        - non-acoustic fit (+0.44)
```

**Lofi / Chill Study**

```
============================================================
  Profile: Lofi / Chill Study
  genre=lofi | mood=chill | energy=0.40 | valence=0.60 | acoustic=yes
============================================================

  #1  Library Rain  by Paper Lanterns
      Score: 5.85 / 6.00
      Why:
        - genre match: lofi (+2.00)
        - mood match: chill (+1.50)
        - energy 0.35 vs target 0.40 (+1.42)
        - valence 0.60 vs target 0.60 (+0.50)
        - acoustic fit (+0.43)

  #2  Midnight Coding  by LoRoom
      Score: 5.82 / 6.00
      Why:
        - genre match: lofi (+2.00)
        - mood match: chill (+1.50)
        - energy 0.42 vs target 0.40 (+1.49)
        - valence 0.56 vs target 0.60 (+0.48)
        - acoustic fit (+0.35)

  #3  Focus Flow  by LoRoom
      Score: 5.14 / 6.00
      Why:
        - genre match: lofi (+2.00)
        - related mood: focused (+0.75)
        - energy 0.40 vs target 0.40 (+1.50)
        - valence 0.59 vs target 0.60 (+0.50)
        - acoustic fit (+0.39)

  #4  Spacewalk Thoughts  by Orbit Bloom
      Score: 3.52 / 6.00
      Why:
        - mood match: chill (+1.50)
        - energy 0.28 vs target 0.40 (+1.09)
        - valence 0.65 vs target 0.60 (+0.47)
        - acoustic fit (+0.46)

  #5  Coffee Shop Stories  by Slow Stereo
      Score: 3.05 / 6.00
      Why:
        - related mood: relaxed (+0.75)
        - energy 0.37 vs target 0.40 (+1.47)
        - valence 0.71 vs target 0.60 (+0.38)
        - acoustic fit (+0.45)
```

**Deep Intense Rock**

```
============================================================
  Profile: Deep Intense Rock
  genre=rock | mood=intense | energy=0.90 | valence=0.45 | acoustic=no
============================================================

  #1  Storm Runner  by Voltline
      Score: 5.94 / 6.00
      Why:
        - genre match: rock (+2.00)
        - mood match: intense (+1.50)
        - energy 0.91 vs target 0.90 (+1.50)
        - valence 0.48 vs target 0.45 (+0.49)
        - non-acoustic fit (+0.45)

  #2  Gym Hero  by Max Pulse
      Score: 3.50 / 6.00
      Why:
        - mood match: intense (+1.50)
        - energy 0.93 vs target 0.90 (+1.47)
        - valence 0.77 vs target 0.45 (+0.05)
        - non-acoustic fit (+0.47)

  #3  Laser Festival  by Pulse Drift
      Score: 2.76 / 6.00
      Why:
        - related mood: energetic (+0.75)
        - energy 0.95 vs target 0.90 (+1.42)
        - valence 0.72 vs target 0.45 (+0.10)
        - non-acoustic fit (+0.49)

  #4  Iron Cathedral  by Grave Engine
      Score: 2.68 / 6.00
      Why:
        - related mood: angry (+0.75)
        - energy 0.97 vs target 0.90 (+1.35)
        - valence 0.18 vs target 0.45 (+0.10)
        - non-acoustic fit (+0.48)

  #5  Night Drive Loop  by Neon Echo
      Score: 1.78 / 6.00
      Why:
        - energy 0.75 vs target 0.90 (+0.91)
        - valence 0.49 vs target 0.45 (+0.48)
        - non-acoustic fit (+0.39)
```

**Sad but High Energy**

```
============================================================
  Profile: Sad but High Energy
  genre=folk | mood=sad | energy=0.90 | valence=0.20 | acoustic=yes
============================================================

  #1  Letters I Never Sent  by Willow & Ash
      Score: 4.41 / 6.00
      Why:
        - genre match: folk (+2.00)
        - mood match: sad (+1.50)
        - energy 0.30 vs target 0.90 (+0.00)
        - valence 0.15 vs target 0.20 (+0.47)
        - acoustic fit (+0.44)

  #2  Iron Cathedral  by Grave Engine
      Score: 1.86 / 6.00
      Why:
        - energy 0.97 vs target 0.90 (+1.35)
        - valence 0.18 vs target 0.20 (+0.50)
        - acoustic fit (+0.01)

  #3  Night Drive Loop  by Neon Echo
      Score: 1.85 / 6.00
      Why:
        - related mood: moody (+0.75)
        - energy 0.75 vs target 0.90 (+0.91)
        - valence 0.49 vs target 0.20 (+0.08)
        - acoustic fit (+0.11)

  #4  Rain on Cello Strings  by Aurelia Quartet
      Score: 1.73 / 6.00
      Why:
        - related mood: melancholic (+0.75)
        - energy 0.22 vs target 0.90 (+0.00)
        - valence 0.21 vs target 0.20 (+0.50)
        - acoustic fit (+0.48)

  #5  Storm Runner  by Voltline
      Score: 1.63 / 6.00
      Why:
        - energy 0.91 vs target 0.90 (+1.50)
        - valence 0.48 vs target 0.20 (+0.09)
        - acoustic fit (+0.05)
```

**Metal but Chill**

```
============================================================
  Profile: Metal but Chill
  genre=metal | mood=chill | energy=0.30 | valence=0.50 | acoustic=yes
============================================================

  #1  Spacewalk Thoughts  by Orbit Bloom
      Score: 3.75 / 6.00
      Why:
        - mood match: chill (+1.50)
        - energy 0.28 vs target 0.30 (+1.49)
        - valence 0.65 vs target 0.50 (+0.30)
        - acoustic fit (+0.46)

  #2  Library Rain  by Paper Lanterns
      Score: 3.75 / 6.00
      Why:
        - mood match: chill (+1.50)
        - energy 0.35 vs target 0.30 (+1.42)
        - valence 0.60 vs target 0.50 (+0.40)
        - acoustic fit (+0.43)

  #3  Midnight Coding  by LoRoom
      Score: 3.41 / 6.00
      Why:
        - mood match: chill (+1.50)
        - energy 0.42 vs target 0.30 (+1.09)
        - valence 0.56 vs target 0.50 (+0.46)
        - acoustic fit (+0.35)

  #4  Focus Flow  by LoRoom
      Score: 2.76 / 6.00
      Why:
        - related mood: focused (+0.75)
        - energy 0.40 vs target 0.30 (+1.20)
        - valence 0.59 vs target 0.50 (+0.42)
        - acoustic fit (+0.39)

  #5  Coffee Shop Stories  by Slow Stereo
      Score: 2.73 / 6.00
      Why:
        - related mood: relaxed (+0.75)
        - energy 0.37 vs target 0.30 (+1.35)
        - valence 0.71 vs target 0.50 (+0.19)
        - acoustic fit (+0.45)
```

**Whitespace Genre**

```
============================================================
  Profile: Whitespace Genre
  genre= Pop  | mood=happy | energy=0.80 | valence=0.80 | acoustic=no
============================================================

  #1  Sunrise City  by Neon Echo
      Score: 4.88 / 6.00
      Why:
        - related genre: pop (+1.00)
        - mood match: happy (+1.50)
        - energy 0.82 vs target 0.80 (+1.49)
        - valence 0.84 vs target 0.80 (+0.48)
        - non-acoustic fit (+0.41)

  #2  Rooftop Lights  by Indigo Parade
      Score: 3.77 / 6.00
      Why:
        - mood match: happy (+1.50)
        - energy 0.76 vs target 0.80 (+1.45)
        - valence 0.81 vs target 0.80 (+0.50)
        - non-acoustic fit (+0.33)

  #3  Fuego Lento  by Brisa Norte
      Score: 3.02 / 6.00
      Why:
        - related mood: playful (+0.75)
        - energy 0.78 vs target 0.80 (+1.49)
        - valence 0.88 vs target 0.80 (+0.43)
        - non-acoustic fit (+0.35)

  #4  Gym Hero  by Max Pulse
      Score: 3.00 / 6.00
      Why:
        - related genre: pop (+1.00)
        - energy 0.93 vs target 0.80 (+1.03)
        - valence 0.77 vs target 0.80 (+0.49)
        - non-acoustic fit (+0.47)

  #5  Golden Hour Cypher  by Verse Theory
      Score: 2.69 / 6.00
      Why:
        - related mood: confident (+0.75)
        - energy 0.71 vs target 0.80 (+1.25)
        - valence 0.62 vs target 0.80 (+0.24)
        - non-acoustic fit (+0.44)
```

**Substring Genre 'r'**

```
============================================================
  Profile: Substring Genre 'r'
  genre=r | mood= | energy=0.50 | valence=0.50 | acoustic=no
============================================================

  #1  Velvet Midnight  by Velour Season
      Score: 3.24 / 6.00
      Why:
        - related genre: r&b (+1.00)
        - energy 0.52 vs target 0.50 (+1.49)
        - valence 0.57 vs target 0.50 (+0.45)
        - non-acoustic fit (+0.30)

  #2  Island Breeze Riddim  by Tide Collective
      Score: 2.84 / 6.00
      Why:
        - related genre: reggae (+1.00)
        - energy 0.48 vs target 0.50 (+1.49)
        - valence 0.79 vs target 0.50 (+0.08)
        - non-acoustic fit (+0.28)

  #3  Dusty Porch Swing  by Hollow Creek
      Score: 2.79 / 6.00
      Why:
        - related genre: country (+1.00)
        - energy 0.55 vs target 0.50 (+1.42)
        - valence 0.68 vs target 0.50 (+0.24)
        - non-acoustic fit (+0.13)

  #4  Storm Runner  by Voltline
      Score: 1.98 / 6.00
      Why:
        - related genre: rock (+1.00)
        - energy 0.91 vs target 0.50 (+0.04)
        - valence 0.48 vs target 0.50 (+0.50)
        - non-acoustic fit (+0.45)

  #5  Midnight Coding  by LoRoom
      Score: 1.91 / 6.00
      Why:
        - energy 0.42 vs target 0.50 (+1.30)
        - valence 0.56 vs target 0.50 (+0.46)
        - non-acoustic fit (+0.15)
```

**Unknown Mood**

```
============================================================
  Profile: Unknown Mood
  genre=edm | mood=hype | energy=0.90 | valence=0.70 | acoustic=no
============================================================

  #1  Laser Festival  by Pulse Drift
      Score: 4.40 / 6.00
      Why:
        - genre match: edm (+2.00)
        - energy 0.95 vs target 0.90 (+1.42)
        - valence 0.72 vs target 0.70 (+0.50)
        - non-acoustic fit (+0.49)

  #2  Gym Hero  by Max Pulse
      Score: 2.39 / 6.00
      Why:
        - energy 0.93 vs target 0.90 (+1.47)
        - valence 0.77 vs target 0.70 (+0.45)
        - non-acoustic fit (+0.47)

  #3  Storm Runner  by Voltline
      Score: 2.12 / 6.00
      Why:
        - energy 0.91 vs target 0.90 (+1.50)
        - valence 0.48 vs target 0.70 (+0.17)
        - non-acoustic fit (+0.45)

  #4  Sunrise City  by Neon Echo
      Score: 2.03 / 6.00
      Why:
        - energy 0.82 vs target 0.90 (+1.30)
        - valence 0.84 vs target 0.70 (+0.32)
        - non-acoustic fit (+0.41)

  #5  Iron Cathedral  by Grave Engine
      Score: 1.83 / 6.00
      Why:
        - energy 0.97 vs target 0.90 (+1.35)
        - valence 0.18 vs target 0.70 (+0.00)
        - non-acoustic fit (+0.48)
```

**Out-of-Range Energy**

```
============================================================
  Profile: Out-of-Range Energy
  genre=rock | mood=intense | energy=1.50 | valence=0.50 | acoustic=no
============================================================

  #1  Storm Runner  by Voltline
      Score: 4.45 / 6.00
      Why:
        - genre match: rock (+2.00)
        - mood match: intense (+1.50)
        - energy 0.91 vs target 1.50 (+0.00)
        - valence 0.48 vs target 0.50 (+0.50)
        - non-acoustic fit (+0.45)

  #2  Gym Hero  by Max Pulse
      Score: 2.08 / 6.00
      Why:
        - mood match: intense (+1.50)
        - energy 0.93 vs target 1.50 (+0.00)
        - valence 0.77 vs target 0.50 (+0.10)
        - non-acoustic fit (+0.47)

  #3  Laser Festival  by Pulse Drift
      Score: 1.41 / 6.00
      Why:
        - related mood: energetic (+0.75)
        - energy 0.95 vs target 1.50 (+0.00)
        - valence 0.72 vs target 0.50 (+0.17)
        - non-acoustic fit (+0.49)

  #4  Iron Cathedral  by Grave Engine
      Score: 1.29 / 6.00
      Why:
        - related mood: angry (+0.75)
        - energy 0.97 vs target 1.50 (+0.00)
        - valence 0.18 vs target 0.50 (+0.05)
        - non-acoustic fit (+0.48)

  #5  Night Drive Loop  by Neon Echo
      Score: 0.89 / 6.00
      Why:
        - energy 0.75 vs target 1.50 (+0.00)
        - valence 0.49 vs target 0.50 (+0.50)
        - non-acoustic fit (+0.39)
```

**Weight-shift experiment: genre halved (2.0 → 1.0), energy doubled (1.5 → 3.0).** Max score is now 6.5. The before results are the outputs above.

| Profile | #1 before (2.0 / 1.5 / 1.5) | #1 after (1.0 / 1.5 / 3.0) | What changed |
|---|---|---|---|
| Pop / Happy | Sunrise City (5.88) | Sunrise City (6.37) | Fuego Lento moved up from #4 to #3, passing Gym Hero |
| Lofi / Chill Study | Library Rain (5.85) | Midnight Coding (6.31) | #1 and #2 swapped; Midnight Coding's energy (0.42) is closer to 0.40 |
| Deep Intense Rock | Storm Runner (5.94) | Storm Runner (6.43) | Top 4 unchanged; Gym Hero still #2 and Iron Cathedral still #4 |
| Sad but High Energy | Letters I Never Sent (4.41) | Letters I Never Sent (3.41) | Still #1, but the gap to Iron Cathedral shrank from 2.55 to 0.21 |
| Metal but Chill | Spacewalk Thoughts (3.75, tie) | Spacewalk Thoughts (5.24) | Tie broken; same chill songs on top |
| Unknown Mood | Laser Festival (4.40) | Laser Festival (4.82) | Same order |
| Out-of-Range Energy | Storm Runner (4.45) | Storm Runner (3.45) | Energy still gives 0 points, so only the smaller genre bonus changed |

**Deep Intense Rock (after)**

```
============================================================
  Profile: Deep Intense Rock
  genre=rock | mood=intense | energy=0.90 | valence=0.45 | acoustic=no
============================================================

  #1  Storm Runner  by Voltline
      Score: 6.43 / 6.50
      Why:
        - genre match: rock (+1.00)
        - mood match: intense (+1.50)
        - energy 0.91 vs target 0.90 (+2.99)
        - valence 0.48 vs target 0.45 (+0.49)
        - non-acoustic fit (+0.45)

  #2  Gym Hero  by Max Pulse
      Score: 4.97 / 6.50
      Why:
        - mood match: intense (+1.50)
        - energy 0.93 vs target 0.90 (+2.94)
        - valence 0.77 vs target 0.45 (+0.05)
        - non-acoustic fit (+0.47)

  #3  Laser Festival  by Pulse Drift
      Score: 4.18 / 6.50
      Why:
        - related mood: energetic (+0.75)
        - energy 0.95 vs target 0.90 (+2.84)
        - valence 0.72 vs target 0.45 (+0.10)
        - non-acoustic fit (+0.49)

  #4  Iron Cathedral  by Grave Engine
      Score: 4.02 / 6.50
      Why:
        - related mood: angry (+0.75)
        - energy 0.97 vs target 0.90 (+2.69)
        - valence 0.18 vs target 0.45 (+0.10)
        - non-acoustic fit (+0.48)

  #5  Sunrise City  by Neon Echo
      Score: 3.03 / 6.50
      Why:
        - energy 0.82 vs target 0.90 (+2.60)
        - valence 0.84 vs target 0.45 (+0.02)
        - non-acoustic fit (+0.41)
```

**Sad but High Energy (after)**

```
============================================================
  Profile: Sad but High Energy
  genre=folk | mood=sad | energy=0.90 | valence=0.20 | acoustic=yes
============================================================

  #1  Letters I Never Sent  by Willow & Ash
      Score: 3.41 / 6.50
      Why:
        - genre match: folk (+1.00)
        - mood match: sad (+1.50)
        - energy 0.30 vs target 0.90 (+0.00)
        - valence 0.15 vs target 0.20 (+0.47)
        - acoustic fit (+0.44)

  #2  Iron Cathedral  by Grave Engine
      Score: 3.20 / 6.50
      Why:
        - energy 0.97 vs target 0.90 (+2.69)
        - valence 0.18 vs target 0.20 (+0.50)
        - acoustic fit (+0.01)

  #3  Storm Runner  by Voltline
      Score: 3.13 / 6.50
      Why:
        - energy 0.91 vs target 0.90 (+2.99)
        - valence 0.48 vs target 0.20 (+0.09)
        - acoustic fit (+0.05)

  #4  Gym Hero  by Max Pulse
      Score: 2.97 / 6.50
      Why:
        - energy 0.93 vs target 0.90 (+2.94)
        - valence 0.77 vs target 0.20 (+0.00)
        - acoustic fit (+0.03)

  #5  Laser Festival  by Pulse Drift
      Score: 2.85 / 6.50
      Why:
        - energy 0.95 vs target 0.90 (+2.84)
        - valence 0.72 vs target 0.20 (+0.00)
        - acoustic fit (+0.01)
```
</details>

---

## 7. Intended Use and Non-Intended Use

VibeMatch is for a classroom, to show how a simple content-based recommender scores and ranks songs. It shouldn't be used for real users or a real music app: the catalog is tiny, it assumes everyone has exactly one favorite genre and mood, and it doesn't catch typos in user input.

---

## 8. Ideas for Improvement

- Add more songs per genre so the lists don't fill up with random loud songs after the first match.
- Let users pick more than one genre or mood, and count related genres like rock and metal as partial matches.
- Clean up user input (strip extra spaces, keep energy between 0 and 1) so typos don't quietly change the results.
