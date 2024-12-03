import os
from openai import OpenAI
from tenacity import (
    retry,
    stop_after_attempt, # type: ignore
    wait_random_exponential, # type: ignore
)
from dotenv import load_dotenv
from typing import Optional, List, Union
 
load_dotenv()
# openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_completion(prompt: Union[str, List[str]], max_tokens: int = 256, stop_strs: Optional[List[str]] = None, is_batched: bool = False) -> Union[str, List[str]]:
    assert (not is_batched and isinstance(prompt, str)) or (is_batched and isinstance(prompt, list))
    # response = openai.Completion.create(
    #     model='text-davinci-003',
    #     prompt=prompt,
    #     temperature=0.0,
    #     max_tokens=max_tokens,
    #     top_p=1,
    #     frequency_penalty=0.0,
    #     presence_penalty=0.0,
    #     stop=stop_strs,
    # )
    if is_batched:
        res: List[str] = [""] * len(prompt)
        for i, p in enumerate(prompt):
            messages = [{"role": "user", "content": p}]
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=messages,
                temperature=0.0,
                max_tokens=max_tokens,
                stop=stop_strs,
                # top_p=1,
                # frequency_penalty=0.0,
                # presence_penalty=0.0,
                )
            res[i] = response.choices[0].message.content
        return res
    else:
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
            temperature=0.0,
            max_tokens=max_tokens,
            stop=stop_strs,
            # top_p=1,
            # frequency_penalty=0.0,
            # presence_penalty=0.0,
            )
        return response.choices[0].message.content
    # # text = response.choices[0].message.content
    # if is_batched:
    #     res: List[str] = [""] * len(prompt)
    #     for choice in response.choices:
    #         res[choice.index] = choice.text
    #     return res
    # return response.choices[0].text
