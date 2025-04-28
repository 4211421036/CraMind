import os
import subprocess
import sys
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from language_support import get_language_config
from datetime import datetime
import markdown

def load_model():
    model_name = "Salesforce/codegen-350M-mono"
    tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side="left")
    tokenizer.pad_token = tokenizer.eos_token  # Set pad token
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return model, tokenizer

def generate_code(model, tokenizer, description, language):
    prompt = f"""
    Create a complete {language} program that:
    {description}
    
    Requirements:
    1. Include comments explaining key parts
    2. Use proper indentation and formatting
    3. Include example usage if applicable
    
    Here's the {language} code:
    """
    
    inputs = tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=512)
    
    # Generate with better configuration
    outputs = model.generate(
        inputs,
        max_new_tokens=512,  # Gunakan max_new_tokens bukan max_length
        temperature=0.7,
        do_sample=True,     # Diperlukan untuk temperature
        pad_token_id=tokenizer.eos_token_id,
        attention_mask=inputs.ne(tokenizer.pad_token_id)  # Tambahkan attention mask
    )
    
    code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    code = code.replace(prompt, "").strip()
    return code

def execute_code(code, language_config, filename):
    try:
        output_dir = Path("Output/running")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = output_dir / f"{filename}.{language_config['extension']}"
        with open(file_path, "w") as f:
            f.write(code)
        
        run_cmd = [part.format(file=str(file_path), filename=filename) 
                  for part in language_config['run_command']]
        
        result = subprocess.run(
            " ".join(run_cmd),
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=str(output_dir)
        )
        
        output_path = output_dir / f"{filename}_output.txt"
        with open(output_path, "w") as f:
            f.write(f"Execution at {datetime.now()}\n\n")
            f.write("=== CODE ===\n")
            f.write(code + "\n\n")
            f.write("=== OUTPUT ===\n")
            f.write(result.stdout)
            if result.stderr:
                f.write("\n=== ERRORS ===\n")
                f.write(result.stderr)
        
        return str(output_path), result.stdout, None
        
    except subprocess.CalledProcessError as e:
        error_path = output_dir / f"{filename}_error.txt"
        with open(error_path, "w") as f:
            f.write(f"Error at {datetime.now()}\n\n")
            f.write("=== CODE ===\n")
            f.write(code + "\n\n")
            f.write("=== ERROR OUTPUT ===\n")
            f.write(e.stderr if e.stderr else str(e))
        return str(error_path), None, str(e)

def generate_explanation(code, language, model, tokenizer):
    prompt = f"""
    Explain this {language} code in a way that helps beginners understand:
    
    {code}
    
    Provide the explanation in the following format:
    1. Overall purpose of the code
    2. Breakdown of each major section
    3. Key concepts used
    4. Example of how to modify or extend it
    
    Explanation:
    """
    
    inputs = tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=512)
    
    outputs = model.generate(
        inputs,
        max_new_tokens=512,
        temperature=0.5,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        attention_mask=inputs.ne(tokenizer.pad_token_id)
    
    explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    explanation = explanation.replace(prompt, "").strip()
    
    return explanation

def save_explanation(explanation, filename, language):
    output_dir = Path("Output/explanations")  # Perbaikan typo: explantions -> explanations
    output_dir.mkdir(parents=True, exist_ok=True)
    
    explanation_path = output_dir / f"{filename}_explanation.md"
    with open(explanation_path, "w") as f:
        f.write(f"# Code Explanation: {filename}.{language}\n\n")
        f.write(explanation)
    
    html_path = output_dir / f"{filename}_explanation.html"
    with open(html_path, "w") as f:
        html = markdown.markdown(explanation)
        f.write(f"<html><body><h1>CraMind Explanation</h1>{html}</body></html>")
    
    return str(explanation_path)

def main():
    description = os.getenv("INPUT_DESCRIPTION")
    language = os.getenv("INPUT_LANGUAGE", "python")
    filename = os.getenv("INPUT_FILENAME", "generated_code")
    generate_explanation_flag = os.getenv("INPUT_EXPLAIN", "true").lower() == "true"
    
    model, tokenizer = load_model()
    language_config = get_language_config(language)
    
    code = generate_code(model, tokenizer, description, language)
    
    output_path, execution_output, error = execute_code(code, language_config, filename)
    
    explanation_path = None
    if generate_explanation_flag:
        explanation = generate_explanation(code, language, model, tokenizer)
        explanation_path = save_explanation(explanation, filename, language_config['extension'])
    
    print(f"::set-output name=code_path::Output/running/{filename}.{language_config['extension']}")
    print(f"::set-output name=output_path::{output_path}")
    if explanation_path:
        print(f"::set-output name=explanation_path::{explanation_path}")
    
    if error:
        sys.exit(1)

if __name__ == "__main__":
    main()
