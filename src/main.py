"""
Command line runner for the Music Recommender Simulation.

This file runs the functions implemented in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    """Run the music recommender with the default user profile."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # This default profile matches the Phase 2 design in README.md.
    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "target_valence": 0.60,
        "target_danceability": 0.60,
        "target_acousticness": 0.80,
        "target_tempo": 80,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop Recommendations\n")
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.4f}")
        print("   Reasons:")
        for reason in reasons:
            print(f"   - {reason}")
        print()


if __name__ == "__main__":
    main()
