class base62Converter:
    def __init__(self):
        self.base62_map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
  
    def base10ToBase62(self, base10):
        tmp = ""
        while base10 > 0:
            remainder = self.base62_map[base10 % 62]
            tmp += remainder
            base10 //= 62
        base62 = tmp[len(tmp)::-1]
        return base62

    def base62ToBase10(self, base62):
        base10 = 0
        for idx, char in enumerate(base62):
            power = len(base62) - idx - 1
            base62Index = self.base62_map.index(char) 
            base10 += base62Index * (62 ** power)
        return base10

if __name__ == "__main__":
    converter = base62Converter()
    id = 12345
    short = converter.base10ToBase62(12345)
    print("short: ", short)
    long = converter.base62ToBase10(short)
    print("long: ", long)

