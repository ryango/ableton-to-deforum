import xml.etree.ElementTree as ET
import sys
import gzip


def reMap(value, maxInput, minInput, maxOutput, minOutput):

	value = maxInput if value > maxInput else value
	value = minInput if value < minInput else value

	inputSpan = maxInput - minInput
	outputSpan = maxOutput - minOutput

	scaledThrust = float(value - minInput) / float(inputSpan)

	return minOutput + (scaledThrust * outputSpan)

with gzip.open(sys.argv[1], 'rb') as f:
    file_content = f.read()

fps = float(sys.argv[2]) if len(sys.argv) > 2 else 15
tree = ET.fromstring(file_content)
root = tree
events = dict()
lastFrame = -1
devices = root.find("LiveSet").find("Tracks")[0].find("DeviceChain").find("DeviceChain").find("Devices").findall("Overdrive")
bpm = float(root.find("LiveSet").find("MasterTrack").find("DeviceChain").find("Mixer").find("Tempo").find("Manual").get("Value"))
print(f"\nGenerating keyframes for Ableston set with {bpm} bpm and target framerate {fps}")
print(f"Found {len(devices)} overdrives on the first audio track")
for device in devices:
    print("\n")

    try: 
        deviceName = device.find("UserName").get("Value")
    except:
        deviceName = "None"
    
    try:
        drive = device.find("Drive")
        automation = drive.find("ArrangerAutomation")
        events = automation.find("Events")
    except:
        print(f"Device named {deviceName} no automation events detected")
        continue


    annotation = device.find("Annotation").get("Value").split(",")
    if annotation == [""]:
        print(f"Device named {deviceName} missing remapped range. Enter remap min:")
        min = input()
        print(f"Enter remap max:")
        max = input()
        annotation = [min, max]

    range = list(map(lambda x: float(x), annotation))
    print(f'Keyframes for: {device.find("UserName").get("Value")} with range {range}')
    
    for child in events:
        frame = round(float(child.get("Time")) / bpm * 60 * fps)
        
        if frame < 0:
            continue

        # for hard vertical discontinuities - just nudge this one to the right
        if frame == lastFrame:
            frame = frame + 1
        lastFrame = frame
        value = float(child.get("Value"))
        value = reMap(value, 100, 0, range[1], range[0])
        print(f"{frame}: ({value}),", end=" ")