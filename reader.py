from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re

##########################################
# 1. Model Setup
##########################################

# Determine the computation device (use GPU if available, otherwise CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Define the model name and load the slow tokenizer to avoid compatibility issues.
model_name = "jinaai/ReaderLM-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

# Load the ReaderLM-v2 model and move it to the appropriate device.
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

##########################################
# 2. HTML Cleaning Functions
##########################################

# Regular expression patterns for removing unwanted HTML elements.
SCRIPT_PATTERN = r"<[ ]*script.*?\/[ ]*script[ ]*>"
STYLE_PATTERN = r"<[ ]*style.*?\/[ ]*style[ ]*>"
META_PATTERN = r"<[ ]*meta.*?>"
COMMENT_PATTERN = r"<[ ]*!--.*?--[ ]*>"
LINK_PATTERN = r"<[ ]*link.*?>"
BASE64_IMG_PATTERN = r'<img[^>]+src="data:image/[^;]+;base64,[^"]+"[^>]*>'
SVG_PATTERN = r"(<svg[^>]*>)(.*?)(<\/svg>)"

def replace_svg(html: str, new_content: str = "this is a placeholder") -> str:
    """Replace SVG content with a placeholder."""
    return re.sub(
        SVG_PATTERN,
        lambda match: f"{match.group(1)}{new_content}{match.group(3)}",
        html,
        flags=re.DOTALL,
    )

def replace_base64_images(html: str, new_image_src: str = "#") -> str:
    """Replace base64 images with a placeholder image source."""
    return re.sub(
        BASE64_IMG_PATTERN,
        f'<img src="{new_image_src}"/>',
        html,
    )

def clean_html(html: str, clean_svg: bool = False, clean_base64: bool = False) -> str:
    """
    Clean HTML content by removing scripts, styles, metadata, comments, and links.
    Optionally replace SVG content and base64 images.
    """
    html = re.sub(SCRIPT_PATTERN, "", html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    html = re.sub(STYLE_PATTERN, "", html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    html = re.sub(META_PATTERN, "", html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    html = re.sub(COMMENT_PATTERN, "", html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    html = re.sub(LINK_PATTERN, "", html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    if clean_svg:
        html = replace_svg(html)
    if clean_base64:
        html = replace_base64_images(html)
    return html

##########################################
# 3. Prompt Creation Functions
##########################################

def create_conversion_prompt(text: str, instruction: str = None, schema: str = None) -> str:
    """
    Create a prompt for HTML conversion.
    By default, instructs the model to convert HTML to Markdown and output only the final markdown text.
    """
    if not instruction:
        instruction = (
            "Extract the main content from the given HTML and convert it to Markdown format. "
            "Output only the resulting markdown without repeating the HTML or instructions."
        )
    if schema:
        # For JSON output, adjust the instruction and include the schema.
        instruction = (
            "Extract the specified information from the HTML and present it as structured JSON. "
            "Output only the JSON result."
        )
        prompt = (
            f"{instruction}\n```html\n{text}\n```\n"
            f"The JSON schema is as follows:\n```json\n{schema}\n```\nOutput:\n"
        )
    else:
        prompt = f"{instruction}\n```html\n{text}\n```\nOutput:\n"
    return prompt

def create_summary_prompt(text: str) -> str:
    """
    Create a prompt for summarization.
    Instructs the model to summarize the text and output only the summary.
    """
    instruction = "Summarize the following text in a concise paragraph. Output only the summary."
    prompt = f"{instruction}\n```\n{text}\n```\nSummary:\n"
    return prompt

##########################################
# 4. HTML Conversion Function
##########################################

def convert_html(input_html: str, max_new_tokens: int = 1024, temperature: float = 0.7, repetition_penalty: float = 1.08) -> str:
    """
    Convert raw HTML into formatted Markdown using ReaderLM-v2.
    
    Parameters:
      - input_html: Raw HTML content to convert.
      - max_new_tokens: Maximum number of tokens to generate.
      - temperature: Controls generation randomness.
      - repetition_penalty: Penalizes repetitive outputs.
    
    Returns:
      - The formatted Markdown output.
    """
    cleaned_html = clean_html(input_html)
    prompt = create_conversion_prompt(cleaned_html)
    print("Conversion Prompt Created:\n", prompt)
    
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
    print("Tokenized input shape:", inputs.shape)
    
    attention_mask = None
    if tokenizer.pad_token_id is not None:
        attention_mask = inputs.ne(tokenizer.pad_token_id)
    
    outputs = model.generate(
        inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_p=0.95,
        top_k=50,
        repetition_penalty=repetition_penalty,
        attention_mask=attention_mask
    )
    print("Raw model output:", outputs)
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result

##########################################
# 5. Summarization Function
##########################################

def summarize_text(input_text: str, max_new_tokens: int = 150, temperature: float = 0.7, repetition_penalty: float = 1.08) -> str:
    """
    Summarize the provided text using ReaderLM-v2.
    
    Parameters:
      - input_text: Text to be summarized.
      - max_new_tokens: Maximum tokens for the summary.
      - temperature: Controls generation randomness.
      - repetition_penalty: Penalizes repetitive outputs.
    
    Returns:
      - A concise summary.
    """
    prompt = create_summary_prompt(input_text)
    print("Summary Prompt Created:\n", prompt)
    
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
    print("Tokenized summary input shape:", inputs.shape)
    
    attention_mask = None
    if tokenizer.pad_token_id is not None:
        attention_mask = inputs.ne(tokenizer.pad_token_id)
    
    outputs = model.generate(
        inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_p=0.95,
        top_k=50,
        repetition_penalty=repetition_penalty,
        attention_mask=attention_mask
    )
    print("Raw summary model output:", outputs)
    
    summary_result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary_result
