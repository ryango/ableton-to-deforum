# ableton-to-deforum

Script for translating Ableton track automation to Deforum keyframes 
![ableton screenshot](https://miro.medium.com/v2/resize:fit:720/format:webp/1*aUm_oTjvA0pgm03AjJBlYg.png)

[Output example](https://www.instagram.com/reel/CpxnmEdDN5a/?utm_source=ig_web_copy_link)

1. Import audio clip onto first audio track
2. Ensure file BPM is correct
3. Put Overdrive effects onto the first audio track
4. Rename them to what parameter you want to animate
5. Specify remapping in each Overdrive's Info Text field
6. Save ALS file
7. Run python script

```python abletonToDeforum.py <als file> <framerate: optional, assumes 15fps>```

More info here:
https://theryangordon.medium.com/audio-synced-ai-animations-cde42688d824
