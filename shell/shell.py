#! /usr/bin/env python3

import os, sys, time, re
import helpers

while True:
    helpers.print_prompt()
    prompt = helpers.read_prompt()
    prompts = prompt.split("&")
    for index, prompt in enumerate(prompts):
        background = index < len(prompts) - 1
        if background:
            rc = os.fork()
            if rc == 0:
                helpers.process_prompt(prompt)
                sys.exit(0)
        else:
            helpers.process_prompt(prompt)
