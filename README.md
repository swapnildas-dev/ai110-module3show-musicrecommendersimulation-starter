# 🎵 Music Recommender Simulation

## Project Summary

I built a simple content-based music recommender for a catalog of 17 songs. It
compares each song with a user's preferred genre, mood, and audio features. It
then scores every song, ranks the scores, and returns the top five with reasons
for each score.

---

## How The System Works

Each `Song` uses genre, mood, energy, valence, danceability, acousticness, and
`tempo_bpm`. The user profile stores target values for the same features:

```python
user_profile = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "target_valence": 0.60,
    "target_danceability": 0.60,
    "target_acousticness": 0.80,
    "target_tempo": 80,
}
```

This profile is fairly specific because it asks for one genre and one mood.
The numerical targets help separate songs within that style, but the profile
does not handle someone who likes several genres at once. A future version
could accept multiple genres, ranges, or unknown preferences.

### Algorithm Recipe

| Feature | Weight | Comparison |
| --- | ---: | --- |
| Genre | 30% | Exact match |
| Mood | 25% | Exact match |
| Energy | 12% | Closeness to the target |
| Valence | 10% | Closeness to the target |
| Danceability | 10% | Closeness to the target |
| Acousticness | 8% | Closeness to the target |
| Tempo | 5% | Closeness to the target BPM |

Genre has the highest weight because it is the broadest signal of style. Mood
is second because it captures the vibe the user asked for. The numerical
features fine-tune the result without taking over the whole score.

For energy, valence, danceability, and acousticness, I use:

```text
similarity = 1 - abs(user_target - song_value)
```

Tempo uses the same idea, but the difference is divided by the 92 BPM range in
the catalog:

```text
tempo_similarity = max(0, 1 - abs(target_tempo - song_tempo) / 92)
```

The final score is:

```text
score = 0.30 * genre_match
      + 0.25 * mood_match
      + 0.12 * energy_similarity
      + 0.10 * valence_similarity
      + 0.10 * danceability_similarity
      + 0.08 * acousticness_similarity
      + 0.05 * tempo_similarity
```

This rewards songs for being close to the user's targets, not for simply
having larger values. `score_song()` returns the score and a list of reasons.
`recommend_songs()` scores every song, sorts from highest to lowest, and returns
the top five. If two scores are equal, the song title breaks the tie.

### Data Flow

```text
User Preferences
        ↓
Load Songs CSV
        ↓
Compare Each Song
        ↓
Calculate Score
        ↓
Rank Songs
        ↓
Return Top Recommendations
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

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

This is the first profile from `python -m src.main`:

```text
Loaded songs: 17

Profile: High-Energy Pop
Top Recommendations

1. Sunrise City by Neon Echo
   Score: 0.9730
   Reasons:
   - Genre match (+0.3000)
   - Mood match (+0.2500)
   - Energy similarity 0.9400 (+0.1128)
   - Valence similarity 0.9900 (+0.0990)
   - Danceability similarity 0.9300 (+0.0930)
   - Acousticness similarity 0.9200 (+0.0736)
   - Tempo similarity 0.8913 (+0.0446)

2. Gym Hero by Max Pulse
   Score: 0.7278
   Reasons:
   - Genre match (+0.3000)
   - Mood no match (+0.0000)
   - Energy similarity 0.9500 (+0.1140)
   - Valence similarity 0.9200 (+0.0920)
   - Danceability similarity 0.9800 (+0.0980)
   - Acousticness similarity 0.9500 (+0.0760)
   - Tempo similarity 0.9565 (+0.0478)

3. Rooftop Lights by Indigo Parade
   Score: 0.6554
   Reasons:
   - Genre no match (+0.0000)
   - Mood match (+0.2500)
   - Energy similarity 0.8800 (+0.1056)
   - Valence similarity 0.9600 (+0.0960)
   - Danceability similarity 0.9600 (+0.0960)
   - Acousticness similarity 0.7500 (+0.0600)
   - Tempo similarity 0.9565 (+0.0478)

4. Electric Horizon by Nova Circuit
   Score: 0.4394
   Reasons:
   - Genre no match (+0.0000)
   - Mood no match (+0.0000)
   - Energy similarity 0.9900 (+0.1188)
   - Valence similarity 0.9700 (+0.0970)
   - Danceability similarity 0.9600 (+0.0960)
   - Acousticness similarity 0.9700 (+0.0776)
   - Tempo similarity 1.0000 (+0.0500)

5. City Crown by Rhyme District
   Score: 0.4112
   Reasons:
   - Genre no match (+0.0000)
   - Mood no match (+0.0000)
   - Energy similarity 0.9600 (+0.1152)
   - Valence similarity 0.8500 (+0.0850)
   - Danceability similarity 1.0000 (+0.1000)
   - Acousticness similarity 0.9800 (+0.0784)
   - Tempo similarity 0.6522 (+0.0326)
```

**Screenshot or video** *(optional)*: Not included.

---

## Experiments You Tried

I tested High-Energy Pop, Chill Lofi, Deep Rock, and one conflicting
High-Energy Classical profile. The first three had clear top matches. The edge
case was useful because the only classical song ranked third; its genre matched,
but its calm audio features were far from the high-energy targets.

For one controlled experiment, I lowered genre from 0.30 to 0.15 and raised
energy from 0.12 to 0.27. Energy-close songs moved up: Rooftop Lights passed Gym
Hero for High-Energy Pop, Spacewalk Thoughts passed Focus Flow for Chill Lofi,
and Electric Horizon passed Night Drive Loop for Deep Rock. Golden Strings also
dropped out of the edge-case top five. The results were different, but I did not
think they were clearly better because the requested genre mattered less. I
restored the original weights after the experiment.

---

## Limitations and Risks

- The catalog has only 17 songs, so the recommendations have limited variety.
- The system only understands the provided labels and audio measurements; it
  does not understand lyrics, language, instruments, or listening context.
- Exact genre and mood matches may oversimplify songs that fit several styles.
- Hand-selected weights reflect my assumptions and may not match every user's
  idea of similarity.
- Giving genre 30% of the score may hide good songs from related genres.
- The recommender does not learn from listening history, skips, ratings, or
  changing preferences.
- New users may not know their exact preferences, which creates a cold-start
  problem.
- Repeatedly favoring the same genres and moods could create a filter bubble and
  make less common music harder to discover.

---

## Reflection

I learned how song data and user preferences can be turned into scores and then
into a ranked list. I was surprised that a small weighted formula could still
produce recommendations that felt personal when several features lined up.

I used Codex heavily because I was short on time, but I still had to check the
work. I ran the program, read the recommendation reasons, reviewed the file
changes, confirmed the original weights were restored, and ran the tests. That
made it clear that AI can help me move faster, but I should not treat its output
as automatically correct. More detail is in the [Model Card](model_card.md).
