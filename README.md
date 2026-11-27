# Stack 2012 (hand on chin edition)

A one-tap 3D tower stacker built from a certain senior portrait. Drop the number blocks so the tower reads **2012** from the top down, keep it straight, and don't let him ride a block off the edge.

## Play

Open `index.html` in a browser. It's a single self-contained file: the photo textures are inlined, and three.js r128 loads from cdnjs.

To play on an iPhone, turn on GitHub Pages (Settings → Pages → Deploy from branch → `main` / root). Then open the Pages URL in Safari and use Share → Add to Home Screen to run it full screen.

## How it plays

- Tap anywhere to drop the swinging block. The blocks come in 2, 1, 0, 2 from the bottom up, and the year repeats forever.
- Round 1 uses big, slow blocks. Each completed 2012 makes the blocks about 12% smaller and a bit faster.
- Perfect drops build a streak, and every third perfect in a row straightens the tower ("Posture check!").
- He blinks at random.
- Too much lean or a big miss ends the run with a DJ airhorn (`sounds/airhorn.mp3`, embedded in the page) and a purple laser show. The game-over screen copies a rotating, overly dramatic copypasta brag with your real stats.
- The Greek ambient music (bouzouki-style plucks in D Hijaz over a drone) starts on the first tap. Gameplay is scored by *Senior Year Stomp*, an original acoustic folk track that starts from the top every game, builds in tempo, and gets nudged a little faster each round. The Greek music stays on the title screen. The ♪ button mutes everything.

All in-game audio is either synthesized live with the Web Audio API or, for *Senior Year Stomp*, rendered by `music/render.py` (numpy, original composition) and embedded in the page. `music/senior-year-stomp.mp3` is the full-quality track. The only outside sample is the airhorn in `sounds/airhorn.mp3`.
