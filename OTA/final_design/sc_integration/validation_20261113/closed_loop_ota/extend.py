"""Check higher resistances and verify the most useful tested cases."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile

from check import OUT, bench, simulate, write_csv


def main():
    tests = [(12,7,r,c) for r,c in ((1000,0),(2000,0),(5000,0),(10000,0),
                                   (1000,26.6),(2000,53.2),(5000,133),(10000,266))]
    tests += [(cp,cn,500,13.3) for cp,cn in ((7,7),(12,12),(7,12),(10,9))]
    with tempfile.TemporaryDirectory(prefix="sc-unity-high-") as tmp:
        with ThreadPoolExecutor(max_workers=5) as pool:
            jobs = [pool.submit(simulate, Path(tmp)/str(i), cp, cn, r,c,
                                save=True) for i,(cp,cn,r,c) in enumerate(tests)]
            fine = pool.submit(simulate,Path(tmp)/"fine",12,7,500,13.3,cycles=5,step="10n")
            write_csv(OUT/"extended.csv",[job.result() for job in jobs])
            write_csv(OUT/"fine.csv",[fine.result()])
    with tempfile.TemporaryDirectory(prefix="sc-unity-scaled-") as tmp:
        cases = ((100, 2.66), (200, 5.32), (300, 7.98), (400, 10.64),
                 (500, 13.3), (600, 15.96), (700, 18.62))
        with ThreadPoolExecutor(max_workers=5) as pool:
            jobs = [pool.submit(simulate, Path(tmp)/str(r), 12, 7, r, cap, save=r==500)
                    for r, cap in cases]
            write_csv(OUT/"scaled_screen.csv", [job.result() for job in jobs])
    bench(OUT/"unity_500k.cir",12,7,500,13.3)


if __name__ == "__main__":
    main()
