from varwizard import VarWizard
import argparse
import warnings
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', help = 'base pretrained model', type = str, default = 'bloom-560m', choices = ['bloom-560m'])
    parser.add_argument('--input', type = str, required = True, help = 'input for VarWizard (a string of code or a file path)')
    parser.add_argument('--lang', type = str, required = True, help = 'the programming language of the input', choices = ['c', 'cpp', 'java', 'php', 'go', 'javascript', 'ruby', 'rust', 'python', 'c_sharp'])
    parser.add_argument('--output-path', type = str, help = 'the path of the output file if you want to save the output')
    parser.add_argument('--max-input-len', type = int, default = 400, help = 'the maximum number of input tokens (default: 400)')
    parser.add_argument('--device', type = str, default = 'cpu', help = 'used device for generating the output (default: cpu)')
    parser.add_argument('--penalty-alpha', default = 0.6, type = float, help = 'penalty-alpha of the contrastive search')
    parser.add_argument('--top-k', default = 4, type = int, help = 'top-k')
    parser.add_argument('--max-new-tokens', default = 100, type = int, help = 'maximum number of generatation tokens')
    args = parser.parse_args()
    warnings.filterwarnings("ignore")
    model = VarWizard(model_name = args.model_name)
    return model.make_new_code(input = args.input, lang = args.lang, output_path = args.output_path, max_input_len = args.max_input_len, max_new_tokens = args.max_new_tokens, penalty_alpha = args.penalty_alpha, top_k = args.top_k, device = args.device)




