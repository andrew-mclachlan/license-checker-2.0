import os
import requests
from dotenv import load_dotenv
import ollama

# Load environment variables in a file called .env

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

# Check the key

if not api_key:
    print(
        "No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!"
    )
elif not api_key.startswith("sk-proj-"):
    print(
        "An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook"
    )
elif api_key.strip() != api_key:
    print(
        "An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook"
    )
else:
    print("API key found and looks good so far!")

system_prompt = "You are an expert in software license compliance. Given two software components, \
    each with an SPDX license, describe whether their licenses are compatible when the components \
    are {linkage} together. For each component, you will be told if the source code is provided to \
    customers and how it is distributed (e.g., as source, binary, or both). Consider all relevant \
    license obligations and distribution scenarios. Respond with Compatible or Not Compatible and \
    provide a brief explanation for your decision."

user_prompt = "Are these software licenses compatible {component1} and {component2}? \
    Where {component1} is distributed as {distribution1} and {component2} is distributed as {distributed2}. \
    {component1} uses {component2} {linkage} and {additional_info}."


def check_licenses(
    component1, component2, linkage, distribution1, distributed2, additional_info
):
    compatible = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": user_prompt.format(
                component1=component1,
                component2=component2,
                distribution1=distribution1,
                distributed2=distributed2,
                linkage=linkage,
                additional_info=additional_info,
            ),
        },
    ]
    response = ollama.chat(model="llama3.2", messages=compatible)
    return response["message"]["content"]


output = check_licenses(
    "MIT",
    "LGPL-3.0",
    "distributed as a binary",
    "distributed as a binary",
    "dynamically",
    "source code is available for the second component ",
)
print(output)
