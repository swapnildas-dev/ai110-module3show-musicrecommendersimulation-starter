# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

My version is a simple content-based music recommender. It compares each song's
genre, mood, and audio features with a user's taste profile, gives each song a
match score, and recommends the highest-scoring songs. This makes the results
easy to calculate and explain.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Each `Song` uses genre, mood, energy, valence, danceability, acousticness, and
`tempo_bpm`. The `UserProfile` stores preferred values for those same features.

### User Profile

This realistic example represents someone who prefers relaxed lofi music:

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

This profile is moderately narrow because it asks for one exact genre and mood,
but the five numerical targets add enough detail to distinguish between quiet,
acoustic lofi and more upbeat lofi songs. It is not flexible enough for a user
with several favorite styles. A future version could accept multiple genres and
moods, preference ranges, or listening history. It could also let users skip
unknown preferences instead of forcing new users to choose every value.

### Algorithm Recipe

The planned weights total 100%:

| Feature | Weight | How it is compared |
| --- | ---: | --- |
| Genre | 30% | 1 for an exact match, otherwise 0 |
| Mood | 25% | 1 for an exact match, otherwise 0 |
| Energy | 12% | Closeness to the target value |
| Valence | 10% | Closeness to the target value |
| Danceability | 10% | Closeness to the target value |
| Acousticness | 8% | Closeness to the target value |
| Tempo | 5% | Closeness to the target BPM |

Genre has the highest weight because it is the strongest broad signal of musical
style. Mood is second because it captures the vibe the user wants. The numerical
features refine the match without overpowering style. Tempo has the lowest
weight because it overlaps with energy and should mainly break close ties.

For energy, valence, danceability, and acousticness, which range from 0 to 1:

```text
similarity = 1 - abs(user_target - song_value)
```

Tempo uses the same idea but divides the difference by the catalog's 92 BPM
range (152 minus 60):

```text
tempo_similarity = max(0, 1 - abs(target_tempo - song_tempo) / 92)
```

The planned score for each song is:

```text
score = 0.30 * genre_match
      + 0.25 * mood_match
      + 0.12 * energy_similarity
      + 0.10 * valence_similarity
      + 0.10 * danceability_similarity
      + 0.08 * acousticness_similarity
      + 0.05 * tempo_similarity
```

This closeness rule rewards a song for being near the user's target, not for
simply having a larger feature value. The recommender will score every song,
sort scores from highest to lowest, and return the top five. Equal scores will
be ordered alphabetically by title so the ranking is predictable.

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loaded songs: 17

Top Recommendations

1. Midnight Coding by LoRoom
   Score: 0.9833
   Reasons:
   - Genre match (+0.3000)
   - Mood match (+0.2500)
   - Energy similarity 0.9800 (+0.1176)
   - Valence similarity 0.9600 (+0.0960)
   - Danceability similarity 0.9800 (+0.0980)
   - Acousticness similarity 0.9100 (+0.0728)
   - Tempo similarity 0.9783 (+0.0489)

2. Library Rain by Paper Lanterns
   Score: 0.9829
   Reasons:
   - Genre match (+0.3000)
   - Mood match (+0.2500)
   - Energy similarity 0.9500 (+0.1140)
   - Valence similarity 1.0000 (+0.1000)
   - Danceability similarity 0.9800 (+0.0980)
   - Acousticness similarity 0.9400 (+0.0752)
   - Tempo similarity 0.9130 (+0.0457)

3. Focus Flow by LoRoom
   Score: 0.7474
   Reasons:
   - Genre match (+0.3000)
   - Mood no match (+0.0000)
   - Energy similarity 1.0000 (+0.1200)
   - Valence similarity 0.9900 (+0.0990)
   - Danceability similarity 1.0000 (+0.1000)
   - Acousticness similarity 0.9800 (+0.0784)
   - Tempo similarity 1.0000 (+0.0500)

4. Spacewalk Thoughts by Orbit Bloom
   Score: 0.6411
   Reasons:
   - Genre no match (+0.0000)
   - Mood match (+0.2500)
   - Energy similarity 0.8800 (+0.1056)
   - Valence similarity 0.9500 (+0.0950)
   - Danceability similarity 0.8100 (+0.0810)
   - Acousticness similarity 0.8800 (+0.0704)
   - Tempo similarity 0.7826 (+0.0391)

5. Old River Road by Juniper Miles
   Score: 0.4287
   Reasons:
   - Genre no match (+0.0000)
   - Mood no match (+0.0000)
   - Energy similarity 0.9700 (+0.1164)
   - Valence similarity 0.9800 (+0.0980)
   - Danceability similarity 0.9100 (+0.0910)
   - Acousticness similarity 0.9700 (+0.0776)
   - Tempo similarity 0.9130 (+0.0457)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

I tried lowering the genre weight and noticed that songs from unrelated genres
could rank highly just because their numerical features were close. Raising the
genre and mood weights produced recommendations that felt more consistent with
the user's requested style.

I also tried scoring numerical features by their raw values. That incorrectly
favored high-energy, high-danceability songs even when the user preferred lower
values. Using distance from the user's preference fixed this behavior. Adding
tempo helped separate otherwise similar songs, but I kept its weight low because
tempo overlaps with energy in this small dataset.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

- The catalog is very small, so the recommendations have limited variety.
- The system only understands the provided labels and audio measurements; it
  does not understand lyrics, language, instruments, or listening context.
- Exact genre and mood matches may oversimplify songs that fit several styles.
- Hand-selected weights reflect my assumptions and may not match every user's
  idea of similarity.
- Giving genre 30% of the score may favor exact genre matches too heavily and
  hide good songs from related genres.
- The recommender does not learn from listening history, skips, ratings, or
  changing preferences.
- New users may not know their exact preferences, so their first profile and
  recommendations may be inaccurate.
- Repeatedly favoring the same genres and moods could create a filter bubble and
  make less common music harder to discover.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
