# Nottingham Splits

Author: Stefan Balke

The Nottingham dataset is a collection of folk music tunes in
lead sheet notation (melody + chords), originally in an ABC
format (http://abc.sourceforge.net/NMD/).

However, for easier access in experiments, those were converted
to MIDI files. In particular, Nicolas Boulanger-Lewandowski et al. [1]
from Universite de Montreal used this dataset in their experiments
and provide a split into
train, validation, and test set on their accompanying website
(http://www-etud.iro.umontreal.ca/~boulanni/icml2012).

Recently, a company for machine-driven composing called JukeDeck
released a much cleaner version of the Nottingham dataset
(https://github.com/jukedeck/nottingham-dataset).
Unfortunately, the filenames do not match with Boulanger-Lewandowski's
released splits.

To overcome this issue, we provide interested users a list of corresponding
filename from Boulanger-Lewandowski's Nottingham data, to JukeDeck's version.

The actual outcome of this mini-project is saved in `train.txt`, `valid.txt`,
and `test.txt`. Everything python-related can be found in `python/`.

## Comparison of the Datasets

JukeDeck: 1034 MIDIs, repetitions included

Montreal: 1037 MIDIs, no repetitions

Number of MIDIs per subset:

| Subset | #MO | #JD |
|--------|-----|-----|
|playford |  15 |  15|
|morris   |  31 |  31|
|**reels**    | **464** | **461**|
|jigs     | 340 | 340|
|xmas     |  13 |  13|
|slip     |  11 |  11|
|ashover  |  46 |  46|
|waltzes  |  52 |  52|
|hpps     |  65 |  65|

## Matching

We will follow a two-step matching approach.
Since the most of the subset have the same number of MIDIs and are both
named with increasing numerical IDs, we match them one-to-one.
(Manual inspection revealed that this is a reasonable choice.)

Only for the **reels** subset, we use a standard content-based
retrieval approach. In our experiments, we regard Montreal's MIDIs
as the database and JukeDeck's MIDIs as the queries.
Since both dataset used different algorithms to extract the MIDI information
from the ABC files (e.g., left-out repetition),
the matching pairs may not have the same length.
We therefore only consider the pitch values of the first 80 note events from
both query and database elements.
We then use dynamic time warping (DTW) [2] to compare a given query sequence
with all possible database elements.
With this process, almost all MIDIs in the **reels** subset could be found.
However, since we only consider the first 80 pitches, we have a couple of wrong
matches due to derived songs in the database, i.e., two songs only deviate
very slightly.
From this manual correction, we found out that
`reelsh-l48.mid`, `reelsh-l49.mid`, and `reelsh-l50.mid` are actually
missing in JukeDeck's MIDIs.

We manually corrected those mismatches and saved the final matches in
`matches_final.csv`.

## Installation

We recommend using Anaconda (https://anaconda.org) for installing Python.
Once installed, all requirements can be satisfied by calling

```
    conda env create -f environment.yml
```

## Usage

```
    python match_fn.py
    python match_dtw.py
```

Both scripts create CSV files with matches which can then be merged
which requires some manual work.

Call

```
    python derive_splits.py
```

to create the new CSV files for the aimed train, validation, and
training splits, now with JukeDeck's MIDIs.

## References

[1] Nicolas Boulanger-Lewandowski, Yoshua Bengio, and Pascal Vincent. "Modeling temporal dependencies in high-dimensional sequences: Application to polyphonic music generation and transcription." arXiv preprint arXiv:1206.6392 (2012).

[2] Meinard Müller. Fundamentals of Music Processing: Audio, Analysis, Algorithms, Applications. Springer, 2015.
