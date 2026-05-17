import sys,os,subprocess,numpy as np,wave;sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,r'C:\Users\TOM\miniconda3\envs\AIStudio\Lib\site-packages\funasr\models\fun_asr_nano')
from funasr import AutoModel as FA
sys.path.insert(0,r'D:\资料库\python\AIStudio\CosyVoice');os.chdir(r'D:\资料库\python\AIStudio\CosyVoice')
from cosyvoice.cli.cosyvoice import AutoModel as Cosy
model=Cosy(model_dir=os.path.expanduser('~/cosyvoice_models/iic/CosyVoice-300M-Instruct'))
WARM='A nostalgic middle-aged woman, recalling old memories with gentle affection. Soft, warm, tender tone, slightly slow, like telling a beloved story.<|endofprompt|>'
tests=[
    "颇踌躇了一会",
    "他和我走到车上，将橘子一股脑儿放在我的皮大衣上",
    "于是扑扑衣上的泥土，心里很轻松似的",
    "于是扑扑衣上的泥土",   # 7 chars,炸过
    "他给我拣定了靠车门的一张椅子",  # 另一个 WARM 句
    "我看见他戴着黑布小帽",         # 另一个 WARM 句
    "我赶紧去搀他",                 # 短 WARM 句
    "他待我渐渐不同往日",           # SAD 但我们用 WARM 测
]
for txt in tests:
    r=model.inference_instruct(txt,'中文女',WARM)
    wavs=[c['tts_speech'].cpu().numpy() for c in r]
    c=np.concatenate(wavs,axis=-1)
    if c.ndim==2 and c.shape[0]==1:c=c.flatten()
    elif c.ndim==2 and c.shape[0]<c.shape[1]:c=c.T
    a=(np.clip(c,-1,1)*32767).astype('<i2')
    if a.ndim==1:a=a.reshape(-1,1)
    out=os.environ['TEMP']+f'\\opencode\\wtest_{hash(txt)%10000}.wav'
    with wave.open(out,'w')as wf:wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(24000);wf.writeframes(a.tobytes())
    wav16=out.replace('.wav','_16k.wav')
    subprocess.run(['ffmpeg','-y','-i',out,'-vn','-ac','1','-ar','16000','-sample_fmt','s16',wav16],check=True,capture_output=True)
    m=FA(model='FunAudioLLM/Fun-ASR-Nano-2512',model_hub='ms')
    r2=m.generate(input=wav16)
    got=r2[0]['text'].strip() if r2 else 'EMPTY'
    ok='OK' if any(c in got for c in txt[:3]) else 'BAD'
    print(f'[{ok}] {txt[:25]:25s} -> {got[:50]}')
