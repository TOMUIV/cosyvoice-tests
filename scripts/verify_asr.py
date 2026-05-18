import sys,os,subprocess,glob
sys.path.insert(0,r'C:\Users\TOM\miniconda3\envs\AIStudio\Lib\site-packages\funasr\models\fun_asr_nano')
from funasr import AutoModel
base=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out=base+'/output'
data=base+'/data'
waves=sorted(glob.glob(out+'/*.wav'))
m=AutoModel(model='FunAudioLLM/Fun-ASR-Nano-2512',model_hub='ms')
lines=[]
for w in waves:
    w16=w.replace('.wav','_16k.wav')
    subprocess.run(['ffmpeg','-y','-i',w,'-vn','-ac','1','-ar','16000','-sample_fmt','s16',w16],check=True,capture_output=True)
    r=m.generate(input=w16)
    t=r[0]['text'].strip() if r else 'EMPTY'
    l=f'{os.path.basename(w)}: {t}'
    lines.append(l)

with open(data+'/asr_results.txt','w',encoding='utf-8')as f:
    f.write('\n'.join(lines))
print('Saved '+str(len(lines))+' results')
for l in lines: print(l)
