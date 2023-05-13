def generate(input_ids, tokenizer, model, max_length: int = 505, penalty_alpha: float = 0.6, top_k: int = 4):
    attention_mask = input_ids.ne(tokenizer.pad_token_id)
    predictions = model.generate(input_ids = input_ids,
                                  attention_mask =  attention_mask,
                   max_length = max_length,
                   penalty_alpha = penalty_alpha,
                   top_k = top_k,
                   eos_token_id = tokenizer.eos_token_id)
    prediction = tokenizer.batch_decode(predictions.cpu().numpy())[0]
    obfuscated_code, prediction = prediction.replace('<s>', '').replace('</s>','').split('Output')
    pred_coms = prediction.split()
    new_code = obfuscated_code
    for i in range(len(pred_coms) // 3):
        key, _, value = pred_coms[3 * i: 3 * i + 3]
        new_code = new_code.replace(key, value)
    return new_code