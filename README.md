# ableton-to-deforum

Script for translating Ableton track automation to Deforum keyframes 
![ableton screenshot](https://miro.medium.com/v2/resize:fit:720/format:webp/1*aUm_oTjvA0pgm03AjJBlYg.png)

[Output example](https://www.instagram.com/reel/CpxnmEdDN5a/?utm_source=ig_web_copy_link)

1. Import audio clip onto first audio track
2. Ensure file BPM is correct
3. Put Overdrive effects onto the first audio track
4. Rename them to what parameter you want to animate
5. Specify remapping in each Overdrive's Info Text field (Right click -> Edit text info and enter 0, -5 to remap the drive's 0->100 range to 0 to -5)
6. Save ALS file
7. Run python script

```python abletonToDeforum.py <als file> <framerate: optional, assumes 15fps>```

There is a sample Ableton 11 file for [this video](https://www.instagram.com/p/CpxnmEdDN5a/). You can generate the keyframes from this directory with

```python abletonToDeforum.py 'kira Project/kira11.als' 15```

You can take at the file to help understand the setup

More info here:
https://theryangordon.medium.com/audio-synced-ai-animations-cde42688d824

Known issues:
- Issues when multiple points resolve to the same frame. 
  For example, in automation events you can put 2 at the same point in time in Ableton, but Deforum builds a map of keyframe->value so one would be overridden.
  Initially I addressed this by incrementing colliding points (if 2 land at frame 15, switch it to 15 and 16). This had the problem that if 3 land at 15 this would end up with 15,16,17 which will start to throw off the timing of the animation.
  This can happen also because you can put automation events at any fraction of a beat, but the script has to discretize them to keyframe indices at a much lower rate (44.1khz+ -> 15hz) which will lead to collisions.
