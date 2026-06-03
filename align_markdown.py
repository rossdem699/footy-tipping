#!/usr/bin/env python3
import sys
import re

def format_separator(cell, width):
    cell = cell.strip()
    left_align = cell.startswith(':')
    right_align = cell.endswith(':')
    
    if left_align and right_align:
        if width >= 2:
            return ':' + '-' * (width - 2) + ':'
        else:
            return ':-:'
    elif left_align:
        return ':' + '-' * (width - 1)
    elif right_align:
        return '-' * (width - 1) + ':'
    else:
        return '-' * width

def align_tables(text):
    lines = text.splitlines()
    output = []
    
    in_table = False
    table_rows = []
    
    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            return
        
        # Parse table cells
        parsed_rows = []
        for line in table_rows:
            content = line.strip()
            if content.startswith('|'):
                content = content[1:]
            if content.endswith('|'):
                content = content[:-1]
            
            cells = [c.strip() for c in content.split('|')]
            parsed_rows.append(cells)
            
        # Determine number of columns
        num_cols = max(len(row) for row in parsed_rows) if parsed_rows else 0
        
        # Pad shorter rows if any
        for row in parsed_rows:
            while len(row) < num_cols:
                row.append("")
                
        # Calculate max column widths
        col_widths = [0] * num_cols
        for row_idx, row in enumerate(parsed_rows):
            is_sep = all(re.match(r'^:?-+:?$', c) for c in row if c)
            if is_sep:
                continue
            for col_idx, cell in enumerate(row):
                col_widths[col_idx] = max(col_widths[col_idx], len(cell))
                
        # Reconstruct table
        for row_idx, row in enumerate(parsed_rows):
            is_sep = all(re.match(r'^:?-+:?$', c) for c in row if c)
            new_cells = []
            for col_idx, cell in enumerate(row):
                width = max(col_widths[col_idx], 3)
                if is_sep:
                    new_cells.append(format_separator(cell, width))
                else:
                    new_cells.append(f"{cell:<{width}}")
            output.append("| " + " | ".join(new_cells) + " |")
            
        table_rows = []
        in_table = False

    for line in lines:
        is_table_line = line.strip().startswith('|')
        
        if is_table_line:
            in_table = True
            table_rows.append(line)
        else:
            if in_table:
                flush_table()
            output.append(line)
            
    if in_table:
        flush_table()
        
    return "\n".join(output)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            print(align_tables(content))
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        content = sys.stdin.read()
        print(align_tables(content))
