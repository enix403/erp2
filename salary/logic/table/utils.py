def make_policy_str(ranges):
    range_segments = []
    for rng in ranges:
        # range_segments.append(str(rng[0]) + '-' + str(rng[1]))
        if rng[0] == rng[1]:
            seg_str = str(rng[0])
        else:
            seg_str = str(rng[0]) + '-' + str(rng[1])

        range_segments.append(seg_str)

    return ','.join(range_segments)


def parse_policy_str(rep_policy: str):
    ranges = []
    for seg in rep_policy.split(","):
        try:
            parts = list(map(int, seg.split("-")))
            if len(parts) >= 2:
                ranges.append((parts[0], parts[1]))
            else:
                ranges.append((parts[0], parts[0]))
        except:
            pass

    return ranges