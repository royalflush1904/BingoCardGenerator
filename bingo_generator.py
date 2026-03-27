#!/usr/bin/env python3
import argparse
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


class BingoCard:
    FREE_SPACE = "FREE"
    
    def __init__(self, content: list[str], card_id: int):
        self.content = content
        self.card_id = card_id
        self.grid = self._create_grid()
    
    def _create_grid(self) -> list[list[str]]:
        random.shuffle(self.content)
        grid = []
        index = 0
        for _ in range(5):
            row = []
            for col in range(5):
                if row == [] and col == 2:
                    row.append(self.FREE_SPACE)
                else:
                    row.append(self.content[index])
                    index += 1
            grid.append(row)
        return grid
    
    def save_as_png(self, output_path: Path, font_size: int = 20):
        cell_size = 150
        padding = 5
        card_size = cell_size * 5
        
        img = Image.new("RGB", (card_size, card_size), "white")
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except (OSError, IOError):
            font = ImageFont.load_default()
        
        for row in range(5):
            for col in range(5):
                x1 = col * cell_size + padding
                y1 = row * cell_size + padding
                x2 = (col + 1) * cell_size - padding
                y2 = (row + 1) * cell_size - padding
                
                draw.rectangle([x1, y1, x2, y2], outline="black", width=2)
                
                text = self.grid[row][col]
                
                if text == self.FREE_SPACE:
                    draw.rectangle([x1, y1, x2, y2], fill="#D3D3D3")
                
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                x_text = x1 + (x2 - x1 - text_width) // 2
                y_text = y1 + (y2 - y1 - text_height) // 2
                
                max_chars = 15
                if len(text) > max_chars:
                    mid = len(text) // 2
                    split_idx = text.rfind(" ", 0, mid + 5)
                    if split_idx == -1:
                        split_idx = mid
                    
                    line1 = text[:split_idx]
                    line2 = text[split_idx:].strip()
                    
                    if len(line1) > max_chars:
                        line1 = line1[:max_chars]
                    if len(line2) > max_chars:
                        line2 = line2[:max_chars]
                    
                    bbox1 = draw.textbbox((0, 0), line1, font=font)
                    bbox2 = draw.textbbox((0, 0), line2, font=font)
                    
                    text_width = max(bbox1[2] - bbox1[0], bbox2[2] - bbox2[0])
                    total_height = (bbox1[3] - bbox1[1]) + (bbox2[3] - bbox2[1]) + 5
                    
                    x_text = x1 + (x2 - x1 - text_width) // 2
                    y_text = y1 + (y2 - y1 - total_height) // 2
                    
                    draw.text((x_text, y_text), line1, fill="black", font=font)
                    draw.text((x_text, y_text + (bbox1[3] - bbox1[1]) + 5), line2, fill="black", font=font)
                else:
                    draw.text((x_text, y_text), text, fill="black", font=font)
        
        img.save(output_path, "PNG")


def generate_integers(count: int) -> list[str]:
    numbers = list(range(101))
    if count > 101:
        numbers = numbers * ((count // 101) + 1)
    random.shuffle(numbers)
    return [str(n) for n in numbers[:count]]


def load_quotes(filepath: Path, count: int) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        quotes = [line.strip() for line in f if line.strip()]
    
    if len(quotes) < count:
        quotes = quotes * ((count // len(quotes)) + 1)
    
    selected = random.sample(quotes, min(count, len(quotes)))
    return selected


def main():
    parser = argparse.ArgumentParser(description="Generate Bingo Cards")
    parser.add_argument("-p", "--players", type=int, required=True, help="Number of players (number of bingo cards to generate)")
    parser.add_argument("-t", "--type", choices=["integers", "quotes"], default="quotes", help="Content type for the cards (default: quotes)")
    parser.add_argument("-i", "--inputfile", type=str, default="quotes.txt", help="Path to text file with quotes (default: quotes.txt)")
    parser.add_argument("-o", "--output-dir", type=str, default=str(Path.cwd()), help="Output directory for PNG files (default: current working directory)")
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    content_count = args.players * 24
    
    if args.type == "integers":
        content = generate_integers(content_count)
    else:
        input_path = Path(args.inputfile)
        if not input_path.exists():
            print(f"Error: Input file '{input_path}' not found")
            return 1
        content = load_quotes(input_path, content_count)
    
    for i in range(args.players):
        card = BingoCard(content.copy(), i + 1)
        output_path = output_dir / f"bingo_card_{i + 1}.png"
        card.save_as_png(output_path)
        print(f"Generated: {output_path}")
    
    print(f"\nSuccessfully generated {args.players} Bingo cards in '{output_dir}'")
    return 0


if __name__ == "__main__":
    exit(main())
