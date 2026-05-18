# CosyVoice-300M-Instruct: "于是扑扑" Bug Reproduction

## Environment
- GPU: RTX 5060 (Blackwell sm_120)
- torch 2.11.0+cu128, transformers 5.6.2
- CosyVoice commit: ace7c47
- Mood: WARM (`"A nostalgic middle-aged woman, recalling old memories with gentle affection..."`) for all tests

## Test Results

| # | File | Input Sentence | ASR Output | Verdict |
|---|------|---------------|------------|:------:|
| 1 | `t01_pupu_fail.wav` | 于是扑扑衣上的泥土 | 神威王も二枚... | ❌ 日文乱码 |
| 2 | `t02_pupu_add_ta.wav` | 于是他扑扑衣上的泥土 | 于是他扑扑衣上的泥土，哼哼哼 | ✅ |
| 3 | `t03_pupu_only.wav` | 于是扑扑 | 油烟开会呢，就秒开哦 | ❌ 乱码 |
| 4 | `t04_pupu_add_ta_only.wav` | 于是他扑扑 | 于是他噗噗 | ✅ |
| 5 | `t05_pupu_full.wav` | 于是扑扑衣上的泥土，心里很轻松似的 | 日式，铺铺衣上的泥土... | ⚠️ |
| 6 | `t06_paipai_fail.wav` | 于是拍了拍衣上的泥土 | 于是拍了拍衣上的泥土 | ✅ |
| 7 | `t07_pu_change.wav` | 于是扑了扑衣上的泥土 | 下の道には長いに... | ❌ 日文乱码 |
| 8 | `t08_dou_dou.wav` | 于是抖了抖衣上的泥土 | 于是抖了抖印上的泥土 | ✅ |

All tests use the EXACT same WARM mood description. Only the Chinese input text differs.

## Key Finding
- Adding a single character "他" at the start (t01→t02) completely fixes the output
- Adding "了" between the double verb (t01→t07) does NOT fix it — still garbled
- Adding more context after the sentence (t01→t05) partially fixes it
- Replacing "扑" with "拍" or "抖" (t06, t08) works fine

## Bug Summary
The character "扑" in the specific context "于是扑扑" causes the Instruct model's speech token sampling to collapse into Japanese/English gibberish. SFT mode (no English mood prefix) does not have this issue.

## Reproduce
```bash
python scripts/gen_pupu_tests.py        # Regenerate all 8 test WAVs
python scripts/verify_asr.py            # Run FunASR-Nano on all WAVs
```

## File Structure
```
scripts/
  gen_pupu_tests.py     # Generate 8 comparison WAVs
  dtest.py              # NORMAL vs WARM deep comparison
  wtest.py              # General WARM sentence stability tests
  verify_asr.py         # ASR verification (FunASR-Nano)
output/
  t01_pupu_fail.wav     ← ❌
  t02_pupu_add_ta.wav   ← ✅
  t03_pupu_only.wav     ← ❌
  t04_pupu_add_ta_only.wav ← ✅
  t05_pupu_full.wav     ← ⚠️
  t06_paipai_fail.wav   ← ✅
  t07_pu_change.wav     ← ❌
  t08_dou_dou.wav       ← ✅
data/
  asr_results.txt       # Full ASR verification output
  ch_long_annotated.py  # Full Zhu Ziqing text with per-sentence mood annotations
```
