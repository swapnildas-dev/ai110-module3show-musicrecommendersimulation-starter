import csv
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


# These weights match the algorithm recipe documented in README.md.
FEATURE_WEIGHTS = {
    "genre": 0.30,
    "mood": 0.25,
    "energy": 0.12,
    "valence": 0.10,
    "danceability": 0.10,
    "acousticness": 0.08,
    "tempo_bpm": 0.05,
}
TEMPO_RANGE = 92.0


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
    target_valence: float = 0.5
    target_danceability: float = 0.5
    target_acousticness: Optional[float] = None
    target_tempo: float = 100.0
    # Kept for compatibility with the starter tests.
    likes_acoustic: bool = False


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for a user in descending score order."""
        song_lookup = {song.id: song for song in self.songs}
        song_dicts = [asdict(song) for song in self.songs]
        recommendations = recommend_songs(
            self._profile_to_dict(user), song_dicts, k
        )
        return [song_lookup[song["id"]] for song, _, _ in recommendations]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain how one song matches a user's preferences."""
        _, reasons = score_song(self._profile_to_dict(user), asdict(song))
        return "; ".join(reasons)

    @staticmethod
    def _profile_to_dict(user: UserProfile) -> Dict:
        """Convert a UserProfile object into the scoring dictionary format."""
        acousticness = user.target_acousticness
        if acousticness is None:
            acousticness = 0.8 if user.likes_acoustic else 0.2

        return {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "target_valence": user.target_valence,
            "target_danceability": user.target_danceability,
            "target_acousticness": acousticness,
            "target_tempo": user.target_tempo,
        }


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and convert numerical fields."""
    required_columns = {
        "id",
        "title",
        "artist",
        "genre",
        "mood",
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
    }
    songs = []

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        missing_columns = required_columns - set(reader.fieldnames or [])
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"CSV is missing required columns: {missing}")

        for row in reader:
            song = dict(row)
            song["id"] = int(song["id"])
            for feature in (
                "energy",
                "tempo_bpm",
                "valence",
                "danceability",
                "acousticness",
            ):
                song[feature] = float(song[feature])
            songs.append(song)

    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Calculate a song's weighted match score and explanatory reasons."""
    reasons = []

    genre_match = (
        str(user_prefs["favorite_genre"]).strip().lower()
        == str(song["genre"]).strip().lower()
    )
    genre_points = FEATURE_WEIGHTS["genre"] if genre_match else 0.0
    genre_result = "match" if genre_match else "no match"
    reasons.append(f"Genre {genre_result} (+{genre_points:.4f})")

    mood_match = (
        str(user_prefs["favorite_mood"]).strip().lower()
        == str(song["mood"]).strip().lower()
    )
    mood_points = FEATURE_WEIGHTS["mood"] if mood_match else 0.0
    mood_result = "match" if mood_match else "no match"
    reasons.append(f"Mood {mood_result} (+{mood_points:.4f})")

    numerical_features = (
        ("energy", "target_energy", "Energy"),
        ("valence", "target_valence", "Valence"),
        ("danceability", "target_danceability", "Danceability"),
        ("acousticness", "target_acousticness", "Acousticness"),
    )
    numerical_points = []

    for song_key, preference_key, label in numerical_features:
        difference = abs(float(user_prefs[preference_key]) - float(song[song_key]))
        similarity = max(0.0, 1.0 - difference)
        points = FEATURE_WEIGHTS[song_key] * similarity
        numerical_points.append(points)
        reasons.append(
            f"{label} similarity {similarity:.4f} (+{points:.4f})"
        )

    tempo_difference = abs(
        float(user_prefs["target_tempo"]) - float(song["tempo_bpm"])
    )
    tempo_similarity = max(0.0, 1.0 - tempo_difference / TEMPO_RANGE)
    tempo_points = FEATURE_WEIGHTS["tempo_bpm"] * tempo_similarity
    reasons.append(
        f"Tempo similarity {tempo_similarity:.4f} (+{tempo_points:.4f})"
    )

    score = genre_points + mood_points + sum(numerical_points) + tempo_points
    return score, reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, List[str]]]:
    """Score all songs and return the top k ranked recommendations."""
    scored_songs = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, reasons))

    scored_songs.sort(key=lambda result: (-result[1], result[0]["title"].lower()))
    return scored_songs[:max(0, k)]
