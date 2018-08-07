"""
    Copy Nottingham MIDIs to separate train, validation, and test folders.

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
import shutil
import pandas as pd


if __name__ == '__main__':
    path_splits = ['../train.txt', '../valid.txt', '../test.txt']
    path_jd = os.path.join('data', 'nottingham_jukedeck', 'MIDI')

    for cur_split in path_splits:
        # create folder
        dir = os.path.splitext(cur_split)[0]
        if not os.path.exists(dir):
            os.makedirs(dir)

        # read MIDIs
        fn_midis = pd.read_csv(cur_split, header=None)

        # copy MIDIs
        for cur_idx, cur_fn_midi in fn_midis.iterrows():
            path_src = os.path.join(path_jd, cur_fn_midi[0])
            path_des = os.path.join(dir, cur_fn_midi[0])
            shutil.copyfile(path_src, path_des)
