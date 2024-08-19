from collections import defaultdict


def generate_initial_hand_tiles(tiles_mountain):
    east_hand_tiles = tiles_mountain[0:8] + tiles_mountain[32:40] + tiles_mountain[64:72] + tiles_mountain[96:98]
    south_hand_tiles = tiles_mountain[8:16] + tiles_mountain[40:48] + tiles_mountain[72:80] + tiles_mountain[98:100]
    west_hand_tiles = tiles_mountain[16:24] + tiles_mountain[48:56] + tiles_mountain[80:88] + tiles_mountain[100:102]
    north_hand_tiles = tiles_mountain[24:32] + tiles_mountain[56:64] + tiles_mountain[88:96] + tiles_mountain[102:104]
    return east_hand_tiles, south_hand_tiles, west_hand_tiles, north_hand_tiles


def process_hand_tiles(hand_tiles):
    result = defaultdict(list)
    for i in range(0, len(hand_tiles), 2):
        cls = hand_tiles[i+1]
        num = hand_tiles[i]
        if num == '0':
            num = 5
        result[cls].append(int(num))
    for cls, nums in result.items():
        result[cls] = sorted(nums)
    return result
