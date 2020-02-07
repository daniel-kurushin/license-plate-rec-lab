from glob import glob


for log in glob('??'):
    print(int(log), end = ' ')
    n, m = 0, 0
    for line in [ _.strip('\n') for _ in open(log).readlines() ]:
        _in = line.split(':')[0].strip()
        _out = line.split(';')[1].strip()
        i = 0
        for c in _out:
            if c == _in[i]: m += 1
            i += 1
            n += 1
    print(m / n)