import alphabet
import logo

print(logo.logo)
finish_line = "yes"
while finish_line == "yes":
    start_end = input("Please, type 'encode' to encrypt or 'decode' to decrypt\n")

    while start_end == 'encode':
        start_encode = input("Please, type your message to encode\n").lower()
        shifter_e = int(input("Please, type the shift number\n"))
        shift_num_encode = shifter_e % 36
        def encrypt(plain_text, shift_num):
            cipher_text = ""
            for letter in plain_text:
                position = alphabet.alphabet.index(letter)
                new_position = position + shift_num
                new_letter = alphabet.alphabet[new_position]
                cipher_text += new_letter
            return cipher_text
        print(f"Here is the encoded result: {encrypt(plain_text = start_encode, shift_num = shift_num_encode)}" )
        finish_encode = input("Please, type 'yes' if you want to try again. Otherwise type 'no'\n").lower()
        if finish_encode == 'no':
            start_end = "stop"
            print("Stopped encryption")
            finish_line = "no"
        else:
            finish_line = "yes"
            start_end = "stop"

    while start_end == 'decode':
        start_decode = input("Please, type your message to decode\n").lower()
        shifter_d = int(input("Please, type the shift number\n"))
        shift_num_decode = shifter_d % 36
        def decrypt(plain_text_dec, shift_num_dec):
            cipher_text = ""
            for letter in plain_text_dec:
                position = alphabet.alphabet.index(letter)
                new_position = position - shift_num_dec
                cipher_text += alphabet.alphabet[new_position]
            return cipher_text
        print(f"Here is the decoded result: {decrypt(plain_text_dec = start_decode, shift_num_dec = shift_num_decode)}")
        finish_decode = input("Please, type 'yes' if you want to try again. Otherwise type 'no'\n").lower()
        if finish_decode == 'no':
            start_end = "stop"
            print("Stopped decoding")
            finish_decode = "no"
        else:
            finish_line = "yes"
            start_end = "stop"