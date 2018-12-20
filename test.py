import re
import time

reaction = re.compile('aA|Aa|bB|Bb|cC|Cc|dD|Dd|eE|Ee|fF|Ff|gG|Gg|hH|Hh|iI|Ii|jJ|Jj|kK|Kk|lL|Ll|mM|Mm|nN|Nn|oO|Oo|pP|Pp|qQ|Qq|rR|Rr|sS|Ss|tT|Tt|uU|Uu|vV|Vv|wW|Ww|xX|Xx|yY|Yy|zZ|Zz')

def polymer_reaction_length(polymer : str):
    while len(reaction.findall(polymer)) > 0:
        polymer = re.sub(reaction, '', polymer)
    
    return len(polymer)

if __name__ == '__main__':
    with open('D:\\input.txt', 'r') as inp:
        polymer = inp.readline().strip()
        
        part_1 = polymer
        start = time.time()
        print(polymer_reaction_length(part_1))
        print(time.time() - start)

        min_length = 100000
        
        start = time.time()
        for c in 'qwertyuiopasdfghjklzxcvbnm':
            new_polymer = polymer.replace(c, '').replace(c.upper(), '')
            polymer_length = polymer_reaction_length(new_polymer)
            if min_length > polymer_length:
                min_length = polymer_length

        print(min_length)
        print(time.time() - start)
