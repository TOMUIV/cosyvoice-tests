# CosyVoice-300M-Instruct: Long Instruction Prompt Produces Garbled Speech

## Environment

| Component | Version |
|-----------|---------|
| Model | CosyVoice-300M-Instruct (ace7c47) |
| GPU | RTX 5060 Laptop (Blackwell sm_120) |
| torch | 2.11.0+cu128 |
| Python | 3.10.19 |

## Experiment

5 groups, each tested with 3 random seeds (77, 88, 99). Same text content across groups; only the **instruction prompt** varies.

| Group | Input Text | Instruction Prompt | 
|:-----:|------------|-------------------|
| G1 | 于是扑扑衣上的泥土 | `<\|endofprompt\|>` (empty, 0 words) |
| G2 | 于是扑扑衣上的泥土 | `A gentle voice.<\|endofprompt\|>` (short, 3 words) |
| G3 | 于是扑扑衣上的泥土 | `A nostalgic middle-aged woman, recalling old memories with gentle affection. Soft, warm, tender tone, slightly slow, like telling a beloved story.<\|endofprompt\|>` (long WARM, 21 words) |
| G4 | 于是拍了拍衣上的泥土 | same long WARM prompt |
| G5 | 于是他扑扑衣上的泥土 | same long WARM prompt |

G4 and G5 change only the input text while keeping the same long prompt as G3.

## Results

ASR transcription (FunASR-Nano). ✅ = intelligible Chinese matching the target text. ❌ = gibberish, Japanese, or wrong words.

| Group | seed=77 | seed=88 | seed=99 | Correct |
|:-----:|---------|---------|---------|:-------:|
| **G1** empty | ✅ 于是，噗噗衣上的泥土。 | ✅ 于是，铺铺衣上的泥土。 | ✅ 于是，噗噗衣上的泥土。 | **3/3** |
| **G2** short | ✅ 于是，噗噗衣裳的泥土。 | ✅ 于是，铺铺衣裳的泥土。 | ✅ 于是，噗噗衣上的泥土。 | **3/3** |
| **G3** WARM | ✅ 于是，铺铺地上的泥土。 | ❌ 以血扑扑衣上的泥土。 | ✅ 于是，蒲布衣上的泥土。 | **2/3** |
| **G4** WARM + paipai | ✅ 于是拍了拍衣裳的泥土。 | ❌ 黑翁也是拍了拍衣裳的泥土，啊。 | ❌ 日语 | **1/3** |
| **G5** WARM + ta-pupu | ❌ 日语 | ✅ 于是他扑扑衣上的泥土。 | ✅ 又又是他瀑布印上的泥土，嗯。 | **2/3** |

- G1/G2 (empty/short prompt): all 3 seeds produce correct Chinese.
- G3/G4/G5 (long WARM prompt): errors appear across all groups, regardless of input text changes (扑扑 / 拍拍 / 他扑扑).

The error modes include:
- Partial word substitution (`地上` instead of `衣上`, `蒲布` instead of `扑扑`)
- Wrong sentence prefix (`以血` instead of `于是`, `黑翁也是` instead of `于是`)
- Complete language switch to Japanese

## Audio Files

All 15 test WAVs are in `output/audio/`. File naming: `G{group}_{variant}_seed{seed}.wav`.

## Generation Scripts

`scripts/capture_full_all.py` — Runs all 15 inferences with logit capture.

Older scripts for reference:
- `scripts/gen_prompt_vary.py` — 5-way SFT/Instruct comparison
- `scripts/gen_pupu_tests.py` — 8-sentence Instruct (WARM) matrix
- `scripts/gen_sft_tests.py` — 8-sentence SFT control matrix
