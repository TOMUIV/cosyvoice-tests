"""Instrument CosyVoice-300M-Instruct to find where '于是扑扑' fails"""
import sys,os,numpy as np
sys.path.insert(0,r'D:\资料库\python\AIStudio\CosyVoice');os.chdir(r'D:\资料库\python\AIStudio\CosyVoice')
sys.stdout.reconfigure(encoding='utf-8')
from cosyvoice.cli.cosyvoice import AutoModel
import torch

model=AutoModel(model_dir=os.path.expanduser('~/cosyvoice_models/iic/CosyVoice-300M-Instruct'))
WARM='A nostalgic middle-aged woman, recalling old memories with gentle affection. Soft, warm, tender tone, slightly slow, like telling a beloved story.<|endofprompt|>'

# Monkey-patch frontend_instruct to capture intermediates
orig_frontend_instruct = model.frontend.frontend_instruct

def debug_frontend_instruct(tts_text, spk_id, instruct_text):
    print(f"\n=== {tts_text} ===")
    model_input = model.frontend.frontend_sft(tts_text, spk_id)
    del model_input['llm_embedding']
    instruct_text_token, instruct_text_token_len = model.frontend._extract_text_token(instruct_text)
    model_input['prompt_text'] = instruct_text_token
    model_input['prompt_text_len'] = instruct_text_token_len
    
    # Decode tokens to see what tokenizer produces
    tokenizer = model.frontend.tokenizer
    print(f"  prompt_text tokens ({instruct_text_token_len.item()}): {instruct_text_token[0,:20]}")
    print(f"  prompt_text decoded: {tokenizer.decode(instruct_text_token[0])}")
    print(f"  tts_text: '{tts_text}'")
    return model_input

model.frontend.frontend_instruct = debug_frontend_instruct

# Also patch the LLM inference to capture first token
orig_tts = model.model.tts
def debug_tts(**kwargs):
    print(f"  model_input keys: {list(kwargs.keys())}")
    print(f"  text shape: {kwargs['text'].shape}, prompt_text shape: {kwargs['prompt_text'].shape}")
    for chunk in orig_tts(**kwargs):
        speech = chunk['tts_speech']
        print(f"  output audio: {speech.shape}, 1st 10 samples: {speech[0,:10].numpy().round(3)}")
        yield chunk

model.model.tts = debug_tts

# Test both sentences
for txt in ['于是扑扑衣上的泥土', '于是他扑扑衣上的泥土']:
    result = model.inference_instruct(txt, '中文女', WARM)
    wavs = [c['tts_speech'].cpu().numpy() for c in result]
    c = np.concatenate(wavs, axis=-1)
    print(f"  total audio: {c.size/24000:.1f}s, range=[{c.min():.3f}, {c.max():.3f}]")

del model; torch.cuda.empty_cache()
