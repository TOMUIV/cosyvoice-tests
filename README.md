# CosyVoice-300M-Instruct: "于是扑扑" Bug Reproduction

## Environment
- GPU: RTX 5060 (Blackwell sm_120)
- torch 2.11.0+cu128, transformers 5.6.2
- CosyVoice commit: ace7c47
- Mood: WARM (`"A nostalgic middle-aged woman, recalling old memories with gentle affection..."`) for all tests

## Test Results

### Instruct Mode (WARM mood)

| # | Input | ASR Output | 
|---|-------|-----------|
| 1 | 于是**扑扑**衣上的泥土 | 神威王も二枚... ❌ Japanese |
| 2 | 于是**他扑扑**衣上的泥土 | 于是他扑扑衣上的泥土 ✅ |
| 3 | 于是**扑扑** | 油烟开会呢 ❌ gibberish |
| 4 | 于是**他扑扑** | 于是他噗噗 ✅ |
| 5 | 于是**扑扑**衣上的泥土，心里很轻松似的 | 日式铺铺衣上的泥土 ⚠️ |
| 6 | 于是**拍了拍**衣上的泥土 | 于是拍了拍衣上的泥土 ✅ |
| 7 | 于是**扑了扑**衣上的泥土 | 下の道には... ❌ Japanese |
| 8 | 于是**抖了抖**衣上的泥土 | 于是抖了抖印上的泥土 ✅ |

### SFT Mode (no mood, control group)

| # | Input | ASR Output |
|---|-------|-----------|
| 1 | 于是扑扑衣上的泥土 | 这是铺铺衣裳的泥土 ✅ |
| 2 | 于是他扑扑衣上的泥土 | 于是他噗噗衣上了泥土 ✅ |
| 3 | 于是扑扑 | 这是扑 ✅ |
| 4 | 于是他扑扑 | 于是他噗噗 ✅ |
| 5 | 于是扑扑衣上的泥土，心里很轻松似的 | 就是铺铺衣裳的泥土 ✅ |
| 6 | 于是拍了拍衣上的泥土 | 于是拍了拍衣上的泥土 ✅ |
| 7 | 于是扑了扑衣上的泥土 | 只是铺了铺衣上的泥土 ✅ |
| 8 | 于是抖了抖衣上的泥土 | 于是抖了抖衣上的泥土 ✅ |

**All 8 SFT tests are intelligible. 4 out of 8 Instruct tests are garbled.**

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
