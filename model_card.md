# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

VibeFinder recommends songs from a small catalog by comparing song features
with a user preference profile. It scores every song, ranks the strongest
matches, and returns the top five. It assumes the user can describe one favorite
genre and mood along with target values for five numerical features.

This project is intended for learning how recommendation systems score and rank
items, experimenting with profiles and feature weights, and demonstrating a
small content-based recommender in a classroom.

It is not intended for real commercial music recommendations or for judging a
person's personality or preferences. It should not be used for medical,
financial, hiring, legal, or safety-critical decisions. Its results should not
be presented as accurate predictions beyond this 17-song dataset.

---

## 3. How the Model Works  

The system compares genre, mood, energy, valence, danceability, acousticness,
and tempo. An exact genre match earns 30% of the score, and an exact mood match
earns 25%. The numerical features earn points based on how close each song is
to the user's target, rather than rewarding values just for being higher.

Every song receives one combined score. The songs are sorted from highest to
lowest, and the top five are returned with simple explanations showing where
their points came from. The starter code did not calculate real rankings, so I
added the scoring, sorting, and explanations.

---

## 4. Data  

The catalog contains 17 songs: 10 starter songs and 7 generated sample songs.
Each row includes a title, artist, genre, mood, energy, valence, danceability,
acousticness, and `tempo_bpm`. The catalog covers several styles, including
pop, lofi, rock, ambient, jazz, classical, hip hop, folk, electronic, Latin,
R&B, and country.

The data is small and partly synthetic, so it cannot represent the full range
of real music or listeners. It does not include lyrics, real Spotify data,
listening history, skips, likes, ratings, or other user behavior.

---

## 5. Strengths  

In my tests, the best results came when the catalog had a song that matched both
the requested style and numerical targets. Sunrise City ranked first for
High-Energy Pop, Midnight Coding ranked first for Chill Lofi, and Storm Runner
ranked first for Deep Rock. Comparing several features also lets the system rank
close alternatives instead of relying on genre alone.

The score explanations are another strength because they make each ranking easy
to inspect. They show when a result is driven by genre, mood, numerical
similarity, or a combination of those features.

---

## 6. Limitations and Bias 

The catalog has only 17 songs, so one song can represent an entire genre or
mood and limit the variety of the results. I chose the weights by hand, and the
exact genre and mood checks can keep similar songs out or repeat the same types
of music. The system has no collaborative filtering and does not learn from
listening history, skips, or ratings. It also cannot understand lyrics,
language, context, or what a new user actually likes. Because seven songs are
generated samples, the catalog may not represent real music or different
listeners fairly.

---

## 7. Evaluation  

I tested four profiles with different styles and numerical targets. Each block
shows the real top-five output from the final scoring logic.

### High-Energy Pop

```text
1. Sunrise City by Neon Echo — 0.9730
2. Gym Hero by Max Pulse — 0.7278
3. Rooftop Lights by Indigo Parade — 0.6554
4. Electric Horizon by Nova Circuit — 0.4394
5. City Crown by Rhyme District — 0.4112
```

This ranking seems reasonable because the top three songs match either pop or
happy and also have energetic, danceable audio features. Electric Horizon at
fourth is slightly surprising because it matches neither category, but its
numerical values are very close. Sunrise City ranks first because it receives
0.30 for genre, 0.25 for mood, and 0.4230 from the five numerical similarities,
for a total of 0.9730.

### Chill Lofi

```text
1. Midnight Coding by LoRoom — 0.9833
2. Library Rain by Paper Lanterns — 0.9829
3. Focus Flow by LoRoom — 0.7474
4. Spacewalk Thoughts by Orbit Bloom — 0.6411
5. Old River Road by Juniper Miles — 0.4287
```

The results are reasonable: the three lofi songs rank first, and the two chill
lofi songs nearly tie. Spacewalk Thoughts ranking fourth shows that the 0.25
mood weight can place a different genre above songs with only numerical
similarity. Midnight Coding receives 0.30 for genre, 0.25 for mood, and 0.4333
from numerical similarities, producing its 0.9833 score.

### Deep Rock

```text
1. Storm Runner by Voltline — 0.9936
2. Gym Hero by Max Pulse — 0.6337
3. Night Drive Loop by Neon Echo — 0.3927
4. Electric Horizon by Nova Circuit — 0.3725
5. City Crown by Rhyme District — 0.3719
```

Storm Runner is a very strong and reasonable match. Gym Hero ranking second is
not a rock match, but it shares the intense mood and similar high-energy audio,
while the remaining songs rely only on numerical similarity. Storm Runner earns
0.30 for genre, 0.25 for mood, and 0.4436 from numerical similarities, totaling
0.9936.

### High-Energy Classical (Edge Case)

```text
1. Storm Runner by Voltline — 0.6626
2. Gym Hero by Max Pulse — 0.6351
3. Golden Strings by Avery Hall — 0.4774
4. Night Drive Loop by Neon Echo — 0.3669
5. Electric Horizon by Nova Circuit — 0.3635
```

This conflicting profile produces the most surprising ranking: the only
classical song is third because its calm audio is far from the high-energy
targets. Storm Runner instead receives 0.25 for its intense mood and 0.4126
from close numerical features; it gets no genre points, for a total of 0.6626.
The score follows my rule, but it also shows that one exact genre label cannot
fully represent conflicting preferences.

The profiles differ because genre contributes 0.30, mood contributes 0.25, and
the numerical weights refine the order: energy 0.12, valence 0.10,
danceability 0.10, acousticness 0.08, and tempo 0.05. Exact category matches
usually lead, but several close numerical matches can overcome one missing
category.

### Controlled Weight Experiment

I temporarily reduced genre from 0.30 to 0.15 and increased energy from 0.12 to
0.27, keeping the total weight at 1.00. Sunrise City, Midnight Coding, Storm
Runner, and Storm Runner remained the four profile leaders, but other rankings
changed: Rooftop Lights moved above Gym Hero for High-Energy Pop, Spacewalk
Thoughts moved above Focus Flow for Chill Lofi, and Electric Horizon moved
above Night Drive Loop for Deep Rock. In the edge case, Golden Strings dropped
out of the top five and City Crown entered, because the experiment rewarded
energy closeness more than genre.

The experimental results were more energy-focused but not clearly better. They
reduced style relevance, especially for the classical request, so I restored
the intended genre 0.30 and energy 0.12 weights. This showed me how much my
chosen weights control what gets recommended. The tiny catalog also gives the
system few alternatives, and it cannot learn whether a user actually prefers
the changed rankings.

After restoring the original weights, I ran the CLI successfully for all four
profiles. I also ran `pytest`, and both tests passed.

---

## 8. Future Work  

- Use a much larger dataset made from real music.
- Include listening history, likes, skips, ratings, and other feedback.
- Add collaborative filtering to learn from similar listeners.
- Learn feature weights from feedback instead of choosing them manually.
- Support partial genre and mood similarity instead of exact matches only.
- Add more tests and evaluation metrics for relevance and recommendation
  diversity.

---

## 9. Personal Reflection  

My biggest learning moment was seeing how a recommender turns song data and user
preferences into scores, rankings, and explanations. I was surprised that even
a small weighted scoring system could feel personalized when it compared
several features and ranked songs consistently.

Codex helped me move faster with implementation, documentation, testing, and
debugging during a stressful time constraint. I still needed to run the
program, inspect the real output, review file changes, confirm the original
weights were restored after the experiment, and verify that `pytest` passed.
Codex saved time, but its output was not proof that the project worked.

I also learned why AI work needs guardrails and human oversight. AI agents can
make mistakes, misunderstand instructions, overwrite files, or change more than
intended, so I need to stay aware of what an agent is doing. Clear prompts,
limits on which files it can modify, diff reviews, tests, and a human in the
loop all matter. I want to revisit this code later so I understand every part
more deeply. After that, I would expand the dataset, add real listening
behavior and collaborative filtering, and let the system learn from user
feedback.
