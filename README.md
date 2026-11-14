# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms like Spotify and YouTube combine two approaches to predict what a user will love next. Collaborative filtering recommends songs that people with similar listening behavior enjoyed, while content-based filtering recommends songs whose features, such as genre, mood, and energy, match what the user already likes. My version is a content-based recommender because it has a small catalog and no listening history from other users. It will prioritize genre first, then mood, then how close a song's energy is to the user's target, with smaller bonuses for matching the user's preferred valence and whether they like acoustic music. After every song is scored, the ranking step sorts them from highest to lowest score and returns the top results. This keeps my recommender easy to explain; every song it suggests comes with clear reasons for why it was chosen.

```
┌─────────────────────────────────────────┐
│ 1. INPUT                                │
│  User prefs (main.py)                   │
│    favorite_genre  = "lofi"             │
│    favorite_mood   = "chill"            │
│    target_energy   = 0.40               │
│    target_valence  = 0.60               │
│    likes_acoustic  = True               │
│  Songs: load_songs() reads songs.csv    │
└────────────────────┬────────────────────┘
                     ▼
┌─────────────────────────────────────────┐
│ 2. PROCESS: score_song()                │
│  FOR each song:                         │
│    G = genre match       1 / 0.5 / 0    │
│    M = mood_similarity   1 / 0.5 / 0    │
│    E = energy closeness  (Gaussian)     │
│    V = valence closeness (Gaussian)     │
│    A = acousticness  (or 1 − it)        │
│    score = 2.0G + 1.5M + 1.5E           │
│            + 0.5V + 0.5A    (max 6.0)   │
│    save (song, score, reasons)          │
└────────────────────┬────────────────────┘
                     ▼
┌─────────────────────────────────────────┐
│ 3. OUTPUT: recommend_songs()            │
│  Sort all songs by score, highest first │
│  Keep the top K                         │
│  Return (song, score, explanation)      │
└─────────────────────────────────────────┘
```

**Expected Biases**

- **Genre may be over-prioritized:** a great mood and energy match from another genre can lose to a weaker genre match.
- **Uneven catalog:** lofi has 3 songs, while most genres have only 1.
- **Exact labels:** a rock fan gets no credit for metal, and the mood groups reflect my own judgment.
- **Filter bubble:** songs far from the target score near zero, so the system rarely suggests anything new.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` or `python3 -m src.main` for the default Pop / Happy profile and the Lofi / Chill Study profile:

```
Loaded 20 songs from data/songs.csv

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

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

**Weight shift: genre 2.0 → 1.0, energy 1.5 → 3.0.** I ran all 9 profiles before and after the change and then switched back to the original weights.

- **Sad but High Energy:** the quiet folk song stayed #1, but its lead shrank from 2.55 points to 0.21, and the rest of the list became loud songs.
- **Lofi / Chill Study:** Midnight Coding passed Library Rain for #1 because its energy (0.42) is closer to the 0.40 target.
- **Deep Intense Rock:** the top 4 didn't change at all, which showed the small catalog is a bigger problem than the weights.

Full before and after results are in the [model card](model_card.md).

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

- **Tiny catalog:** only 20 songs, and 15 of the 17 genres have just one song, so lists fill up with the same few loud songs like "Gym Hero."
- **Labels beat sound:** a genre and mood match (3.5 points) outweighs energy, valence, and acousticness combined (2.5), so a "sad but loud" user gets a quiet folk song first.
- **No understanding of music itself:** it doesn't know lyrics, language, or that rock and metal are related.
- **Fragile input:** extra spaces in a genre or an energy outside 0 to 1 quietly change the results instead of causing an error.


---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

I learned that a recommender doesn't really "know" music; it just scores every song against what the user says they like and sorts by points, so the weights I pick decide everything.

Bias showed up because labels counted more than sound and most genres only had one song, so users with simple tastes got great results while users with mixed tastes, like "sad but loud," got the wrong songs without any warning.





