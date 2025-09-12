import re
import json
import os
import glob

latex_file_path = 'C:/Users/nussis/Putnam_Practice_Site/backend/tex_files/'
output_dir = "JSON_solutions"
domain = "Putnam"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

pattern = re.compile(r"\\item\[(.*?)\](.*?)(?=\\item\[|\\end{itemize\})", re.DOTALL)

tex_files = glob.glob(os.path.join(latex_file_path, "*.tex"))

for tex_file in tex_files:
    with open(tex_file, 'r', encoding="utf-8") as f:
        content = f.read()
    matches = pattern.findall(content)
    year = (os.path.basename(tex_file)).removesuffix('s.tex')
    for label, solution_text in matches:
        question_num = label[1:].replace('-', '')
        problem_id = f"{year}_{label}"

        json_object = {
            "year": year,
            "question_number": question_num,
            "domain": domain,
            "statement": "",
            "solution": [
                {
                    "hint_level": 0,
                    "content": solution_text.strip()
                }
            ]
        }

        filename = os.path.join(output_dir, f"{problem_id}.json")
        with open(filename, "w", encoding='utf-8') as json_file:
            json.dump(json_object, json_file, indent = 2, ensure_ascii=False)

        print(f"Saved solution for {label} from file {os.path.basename(tex_file)}")
