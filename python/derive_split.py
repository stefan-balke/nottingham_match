"""
    Derive CSVs with the new filenames from JukeDeck's MIDIs.

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
    matches = pd.read_csv('matches_final.csv')
    path_mo = os.path.join('data', 'nottingham_montreal')

    subset_folder = ['test', 'train', 'valid']

    for cur_subset in subset_folder:
        # get all MIDI files for this split
        fn_midi = glob.glob(os.path.join(path_mo, cur_subset, '*.mid'))
        fn_midi = [os.path.basename(cur_fn) for cur_fn in fn_midi]

        output = []

        # lookup corresponding JukeDeck MIDI
        for cur_fn in fn_midi:
            cur_match = matches[matches['fn_mo'] == cur_fn]
            cur_match = cur_match['fn_jd'].values

            if len(cur_match) == 0:
                print('No match for {}'.format(cur_fn))
            else:
                output.append(cur_match[0])

        # save as CSV
        output = pd.DataFrame(output)
        output.to_csv(cur_subset + '.csv', header=False, index=False)
