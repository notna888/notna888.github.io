# A basic script thrown together to convert my old pelican blog files to something I can use with zola

# You can find my zola blog at notna888.com

import os
import re

def get_all_md_files():
    all_md_files = [filename for filename in os.listdir() if filename.endswith('.md')]
    return all_md_files


def extract_front_matter(filename):
    with open(filename, 'r') as infile:
        in_frontmatter = True
        front_matter_rows = list()
        rest_of_post = list()

        regex_pattern = "^([\w]+):"

        for line in infile.readlines():
            line_is_front_matter = re.match(regex_pattern, line)
            if line_is_front_matter is None:
                in_frontmatter = False
            
            if in_frontmatter:
                front_matter_rows.append(line)
            else:
                rest_of_post.append(line)
    return front_matter_rows, rest_of_post


def convert_pelican_frontmatter_to_zola(front_matter_rows, timezone_offset="+08:00"):
    '''
    Converts a list of Pelican markdown front matter rows (e.g., "Field: Value") 
    into a Zola-compatible TOML front matter string.

    Special Handling:
    - 'Date': Converts "YYYY-MM-DD HH:MM" to "YYYY-MM-DDTHH:MM:00+TZ" 
      (e.g., '2018-12-02 21:50' -> '2018-12-02T21:50:00+08:00').
    - Other fields: Converts 'Field: Value' to 'field = "Value"' and 
      lower-cases the field name.

    Args:
        front_matter_rows: A list of strings, each representing a row of Pelican front matter.
        timezone_offset: The UTC offset to append to the date string (default is "+08:00").

    Returns:
        A string containing the Zola TOML front matter block.
    '''
    zola_toml = "+++\n"  # Zola TOML starts and ends with "+++"
    
    # Define common fields that should be converted to lowercase keys and string values
    string_fields = [
        'title', 'slug', 'author', 'summary', 'keywords', 'status', 'modified',
    ]

    for row in front_matter_rows:
        # Use a more robust regex to handle potential leading/trailing whitespace 
        # that might be present in the extracted rows.
        # It captures the field name and everything after the colon as the value.
        match = re.match(r"^\s*([\w]+):\s*(.*)\s*$", row)
        
        if not match:
            # Skip rows that don't match the expected "Field: Value" format
            continue

        pelican_key, pelican_value = match.groups()
        pelican_key = pelican_key.strip()
        pelican_value = pelican_value.strip()

        zola_key = pelican_key.lower()
        
        # --- Date Conversion ---
        if zola_key == 'date':            
            # Use regex to ensure the date format is correct before manipulation
            date_match = re.match(r"(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})", pelican_value)

            if date_match:
                date_part, time_part = date_match.groups()
                # date_part YYYY-MM-DD
                # time_part HH:MM
                
                zola_value = f"{date_part}T{time_part}:00{timezone_offset}"
                # YYYY-MM-DDTHH:MM:00+08:00
                
                zola_toml += f"date = {zola_value}\n"
            else:
                # worst case scenario, leave just convert it to lowercase basically
                zola_toml += f'date = "{pelican_value}"\n'
                
        elif zola_key in ['tags', 'category']:
            # convert to a toml list
                    
            # Split by comma (for tags) or treat as a single item (for category), 
            # strip whitespace, and quote each item.
            items = []
            if pelican_key == 'Tags':
                items = [f'"{item.strip()}"' for item in pelican_value.split(',') if item.strip()]
            elif pelican_key == 'Category':
                 if pelican_value:
                    zola_key = 'categories'
                    items = [f'"{pelican_value}"']

            if items:
                zola_toml += f"{zola_key} = [{', '.join(items)}]\n"

        elif zola_key in string_fields:
            # could probably delete this part, kept it for checking lol
            clean_value = pelican_value.replace('"', '\\"') 
            zola_toml += f'{zola_key} = "{clean_value}"\n'
            
        # Other Fields
        else:
            clean_value = pelican_value.replace('"', '\\"') 
            zola_toml += f'{zola_key} = "{clean_value}"\n'

    zola_toml += "+++\n"
    
    return zola_toml

def main():
    all_md_files = get_all_md_files()
    for filename in all_md_files:
        print(f'Doing {filename}...')
        front_matter_rows, rest_of_post = extract_front_matter(filename)

        zola_frontmatter_text = convert_pelican_frontmatter_to_zola(front_matter_rows)

        os.makedirs('converted', exist_ok=True)

        with open(f'converted/{filename}', 'w') as outfile:
            outfile.write(zola_frontmatter_text)
            outfile.writelines(rest_of_post)
        # breakpoint()





if __name__ == '__main__':
    main()
