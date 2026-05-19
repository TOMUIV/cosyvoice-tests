"""Capture FULL 4097-dim logit + WAV for 5-group experiment.
Groups: 1=empty, 2=short, 3=WARM, 4=paipai+WARM, 5=ta+WARM
Seeds: 77, 88, 99 for each group. Total 15 runs."""
import sys,os,numpy as np,wave,torch,random
sys.path.insert(0,'.'); os.chdir('.')
sys.stdout.reconfigure(encoding='utf-8')
from cosyvoice.cli.cosyvoice import AutoModel

WARM = 'A nostalgic middle-aged woman, recalling old memories with gentle affection. Soft, warm, tender tone, slightly slow, like telling a beloved story.<|endofprompt|>'
SHORT = 'A gentle voice.<|endofprompt|>'

tests = [
    ("G1_empty",  "于是扑扑衣上的泥土",   "<|endofprompt|>"),
    ("G2_short",  "于是扑扑衣上的泥土",   SHORT),
    ("G3_warm",   "于是扑扑衣上的泥土",   WARM),
    ("G4_paipai", "于是拍了拍衣上的泥土",  WARM),
    ("G5_ta",     "于是他扑扑衣上的泥土",  WARM),
]

model = AutoModel(model_dir=os.path.expanduser('~/cosyvoice_models/iic/CosyVoice-300M-Instruct'))
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output')
audiodir = os.path.join(outdir, 'audio')
datadir = os.path.join(outdir, 'data')
os.makedirs(audiodir, exist_ok=True)
os.makedirs(datadir, exist_ok=True)

captured_full = []
original_sampling_ids = model.model.llm.sampling_ids

def patched_sampling_ids(self, weighted_scores, decoded_tokens, sampling, ignore_eos=True):
    captured_full.append(weighted_scores.detach().cpu().numpy().copy())
    return original_sampling_ids(weighted_scores, decoded_tokens, sampling, ignore_eos)

import types
model.model.llm.sampling_ids = types.MethodType(patched_sampling_ids, model.model.llm)

SEEDS = [77, 88, 99]
summary = []

for tag, txt, prompt in tests:
    for s in SEEDS:
        captured_full.clear()
        torch.manual_seed(s); torch.cuda.manual_seed_all(s); random.seed(s); np.random.seed(s)

        r = model.inference_instruct(txt, '中文女', prompt)
        wavs = [c['tts_speech'].cpu().numpy() for c in r]
        c = np.concatenate(wavs, axis=-1).astype(np.float32)
        if c.ndim == 2 and c.shape[0] == 1: c = c.flatten()
        elif c.ndim == 2 and c.shape[0] < c.shape[1]: c = c.T
        c = c.flatten()
        a = (np.clip(c, -1, 1) * 32767).astype(np.int16)
        if a.ndim == 1: a = a.reshape(-1, 1)

        wav_path = os.path.join(audiodir, '{0}_seed{1}.wav'.format(tag, s))
        with wave.open(wav_path, 'w') as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(24000); wf.writeframes(a.tobytes())

        n = len(captured_full)
        mid = n // 2
        near_end = max(n - 3, mid + 1)  # 3 steps before end, but not same as mid
        for step in [0, 1, 2, mid, near_end]:
            if step < n:
                np.save(os.path.join(datadir, '{0}_seed{1}_logit_step{2}.npy'.format(tag, s, step)),
                        captured_full[step])

        duration = len(c) / 24000
        summary.append('{0}_seed{1}: {2} steps, {3:.1f}s [saved 0,1,2,{4},{5}]'.format(
            tag, s, n, duration, mid, near_end))
        print(summary[-1])

import torch; del model; torch.cuda.empty_cache()
print('\nAll done! {} runs complete.'.format(len(summary)))
