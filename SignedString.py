

class SignedString:
    def __init__(self, string) -> None:
        self.chars = string[1::2]
        self.signs = string[::2]

    def index(self, char):
        return self.chars.index(char)
    
    def __len__(self):
        return len(self.chars)
    
    def __repr__(self):
        string = ''
        for i in range(len(self.chars)):
            string += self.signs[i] + self.chars[i]
        return string
    
    def __getitem__(self, i):
        return self.chars[i]
    
    def get_sign(self, i):
        return self.signs[i]