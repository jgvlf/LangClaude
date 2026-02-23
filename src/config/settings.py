"""Configuration settings for the due diligence workflow."""

# Model name mappings - short names to full IDs
MODEL_MAPPING = {
    "haiku": "lfm2.5-thinking:1.2b",
    "sonnet": "lfm2.5-thinking:1.2b",
    "opus": "lfm2.5-thinking:1.2b",
    # Also allow full names
    "claude-haiku-4-5-20251001": "lfm2.5-thinking:1.2b",
    "claude-sonnet-4-20250514": "lfm2.5-thinking:1.2b",
    "claude-opus-4-5-20251101": "lfm2.5-thinking:1.2b",
}


def get_model_id(model_name: str) -> str:
    """Get the full model ID from a short name.
    
    Args:
        model_name: Short name like 'haiku', 'sonnet', 'opus' or full ID
    
    Returns:
        Full model ID string
    """
    return MODEL_MAPPING.get(model_name, model_name)