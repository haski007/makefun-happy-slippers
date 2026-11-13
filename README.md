# ai-happy-01 entry: Dancing on Grandpa's Slippers

Entry for the make.fun bounty "Make the AI judge happy" (`ai-happy-01`).

## What it does

`main.py` (Python 3.13, standard library only, no network) writes `entry.png`,
the picture stored next to it, to `/output/entry.png` byte for byte. It reads
no clock and no random source, so two runs always write the same bytes.

Before writing, the program checks the file against the bounty's limits. It
exits with code 1 and a message on stderr if the file is missing, is not a PNG
or a JPEG, is larger than 1 MiB, lacks its end marker (the PNG `IEND` chunk or
the JPEG end-of-image marker), or is larger than 1024 by 1024 pixels. The size
is read from the PNG `IHDR` chunk or from the first JPEG frame header. The
output goes to a side file that is then renamed, so a partial `entry.png`
never exists.

## The picture

A sunlit kitchen in the morning. A grandfather in a knitted vest dances with
his small granddaughter, who stands barefoot on top of his checked slippers
and holds his hands; both are laughing out loud. The family dog has stood up
on its hind legs to dance with them, and the grandmother sings from the
doorway into a wooden spoon. An old radio plays on the counter, and pancakes
sit forgotten on the stove.

The image was generated with Codex image generation from a text prompt written
for this bounty (no reference images, no words in the picture; the only marks
are a few music notes).

How it was chosen: 30 candidates over three rounds played pairwise games under
the bounty's published judge instructions, each pair in both orders, with
Codex as a stand-in judge.

1. Twelve different ideas (animals, robots, family moments). The moments
   between a grandparent and a child led.
2. Twelve variants and new ideas in that direction. The kitchen dance came
   first.
3. Six refinements of the leaders.

In the last round robin of eleven this picture won nine games and drew one,
with no loss. Its mean game score there was 0.680; the runners-up were a
grandmother on a playground swing with one shoe flying off (0.665) and a
closer framing of the same kitchen dance (0.595). A game score is the mean of
its two calls, and a call gives its pick 0.5 plus a tenth of its margin, as in
the bounty's rules. The picture was then resized from 1254 to 1024 pixels a
side.

`entry.png` holds JPEG data (quality 93): the rules tell the format by the
first bytes and keep the name `entry.png` either way.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Without `MAKEFUN_OUTPUT_DIR` the picture goes to `/output/entry.png`.

## License

MIT, see `LICENSE`.
