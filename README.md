# CosyVoice-300M-Instruct: Long Prompt Triggers Garbled Output

## Environment
- GPU: RTX 5060 (Blackwell sm_120)
- torch 2.11.0+cu128, transformers 5.6.2
- CosyVoice ace7c47

## 5-way Comparison

Same input: `于是扑扑衣上的泥土`

| File | Mode | Prompt | ASR |
|------|------|--------|-----|
| `cmp_sft.wav` | SFT | (none) | 这是铺铺衣裳的泥土 ✅ |
| `cmp_inst_0.wav` | Instruct | `<\|endofprompt\|>` (0 words) | 于是，噗噗衣上的泥土 ✅ |
| `cmp_inst_2en.wav` | Instruct | `A narrator.` (2 words) | 于是，铺铺印上的泥土 ✅ |
| `cmp_inst_3cn.wav` | Instruct | `温柔的女声。` (1 word) | 于是扑扑衣上的泥土 ✅ |
| `cmp_inst_39.wav` | Instruct | WARM (21 words) | 神威王も二枚… ❌ Japanese |

## Instruct (WARM, 21 words) vs SFT

| # | Input | Instruct+WARM | SFT |
|---|-------|:---:|:---:|
| 1 | 于是**扑扑**衣上的泥土 | ❌ Japanese | ✅ |
| 2 | 于是**他扑扑**衣上的泥土 | ✅ | ✅ |
| 3 | 于是**扑扑** | ❌ gibberish | ✅ |
| 4 | 于是**他扑扑** | ✅ | ✅ |
| 5 | 于是**扑扑**衣上的泥土，心里很轻松似的 | ⚠️ borderline | ✅ |
| 6 | 于是**拍了拍**衣上的泥土 | ✅ | ✅ |
| 7 | 于是**扑了扑**衣上的泥土 | ❌ Japanese | ✅ |
| 8 | 于是**抖了抖**衣上的泥土 | ✅ | ✅ |

Instruct+WARM: **4/8 garbled**. SFT: **8/8 correct**.

## Key Finding
Long English prompts (21 words) cause garbled output. Short prompts (0-3 words) work fine. SFT mode works regardless.

## Reproduce
```bash
cd /path/to/CosyVoice
python scripts/gen_prompt_vary.py    # 5-way comparison
python scripts/gen_pupu_tests.py     # 8-sentence Instruct matrix
python scripts/gen_sft_tests.py      # 8-sentence SFT matrix
python scripts/verify_asr.py         # ASR all WAVs
```

## File Structure
```
scripts/
  gen_prompt_vary.py     # 5-way comparison (SFT + 4 Instruct variants)
  gen_pupu_tests.py      # 8-sentence Instruct (WARM) matrix
  gen_sft_tests.py       # 8-sentence SFT matrix
  verify_asr.py          # ASR verification (FunASR-Nano)
output/
  cmp_*.wav              # 5-way comparison (5 files)
  t0*_*.wav              # Instruct 8-sentence matrix (8 files)
  s0*_*.wav              # SFT 8-sentence matrix (8 files)
data/
  asr_results.txt        # ASR output for all 21 WAVs
```
