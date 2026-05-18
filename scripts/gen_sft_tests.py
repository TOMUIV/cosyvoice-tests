"""Generate SFT versions for comparison"""
import sys,os,numpy as np,wave
sys.path.insert(0,r'D:\资料库\python\AIStudio\CosyVoice');os.chdir(r'D:\资料库\python\AIStudio\CosyVoice')
sys.stdout.reconfigure(encoding='utf-8')
from cosyvoice.cli.cosyvoice import AutoModel

model=AutoModel(model_dir=os.path.expanduser('~/cosyvoice_models/iic/CosyVoice-300M-SFT'))

tests=[
    ("s01_pupu_sft",       "于是扑扑衣上的泥土"),
    ("s02_pupu_add_ta_sft","于是他扑扑衣上的泥土"),
    ("s03_pupu_only_sft",  "于是扑扑"),
    ("s04_pupu_add_ta_only_sft","于是他扑扑"),
    ("s05_pupu_full_sft",  "于是扑扑衣上的泥土，心里很轻松似的"),
    ("s06_paipai_sft",     "于是拍了拍衣上的泥土"),
    ("s07_pu_change_sft",  "于是扑了扑衣上的泥土"),
    ("s08_dou_dou_sft",    "于是抖了抖衣上的泥土"),
]

outdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/output'
for name,txt in tests:
    r=model.inference_sft(txt,'中文女')
    wavs=[c['tts_speech'].cpu().numpy() for c in r]
    c=np.concatenate(wavs,axis=-1)
    if c.ndim==2 and c.shape[0]==1:c=c.flatten()
    elif c.ndim==2 and c.shape[0]<c.shape[1]:c=c.T
    a=(np.clip(c,-1,1)*32767).astype('<i2')
    if a.ndim==1:a=a.reshape(-1,1)
    path=os.path.join(outdir,f'{name}.wav')
    with wave.open(path,'w')as wf:wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(24000);wf.writeframes(a.tobytes())
    print(f'{name}.wav  [{c.size/24000:.1f}s]  {txt}')

import torch; del model; torch.cuda.empty_cache()
