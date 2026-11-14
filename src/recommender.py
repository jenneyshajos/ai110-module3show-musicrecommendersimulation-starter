import csv
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: float = 0.5  # 0 = sad, 1 = happy; defaults to neutral so older code still works

# Moods that feel alike. Two moods are "related" if they share at least one group.
# A mood can sit in more than one group (e.g., "energetic" is both upbeat and intense).
MOOD_GROUPS: Dict[str, set] = {
    "calm":       {"chill", "relaxed", "peaceful", "focused"},
    "upbeat":     {"happy", "playful", "confident", "energetic"},
    "intense":    {"intense", "angry", "energetic"},
    "reflective": {"sad", "melancholic", "moody", "nostalgic"},
    "warm":       {"romantic", "soulful", "nostalgic"},
}

def mood_similarity(user_mood: str, song_mood: str) -> float:
    """Returns 1.0 for an exact mood match, 0.5 for a related mood, 0.0 otherwise."""
    user_mood, song_mood = user_mood.lower(), song_mood.lower()
    if user_mood == song_mood:
        return 1.0
    for group in MOOD_GROUPS.values():
        if user_mood in group and song_mood in group:
            return 0.5
    return 0.0

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

# Scoring weights from the Algorithm Recipe (max total = 6.0)
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.5
ENERGY_WEIGHT = 1.5
VALENCE_WEIGHT = 0.5
ACOUSTIC_WEIGHT = 0.5
SIGMA = 0.15  # how strict "close to the target" is for energy and valence

def closeness(value: float, target: float, sigma: float = SIGMA) -> float:
    """Gaussian closeness: 1.0 when value == target, falling smoothly toward 0 as they move apart."""
    return math.exp(-((value - target) ** 2) / (2 * sigma ** 2))

def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv into a list of dicts, converting id to int and audio features to float."""
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            song = {}
            for key, value in row.items():
                value = value.strip()
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song against the user's preferences and returns (score, list of reasons)."""
    score = 0.0
    reasons: List[str] = []

    # G: genre match (exact = 1, partial like "pop" / "indie pop" = 0.5)
    user_genre = user_prefs.get("favorite_genre", "").lower()
    song_genre = song["genre"].lower()
    if user_genre and user_genre == song_genre:
        points = GENRE_WEIGHT
        reasons.append(f"genre match: {song['genre']} (+{points:.2f})")
        score += points
    elif user_genre and (user_genre in song_genre or song_genre in user_genre):
        points = GENRE_WEIGHT * 0.5
        reasons.append(f"related genre: {song['genre']} (+{points:.2f})")
        score += points

    # M: mood match (exact = 1, related mood from MOOD_GROUPS = 0.5)
    user_mood = user_prefs.get("favorite_mood", "")
    if user_mood:
        similarity = mood_similarity(user_mood, song["mood"])
        if similarity > 0:
            points = MOOD_WEIGHT * similarity
            label = "mood match" if similarity == 1.0 else "related mood"
            reasons.append(f"{label}: {song['mood']} (+{points:.2f})")
            score += points

    # E: energy closeness (Gaussian: 1 at the target, near 0 when far away)
    target_energy = user_prefs.get("target_energy")
    if target_energy is not None:
        points = ENERGY_WEIGHT * closeness(song["energy"], target_energy)
        reasons.append(f"energy {song['energy']:.2f} vs target {target_energy:.2f} (+{points:.2f})")
        score += points

    # V: valence closeness (same Gaussian rule)
    target_valence = user_prefs.get("target_valence")
    if target_valence is not None:
        points = VALENCE_WEIGHT * closeness(song["valence"], target_valence)
        reasons.append(f"valence {song['valence']:.2f} vs target {target_valence:.2f} (+{points:.2f})")
        score += points

    # A: acoustic preference
    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        fit = song["acousticness"] if likes_acoustic else 1 - song["acousticness"]
        points = ACOUSTIC_WEIGHT * fit
        label = "acoustic" if likes_acoustic else "non-acoustic"
        reasons.append(f"{label} fit (+{points:.2f})")
        score += points

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song, sorts by score from highest to lowest, and returns the top k as (song, score, explanation)."""
    # The loop: score every song -> list of (song, score, reasons)
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # The ranking: sort by score, highest first, and keep the top k
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]
