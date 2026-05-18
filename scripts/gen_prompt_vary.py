"""Test Instruct with varying prompt lengths to isolate root cause.
Usage: cd /path/to/CosyVoice && python path/to/this_script.py
Requires: CosyVoice-300M-Instruct at ~/cosyvoice_models/iic/CosyVoice-300M-Instruct"""
import sys,os,numpy as np,wave
sys.path.insert(0,'.'); os.chdir('.')
sys.stdout.reconfigure(encoding='utf-8')
from cosyvoice.cli.cosyvoice import AutoModel

model=AutoModel(model_dir=os.path.expanduser('~/cosyvoice_models/iic/CosyVoice-300M-Instruct'))
WARM='A nostalgic middle-aged woman, recalling old memories with gentle affection. Soft, warm, tender tone, slightly slow, like telling a beloved story.<|endofprompt|>'

outdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/output'
tests=[
    ("prompt_0_empty","于是扑扑衣上的泥土","<|endofprompt|>"),
    ("prompt_2_en","于是扑扑衣上的泥土","A narrator.<|endofprompt|>"),
    ("prompt_3_cn","于是扑扑衣上的泥土","温柔的女声。<|endofprompt|>"),
    ("prompt_39_warm","于是扑扑衣上的泥土",WARM),
]
for name,txt,instr in tests:
    r=model.inference_instruct(txt,'中文女',instr)
    wavs=[c['tts_speech'].cpu().numpy() for c in r]
    c=np.concatenate(wavs,axis=-1)
    if c.ndim==2 and c.shape[0]==1:c=c.flatten()
    elif c.ndim==2 and c.shape[0]<c.shape[1]:c=c.T
    a=(np.clip(np.asarray(c,dtype=np.float32),-1,1)*32767).astype(np.int16)
    if a.ndim==1:a=a.reshape(-1,1)
    path=os.path.join(outdir,f'{name}.wav')
    with wave.open(path,'w')as wf:wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(24000);wf.writeframes(a.tobytes())
    print(f'{name}.wav  [{c.size/24000:.1f}s]  prompt_len={len(instr.split())} words')

import torch; del model; torch.cuda.empty_cache()
