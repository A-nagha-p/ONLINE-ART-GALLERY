from PIL import Image

def hide_text(image, text):
    # Convert text to binary
    binary_text = ''.join(format(ord(char), '016b') for char in text)  # Using 16 bits per character
    text_length = len(binary_text)

    width, height = image.size
    pixels = image.load()

    char_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            # Embed text into LSB of each color channel
            if char_index < text_length:
                # Check if there's enough bits left in the binary text for embedding
                if char_index + 6 <= text_length:
                    pixels[x, y] = (r & 0xFFC0 | int(binary_text[char_index:char_index+6], 2), 
                                    g & 0xFFC0 | int(binary_text[char_index:char_index+6], 2), 
                                    b & 0xFFC0 | int(binary_text[char_index:char_index+6], 2))
                else:
                    # If there's not enough bits, pad with zeros
                    remaining_bits = text_length - char_index
                    padding = '0' * (6 - remaining_bits)
                    pixels[x, y] = (r & 0xFFC0 | int(binary_text[char_index:] + padding, 2), 
                                    g & 0xFFC0 | int(binary_text[char_index:] + padding, 2), 
                                    b & 0xFFC0 | int(binary_text[char_index:] + padding, 2))
                char_index += 6  # Move to the next character
            else:
                # End of text, break the loop
                break