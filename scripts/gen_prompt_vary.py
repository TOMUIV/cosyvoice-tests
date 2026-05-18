"""5-way comparison: SFT vs Instruct with varying prompt lengths.
Usage: cd /path/to/CosyVoice && python path/to/this_script.py
Requires: CosyVoice-300M-Instruct and CosyVoice-300M-SFT at ~/cosyvoice_models/iic/"""
import sys,os,numpy as np,wave
sys.path.insert(0,'.'); os.chdir('.')
sys.stdout.reconfigure(encoding='utf-8')
from cosyvoice.cli.cosyvoice import AutoModel

instruct_model=AutoModel(model_dir=os.path.expanduser('~/cosyvoice_models/iic/CosyVoice-300M-Instruct'))
sft_model=AutoModel(model_dir=os.path.expanduser('~/cosyvoice_models/iic/CosyVoice-300M-SFT'))
WARM='A nostalgic middle-aged woman, recalling old memories with gentle affection. Soft, warm, tender tone, slightly slow, like telling a beloved story.<|endofprompt|>'
TXT='于是扑扑衣上的泥土'

outdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/output'
tests=[
    ("cmp_sft",        "SFT",  TXT, None),
    ("cmp_inst_0",    "Ins-0",TXT, "<|endofprompt|>"),
    ("cmp_inst_2en",  "Ins-2",TXT, "A narrator.<|endofprompt|>"),
    ("cmp_inst_3cn",  "Ins-1",TXT, "温柔的女声。<|endofprompt|>"),
    ("cmp_inst_39",   "Ins-21",TXT, WARM),
]
for name,label,txt,instr in tests:
    if instr is None:
        r=sft_model.inference_sft(txt,'中文女')
    else:
        r=instruct_model.inference_instruct(txt,'中文女',instr)
    wavs=[c['tts_speech'].cpu().numpy() for c in r]
    c=np.concatenate(wavs,axis=-1)
    if c.ndim==2 and c.shape[0]==1:c=c.flatten()
    elif c.ndim==2 and c.shape[0]<c.shape[1]:c=c.T
    a=(np.clip(np.asarray(c,dtype=np.float32),-1,1)*32767).astype(np.int16)
    if a.ndim==1:a=a.reshape(-1,1)
    path=os.path.join(outdir,f'{name}.wav')
    with wave.open(path,'w')as wf:wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(24000);wf.writeframes(a.tobytes())
    print(f'{name}.wav  [{label}]  [{c.size/24000:.1f}s]')

import torch; del instruct_model; del sft_model; torch.cuda.empty_cache()
