# CosyVoice-300M-Instruct: "于是扑扑" Bug Reproduction

## Environment
- GPU: RTX 5060 (Blackwell sm_120)
- torch 2.11.0+cu128, transformers 5.6.2
- CosyVoice commit: ace7c47
- Model: CosyVoice-300M-Instruct (iic/CosyVoice-300M-Instruct)

## Bug Summary
CosyVoice-300M-Instruct produces garbled/nonsensical audio when synthesizing the phrase "于是扑扑衣上的泥土" with long English mood descriptions (WARM mode). Adding a single character "他" at the start ("于是他扑扑衣上的泥土") fixes the output. SFT mode (no mood description) does not have this issue.

## File Structure
```
scripts/
  gen_pupu_tests.py   # Generate 8 comparison WAVs with different variants
  dtest.py            # Deep test with NORMAL vs WARM mode comparison
  wtest.py            # General WARM sentence tests
output/
  t01_pupu_fail.wav   # "于是扑扑衣上的泥土" WARM -> garbled
  t02_pupu_add_ta.wav # "于是他扑扑衣上的泥土" WARM -> works
  t05_pupu_full.wav   # "于是扑扑衣上的泥土，心里很轻松似的" WARM -> works
  t06_paipai_fail.wav # "于是拍了拍衣上的泥土" WARM -> works (听感)
data/
  ch_long_annotated.py # Full annotated text (Zhu Ziqing)
```

## Root Cause Hypothesis
The character "扑" has extremely low frequency in CosyVoice-300M's Chinese training data. In Instruct mode, the English mood description concatenated before Chinese text creates a specific token boundary that the LLM's speech token sampling cannot handle for this rare character. SFT mode (no English prefix) works correctly.

## Key Finding
- SFT mode: ALL variants work
- Instruct + "扑扑": FAILS
- Instruct + "拍拍"/"抖抖": WORKS  
- Instruct + "扑扑" with added context: WORKS
