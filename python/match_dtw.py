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

import librosa
import pretty_midi
import tqdm
import pandas as pd


def get_note_seq(path, n_notes=80):
    # load MIDI
    midi = pretty_midi.PrettyMIDI(path)
    midi.instruments[0].notes = midi.instruments[0].notes[:n_notes]

    note_sequence = [cur_note.pitch for cur_note in midi.instruments[0].notes]

    return note_sequence


if __name__ == '__main__':
    DEBUG = False
    N_NOTES = 80
    path_jd = os.path.join('data', 'nottingham_jukedeck')
    path_mo = os.path.join('data', 'nottingham_montreal')

    subsets = ['reels']

    # Montreal's MIDIs form the DB
    # JukeDeck's MIDIs are the queries

    best_matches = []

    # build DB
    for cur_subset in tqdm.tqdm(subsets):
        db = []

        # collect piano rolls
        for cur_path_db_midi in glob.glob(os.path.join(path_mo, 'complete', cur_subset + '*.mid')):
            note_sequence = get_note_seq(cur_path_db_midi, n_notes=N_NOTES)

            cur_db_item = {'fn': os.path.basename(cur_path_db_midi),
                           'seq': note_sequence}

            db.append(cur_db_item)

        # do the matching
        for cur_path_query_midi in tqdm.tqdm(glob.glob(os.path.join(path_jd, 'MIDI', cur_subset + '*.mid'))):
            cur_query_fn = os.path.basename(cur_path_query_midi)
            best_match = {'fn_query': cur_query_fn, 'fn_db': 'init', 'matching_cost': 100000}
            cur_query_seq = get_note_seq(cur_path_query_midi, n_notes=N_NOTES)

            # match query with all db items
            for cur_db in db:
                D = librosa.core.dtw(X=cur_db['seq'], Y=cur_query_seq, metric='euclidean', backtrack=False)
                cur_matching_cost = D[-1, -1]

                if cur_matching_cost < best_match['matching_cost']:
                    best_match = {'fn_query': cur_query_fn, 'fn_db': cur_db['fn'], 'matching_cost': cur_matching_cost}

            # store the best match
            best_matches.append(best_match)

    best_matches = pd.DataFrame(best_matches)
    best_matches.to_csv('matches_dtw.csv')
