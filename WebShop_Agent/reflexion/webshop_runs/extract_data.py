import json
import os
import re


def extract_data(log_dir: str, out_file: str, last_only=False, file_num=5) -> None:
    with open(out_file, 'w') as out_f:
        for i in range(file_num):
            trial_file = f"{log_dir}/trial_{i}.log"

            # Check if the file exists
            if not os.path.exists(trial_file):
                print(f"File not found: {trial_file}")
                continue

            # Read the file content
            with open(trial_file, "r") as file:
                content = file.read()

            # Split based on "Here is the task:"
            task_contents = content.split("Here is the task:")[1:]
            print(f"Processing file {trial_file}: found {len(task_contents)} tasks.")

            for task in task_contents:
                success = False
                score = 0
                trajectory = task.split("STATUS:")[0].strip()
                instruction = ""
                status = task.split("STATUS:")[1].strip()
                conversation = []  # List to store conversation

                # Determine success status
                if status.startswith("OK"):
                    success = True

                # Extract instruction using regex
                ins_match = re.search(r'Instruction:\s*([\s\S]*?)(?=\n\[Search\])', trajectory)
                if ins_match:
                    instruction = ins_match.group(1).strip()

                # Extract score if available
                traj_score = trajectory.split("Your score (min 0.0, max 1.0):")
                if len(traj_score) > 1:
                    score = float(traj_score[1].strip())
                    trajectory = traj_score[0].strip()

                # Extract conversation
                conv_lines = trajectory.split("\n")
                current_role = 'user'  # Start with WebShop
                buffer = []

                for line in conv_lines:
                    if line.startswith(">"):  # Assistant reply
                        # Save previous user content
                        if buffer:
                            conversation.append({'role': current_role, 'content': '\n'.join(buffer).strip()})
                            buffer = []
                        current_role = 'assistant'
                        buffer.append(line.lstrip("> ").strip())
                    elif line.strip():  # Non-empty line
                        if current_role == 'assistant':
                            # Save previous assistant content
                            if buffer:
                                conversation.append({'role': current_role, 'content': '\n'.join(buffer).strip()})
                                buffer = []
                            current_role = 'user'
                        buffer.append(line.strip())

                # Append the last buffer content
                if buffer:
                    conversation.append({'role': current_role, 'content': '\n'.join(buffer).strip()})

                # Handle `last_only` option
                if last_only:
                    trajectory = "Webshop\nInstruction: " + trajectory.split("instruction")[-1].strip()

                # Write results as JSON
                out_f.write(json.dumps({
                    "instruction": instruction,
                    "score": score,
                    "success": success,
                    "trajectory": trajectory,
                    "conversation": conversation
                }) + "\n")


# Example usage
extract_data("./reflexion_run_logs_final", "train.json", last_only=False, file_num=5)
