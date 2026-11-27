# Stack 2012 (hand on chin edition)

A one-tap 3D tower stacker built from a certain senior portrait. Drop the number blocks so the tower reads **2012** from the top down, keep it straight, and don't let him ride a block off the edge.

## Play

Open `index.html` in a browser. It's a single self-contained file: the photo textures are inlined, and three.js r128 loads from cdnjs.

To play on an iPhone, turn on GitHub Pages (Settings → Pages → Deploy from branch → `main` / root). Then open the Pages URL in Safari and use Share → Add to Home Screen to run it full screen.

## How it plays

- Tap anywhere to drop the swinging block. The blocks come in 2, 1, 0, 2 from the bottom up, and the year repeats forever.
- Round 1 uses big, slow blocks. Each completed 2012 makes the blocks about 12% smaller and a bit faster.
- Perfect drops build a streak, and every third perfect in a row straightens the tower ("Posture check!").
- Too much lean or a big miss ends the run with a DJ airhorn and a purple laser show.
- The Greek ambient music (bouzouki-style plucks in D Hijaz over a drone) starts on the first tap. From round 3 ("Stomp mode!") it crossfades into *Senior Year Stomp*, an original acoustic folk track that keeps speeding up. The ♪ button mutes everything.

All in-game audio is either synthesized live with the Web Audio API or, for *Senior Year Stomp*, rendered by `music/render.py` (numpy, original composition) and embedded in the page. `music/senior-year-stomp.mp3` is the full-quality track. There are no samples or copyrighted songs.
