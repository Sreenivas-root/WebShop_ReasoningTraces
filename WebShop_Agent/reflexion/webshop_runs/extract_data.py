import json
import re


def extract_data(log_dir: str, out_f: str, last_only = False, file_num = 5) -> None:
    with open(out_f, 'w') as out_f:
        for i in range(5):
            trial_file = f"{log_dir}/trial_{i}.log"
            with open(trial_file, "r") as file:
                content = file.read()
            contents = content.split("Here is the task:")[1:]
            print(f"dump {len(contents)}")
            for c in contents:
                success = False
                score = 0
                trajectory = c.split("STATUS:")[0].strip()
                instruction = ""
                other = c.split("STATUS:")[1].strip()
                if other.startswith("OK"):
                    success = True
                ins_match = re.search(r'Instruction:\s*([\s\S]*?)(?=\s*(?:\n|$))', trajectory)
                if ins_match:
                    instruction = ins_match.group(1)
                    print(instruction)
                traj_score = trajectory.split("Your score (min 0.0, max 1.0):")
                if len(traj_score) > 1:
                    score = float(traj_score[1].strip())
                    trajectory = traj_score[0].strip()

                if last_only:
                    trajectory = "Webshop\nInstruction: " + trajectory.split("instruction")[-1]

                #write instruction, score, success as jsons
                out_f.write(json.dumps({
                    "instruction": instruction,
                    "score": score,
                    "success": success,
                    "trajectory": trajectory
                }) + "\n")


# last_only: only extract the last trial of the environment,later the successful trials can be extracted easily.
extract_data("./reflexion_run_logs_3", "train.json", False)


