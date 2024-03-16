# Hear The Flag

## Challenge Description
Relax. Breath. Hear. Enjoy!

## Solution
1. Visit the YouTube link provided in the challenge: [https://youtu.be/yGL5YZUINq8](https://youtu.be/yGL5YZUINq8)
2. Listen to the music and observe the AI-generated video clips.
3. In the video description, find the Python code that generates a MIDI file based on a base-7 encoded string.
4. Using a tool like [ChordAI](https://www.chordai.net), recognize the chord progression used in the music.
5. Write down the chord progression using the following notation:
  - C: 0
  - Dm: 1
  - Em: 2
  - F: 3
  - G: 4
  - Am: 5
  - Bdim: 6
6. Write a reverse script to decode the base-7 string and obtain the flag.

Here's the reverse script in Python:

```python
def base_7_to_text(base_7_string):
   text_as_int = 0
   for digit in base_7_string:
       text_as_int = text_as_int * 7 + int(digit)
   return text_as_int.to_bytes((text_as_int.bit_length() + 7) // 8, 'big').decode()

chord_progression = "0222543045222543045...."
flag = base_7_to_text(chord_progression)
print(flag)
```

The script takes the chord progression as input, where each chord is represented by a digit from 0 to 6. It then converts the base-7 string back to an integer and decodes it into the original text.

### Music Theory Explanation
In music theory, a scale is a set of musical notes ordered by fundamental frequency or pitch. The C Major scale consists of the following notes: C, D, E, F, G, A, B. Each note in the scale can be used as the root note to form a chord.

The chords used in the challenge are:
- C (0): C, E, G
- Dm (1): D, F, A
- Em (2): E, G, B
- F (3): F, A, C
- G (4): G, B, D
- Am (5): A, C, E
- Bdim (6): B, D, F

By recognizing the chord progression in the music, we can obtain the base-7 encoded string and decode it to retrieve the flag.

Flag: `1753c{I_w4nna_r0cK}`

### Conclusion

The "Hear The Flag" challenge combines music and encoding to hide the flag. By analyzing the music and recognizing the chord progression, the base-7 encoded string can be obtained. The challenge also provides the encoding script in the video description, which can be reversed to decode the flag. 
