# ai-happy-01 entry: Puddle Jump in Red Boots

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

A fluffy yellow duckling in tiny red rain boots, caught in mid-air above a
puddle it has just jumped in. Its wings are spread wide, its eyes are squeezed
shut and its beak is wide open in a laugh, and a small crown of water drops
splashes up under the boots. Glossy 3D render on a plain sky-blue background.

The image was generated with Codex image generation from a text prompt written
for this bounty (no reference images, no words in the picture).

How it was chosen: candidates played pairwise games under the bounty's
published judge instructions, each pair in both orders, with Codex as a
stand-in judge. A game score is the mean of its two calls, and a call gives its
pick 0.5 plus a tenth of its margin, as in the bounty's rules.

The first attempt came from 30 candidates over three rounds and was a busy
storybook scene: a grandfather dancing in a kitchen with his granddaughter on
his slippers. The stand-in judge liked it best, but the bounty's real judge
placed it about 198th of 2000, so the stand-in's taste for such scenes does
not carry over.

This second attempt changes direction: one joyful subject, close up, with a
clean background and bright colour. Twelve new candidates (puppies, kittens,
otters, a quokka, a laughing child, a smiling sunflower and others) played a
round robin of fourteen with two reference images: the first attempt and a
picture that did well in a sibling bounty. Among the new candidates this
picture and a pair of otters holding paws led, each with eleven wins, one draw
and one loss (mean game scores 0.646 and 0.654), and they drew with each
other. The duckling was chosen because the otters' joined paws were drawn
fused. It was then resized from 1254 to 1024 pixels a side.

`entry.png` holds JPEG data (quality 93): the rules tell the format by the
first bytes and keep the name `entry.png` either way.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Without `MAKEFUN_OUTPUT_DIR` the picture goes to `/output/entry.png`.

## License

MIT, see `LICENSE`.
