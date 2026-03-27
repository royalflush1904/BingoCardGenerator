# Bingo Card Generator

Generate Bingo cards as PNG images for social gatherings. Supports both integer grids and custom text content.

## Origin

This project was created for a friend's bachelor party. The idea: whenever someone does something stupid or memorable, the group shouts "BINGO!" and checks if they have a winning row. It's a social game designed to make good moments even better - and to keep things interesting when things get rowdy.

## Usage

```bash
# Generate integer bingo cards (5x5 default)
python3 bingo_generator.py -p 5 -t integers

# Generate quote-based bingo cards
python3 bingo_generator.py -p 3 -t quotes -i quotes.txt

# Custom grid size (e.g., 4x4)
python3 bingo_generator.py -p 5 -t quotes -i quotes.txt -g 4

# Allow duplicate quotes on a single card
python3 bingo_generator.py -p 3 -t quotes -i quotes.txt -d
```

### Parameters

| Flag | Description | Default |
|------|-------------|---------|
| `-p, --players` | Number of bingo cards to generate | Required |
| `-t, --type` | Content type: `integers` or `quotes` | `quotes` |
| `-i, --inputfile` | Path to quotes file (newline-separated) | `quotes.txt` |
| `-o, --output-dir` | Output directory for PNG files | Current directory |
| `-g, --grid-size` | Grid size (NxN, e.g., 4 for 4x4) | `5` |
| `-d, --duplicates` | Allow duplicate quotes on a card | `False` |

## Installation

```bash
pip install Pillow>=10.0.0
```

## Creating Quotes

Create a `quotes.txt` file with one quote per line:

```
First drink of the night
Falls asleep before midnight
Tells an embarrassing story
Starts a chant
Challenges someone to a duel
```

## How to Play

1. Generate cards for each participant
2. Distribute the cards
3. When someone does something worth noting, everyone checks their card
4. First to get a row (horizontal, vertical, or diagonal) shouts "BINGO!"
5. Verify and celebrate (or roast) accordingly
