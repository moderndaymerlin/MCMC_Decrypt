"""
The following code takes as input an encoded piece of text that requires a 26-letter key to
decode. Using a lengthy novel as a training resource to learn the frequencies
of different two-letter pairs, the algorithm traverses the probability field and tends
to local minima. As a result of this, it will find the combination of adjacent letters that
most resembles the training resource, thus tending to the true 26-letter key.
"""
import random
import string
import math

# Generate key dictionary by pairing key with respective letter in alphabet (e.g. "FHE" -> "F:A, H:B, E:C")
def create_key_dict(key):
    keys = {}
    for i in range(len(key)):
        keys[list(string.ascii_uppercase)[i]] = key[i]
    return keys

# Apply the key dictionary with above function to the provided text to "decrypt"
def apply_key(key, text):
    keys = create_key_dict(key)
    output = ""
    for character in text:
        if character.upper() in keys:
            output += keys[character.upper()]
        else:
            output += " "
    return output

# Generate score for a given key
def key_score(text, key, frequencies):
    keys = create_key_dict(key)
    decrypted_text = apply_key(key, text)
    text_freq = adj_letters_test(decrypted_text)
    score = 0
    for i,j in text_freq.items():
        if i in frequencies:
            score += j*math.log(frequencies[i])
    return score

# Go through training data (e.g. a long novel) and find frequencies of adjacent letters (e.g. "SH: 2039, AB: 140")
def adj_letters_train(training):
    frequencies = {}
    alphabet = list(string.ascii_uppercase + " ")
    with open(training) as f:
        for line in f:
            data = list(line.strip())
            for i in range(len(data)-1):
                x = data[i].upper()
                y = data[i+1].upper()
                if x not in alphabet:
                    x = " "
                if y not in alphabet:
                    y = " "
                key = x + y
                if key not in frequencies:
                    frequencies[key] = 1
                else:
                    frequencies[key] += 1
    return frequencies

# Go through test data (i.e. text decrypted using current key) and find frequencies of adjacent letters (e.g. "SH: 12, AB: 3")
def adj_letters_test(text):
    frequencies = {}
    alphabet = list(string.ascii_uppercase + " ")
    data = list(text.strip())
    for i in range(len(data)-1):
        x = data[i].upper()
        y = data[i+1].upper()
        if x not in alphabet:
            x = " "
        if y not in alphabet:
            y = " "
        key = x + y
        if key not in frequencies:
            frequencies[key] = 1
        else:
            frequencies[key] += 1
    return frequencies

# Generate a new key
def new_key(key):
    first = random.randint(0, len(list(key))-1)
    second = random.randint(0, len(list(key))-1)
    if first == second:
        return new_key(key)
    else:
        key = list(key)
        x, y = key[first], key[second]
        key[first], key[second] = y, x
        return "".join(key)

# Core MCMC algorithm
def mcmc(n, text, frequencies):
    key = string.ascii_uppercase
    keys = set()
    best_key = ''
    score = 0
    best_score = 0
    for i in range(n):
        keys.add(key)
        proposed_key = new_key(key)
        current_key_score = key_score(text, key, frequencies)
        new_key_score = key_score(text, proposed_key, frequencies)
        if new_key_score - current_key_score < -10000:
        	accept_prob = 0
        else:
        	accept_prob = min(1, math.exp(new_key_score - current_key_score))
        if current_key_score > best_score:
            best_score = current_key_score
        if current_key_score > score:
            best_key = key
        if random.uniform(0,1) < accept_prob:
            key = proposed_key
        if i % 1000 == 0:
            print("Iteration", i, ":", apply_key(key, text)[0:50], current_key_score, best_score,key)
    return keys, best_key, best_score

# Function to run MCMC
def run_mcmc():

    frequencies = adj_letters_train('training.txt')
    with open('test5.txt', 'r') as text:
        data = text.read().replace('\n',' ')

    encrypt_key = "FADGZPKYVWXCNTUQRIJSBHLOEM"
    decrypt_key = "BULCYADVRSGWZNXFPQTOMIJKHE"

    #test = apply_key(encrypt_key, data)
    test = data
    bestest_score = 0
    bestest_key = ''
    iterations = 5

    for iteration in range(iterations):
        print('\n')
        print('TRIAL #',iteration+1)
        print('\n')
        print('Encrypted text', test)
        states,best_key,best_score = mcmc(10000, test, frequencies)
        if best_score > bestest_score:
            bestest_score = best_score
            bestest_key = best_key
        print('\n')
        print('Decrypted text:', apply_key(best_key, test))
        print('\n')
        print('Key found:', best_key)
        print('Best score:', best_score)
        print('All-time best score:', bestest_score)
        print('\n')

    print('###################')
    print('##### SUMMARY #####')
    print('###################')
    print('\n')
    print('All-time best score: ', bestest_score)
    print('Corresponding key: ', bestest_key)
    print('Actual key:', decrypt_key)
    print('\n')
    print('Encrypted text: ', test)
    print('\n')
    print('Decrypted text: ', apply_key(bestest_key, test))
    print('\n')
    #print('Original text: ', data)
    #print('\n')

    with open('decrypted.txt', 'w') as output:
        output.write('All-time best score: ')
        output.write(str(bestest_score))
        output.write('\n')
        output.write('Corresponding key: ')
        output.write(bestest_key)
        output.write('\n')
        output.write('Actual key: ')
        output.write(decrypt_key)
        output.write('\n\n')
        output.write('Encrypted text: ')
        output.write(test)
        output.write('\n\n')
        output.write('Decrypted text: ')
        output.write(apply_key(bestest_key, test))
        output.write('\n\n')
        output.write('Original text: ')
        output.write(data)

if __name__ == '__main__':
    run_mcmc()