def generate(input_ids, vmap, tokenizer, model, base_model_name, max_new_tokens: int = 100, penalty_alpha: float = 0.6, top_k: int = 4):
    attention_mask = input_ids.ne(tokenizer.pad_token_id)
    
    predictions = model.generate(input_ids = input_ids,
                                  attention_mask =  attention_mask,
                   max_new_tokens = max_new_tokens,
                   penalty_alpha = penalty_alpha,
                   top_k = top_k,
                   eos_token_id = tokenizer.eos_token_id)
    prediction = tokenizer.batch_decode(predictions.cpu().numpy())[0]
    if 'bloom' in base_model_name:
        obfuscated_code, prediction, *_ = prediction.replace('<s>', '').replace('</s>','').split('Output')
        new_code = obfuscated_code
    elif 'codet5' in base_model_name:
        start_pos = prediction.find('var0')
        prediction = prediction[start_pos:].replace('</s>', '')
        new_code = tokenizer.decode(input_ids[0]).replace('<s>', '').replace('</s>', '')
    pred_coms = prediction.split()
    new_vmap = {}
    for i in range(len(pred_coms) // 3):
        key, _, value = pred_coms[3 * i: 3 * i + 3]
        if value.startswith('var') or value.startswith('$var'): continue
        new_vmap[key] = value
    vmap.update(new_vmap)
    for key, value in vmap.items():
        new_code = new_code.replace(key, value)
    return new_code