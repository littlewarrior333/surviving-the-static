
import json
import os
from pathlib import Path

GLOSSARY_PATH = Path(__file__).parent / "glossary.json"

def load_glossary():
    if not GLOSSARY_PATH.exists():
        return {}
    with open(GLOSSARY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_glossary(data):
    with open(GLOSSARY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def translate_error(error_text: str) -> str:
    """Translates a raw technical error into plain, friendly terms."""
    glossary = load_glossary()
    key = error_text.strip().upper()
    
    errors = glossary.get("errors", {})
    if key in errors:
        err_data = errors[key]
        return f"**{err_data.get('title')}**\n\n{err_data.get('explanation')}\n\n*Next Step:* {err_data.get('next_step')}"
        
    terms = glossary.get("terms", {})
    for term, explanation in terms.items():
        if term.lower() in error_text.strip().lower():
            return f"**Plain English Definition ({term.title()}):** {explanation}"
            
    return f"I haven't logged '{error_text}' in our living guide yet, but let's add it so nobody else has to guess!"

def add_new_term(term: str, explanation: str) -> str:
    """Adds a new error or term to the living glossary permanently."""
    glossary = load_glossary()
    if "terms" not in glossary:
        glossary["terms"] = {}
    glossary["terms"][term.strip().lower()] = explanation
    save_glossary(glossary)
    return f"Successfully added '{term}' to the Surviving the Static living document!"

def register(ctx):
    ctx.register_tool(
        toolset="surviving-the-static",
        name="translate_error",
        schema={
            "description": "Translates a raw technical error into plain, friendly terms.",
            "parameters": {
                "type": "object",
                "properties": {
                    "error_text": {
                        "type": "string",
                        "description": "The raw error code or text to translate"
                    }
                },
                "required": ["error_text"]
            }
        },
        handler=translate_error
    )
    ctx.register_tool(
        toolset="surviving-the-static",
        name="add_new_term",
        schema={
            "description": "Adds a new error or term to the living glossary permanently.",
            "parameters": {
                "type": "object",
                "properties": {
                    "term": {
                        "type": "string",
                        "description": "The term or error code to add"
                    },
                    "explanation": {
                        "type": "string",
                        "description": "The friendly explanation"
                    }
                },
                "required": ["term", "explanation"]
            }
        },
        handler=add_new_term
    )