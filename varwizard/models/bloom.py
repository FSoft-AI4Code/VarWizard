from transformers import BloomForCausalLM, BloomTokenizerFast

def get_tokenizer_and_model(model_name):
    tokenizer = BloomTokenizerFast.from_pretrained(model_name)
    model = BloomForCausalLM.from_pretrained(model_name)
    return tokenizer, model
