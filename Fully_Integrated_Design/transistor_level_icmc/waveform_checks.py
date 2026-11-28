"""Measure cycle settling and the ICMC update window."""
import csv
import numpy as np


def first_settled(rows):
    final = rows[-1]["held_at_88_mV"]
    acceptable = lambda row: (abs(row["input_cm_at_85_V"]-2.5) <= .005
                              and abs(row["held_at_88_mV"]-final) <= 1)
    for index, row in enumerate(rows):
        if all(acceptable(later) for later in rows[index:]):
            return int(row["cycle"])
    return None


def window(w, last_cycle, rail):
    t = w["time"]*1e6
    cm_sample = w["v(cm_sample)"]
    inside = (t > last_cycle+75) & (t < last_cycle+90)
    edges = np.flatnonzero(inside[:-1] & (np.diff(cm_sample > rail/2) != 0))
    rising = [i for i in edges if cm_sample[i+1] > cm_sample[i]]
    falling = [i for i in edges if cm_sample[i+1] < cm_sample[i]]
    def crossing(i):
        return float(t[i] + (t[i+1]-t[i])*(rail/2-cm_sample[i])/(cm_sample[i+1]-cm_sample[i]) - last_cycle)
    assert len(rising) == len(falling) == 1, (rising, falling)
    return crossing(rising[0]),crossing(falling[0])




def write_table(path, rows):
    with path.open("w") as out:
        csvout = csv.DictWriter(out, fieldnames=rows[0])
        csvout.writeheader()
        csvout.writerows(rows)
