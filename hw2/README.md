# CS249S/W 2020 Homework 2: Transaction Dialogues

In this homework, you will build an interactive dialogue agent that performs a _transaction_, such as ordering food, booking an hotel, or choosing a movie to play.
A transaction is defined as containing one _query_, that defines the database over which the transaction is performed, and one or more _actions_, which execute the actual operation the user is trying to accomplish.

To do this homework, you will use and learn the latest version of Genie. This is research code, which might have issues. Please do not hesitate to ask in the community forum if you need technical help.

**Please start early and budget your time accordingly!** This homework requires generating a large dataset and training a large neural network. Simply running every command once will take about 11 hours.

### Running on Google Cloud Platform

This homework requires access to significant compute resources, including GPUs to train a neural network. To simplify that, all students will receive a Google Cloud Platform coupon. You should have received an email with instructions to redeem your coupon and apply it to your personal GCP account.

You will be responsible for creating and managing (starting, stopping) the VM instances used by this homework. **You will be billed while the instances are running** (and you will be responsible for charges beyond the coupon) so make sure you turn off any VM instance you are not using.


For cost efficiency, it is recommended to create two instances:
- a CPU only instance, with at least 8 vCPUs and 60 GBs of RAM (~$0.4/hour)
- a CPU+GPU instance, using an NVidia V100 GPU (~$2/hour)

We recommend using the Oregon (us-west-1) region, as it slightly cheaper and includes a larger set of available machine types, but any North American region should work.

**See detailed instructions and a tutorial for GCP [here](./instructions/google-cloud.md).**

You should do the development locally, testing and refining the annotations on small datasets. Then use the CPU-only instance to generate the final large dataset, and the CPU+GPU instance to train the model.
To share data between your personal computer and the two instances, refer to the tutorial.

## Setup

You will need a Linux machine for this homework, and you will need access to a Nvidia GPU with CUDA enabled. You should have received Google Cloud credits, and it is recommended you use some of those for the homework. The installation script supports Ubuntu (18.04 LTS and more recent) & Fedora (>= 31), as well as the Google Cloud Deep Learning VM image (Debian-based). If you install the dependencies manually you might be able to run this homework on other distros.

If you have not done so, first clone this repository:
```bash
git clone https://github.com/stanford-oval/cs294-homework-workdir
```

If you have done so for Homework 1, use `git pull` to receive the content of Homework 2.

Then, inside the `hw2` directory, run:
```bash
./install.sh
```

This will install all the dependencies, clone the latest version of all the Genie libraries, and set them up so you can change the code.

**NOTE:** on Debian (including on Google Cloud Platform) you will need to log out and log in again for changes to the PATH environment variable to take effect.


## Part 1: Restaurants

In this part, you will reproduce the experiment of training a dialogue agent for restaurant reservations.

### Starter code layout

The code for this part is in the `restaurant/` subfolder of `hw2`, and in the `devices/` folder. Read through it to familiarize with the new syntax, and compare and constrast with homework 1.

#### restaurant/schema.tt
This is the class definition for the restaurant agent. This should be familiar from homework 1, but you should notice that the in addition to a query called `Restaurant`, you have an action called `make_reservation`. This action uses `in req` parameter (required input parameters) instead of `out` parameters, because
logically it requires that data to function, rather than producing that data as a result and letting the user filter on it. Both queries and actions can have both `in` and `out` parameters, but most queries do not have any input parameter. Also note that the first parameter of the `make_reservation()` action has the same type as the `id` parameter of the `Restaurant()` query. Genie uses this fact to connect the action and the query: when the user tries to execute the action, and has to provide the restaurant to reserve, Genie will let the user search in the database first.

Also note the following the new annotations:
- `#_[prompt]`: one or more questions that the agent will ask when inquiring about a specific parameter
- `#[confirm]`: whether the agent should confirm explicitly with the user before executing the action (leave this to `false` for the homework)
- `#[on_error]`: error messages that can arise from executing the action (leave this to `false` for the homework)

#### restaurant/dataset.tt

This file contains the utterance definitions for the actions. These are defined as _primitive templates_, a simplified syntax for Genie templates. Observe that there are two groups of templates: one with a placeholder, and one without a placeholder. The placeholder refers to a restaurant phrase, as indicated by the type. The restaurant phrase could be the name of a restaurant, or it could be a search expression such as "restaurants that serve Chinese food".

#### devices/uk.ac.cam.multiwoz.Restaurant

This is the backend of the dialogue, in the form of a Thingpedia device. It's a standard node.js module, and it exports one class, which inherits from the `BaseDevice` class in the Thingpedia SDK. It has two methods: one is called `get_Restaurant()` and implements the query, and the other is called `do_make_reservation` and implements the action. You can find out more about Thingpedia devices in the [Thingpedia documentation](https://almond.stanford.edu/doc/thingpedia-intro.md), and you can find the [Thingpedia SDK reference](https://almond.stanford.edu/doc/jsdoc/thingpedia/) as well. 

This folder also has symlinks to the dataset.tt and schema.tt files in the restaurant/ folder, because the restaurant experiment only contains one device so those files are identical. (In principle, a single dialogue model could include multiple devices).

For simplicity, in this device the restaurant database is represented as a plain JSON file, called `restaurant_db.json`. If you wish, your device could be calling out to a SQL database or a web API to retrieve it instead.

#### Makefile

This Makefile is similar to the one in homework 1, but it's set up to generate multi-turn dialogues instead of single-shot commands. **You will need to modify the Makefile**. Look for "BEGIN EDIT HERE" blocks in it, and follow the instructions inside.

### Running a pretrained model

In this part of the homework, you will download, evaluate and try out a pretrained model for the restaurant dialogue agent.

Download the model with:
```bash
mkdir restaurant/models/
curl -L https://almond-static.stanford.edu/test-data/models/cs294s-2020-hw2-restaurants.tar.gz -o cs294s-2020-hw2-restaurants.tar.gz # This will download ~400MB weights of a neural network
tar -C restaurant/models/ -xvf cs294s-2020-hw2-restaurants.tar.gz
```

(run this command from inside the `hw2` folder)

You can evaluate the model with:
```
make evaluate experiment=restaurant eval_set=eval
```

This will evaluate the model on the MultiWOZ evaluation set - a very challenging set of human-human conversations, annotated with their interpretation in the ThingTalk language. The evaluation set is in `restaurant/eval/annotated.txt`. The first time you run this command, it will also download and cache the ~400 MB [BERT](https://towardsdatascience.com/bert-explained-state-of-the-art-language-model-for-nlp-f8b21a9b6270) that you will need for training your own models.

After evaluation is done, you will have two files:
- `./restaurant/eval/pretrained.results`: short file in CSV form containing turn-by-turn accuracy
- `./restaurant/eval/pretrained.debug`: turn-by-turn error analysis: this compares the output of the model with the gold annotation, and reports all the errors

See [instructions/eval-metrics.md](instructions/eval-metrics.md) for details of these files.

With the pretrained model, you should expect an exact match accuracy of about **66%**.

Then, you can start a server that will continuously run the model in inference mode with:
```bash
./run-nlu-server.sh --experiment restaurant --nlu_model pretrained
```

Finally, in a different tab, run:
```bash
./run-almond.sh
```

This will start an Almond server. You can connect to it at <http://127.0.0.1:3000>. Follow the configuration instructions, then click on Conversation to access the dialogue agent. Try the following to start: _"Hello, I'm looking for a restaurant in the south of town."_. You can see how Almond interprets the sentence in the terminal. Note that the accuracy is only *66%*, so it will not understand everything you say.

### Generating your own dataset

To generate a dataset, run:

```bash
make -j experiment=restaurant datadir
```

This command will generate the full dataset and will take about 7 hours and about 50GB of RAM.

You can also generate a smaller dataset (to experiment with it) with:

```bash
make -j custom_gen_flags=--debug subdatasets=1 target_size=5000 minibatch_size=5000 target_pruning_size=25 max_turns=3 datadir
```

Use `subdatasets` to control how many datasets to generate in parallel (e.g. `subdatasets="1 2"` to generate 2, `subdatasets="1 2 3"` to generate 3). `target_size` is the desired size of each dataset, and `minibatch_size` is the number of initial sentences to generate a minibatch of dialogues. `target_pruning_size` affects the exploration of the dialogue space, and `max_turns` controls how many turns per dialogue at most.

After generation, you will have the following files:

- `datadir/synthetic.txt`: the generated dialogues, with annotations, alternating between agent and user turns
- `datadir/user/synthetic.user.tsv`: all generated user turns, one per line, with the state of the conversation before the user spoke, and the interpretation of the user sentence
- `datadir/user/train.tsv` & `datadir/user/eval.tsv`: train/dev split of the user dataset
- `datadir/agent`: contains similar files to `datadir/user`, but for the agent turns. You can use this in your project to train a natural language generation (NLG) model, or a natural language understanding (NLU) model that understands agent sentences, e.g. to annotate human-human conversations

### (Optional) Training restaurants again

After you generated the dataset, train with:

```bash
make -j train-user experiment=restaurant model=mymodelname
```

The model name can be anything, as long as it is alphanumeric only. It is recommended to use a sequential name, e.g. `bert1`, `bert2`, etc. It is also recommended to save the training flags and accuracy in a spreadsheet. The model will be saved in `restaurant/models/mymodelname`.

After training, add the new model name to the Makefile in `restaurant_eval_models`, then evaluate again to see the results, or restart the NLU server with the new model name to try it out. You can also start a tensorboard with `tensorboard --logdir restaurant/models` to compare your model with the pretrained one.

## Part 2: Your Domain

In this part, you will built your own dialogue agent for a transaction in a domain of your choosing. You will build the Thingpedia device based on your homework 1, generate a dataset, and train a model.


### Step 1: the schema definition

The first step is to define the domain of discourse, that is, the database schema, the actions that we will perform on it, and the parameters those actions need. There can be multiple possible actions, for example a movie dialogue agent could offer to buy a ticket, or watch it on Netflix.

You will start from the schema definition of homework 1. First, create a new experiment folder next to `restaurant`, and edit the Makefile accordingly. Instructions on how to edit the Makefile are in the Makefile itself. Copy over the `schema.tt`, `entities.json` and `dataset.tt` from homework 1 in the new directory.

Then, edit `schema.tt` and `dataset.tt` to include one or more actions. You should describe the input and output parameters of the action, using the appropriate type and annotations. The action must include at least one parameter with an `Entity()` type matching the kind of object returned by main query of your homework 1 device. 
You will also need to add new dialogue-specific annotations to schema.tt. See [instructions/nl-annotations.md](instructions/nl-annotations.md) for the full list of required and optional annotations.

For example, `restaurant/schema.tt`, we have the following action to reserve a restaurant:
```js
 action make_reservation(in req restaurant : Entity(uk.ac.cam.multiwoz.Restaurant:Restaurant)
                          #[string_values="uk.ac.cam.multiwoz.Restaurant:name"]
                          #_[prompt="what restaurant would you like to book?"],
                          ...
                          )
  #_[confirmation="make a reservation at ${restaurant}"]
  #[confirm=false]
  #[on_error={
     no_slot_available=["there are no tables available on ${book_day} for ${book_time}",
                        "all slots are taken at ${book_time} on ${book_day}"]
  }];
```
Make sure the new action is mentioned in the `#[whitelist]` annotation, and remove all but the main query. 
**For this homework, your agent should include exactly one whitelisted query and at least one action**.

You should also include domain-specific templates for the action in `dataset.tt`. Detailed instruction on how
to write domain-specific templates can be found in [Thingpedia documentation](https://almond.stanford.edu/doc/thingpedia-tutorial-dataset.md).
As an example, `restaurant/dataset.tt` looks as follows: 
```js
dataset @uk.ac.cam.multiwoz.Restaurant {
  action := @uk.ac.cam.multiwoz.Restaurant.make_reservation()
  #_[preprocessed=["book a restaurant",
                   "make a restaurant reservation"]];

  action (p_restaurant : Entity(uk.ac.cam.multiwoz.Restaurant:Restaurant)) := @uk.ac.cam.multiwoz.Restaurant.make_reservation(restaurant=p_restaurant)
  #_[preprocessed=["book ${p_restaurant}",
                   "reserve ${p_restaurant}",
                   "make a restaurant reservation for ${p_restaurant}",
                   "make a reservation at ${p_restaurant}"]];
}
```


As a result of this step, you should have a new experiment folder, containing `schema.tt`, `entities.json` and `dataset.tt` in the same format as the restaurant one.
Please **do not change the name of your device from homwork 1**, i.e., keep the `edu.stanford.cs294s.<owner>` as the identifier of the device in `schema.tt` and everywhere where `uk.ac.cam.multiwoz.Restautant` is mentioned.

### Step 2: parameter datasets

For every parameter of `String` or `Entity` type in your queries and actions, you will need a sample of possible values, in TSV format. You can find examples of the format in `shared-parameter-datasets/`. 

In homework 1, you have created all the parameter dataset for your query parameters and uploaded to Thingpedia, you can download them from Thingpedia with:

```bash
make -B shared-parameter-datasets.tsv
```

(You must set the developer key in the Makefile before you run this command)

For the action parameters, you can probably find what you need from the datasets you created for queries. If you need additional string dataset, you can find the full list [here](https://almond.stanford.edu/thingpedia/strings).
To connect a parameter with a string dataset, use `string_values` annotation. See [instructions/nl-annotations.md](instructions/nl-annotations.md) for how to use it. You can also find examples from your own queries. 

### Step 3: the Thingpedia device

The Thingpedia device provides the backend for the dialogue agent.

Inside the `devices/` folder, you can bootstrap a new device with:

```bash
thingpedia init-device <your-device-id>
```

Remove the generated skeletons of `manifest.tt` and `dataset.tt`, and replace them with the real files (or a symlink) from step 1.

The add the implementation. Copy over the `index.js`, `meta.json`, `data.json` files from the skill-package.zip you created in homework 1.

Then edit the index.js to include the implementation of the action, by adding a new method to the class. The method should be called `do_` followed by the action name. It will receive as input an object with properties named after the action input parameters. On success, it should return an object wiht properties named after the action output parameters. On failure, it should throw an exception with an appropriate error code. See [instructions/nl-annotations.md](instructions/nl-annotations.md) for a discussion of error handling.

For example, if you want to add an action called `make_reservation` to the `index.js`, you can add the following lines inside the main class: 
```js
async do_make_reservation({ param1, param2, ... }, env) {
    // mock up code to make reservation ...
}
```

For this homework, you don't need to connect to a real API for your actions, only mock it up. Refer to [devices/uk.ac.cam.multiwoz.Restaurant/index.js](devices/uk.ac.cam.multiwoz.Restaurant/index.js) as an example.

### Step 4: generate the dataset and train

As before, you can now generate the dataset with `make -j datadir`, and train with `make -j train-user`. This time, you don't have a pretrained model, so you will need to train a model from scratch. Generating a dataset takes about 6 hours on a very fast machine with a lot of RAM, and training takes about 5 hours on a machine with a Nvidia V100 GPU.

### Step 5: test, rinse, repeat

After training, test your new dialogue agent with `./run-nlu-server.sh` and `./run-almond.sh` as in part 1.

You can also look at the tensorboard to see the performance of your model on the synthetic dev set.
To do so, run:
```bash
tensorboard --logdir $(experiment)/models # e.g., restaurant/models
```
and navigate to <http://127.0.0.1:6006>. You will see several plots who describe various metrics through training. The "almond\_dialogue\_nlu/em" plot (in the "almond\_dialogue\_nlu" section) is the main accuracy metric.

Your model should achieve higher than **95%** accuracy on the synthetic evaluation set.

**Optionally**, you can write a small evaluation set yourself and use `make evaluate`. See the restaurant example for the file format.

## Submission

Your submission should include a complete dialogue agent for a new domain. Package the whole starter code and all generated files (datasets, trained models, etc.) into a zip file or tarball, then upload it to [Stanford Box](https://stanford.account.box.com/). If you have multiple trained models and multiple versions of your dataset for your domain, only submit the best one.

All members of a group should submit the same text file on Canvas, and include the following information:
  - Name of the students in your group
  - A link to the uploaded file on Stanford box (make sure you choose "People in your company" when creating the shared link)
  - One example dialogue that you had with your agent (the agent does NOT need to understand you at every turn)

