#!/usr/bin/python
import sys

# parse specified file for 1h nmr shifts
# file[in]: filename to parse
# shifts[return]: dict of atomindices with associated shift

def get_shifts(filename):

    if not filename.endswith('_property.txt'):
        print('Error: orca propertyfile expected')
        sys.exit(1)

    shifts, index, type = [], [], []
    data = {}

    # read file
    try:
        with open(filename) as file:
            lines = file.readlines()

            # fix insanely stupid orca printing multiple results for different densities, use only last one
            count = 0
            for line in lines:
                if '$ EPRNMR_OrbitalShielding' in line:
                    count += 1

            while True:
                line = lines.pop(0)
                if '$ EPRNMR_OrbitalShielding' in line:
                    count -= 1
                if count == 0:
                    break
            # end fix

            #read shiftds
            for line in lines:
                # get grad time
                if ' Nucleus:' in line:
                    splitline = line.split()
                    try:
                        index.append(int(splitline[1]))
                        type.append(splitline[2])
                    except ValueError:
                        print('Error while reading index ' + filename)
                        sys.exit(1)
                if 'P(iso)' in line:
                    splitline = line.split()
                    try:
                        shifts.append(float(splitline[1]))
                    except ValueError:
                        print('Error while reading shift ' + filename)
                        sys.exit(1)
    except OSError:
        print('cannot open ' + filename)
        sys.exit(1)

    # check data
    if len(shifts) != len(index) or len(shifts) != len(type):
        print('shifts were not read correctly from ' + filename)
        sys.exit(1)

    if len(shifts) == 0:
        print('found no shifts .. abort ...')
        sys.exit(1)

    while shifts:
        # skip atomtypes other than H
        if type.pop() != 'H':
            shifts.pop(), index.pop()
            continue
        atomindex = index.pop()
        if atomindex in data:
            print('found several atoms with same index ... abort!')
            sys.exit(1)
        data[atomindex] = shifts.pop()

    return data

# read molecular positions from file specified by argv and print positions
def main():
    # get inputfile
    propertyfile = str(sys.argv[1])
    print(propertyfile)
    # parse for shifts
    shifts = get_shifts(propertyfile)

    keys = sorted(shifts.keys())

    print('1H Shifts:')
    for index in keys:
        print(str(index) + ' ' + str(shifts[index]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
