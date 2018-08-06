"""
    Analyze the matching results. Basically looking at possible duplicates
    and matches with high costs.

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
import pandas as pd


if __name__ == '__main__':
    best_matches = pd.read_csv('matches_dtw.csv')

    # number of queries
    print('Number of queries: {}'.format(best_matches.shape[0]))

    # number of unique database elements
    print('Number of used db elements: {}'.format(best_matches['fn_db'].unique().shape[0]))

    print('List of possible duplicates:')
    print(best_matches[best_matches.duplicated(['fn_db'], keep=False)].sort_values(by=['fn_db']))
    # print('Number of unique db items: {}'.format())

    print('List of bad matches:')
    print(best_matches[best_matches['matching_cost'] > 10].sort_values(by=['matching_cost']))
