"""
Command line runner for the Music Recommender Simulation.

This file runs the functions implemented in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    """Run the music recommender for several test profiles."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.88,
            "target_valence": 0.85,
            "target_danceability": 0.86,
            "target_acousticness": 0.10,
            "target_tempo": 128,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.40,
            "target_valence": 0.60,
            "target_danceability": 0.60,
            "target_acousticness": 0.80,
            "target_tempo": 80,
        },
        "Deep Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.90,
            "target_valence": 0.50,
            "target_danceability": 0.65,
            "target_acousticness": 0.10,
            "target_tempo": 148,
        },
        "High-Energy Classical (Edge Case)": {
            "favorite_genre": "classical",
            "favorite_mood": "intense",
            "target_energy": 0.95,
            "target_valence": 0.35,
            "target_danceability": 0.80,
            "target_acousticness": 0.05,
            "target_tempo": 155,
        },
    }

    for profile_name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\nProfile: {profile_name}")
        print("Top Recommendations\n")
        for rank, (song, score, reasons) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} by {song['artist']}")
            print(f"   Score: {score:.4f}")
            print("   Reasons:")
            for reason in reasons:
                print(f"   - {reason}")
            print()


if __name__ == "__main__":
    main()
