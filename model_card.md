# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The catalog has only 17 songs, so one song can represent an entire genre or
mood and limit the variety of the results. The handcrafted weights and exact
genre and mood matches may over-prioritize familiar categories, reinforcing a
filter bubble. The system has no collaborative filtering and does not learn
from listening history, skips, or ratings. It also cannot understand lyrics,
language, context, or a new user's preferences, which creates cold-start and
relevance problems.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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

This deliberately conflicting profile produces the most surprising ranking:
the only classical song is third because its calm audio is far from the
high-energy targets. Storm Runner instead receives 0.25 for its intense mood
and 0.4126 from close numerical features; it gets no genre points, for a total
of 0.6626. This is mathematically consistent, but it shows that one exact genre
label cannot fully represent a conflicted preference.

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
the intended genre 0.30 and energy 0.12 weights. The experiment reinforces the
limitations above: handcrafted weights can strongly shape exposure, the tiny
catalog offers few alternatives, and the system cannot learn whether a user
actually prefers the changed rankings.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
