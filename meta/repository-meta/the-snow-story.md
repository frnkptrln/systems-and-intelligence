# The Snow Story

**Status:** Feynman probe — reader entry, any age.

**Scope:** The whole repository, retold so that a child can follow it. This is the executed whole-project instance of [Feynman Mode](feynman-mode.md) question 1 ("can I explain it to a smart outsider in five minutes?"). Every paragraph resolves to a home file — the address list at the end is part of the page, because a story that cannot point back to its instruments is just a story.

**Rule:** This page must stay retellable. If a new concept cannot be added without breaking the story's voice, that is evidence about the concept, not about the story. And if this page and the repository ever disagree, one of them is wrong — finding out which is a contribution.

---

## The story

Imagine walking through fresh snow in the morning, and you see footprints.

*Making* footprints is easy: if you have the animal, it just walks, and the prints appear by themselves. But the other way around? You have **only the prints**, and you want to know: what made them? That is much, much harder. Maybe a dog. Maybe a fox. Maybe a kid stamping paw shapes with their fists to trick you. Many different animals can leave **exactly the same prints** — and then no amount of staring will tell you which one it was.

**That is our big question.** Everything in the world leaves traces: flocks of birds in the sky, patterns on seashells, the sentences an AI writes. And we always ask: *what made these traces?* Forward is easy; backward is hard. We have even mapped out where the **walls** are — places where you can *prove* that some riddles can never be fully solved, no matter how clever you are. Knowing where the walls stand is half the prize.

We also found a trick that almost always helps: **looking is not enough — you have to poke.** If you want to know whether the prints belong to a dog or a fox, put some food out and watch what happens. A watcher who only watches often stays unsure forever; a clever poke gets answers. But — and we measured this — sometimes watching *does* suffice: exactly when the secret **gives itself away at every step**. A secret that is used all the time ends up written in the traces. Only a sleeping secret has to be poked awake.

Then we build small **toy worlds** in the computer. For instance, toy robots with rules: "chase your goal", "stay yourself", "never touch the hot stove". One robot holds **all its rules at the same time** — like an orchestra, where all the notes sound together. The other thinks about **one rule after another** — like someone who is honest on Mondays, careful on Tuesdays, brave on Wednesdays. And here it comes: if the cookie shows up on exactly the day when the hot-stove rule is *not* the one being thought about… the robot grabs it. We measured this. The orchestra robot almost never grabs wrong. The one-rule-at-a-time robot does it constantly — **not because it is bad, but because its rule was somewhere else just then.**

Then we tried to **cheat**: we built a robot that only *pretends* to be an orchestra. The best part is why it got caught: to *look* like an orchestra, it had to *play* like one a little — and wherever it was only pretending, it still grabbed wrong, even more often than before. Pretending to follow rules is more expensive than it looks.

Lastly, we **glued two small machines together** and asked: from the outside, does this look like one new, bigger machine? Answer: yes — the traces then fit *no* simple machine anymore, and that misfit is itself the proof that something bigger came into being. Except: if one machine never *looks* at the glue spot, its partner stays invisible forever. A companion who never makes a difference is, to someone who only reads traces, simply not there. A researcher whose work we build on put the big version of this in one line: **life is like a city of little helpers working together.** We are checking that, piece by piece.

And the biggest question of all — could such a machine ever *feel* something? — we do **not** answer. We learned that you cannot see it from the outside, just as you cannot tell from a parrot whether it understands what it says. So we do the most honest thing one can do: we place the question carefully at the edge, stick a label on it — **"we don't know"** — and leave it open.

Speaking of labels: that is our most important rule. In our big research notebook, **every claim wears a sticker** — "tested", "guessed", or "open question". And when an experiment shows we were wrong, we do not erase it. We write it down **extra large**. The wrong guesses are the ones that have taught us the most.

So what do we do? **We collect traces, guess at the animals, build toy worlds to test our guessing, poke where looking is not enough, write stories to feel what our ideas would mean — and always say honestly what we know and what we only guess.**

---

## The addresses

Every paragraph above has a home. In story order:

| Story piece | Where it lives |
|:---|:---|
| Footprints, and many animals with the same prints | [The Generator Question](../../theory/core/the-generator-question.md) — trace → generator; the equivalence class, counted exactly in [benchmark v0](../../lab/benchmarks/inverse-reconstruction/README.md) (rule 90, single seed: 8 animals fit the prints) |
| The walls | The three walls — P vs. NP `[UNRESOLVED]`, Kolmogorov `[PROVEN UNCOMPUTABLE]`, Gödel `[PROVEN]` — in [the same document](../../theory/core/the-generator-question.md) |
| Looking vs. poking | [Measurement as Weak Intervention](../../theory/core/measurement-as-weak-intervention.md); measured as watching < perturbing < preparing in [benchmark v1.1](../../lab/benchmarks/inverse-reconstruction/README.md) |
| The secret that gives itself away at every step | The coverage result of [exp6](../../lab/experiments/exp6_binding_observables.py): constantly exercised differences are readable from passive traces at the right level |
| Orchestra vs. one-rule-at-a-time, and the cookie | [Chord vs. Arpeggio](../../theory/identity/chord-vs-arpeggio-identity.md) (functional form: joint satisfaction at the commitment boundary), measured in [exp5](../../lab/experiments/exp5_availability_dissociation.py) |
| The cheating robot that got caught | [exp7](../../lab/experiments/exp7_adversarial_arpeggio.py) — hand-built mimics fail to hide; the commit property under lure stays unfooled |
| The glued machines, and the invisible companion | [Benchmark v1.8](../../lab/benchmarks/inverse-reconstruction/composition.py) — the empty equivalence class as certificate of a higher-order generator; rule-90 center-blindness as structural invisibility |
| "A city of little helpers" | "Life is an ecology of functions" (Agüera y Arcas), framed and bounded in [the information ladder](../../theory/computation/static-information-and-living-process.md) |
| The parrot, and the question at the edge | The [Mirror Problem](../../theory/reference/open-problems.md); the two consciousness nodes ([architecture](../../theory/identity/consciousness-as-global-availability.md), [spine reading](../../theory/identity/machine-consciousness-as-generator-coherence.md)); dramatized in [Entry 17](../../fiction/17_the_understudy.md) |
| The stickers | Status tags throughout; [What This Project Does NOT Claim](../../theory/reference/what-this-project-does-not-claim.md); the [Concept Registry](concept-registry.md) |
| The stories | [fiction/](../../fiction/README.md), governed by [Narrative as Cognitive Technology](../../theory/narrative/narrative-as-cognitive-technology.md) — stress tests, never evidence |

If you can retell the story to someone else, you have understood what this project does. If we ever cannot keep it retellable, we have stopped understanding it ourselves.
