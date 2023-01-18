import codecs


def main(input):
    # The string with Unicode escape sequences
    s = input.encode()
    # Decode the string from its current encoding to Unicode
    s = codecs.decode(s, "utf-8")

    # Encode the string back to its original encoding


    # The string with all Unicode escape sequences converted to their respective normal characters
    print(s)

    return s

