#!/usr/bin/env python

# To run this file, use the command:
# python src/crewai_bravesearch/main.py "Your topic here"

import sys
import os
# Add the 'src' directory to the Python path to resolve module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import argparse

import warnings
from crewai_bravesearch.crew import CrewaiBravesearch

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run(topic):
    """
    Run the crew.
    """
    inputs = {
        'topic': topic
    }
    CrewaiBravesearch().crew().kickoff(inputs=inputs)



def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CrewaiBravesearch().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CrewaiBravesearch().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CrewaiBravesearch().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

if __name__ == "__main__":
    """
    This allows the crew to be run directly from the command line using `python src/crewai_bravesearch/main.py`.
    """
    parser = argparse.ArgumentParser(description="Run the CrewaiBravesearch crew with a specific topic.")
    parser.add_argument(
        "topic",
        nargs="?",
        default="Vision Language Models",
        help="The topic for the crew to research and report on."
    )
    args = parser.parse_args()
    run(args.topic)
