from collections import Counter, defaultdict

from enums import M, P, S, Z
from shanten_count import find_melds, find_waits, calc_normal_shanten_count, calc_kokushi_musou_shanten_count
from utils import process_hand_tiles, generate_initial_hand_tiles


if __name__ == '__main__':
    tiles_mountain = "6p2p5z2m7m4m7s7z1s7s5p3p9s4p1m1m1s7z8s" \
                     "5s0m8p9p5p4p1s5m2m5p1p7z6z1z7m6p4z4s9s" \
                     "8m6s5m2s6m2z3z9s9p9m8s8s3s9p8m3s6z1p5z" \
                     "7s1p3z4s4m2s3z3p2m4s6s6z1z7p5z7z9m8s6m" \
                     "4z6p3m8p9p5s1z4p6z9m4p2s3m0p2s4s4m3m1z" \
                     "6s4z7p3s2z1m5m7p6m4z1s2z2z0s4m5s7s6m7p" \
                     "2p8p3p8p3s8m2p3z9s3m2p2m6s8m5z3p7m6p9m" \
                     "1m7m1p"

    east_hand_tiles, south_hand_tiles, west_hand_tiles, north_hand_tiles = generate_initial_hand_tiles(tiles_mountain)
    test_tiles = process_hand_tiles(south_hand_tiles)
    all_nums = defaultdict(list)
    for cls in [M, P, S, Z]:

        if cls == Z:
            is_number = False
        else:
            is_number = True

        melds = find_melds(test_tiles[cls], is_number)
        melds = list(set(map(tuple, [sorted(meld) for meld in melds])))
        if not melds:
            waits = find_waits(test_tiles[cls], is_number)
            waits = list(set(map(tuple, [sorted(wait) for wait in waits])))
            num_melds, num_waits, num_pairs = 0, 0, 0
            if not waits:
                all_nums[cls].append([num_melds, num_waits, num_pairs])
            else:
                for wait in waits:
                    for i in range(0, len(wait), 2):
                        if wait[i] == wait[i + 1]:
                            num_pairs += 1
                        num_waits += 1
                    all_nums[cls].append([num_melds, num_waits, num_pairs])
        else:
            counter1 = Counter(test_tiles[cls])
            for meld in melds:
                counter2 = Counter(meld)
                left_tiles = list((counter1 - counter2).elements())
                waits = find_waits(left_tiles, is_number)
                waits = list(set(map(tuple, [sorted(wait) for wait in waits])))
                num_melds, num_waits, num_pairs = len(meld) // 3, 0, 0
                if not waits:
                    all_nums[cls].append([num_melds, num_waits, num_pairs])
                else:
                    for wait in waits:
                        for i in range(0, len(wait), 2):
                            if wait[i] == wait[i + 1]:
                                num_pairs += 1
                            num_waits += 1
                        all_nums[cls].append([num_melds, num_waits, num_pairs])

    normal_shanten_count = calc_normal_shanten_count(all_nums)
    kokushi_musou_shanten_count = calc_kokushi_musou_shanten_count(test_tiles)
    shanten_count = min(normal_shanten_count, kokushi_musou_shanten_count)
    print("shanten_count: ", shanten_count)
