# N-back Task

A configurable digit N-back cognitive task implemented in Python with PsychoPy.
It presents a short practice block followed by the main task and records trial-level
responses and reaction times.

## N-back Digit Task

This repository contains a custom implementation of a digit-based N-back task,
developed for experimental research on working memory. The task is based on the
N-back paradigm described in the published literature by Kirchner (1958).

**Reference:**

Kirchner, W. K. (1958). Age differences in short-term retention of rapidly changing
information. *Journal of Experimental Psychology, 55*(4), 352–358.
https://doi.org/10.1037/h0043688

## Requirements

- Python 3
- [PsychoPy](https://www.psychopy.org/)

Install PsychoPy using its recommended installation instructions for your operating
system. PsychoPy has several system dependencies, so its standalone application or
official installation guide may be more reliable than a generic `pip` install.

## Run

From the project directory, launch:

```bash
python N-back_task.py
```

The experiment opens a dialog for participant, session, condition, N-back level,
number of trials, and target percentage. Press **Space** when the displayed digit
matches the digit shown N trials earlier. The experiment includes a 10-trial
practice block before the main block. Press **Escape** during a block to quit.

## Output and participant data

Results are written to the `data/` directory. The output filename includes the
participant/session details, task settings, and run date. PsychoPy may create
multiple output formats for an experiment; these files can contain sensitive
participant data and are excluded from Git by `.gitignore`.

Do not publish identifiable or otherwise sensitive participant data. Follow your
research protocol, consent terms, and institutional data-management requirements
when collecting, storing, or sharing results. The generated filename is
BIDS-inspired; this project does not claim that its outputs constitute a complete
BIDS dataset.

## Project files

- `N-back_task.py` — experiment setup, sequence generation, task presentation, and
  response logging.

## Notes

This is an experimental research task. Validate the task flow, timing, and output
with your intended hardware and study protocol before collecting research data.