"""Generate test WAVs for '于是扑扑' hypothesis"""
import sys,os,numpy as np,wave
sys.path.insert(0,r'D:\资料库\python\AIStudio\CosyVoice');os.chdir(r'D:\资料库\python\AIStudio\CosyVoice')
sys.stdout.reconfigure(encoding='utf-8')
from cosyvoice.cli.cosyvoice import AutoModel

model=AutoModel(model_dir=os.path.expanduser('~/cosyvoice_models/iic/CosyVoice-300M-Instruct'))
WARM='A nostalgic middle-aged woman, recalling old memories with gentle affection. Soft, warm, tender tone, slightly slow, like telling a beloved story.<|endofprompt|>'

tests=[
    ("t01_pupu_fail",       "于是扑扑衣上的泥土",      WARM, "❌ 原句（应该炸）"),
    ("t02_pupu_add_ta",     "于是他扑扑衣上的泥土",     WARM, "✅ 加'他'（应该好）"),
    ("t03_pupu_only",       "于是扑扑",                 WARM, "❌ 只有'于是扑扑'"),
    ("t04_pupu_add_ta_only","于是他扑扑",               WARM, "✅ 加'他'短版"),
    ("t05_pupu_full",       "于是扑扑衣上的泥土，心里很轻松似的", WARM, "✅ 完整 17 字"),
    ("t06_paipai_fail",     "于是拍了拍衣上的泥土",     WARM, "❌ '拍拍'也炸？"),
    ("t07_pu_change",       "于是扑了扑衣上的泥土",     WARM, "⚠️ '扑了扑'"),
    ("t08_dou_dou",         "于是抖了抖衣上的泥土",     WARM, "❌ '抖了抖'"),
]

outdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/output'
for name,txt,instr,note in tests:
    r=model.inference_instruct(txt,'中文女',instr)
    wavs=[c['tts_speech'].cpu().numpy() for c in r]
    c=np.concatenate(wavs,axis=-1)
    if c.ndim==2 and c.shape[0]==1:c=c.flatten()
    elif c.ndim==2 and c.shape[0]<c.shape[1]:c=c.T
    a=(np.clip(c,-1,1)*32767).astype('<i2')
    if a.ndim==1:a=a.reshape(-1,1)
    path=os.path.join(outdir,f'{name}.wav')
    with wave.open(path,'w')as wf:wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(24000);wf.writeframes(a.tobytes())
    print(f'{name}.wav  {note}  [{c.size/24000:.1f}s]  {txt}')

import torch; del model; torch.cuda.empty_cache()
