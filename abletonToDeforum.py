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
devices = root.find("LiveSet").find("Tracks")[0].find("DeviceChain").find("DeviceChain").find("Devices").findall("Overdrive")
bpm = float(root.find("LiveSet").find("MasterTrack").find("DeviceChain").find("Mixer").find("Tempo").find("Manual").get("Value"))


print(f"\nGenerating keyframes for Ableston set with {bpm} bpm and target framerate {fps} and Ableton XML version {root.get('MajorVersion')}")
if root.get("MajorVersion") == '4':
    print(f"Found {len(devices)} overdrives on the first audio track")
    lastframe = -1
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
                frame = 0
            
            if frame == lastframe:
                frame += 1
            
            lastframe = frame

            value = float(child.get("Value"))
            value = reMap(value, 100, 0, range[1], range[0])
            print(f"{frame}: ({value}),", end=" ")
elif root.get("MajorVersion") == '5':
    deviceInfo = dict()
    for device in devices:
        try: 
            deviceName = device.find("UserName").get("Value")
        except:
            deviceName = "None"
        
        try:
            drive = device.find("Drive")
            automationId = drive.find("AutomationTarget").get("Id")

            annotation = device.find("Annotation").get("Value").split(",")
            if annotation == [""]:
                print(f"Device named {deviceName} missing remapped range. Enter remap min:")
                min = input()
                print(f"Enter remap max:")
                max = input()
                annotation = [min, max]

            range = list(map(lambda x: float(x), annotation))
            deviceInfo[automationId] = {
                'range': range,
                'name': deviceName
            }
        except:
            print(f"Device named {deviceName} missing automation")
            continue

    envelopes = root.find("LiveSet").find("Tracks")[0].find("AutomationEnvelopes").find("Envelopes").findall("AutomationEnvelope")
    for envelope in envelopes:
        events = envelope.find("Automation").find("Events").findall("FloatEvent")
        id = envelope.find("EnvelopeTarget").find("PointeeId").get("Value")
        range = deviceInfo[id]['range']
        name = deviceInfo[id]['name']
        print(f'Keyframes for: {name} with range {range}')
        for child in events:
            frame = round(float(child.get("Time")) / bpm * 60 * fps)
            if frame < 0:
                continue
            value = float(child.get("Value"))
            value = reMap(value, 100, 0, range[1], range[0])
            print(f"{frame}: ({value}),", end=" ")

