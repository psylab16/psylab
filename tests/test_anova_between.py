"""
Test anova analysis.
"""
import os
import numpy as np
from psylab.dataview import from_csv
from psylab.stats import anova_between


# F values taken from
# http://davidmlane.com/hyperstat/factorial_ANOVA.html
known_f = [273.038, 535.154, 246.416, 141.543, 55.290, 60.314, 7.891, np.nan, np.nan]
hyperstat_3f = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/hyperstat_3f_between.csv')


def test_stats_anova_between():
    """ Test anova """
    data = from_csv(hyperstat_3f, dv="dv")
    anova = anova_between(data.data)
    assert np.allclose(known_f, anova.f)
    # print known_f
    # print an.f
    # print psylab.stats.anova_table(an)
