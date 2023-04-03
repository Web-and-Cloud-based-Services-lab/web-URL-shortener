# the implementation of this converter is based on the ideas and pseudocode provided by Marcel Jackwerth
# reference: https://stackoverflow.com/questions/742013/how-do-i-create-a-url-shortener

class base62Converter:
    def __init__(self):
        # the map that is used to encode base10 values to base62 characters
        self.base62_map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
  
    def base10ToBase62(self, base10):
        tmp = ""
        while base10 > 0:
            # take the modulo of the remaining base10 as the index to map a corresponding base62 character
            remainder = self.base62_map[base10 % 62]
            tmp += remainder
            # update the remaining base10
            base10 //= 62
        # reverse the tmp to fetch the correct base62 because the encoding of base62 is done in a revsersed order
        base62 = tmp[len(tmp)::-1]
        return base62

    def base62ToBase10(self, base62):
        base10 = 0
        # for every character of the base62, calculate the corresponding base10 value and add them up
        for idx, char in enumerate(base62):
            # power = the length of the remaining base62
            power = len(base62) - idx - 1
            # base62Index = the index of the current base62 character to the base62_map
            base62Index = self.base62_map.index(char) 
            # calculate and add up the corresponding base10 value for the current base62 character 
            base10 += base62Index * (62 ** power)
        return base10

if __name__ == "__main__":
    converter = base62Converter()
    id = 123456666666
    short = converter.base10ToBase62(id)
    print("short: ", short)
    long = converter.base62ToBase10(short)
    print("long: ", long)

