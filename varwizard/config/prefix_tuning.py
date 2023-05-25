from peft import get_peft_config, get_peft_model, PrefixTuningConfig, TaskType

def get_prefix_tuning_config(base_model_name):

    if base_model_name == 'bloom_560m':
        peft_config = PrefixTuningConfig(
                task_type = TaskType.CAUSAL_LM,
                inference_mode = False, 
                encoder_hidden_size = 1024,
                prefix_projection = True,
                num_virtual_tokens = 30
            )
    elif base_model_name == 'codet5_base':
        peft_config = PrefixTuningConfig(
                task_type = TaskType.SEQ_2_SEQ_LM,
                inference_mode = False, 
                encoder_hidden_size = 768,
                prefix_projection = True,
                num_virtual_tokens = 15
            )
    return peft_config