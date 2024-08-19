import numpy as np
from copy import deepcopy

from enums import M, P, S, Z


def check_meld_existence(tiles, start_idx, is_number=True):
    copy_tiles = deepcopy(tiles)
    if len(copy_tiles) < 3:
        return None

    if is_number:
        if len(copy_tiles) == 3:
            copy_tiles.append(99)
        if copy_tiles[0] == copy_tiles[1] == copy_tiles[2]:
            return start_idx + np.array([0, 1, 2])
        if copy_tiles[0] + 1 == copy_tiles[1] and copy_tiles[0] + 2 == copy_tiles[2]:
            return start_idx + np.array([0, 1, 2])
        if copy_tiles[0] + 1 == copy_tiles[1] and copy_tiles[0] + 2 == copy_tiles[3]:
            return start_idx + np.array([0, 1, 3])
        if copy_tiles[0] + 1 == copy_tiles[2] and copy_tiles[0] + 2 == copy_tiles[3]:
            return start_idx + np.array([0, 2, 3])
        return None
    else:
        if copy_tiles[0] == copy_tiles[1] == copy_tiles[2]:
            return start_idx + np.array([0, 1, 2])
        return None


def find_melds(hand_tiles, is_number=True):
    routes = []

    if is_number:
        num_select = 4
    else:
        num_select = 3

    for i in range(len(hand_tiles)-2):
        idx_to_del = check_meld_existence(hand_tiles[i:i+num_select], i, is_number)
        if idx_to_del is not None:
            sel_hand_tiles = [hand_tiles[j] for j in range(len(hand_tiles)) if j not in idx_to_del]
            route = [hand_tiles[i] for i in idx_to_del]
            deeper_routes = find_melds(sel_hand_tiles)
            if not deeper_routes:
                routes.append(route)
            else:
                for dr in deeper_routes:
                    routes.append(route+dr)
    return routes


def check_wait_existence(tiles, start_idx, is_number=True):
    if len(tiles) < 2:
        return None

    if is_number:
        if tiles[0] == tiles[1] or tiles[0] + 1 == tiles[1] or tiles[0] + 2 == tiles[1]:
            return start_idx + np.array([0, 1])
        else:
            return None
    else:
        if tiles[0] == tiles[1]:
            return start_idx + np.array([0, 1])
        else:
            return None


def find_waits(hand_tiles, is_number=True):
    waits = []

    for i in range(len(hand_tiles) - 1):
        idx_to_del = check_wait_existence(hand_tiles[i:i + 2], i, is_number)
        if idx_to_del is not None:
            sel_hand_tiles = [hand_tiles[j] for j in range(len(hand_tiles)) if j not in idx_to_del]
            wait = [hand_tiles[i] for i in idx_to_del]
            deeper_waits = find_waits(sel_hand_tiles, is_number)
            if not deeper_waits:
                waits.append(wait)
            else:
                for dr in deeper_waits:
                    waits.append(wait + dr)

    return waits


def calc_normal_shanten_count(num_compositions):
    counts = []

    num_compositions_m = num_compositions[M]
    num_compositions_p = num_compositions[P]
    num_compositions_s = num_compositions[S]
    num_compositions_z = num_compositions[Z]

    for num_m in num_compositions_m:
        for num_p in num_compositions_p:
            for num_s in num_compositions_s:
                for num_z in num_compositions_z:
                    nums = np.array(num_m) + np.array(num_p) + np.array(num_s) + np.array(num_z)
                    print(nums)
                    m, d, p = nums[0], nums[1], nums[2]
                    if m == 4:
                        return 0
                    c = m + d - 5 if m + d > 5 else 0
                    q = 1 if p > 0 else 0
                    counts.append(9 - 2 * m - d + c - q)
    return min(min(counts), 6)


def calc_kokushi_musou_shanten_count(hand_tiles):
    num = 0
    for cls in ['m', 'p', 's']:
        cur_tiles = hand_tiles[cls]
        if 1 in cur_tiles:
            num += 1
        if 9 in cur_tiles:
            num += 1
    num += len(set(hand_tiles['z']))
    return 13 - num
