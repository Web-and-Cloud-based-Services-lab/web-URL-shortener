base62_map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def base10ToBase62(base10):
    tmp = ""
    while base10 > 0:
        remainder = base62_map[base10 % 62]
        tmp += remainder
        base10 //= 62
    base62 = tmp[len(tmp)::-1]
    return base62

def base62ToBase10(base62):
    base10 = 0
    for idx, char in enumerate(base62):
        power = len(base62) - idx - 1
        base62Index = base62_map.index(char) 
        base10 += base62Index * (62 ** power)
    return base10

if __name__ == "__main__":
    id = 12345
    short = base10ToBase62(12345)
    print("short: ", short)
    long = base62ToBase10(short)
    print("long: ", long)
    # print(len('hnd'))

