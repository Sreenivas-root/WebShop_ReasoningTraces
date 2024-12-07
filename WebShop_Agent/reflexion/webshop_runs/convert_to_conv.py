import json
import re

def convert_to_conversation(trace):
    conversation_text = trace['trajectory']
    conversation = []
    lines = conversation_text.splitlines()
    buffer = []

    for line in lines:
        if line.startswith(">"):
            if buffer:
                user_content = "\n".join(buffer).strip()
                if user_content:
                    conversation.append({"role": "user", "content": user_content})
                buffer = []

            action_match = re.match(r"> (\w+)\[(.*?)\]", line)
            if action_match:
                action, details = action_match.groups()
                conversation.append({"role": "assistant", "content": {"action": action.lower(), "text": details.strip()}})
            else:
                action_match = re.match(r"> (\w+)", line)
                if action_match:
                    action = action_match.group(1)
                    conversation.append({"role": "assistant", "content": {"action": action.lower(), "content": ""}})
        else:
            buffer.append(line)

    if buffer:
        user_content = "\n".join(buffer).strip()
        if user_content:
            conversation.append({"role": "user", "content": user_content})

    return conversation


with open('train.json', 'r') as infile, open ('train_conversation.json', 'w') as outfile:
    for line in infile:
        trace = json.loads(line)
        conv = convert_to_conversation(trace)
        trace['conversation'] = conv
        outfile.write(json.dumps(trace) + '\n')

        
