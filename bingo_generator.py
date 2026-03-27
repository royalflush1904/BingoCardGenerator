#!/usr/bin/env python3
import argparse
import random
from pathlib import Path
from typing import Any, Union
from PIL import Image, ImageDraw, ImageFont


class BingoCard:
    IMAGE_SIZE = 1200
    
    def __init__(self, content: list[str], card_id: int, grid_size: int = 5):
        self.content = content
        self.card_id = card_id
        self.grid_size = grid_size
        self.grid = self._create_grid()
    
    def _create_grid(self) -> list[list[str]]:
        random.shuffle(self.content)
        grid = []
        index = 0
        
        for row in range(self.grid_size):
            row_content = []
            for col in range(self.grid_size):
                row_content.append(self.content[index])
                index += 1
            grid.append(row_content)
        return grid
    
    def save_as_png(self, output_path: Path):
        cell_size = self.IMAGE_SIZE // self.grid_size
        padding = 8
        card_size = self.IMAGE_SIZE
        
        img = Image.new("RGB", (card_size, card_size), "white")
        draw = ImageDraw.Draw(img)
        
        max_font_size = 20
        min_font_size = 8
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * cell_size + padding
                y1 = row * cell_size + padding
                x2 = (col + 1) * cell_size - padding
                y2 = (row + 1) * cell_size - padding
                
                draw.rectangle([x1, y1, x2, y2], outline="black", width=2)
                
                text = self.grid[row][col]
                cell_width = x2 - x1
                cell_height = y2 - y1
                
                font_size = max_font_size
                font = None
                lines = []
                while font_size >= min_font_size:
                    try:
                        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
                    except (OSError, IOError):
                        font = ImageFont.load_default()
                    
                    lines = self._wrap_text(draw, text, font, cell_width)
                    total_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines) + (len(lines) - 1) * 3
                    
                    if self._text_fits(draw, lines, font, cell_width, cell_height):
                        break
                    font_size -= 1
                
                if font is None or (lines and not self._text_fits(draw, lines, font, cell_width, cell_height)):
                    font_size = min_font_size
                    try:
                        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
                    except (OSError, IOError):
                        font = ImageFont.load_default()
                    lines = self._wrap_text(draw, text, font, cell_width)
                
                self._draw_wrapped_text(draw, lines, font, x1, y1, cell_width, cell_height)
        
        img.save(output_path, "PNG")
    
    def _wrap_text(self, draw: ImageDraw.ImageDraw, text: str, font: Any, max_width: int) -> list[str]:
        words = text.split()
        if not words:
            return [""]
        
        lines = []
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            test_width = bbox[2] - bbox[0]
            
            if test_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines if lines else [""]
    
    def _text_fits(self, draw: ImageDraw.ImageDraw, lines: list[str], font: Any, cell_width: int, cell_height: int) -> bool:
        total_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines) + (len(lines) - 1) * 3
        max_line_width = max(draw.textbbox((0, 0), line, font=font)[2] for line in lines)
        return max_line_width <= cell_width and total_height <= cell_height
    
    def _draw_wrapped_text(self, draw: ImageDraw.ImageDraw, lines: list[str], font: Any, x1: int, y1: int, cell_width: int, cell_height: int):
        line_heights = [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
        total_height = sum(line_heights) + (len(lines) - 1) * 3
        
        y_offset = y1 + (cell_height - total_height) // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x_offset = x1 + (cell_width - text_width) // 2
            draw.text((x_offset, y_offset), line, fill="black", font=font)
            y_offset += line_heights[i] + 3


def generate_integers(count: int) -> list[str]:
    numbers = list(range(101))
    if count > 101:
        numbers = numbers * ((count // 101) + 1)
    random.shuffle(numbers)
    return [str(n) for n in numbers[:count]]


def load_quotes(filepath: Path, count: int, allow_duplicates: bool = False) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        quotes = [line.strip() for line in f if line.strip()]
    
    if len(quotes) < count and not allow_duplicates:
        raise ValueError(f"Not enough unique quotes ({len(quotes)}) to fill the card without duplicates. Need at least {count} quotes.")
    
    if len(quotes) < count:
        quotes = quotes * ((count // len(quotes)) + 1)
    
    selected = random.sample(quotes, min(count, len(quotes)))
    return selected


def distribute_quotes_evenly(quotes: list[str], num_cards: int, cells_per_card: int) -> list[list[str]]:
    total_cells_needed = num_cards * cells_per_card
    
    if len(quotes) < total_cells_needed:
        repeats_needed = (total_cells_needed // len(quotes)) + 1
        extended_quotes = quotes * repeats_needed
    else:
        extended_quotes = quotes[:]
    
    random.shuffle(extended_quotes)
    
    cards_content = [[] for _ in range(num_cards)]
    
    for i, quote in enumerate(extended_quotes[:total_cells_needed]):
        card_index = i % num_cards
        cards_content[card_index].append(quote)
    
    for card_content in cards_content:
        random.shuffle(card_content)
    
    return cards_content


def main():
    parser = argparse.ArgumentParser(description="Generate Bingo Cards")
    parser.add_argument("-p", "--players", type=int, required=True, help="Number of players (number of bingo cards to generate)")
    parser.add_argument("-t", "--type", choices=["integers", "quotes"], default="quotes", help="Content type for the cards (default: quotes)")
    parser.add_argument("-i", "--inputfile", type=str, default="quotes.txt", help="Path to text file with quotes (default: quotes.txt)")
    parser.add_argument("-o", "--output-dir", type=str, default=str(Path.cwd()), help="Output directory for PNG files (default: current working directory)")
    parser.add_argument("-g", "--grid-size", type=int, default=5, help="Grid size (NxN, e.g., 4 for 4x4, 5 for 5x5, default: 5)")
    parser.add_argument("-d", "--duplicates", action="store_true", help="Allow duplicate quotes on a single card (default: False)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print all parameters before generating (default: False)")
    
    args = parser.parse_args()
    
    if args.verbose:
        print("Parameters:")
        print(f"  -p, --players   | required=True  | int    | Number of bingo cards to generate")
        print(f"  -t, --type      | required=False | str    | Content type (choices: integers, quotes), default: quotes")
        print(f"  -i, --inputfile | required=False | str    | Path to quotes file, default: quotes.txt")
        print(f"  -o, --output-dir| required=False | str    | Output directory, default: {Path.cwd()}")
        print(f"  -g, --grid-size | required=False | int    | Grid size (NxN), default: 5")
        print(f"  -d, --duplicates| required=False | bool   | Allow duplicates (action=store_true), default: False")
        print(f"  -v, --verbose   | required=False | bool   | Print parameters (action=store_true), default: False")
        print()
        print("Current values:")
        print(f"  --players    = {args.players}")
        print(f"  --type       = {args.type}")
        print(f"  --inputfile  = {args.inputfile}")
        print(f"  --output-dir = {args.output_dir}")
        print(f"  --grid-size  = {args.grid_size}")
        print(f"  --duplicates = {args.duplicates}")
        print(f"  --verbose    = {args.verbose}")
        print()
    
    if args.grid_size < 2:
        print("Error: Grid size must be at least 2")
        return 1
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for png_file in output_dir.glob("bingo_card_*.png"):
        png_file.unlink()
    
    cells_needed = args.grid_size * args.grid_size
    
    if args.type == "integers":
        content = generate_integers(cells_needed)
        cards_content = [content.copy() for _ in range(args.players)]
        for card_content in cards_content:
            random.shuffle(card_content)
    else:
        input_path = Path(args.inputfile)
        if not input_path.exists():
            print(f"Error: Input file '{input_path}' not found")
            return 1
        try:
            all_quotes = load_quotes(input_path, cells_needed, args.duplicates)
            cards_content = distribute_quotes_evenly(all_quotes, args.players, cells_needed)
        except ValueError as e:
            print(f"Error: {e}")
            return 1
    
    for i in range(args.players):
        card = BingoCard(cards_content[i], i + 1, args.grid_size)
        output_path = output_dir / f"bingo_card_{i + 1}.png"
        card.save_as_png(output_path)
        print(f"Generated: {output_path}")
    
    print(f"\nSuccessfully generated {args.players} {args.grid_size}x{args.grid_size} Bingo cards in '{output_dir}'")
    return 0


if __name__ == "__main__":
    exit(main())
