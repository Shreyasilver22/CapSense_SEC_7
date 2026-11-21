"""Small diagnostic to check whether reinitializing the two sensor electrodes restores signal."""
from concurrent.futures import ThreadPoolExecutor

import test_provided_sc as sc


baseline = sc.build
sc.WIRINGS['sensor_reset_diagnostic'] = (False, 'negative', 'grounded')


def with_sensor_reset(trial, case):
    circuit = baseline(trial,case)
    if trial.wiring != 'sensor_reset_diagnostic':
        return circuit
    devices = []
    for branch in 'pn':
        devices += [f'MN_SRESET_{branch} sens{branch} phi1 0 0 N W=10u L=.8u AD=45p AS=45p PD=29u PS=29u',
                    f'MP_SRESET_{branch} sens{branch} phi1b 0 vdd P W=20u L=.8u AD=90p AS=90p PD=49u PS=49u']
    return circuit.replace('.save ','\n'.join(devices)+'\n.save ')


def main():
    sc.build = with_sensor_reset
    tests = [sc.Trial('sensor_reset_diagnostic',p) for p in (7.82,9,10,10.5,11.79)]
    tests += [sc.Trial(w,10.5,cycles=8,step=40,solver='gear')
              for w in ('sensor_common_grounded','sensor_reset_diagnostic')]
    with ThreadPoolExecutor(4) as pool:
        rows=list(pool.map(sc.run,tests))
    sc.save(sc.ROOT/'provided_sc_sensor_reset_diagnostic.csv',rows)


if __name__=='__main__':
    main()

