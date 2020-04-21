# Evaluation Scripts & Metrics

This homework includes some scripts to evaluate your datasets and trained models quantitatively.
Here is the detail of what those metrics are.

## Training Set Metrics

You can use the `measure.py` script to quantitatively evaluate the quality of a training set,
before training the model. Use it by passing the dataset directory you want to evaluate as
the first command line argument.

The script produces output similar to the following:
```
datadir	75000	226223	1131115	4.749742	6.409798	4.430815
```

The numbers are:

- number of dialogues
- number of unique turns
- number of turns, after augmenting parameters
- entropy of the context ThingTalk code (dialogue state before the user utterance)
- entropy of the user utterance
- entropy of the target ThingTalk code (delta state before and after the user utterance)

Entropy is calculated using a bigram language model. Roughly speaking, more natural datasets have higher entropy. We calculate entropy of our synthesized training set to see how far it is from capturing the complexity of natural sentences in MultiWOZ.

## Evaluation Metrics

After you train a model, you can add it to the Makefile and run `make evaluate` to produce
the evaluation metrics. These metrics are stored in files ending in `.results` and `.debug`
in the directory containing the evaluation set.

The `.results` file is a comma-separated file that looks like this:
```
eval,all,202,0.6584158415841584,0.6831683168316832,0.8613861386138614,0.8712871287128713,0.8712871287128713,0.9306930693069307
eval,0,46,0.7608695652173914,0.7608695652173914,0.7608695652173914,0.8043478260869565,0.8043478260869565,0.9347826086956522
eval,1,24,0.5416666666666666,0.6666666666666666,0.875,0.875,0.875,0.875
eval,2,54,0.8703703703703703,0.9074074074074074,0.9814814814814815,0.9814814814814815,0.9814814814814815,0.9814814814814815
eval,3,20,0.55,0.55,0.95,0.95,0.95,0.95
eval,4,38,0.5,0.5,0.8421052631578947,0.8421052631578947,0.8421052631578947,0.8947368421052632
eval,5,10,0.7,0.7,0.9,0.9,0.9,1
eval,6,8,0.125,0.125,0.625,0.625,0.625,0.875
eval,7,1,0,0,0,0,0,0
eval,8,1,0,0,0,0,0,1
```

The columns are:
- name of the set being evaluated
- complexity of the current turn (number of parameters in the prediction)
- dataset size (number of turns)-
- exact match accuracy
- accuracy w/o parameters (that is, ignoring any part of the code between quote marks)
- function accuracy (in this task, this is equivalent to distinguishing query vs action)
- device accuracy (finding the correct device, not relevant to this homework because there is only one device)
- number of function accuracy (used to identify joins and when-do commands, not relevant to this homework)
- syntax accuracy

In practice, the most important metric you should pay attention to is the exact match accuracy in the first row.
