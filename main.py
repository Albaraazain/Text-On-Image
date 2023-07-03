# Importing the necessary modules for image manipulation, drawing, and text wrapping
from PIL import Image, ImageDraw, ImageFont
import textwrap

# setting the scale factor, so we control the resolution of the image, we multiply it to the width and height.
scale_factor = 10

# Creating a blank image with a white background
image_width = 200 * scale_factor
image_height = 200 * scale_factor
background_color = (255, 255, 255)  # white
image = Image.new("RGB", (image_width, image_height), background_color)

# Defining the base(English) font size
base_font_size = 10 * scale_factor
# Here we can replace the font with any font file, but must be in our directory. another way is to write the path of
# the font stored in our computer
base_font = ImageFont.truetype("FiraCode-Regular.otf", base_font_size)

# Defining the translation(Turkish) font size for the text
trans_font_size = base_font_size // 2
trans_font = ImageFont.truetype("FiraCode-Regular.otf", trans_font_size)  # replace with your font file

# Creating a drawing object to draw on the image
draw = ImageDraw.Draw(image)

# Defining the English and Turkish text as lists of words.
english_text = "Hello, World! This is a longer English sentence.".split(' ')
turkish_text = "Merhaba, Dünya! Bu daha uzun bir Türkçe cümle.".split(' ')

# Defining a word mapping between English and Turkish.
# Because the order of the word in english is not the same as the order of words in turkish so that way we can get the
# corresponding definition of each english word to turkish
word_mapping = {
    "Hello,": "Merhaba,",
    "World!": "Dünya!",
    "This": "Bu",
    "is": "-",
    "a": "bir",
    "longer": "daha uzun",
    "English": "inglizce",
    "sentence.": "cümle."
}

# Text Color
text_color = (0, 0, 0)  # black

# Calculating the required dimensions for the text -> will be updated later in code as we are positioning word by word
max_width = 0
total_height = 0

# Iterating over the English words to calculate dimensions and positions.
lines = []
lineVerticalSpacing = base_font_size * 3
x, y = 0, 0 # Starting x, y positions
for en_word in english_text:
    # Get the turkish equivalent of the word otherwise "-"
    tr_word_mapped = word_mapping.get(en_word, "-")

    # Calculating the width of each word in English and Turkish. Note that draw.textsize method got deprecated in
    # Pillow 10.0
    # -
    # .textbox method is used to calculate the bounding box of the text when rendered on the image. It
    # takes parameters (0, 0) as the starting coordinates (top-left corner), the en_word as the text to measure,
    # and font=base_font to specify the font to be used.
    # -
    # returns a tuple representing the bounding box of the text.
    # The tuple contains four values (x0, y0, x1, y1), where (x0, y0) are the coordinates of the top-left corner of
    # the bounding box, and (x1, y1) are the coordinates of the bottom-right corner.
    # -
    # [2] at the end of the line accesses the third value of the tuple, which is x1. This represents the x-coordinate
    # of the bottom-right corner of the bounding box.
    # -
    # The tuple contains four values (x0, y0, x1, y1)
    # x0 is the x-coordinate of the top-left corner of the bounding box.
    # y0 is the y-coordinate of the top-left corner of the bounding box.
    # x1 is the x-coordinate of the bottom-right corner of the bounding box.
    # y1 is the y-coordinate of the bottom-right corner of the bounding box.
    en_width = draw.textbbox((0, 0), en_word, font=base_font)[2]
    tr_width = draw.textbbox((0, 0), tr_word_mapped, font=trans_font)[2]
    width = max(en_width, tr_width)     # width of the word

    # Checking if the current word fits within the current line or needs to wrap.
    widthNotIncludingMargin = ((image_width // 3) * 2)
    if x + width > widthNotIncludingMargin:
        x = 0
        y += lineVerticalSpacing

    # Storing the positions and dimensions of each word.
    lines.append((x, y, en_word, tr_word_mapped, width))
    # updating the x position preparing for the next word
    x += width + (base_font_size // 4)
    # updating the max width of the paragraph by comparing to the width of this line. it compares it to every line(word)
    max_width = max(max_width, x)

# Defining the total height as it will be used later to center align the text layout
total_height = y

# Calculating the top left corner that would center the paragraph
start_x = (image_width - max_width) / 2
start_y = (image_height - total_height) / 2

# Drawing the text on the image.
for x, y, en_word, tr_word, width in lines:
    x += start_x
    y += start_y

    # Calculating the offset to center-align the text in each line
    en_offset = (width - draw.textbbox((0, 0), en_word, font=base_font)[2]) / 2
    tr_offset = (width - draw.textbbox((0, 0), tr_word, font=trans_font)[2]) / 2

    # Drawing the English and Turkish text with center alignment and reduced vertical spacing
    draw.text((x + en_offset, y), en_word,
              fill=text_color,
              font=base_font)
    draw.text((x + tr_offset,
               y - (base_font_size - (base_font_size // 4))),
              tr_word,
              fill=text_color,
              font=trans_font)

# Drawing the Turkish sentence at the bottom of the image
trans_bottom_font_size = base_font_size * 2 // 3
trans_bottom_font = ImageFont.truetype("FiraCode-Regular.otf", trans_bottom_font_size)  # replace with your font file

# Wrapping the Turkish sentence into multiple lines to fit within the image width
turkish_sentence_text_wrapped_lines = textwrap.wrap(' '.join(turkish_text),
                                                    width=int(image_width / trans_font_size))

# Calculating the height of each wrapped line.
turkish_sentence_text_wrapped_lines_heights_summation = sum(
    [draw.textbbox((0,
                    line_index * (base_font_size * 2)),  # line spacing
                   line,
                   font=base_font)[3] for line_index,
                                          line in enumerate(turkish_sentence_text_wrapped_lines)])

# Calculating the maximum line width among the wrapped lines
max_line_width = max(
    [draw.textbbox((0, 0), line, font=trans_bottom_font)[2] for line in turkish_sentence_text_wrapped_lines])

# Drawing the wrapped Turkish sentence at the bottom of the image with multiline alignment
draw.multiline_text(((image_width - max_line_width) // 2,
                     image_height - (image_height // 6)),
                    '\n'.join(turkish_sentence_text_wrapped_lines),
                    fill=text_color,
                    font=trans_bottom_font, align="center")

# Saving the image in PNG format.
image.save("image_with_text.png", format="PNG")
