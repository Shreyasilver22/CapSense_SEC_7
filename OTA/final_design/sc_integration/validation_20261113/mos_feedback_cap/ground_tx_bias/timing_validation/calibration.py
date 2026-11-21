"""Check whether gain and offset calibration transfer across sensor pairs."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory

from check import Case, evaluate, write_csv

MODELS = (("tntp49_5v",5,27),("wnwp49_5v",4.5,85),("bnbp49_5v",5.5,0),
          ("wnbp49_5v",4.5,85),("bnwp49_5v",5.5,0))
PAIRS = ((9.5,9.5),(12,7),(7,12),(10.5,8.5),(8.5,10.5),(8,7),(12,11),(12,12))


def main():
    with TemporaryDirectory(prefix="sc-calibration-") as temp, ThreadPoolExecutor(max_workers=6) as pool:
        raw = evaluate(pool,Path(temp),"calibration_raw",[
            Case(8,3,cp,cn,model=m,supply=v,temp=t)
            for m,v,t in MODELS for cp,cn in PAIRS])
    for model, _, _ in MODELS:
        group = [r for r in raw if r["model"] == model]
        zero, positive = group[:2]
        gain = (positive["diff_mv"]-zero["diff_mv"])/positive["ideal_diff_mv"]
        for row in group:
            row["calibrated_error_mv"] = (row["diff_mv"]-zero["diff_mv"])/gain-row["ideal_diff_mv"]
            row["used_for_fit"] = (row["cp_pf"],row["cn_pf"]) in PAIRS[:2]
    write_csv(Path(__file__).with_name("calibration.csv"), raw)


if __name__ == "__main__":
    main()
