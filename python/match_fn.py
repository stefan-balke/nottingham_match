"""
    Matching JukeDeck's version of the Nottingham DB with Montreal's version.
    The goal is to use JukeDeck's MIDIs but Montreal's train/val/test splits.
    Mathing will be performed on subsets of the database (e.g., 'ashover').

    Copyright (C) 2018 Stefan Balke

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os
import glob
import pandas as pd


if __name__ == '__main__':

    FRAME_EXCERPT = 20  # we only use the first 20 frames for the matching
    path_jd = os.path.join('data', 'nottingham_jukedeck')
    path_mo = os.path.join('data', 'nottingham_montreal')

    subsets = ['playford', 'morris', 'reels', 'jigs', 'xmas', 'slip', 'ashover', 'waltzes', 'hpps']

    matches = []

    for cur_subset in subsets:
        fn_mo = sorted(glob.glob(os.path.join(path_mo, 'complete', cur_subset + '*.mid')))
        fn_jd = sorted(glob.glob(os.path.join(path_jd, 'MIDI', cur_subset + '*.mid')))

        fn_mo = [os.path.basename(cur_fn) for cur_fn in fn_mo]
        fn_jd = [os.path.basename(cur_fn) for cur_fn in fn_jd]

        # if number of items is equal, use direct matches based on filenames
        if len(fn_mo) == len(fn_jd):
            for cur_match_idx, _ in enumerate(fn_mo):
                cur_match = {'fn_mo': fn_mo[cur_match_idx], 'fn_jd': fn_jd[cur_match_idx]}
                matches.append(cur_match)

    matches = pd.DataFrame(matches)
    matches.to_csv('matches_fn.csv')
