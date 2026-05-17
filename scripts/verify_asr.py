"""ASR verify all test WAVs"""
import sys,os,subprocess,glob;sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,r'C:\Users\TOM\miniconda3\envs\AIStudio\Lib\site-packages\funasr\models\fun_asr_nano')
from funasr import AutoModel

output_dir=os.path.dirname(os.path.abspath(__file__))+'/output'
waves=sorted(glob.glob(output_dir+'/*.wav'))
m=AutoModel(model='FunAudioLLM/Fun-ASR-Nano-2512',model_hub='ms')
for w in waves:
    w16=w.replace('.wav','_16k.wav')
    subprocess.run(['ffmpeg','-y','-i',w,'-vn','-ac','1','-ar','16000','-sample_fmt','s16',w16],check=True,capture_output=True)
    r=m.generate(input=w16)
    print(f'{os.path.basename(w)}: {r[0]["text"].strip() if r else "EMPTY"}')
