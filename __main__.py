
import json
import itertools
import random
import os
import argparse
import sys
import Level1gen as lvl1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', type=int, default=1, help="a number")
    args = parser.parse_args()
    sys.stdout.write(str(arghandler(args)))

def arghandler(args):
    if args.level == 1:
        raw = lvl1.generateQuestions()
        questions = lvl1.pruneQuestions(raw)
        answers = lvl1.generateAnswers(questions)
        dict = lvl1.answersdict(answers)
        jsonDump = json.dumps(dict)
        with open('lvl1QnA.json', 'w') as file:
            json.dump(jsonDump, file)
        return "JSON created with name 'lvl1QnA.json'" + "\n"


if __name__ == "__main__":
    main()