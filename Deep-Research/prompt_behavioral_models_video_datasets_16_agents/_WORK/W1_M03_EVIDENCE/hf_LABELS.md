# OmniFall Label Definitions

The benchmark uses a sixteen-class activity taxonomy. Staged datasets use classes 0-9. OF-ItW and OF-Syn use the full range 0-15. The extended classes (10-15) are infrequent and can be mapped to "other" (class 9) for compatibility.

## Core Classes (0-9, all datasets)

- **`0|walk`** - Move around, including jogging and running and "drunk walking", but only if it is not part of some special exercise like pulling your knees up. Not when pushing a large object like a chair, but included carrying something small like an apple.
- **`1|fall`** - The act of falling (from any previous state). Includes falling on a bed, if the process is not a controlled lying down with arms as support.
- **`2|fallen`** - Being on the ground or a mattress after a fall.
- **`3|sit_down`** - Sitting down on bed or chair or ground.
- **`4|sitting`** - Sitting on bed or chair or ground.
- **`5|lie_down`** - Lying down intentionally (in contrast to a fall) on ground or bed.
- **`6|lying`** - Being in a lying position (in bed or on the ground) after intentionally getting into that position.
- **`7|stand_up`** - Standing up from a fallen state, from lying or sitting. Includes getting from lying position into sitting position.
- **`8|standing`** - Standing around without walking.
- **`9|other`** - Any other activity, including e.g. walking while pushing an object like a chair.

## Extended Classes (10-15, OF-ItW and OF-Syn)

These classes capture additional activities observed in genuine accident and synthetic videos. They do not occur in staged datasets.

- **`10|kneel_down`** - Transitioning from standing or another posture to a kneeling position.
- **`11|kneeling`** - Being in a kneeling position (static posture).
- **`12|squat_down`** - Transitioning to a squatting position.
- **`13|squatting`** - Being in a squatting position (static posture).
- **`14|crawl`** - Crawling on hands and knees or similar locomotion on the ground.
- **`15|jump`** - Jumping action, including vertical jumps and jumps from elevated positions.

## Motion Types

There are two types of motions: **dynamic** ones like `walk` or `stand_up` and **static** ones like `fallen`, `sitting`, `lying`.

**Dynamic motions** are annotated starting from the first frame that belongs to that action. For example, the transition from `walk` to `fall` begins at the first frame where the motion visibly diverges from walking.

**Static motions** begin at the first frame where the person reaches a resting state. For `sit_down`, the label ends when the person stops adjusting their body position. For `fall`, the label ends when inertia-driven movement stops, and the subsequent `fallen` segment may still contain ground-level movement unrelated to the fall or recovery.

## Label Sequences

There are natural sequences of labels like `fall`, `fallen`, `stand_up`. However, these do not always appear together. A person might stand up directly after falling without a `fallen` segment, or sit down and immediately stand up without a `sitting` segment.

Lying down is intentional (in contrast to `fall`). Falls can follow `sit_down` or `lie_down` when falling from a chair or bed.

Getting from a lying position to sitting counts as `stand_up`, even if the person remains seated. A full sequence might be: `lying`, `stand_up`, `sitting`, `stand_up` (lying in bed, sitting up, pausing, then fully standing).

The distinction between `sit_down` followed by `lie_down` versus a single `lie_down` depends on whether there is a moment of rest in the sitting position. If the person transitions directly from standing through sitting to lying without pause, only `lie_down` is labeled.

## Annotation Process

The annotation video below demonstrates how VGG VIA was used for dense temporal annotation. Pre-existing dataset labels served as visual aid, but all videos were relabeled using OmniFall's label definitions to ensure consistency. The example shows CMDFall, which already provides relatively detailed labels; other source datasets have sparser original annotations.

Blurred regions in the video were added in post-processing to protect subject privacy on this page.

<video src="https://huggingface.co/datasets/simplexsigil2/omnifall/resolve/main/annotation_remarks.webm" controls />
