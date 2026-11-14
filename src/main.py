"""
Command line runner for the Music Recommender Simulation.

Run from the project folder with either:
    python -m src.main
    python src/main.py
"""

try:
    from src import recommender                     # python -m src.main
except ImportError:
    import recommender                              # python src/main.py

load_songs = recommender.load_songs
recommend_songs = recommender.recommend_songs

# Highest possible score, computed from the weights so it stays correct if they change.
MAX_SCORE = (recommender.GENRE_WEIGHT + recommender.MOOD_WEIGHT + recommender.ENERGY_WEIGHT
             + recommender.VALENCE_WEIGHT + recommender.ACOUSTIC_WEIGHT)
WIDTH = 60

# Taste profiles. Keys match the UserProfile fields so the same profile works for both versions.
PROFILES = {
    # Default profile: an upbeat pop listener.
    "Pop / Happy": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_valence": 0.80,
        "likes_acoustic": False,
    },
    # A late-night study listener who wants calm, acoustic background music.
    "Lofi / Chill Study": {
        "favorite_genre": "lofi",   # genre match: worth up to 2.0 points
        "favorite_mood": "chill",   # mood match: 1.5 points exact, 0.75 for a related mood (see MOOD_GROUPS)
        "target_energy": 0.40,      # energy closeness (Gaussian, sigma 0.15): worth up to 1.5 points
        "target_valence": 0.60,     # valence closeness (Gaussian, sigma 0.15): worth up to 0.5 points
        "likes_acoustic": True,     # acoustic bonus: worth up to 0.5 points
    },
    # A listener who wants loud, aggressive, high-energy rock.
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_valence": 0.45,
        "likes_acoustic": False,
    },
    # Adversarial: conflicting preferences, a sad mood but very high energy.
    "Sad but High Energy": {
        "favorite_genre": "folk",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "target_valence": 0.20,
        "likes_acoustic": True,
    },
    # Adversarial: genre and mood pull in opposite directions.
    "Metal but Chill": {
        "favorite_genre": "metal",
        "favorite_mood": "chill",
        "target_energy": 0.30,
        "target_valence": 0.50,
        "likes_acoustic": True,
    },
    # Edge case: extra spaces and capitals in the genre.
    "Whitespace Genre": {
        "favorite_genre": " Pop ",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_valence": 0.80,
        "likes_acoustic": False,
    },
    # Edge case: a one-letter genre that is a substring of many real genres.
    "Substring Genre 'r'": {
        "favorite_genre": "r",
        "favorite_mood": "",
        "target_energy": 0.50,
        "target_valence": 0.50,
        "likes_acoustic": False,
    },
    # Edge case: a mood that is not in MOOD_GROUPS.
    "Unknown Mood": {
        "favorite_genre": "edm",
        "favorite_mood": "hype",
        "target_energy": 0.90,
        "target_valence": 0.70,
        "likes_acoustic": False,
    },
    # Edge case: target energy outside the 0 to 1 range.
    "Out-of-Range Energy": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 1.50,
        "target_valence": 0.50,
        "likes_acoustic": False,
    },
}


def print_profile_header(name: str, prefs: dict) -> None:
    acoustic = "yes" if prefs.get("likes_acoustic") else "no"
    print("=" * WIDTH)
    print(f"  Profile: {name}")
    print(
        f"  genre={prefs['favorite_genre']} | mood={prefs['favorite_mood']} | "
        f"energy={prefs['target_energy']:.2f} | valence={prefs['target_valence']:.2f} | "
        f"acoustic={acoustic}"
    )
    print("=" * WIDTH)


def print_recommendations(recommendations: list) -> None:
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  by {song['artist']}")
        print(f"      Score: {score:.2f} / {MAX_SCORE:.2f}")
        print("      Why:")
        for reason in explanation.split("; "):
            print(f"        - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, prefs in PROFILES.items():
        print()
        print_profile_header(name, prefs)
        recommendations = recommend_songs(prefs, songs, k=5)
        print_recommendations(recommendations)


if __name__ == "__main__":
    main()
