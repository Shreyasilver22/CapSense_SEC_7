"""Run the 2 V RX precharge end-point and corner comparison."""
from concurrent.futures import ThreadPoolExecutor
from check_sensitivity_rx_bias import BiasCase, evaluate, make_biased, s


def main():
    s.make_files = make_biased
    trials = (
        ("typ", 7.82), ("typ", 10.5), ("typ", 11.79),
        ("cold", 7.82), ("cold", 11.79), ("hot", 7.82), ("hot", 11.79),
    )
    cases = [BiasCase(20, 60, c, corner=k, rx_v=2) for k, c in trials]
    with ThreadPoolExecutor(5) as pool:
        rows = list(pool.map(evaluate, cases))
    s.write_csv("rx_precharge_2v_points.csv", rows)


if __name__ == "__main__":
    main()
