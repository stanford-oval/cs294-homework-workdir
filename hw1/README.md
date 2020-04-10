# Homework 1
In this homework, you will build a toy question answering (QA) skill for the Almond virtual assistant on 
a domain of your choice using schema.org data from a website of your choice.
This workdir provides you with a `Makefile` to help you run the scripts needed, as 
well as an example QA skill for the restaurant domain.

(The scripts have been tested on Fedora, Ubuntu, and Mac. Windows users can use 
[WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10), but using a Linux virtual machine is recommended.)

## Install dependencies
This homework requires `docker`, `nodejs` (>=10.0), and `yarn` as a package manager. 
See [docker](https://docs.docker.com/get-docker/), [nodejs](https://nodejs.org/en/download/) and [yarn](https://classic.yarnpkg.com/en/docs/install/) for installation details. 
You can check your installation by running `node --version` and `yarn --version`.

In addition, you will need 3 libraries from OVAL: 
[genie-toolkit](https://github.com/stanford-oval/genie-toolkit), 
[almond-tokenizer](https://github.com/stanford-oval/almond-tokenizer),
[thingpedia-cli](https://github.com/stanford-oval/thingpedia-cli).
`genie-toolkit` provides you tools to process schema.org data, generate manifest, and synthesize data. 
`thingpedia-cli` provides easy way to download data from and upload data to Thingpedia. 

Run the following command to install them: 
```bash
# install genie-toolkit
git clone https://github.com/stanford-oval/genie-toolkit.git
cd genie-toolkit
yarn

# install thingpedia-cli 
yarn global add thingpedia-cli
```

After installation, you should get a command called `thingpedia`.
If encounter `command not found`, make sure the Yarn global bin directory
(usually `~/.yarn/bin`) is in your PATH. You can find the path with the command
`yarn global bin`.

```bash
export PATH=~/.yarn/bin:$PATH
```

You also need a local tokenizer for process raw data. 
Run the following docker to deploy that. Make sure tokenizer is running when you do this homework.
```bash
# first time
docker run --name tokenizer -p 8888:8888 -e LANGUAGES=en stanfordoval/almond-tokenizer:latest
# the next time 
docker start tokenizer
```

If you are using Windows WSL, it might be painful to use docker. 
Instead you can run your tokenizer as follows:
```bash
# install almond-tokenizer
git clone https://github.com/stanford-oval/almond-tokenizer.git
cd almond-tokenizer
./pull-dependencies.sh # This will download ~2 GB data
JAVAHOME=$(path-to-java) ant
# e.g., JAVAHOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64 ant

LANGUAGES=en ./run.sh
```

## Configuration 

This workdir comes with a `Makefile` to help you run the scripts needed to build 
the QA skill. You will need to configure the following fields in the [`Makefile`](Makefile):

- `geniedir`: set this to the absolute path of where `genie-toolkit` is installed.
- `developer_key`: set this to your own developer key in Thingpedia. 
Follow these [instructions](instructions/almond-registration.md) to register as a Thingpedia developer, 
and get your developer key. 
- `access_token`: set this to your access token in Thingpedia. 
Again, see the [instructions](instructions/almond-registration.md) for where to find it.
- `owner`: set this either your sunetID, or your group name (letter, numbers, and `-` only; no spaces). 
This is used to name your device automatically, so we won't have conflicts among homeworks.

We also suggest that you to follow at least one of the [tutorials](https://almond.stanford.edu/doc/thingpedia-tutorial-hello-world.md) 
to learn the basics of Thingpedia skill development.



## An Example QA Skill: Restaurant
This work directory comes with sample data for restaurants: [`./source-data/restaurants/sample.json`](source-data/restaurants/sample.json). 
It is similar to what you can crawl from yelp.com pages, which contain schema.org markups in the form of [`json-ld`](https://en.wikipedia.org/wiki/JSON-LD).

### Generate Manifest and Value Datasets
With this sample data you can run the following two commands under `hw1` directory to 
get a base manifest and a set of value datasets for your skill.

```bash
make restaurants/schema.tt
make restaurants/parameter-datasets.tsv
```

The first command, will call 3 commands `process-schemaorg`, `normalize-data`, `trim-class` in Genie. 
It takes the source data, checks the schema.org ontology (in `schema.jsonld`), and produces a Thingpedia manifest
that only contains the subset of classes and properties in schema.org that are used in your source data. 
The result manifest is stored in `schema.tt`.

The second command will generate a `parameter-datasets` folder under `restaurants`, which contains the values 
for each property in source data. This will be used by Genie to generate natural sentence with real values. 
It also creates `parameter-datasets.tsv` that provides an index for the datasets. 


### Iterate Natural Language Annotations
The `schema.tt` contains the function signature of your skill. Each function has a list of parameters, and
each parameters has one or more canonical annotations. 
Note that we only offer very basic heuristics to automatically generate these annotations.
Therefore, to improve the natural language part for your skill, you need to tweak these annotations manually. 
A full documentation of the different annotation types can be found [here](instructions/nl-annotations.md).

NOTE: **all** natural language annotations must be lower case.

You can also update the `canonical` annotation of a function. By default, it's the same as the function name.
However, this is not always suitable. For example, if you are building a 
QA skill for dentists and scraping your data from Yelp. Yelp is not using the `Dentist` class, instead, 
they use `LocalBusiness`. In this case, you can replace the `canonical` annotation for function `LocalBusiness`
to `dentist` in your `schema.tt`.

You can use Thingpedia website to edit the `schema.tt`. In the [device creation page](https://almond.stanford.edu/thingpedia/upload/create),
`manifest.tt` tab provides an online editor - including syntax highlighting, syntax error warning, which 
you might find helpful.

<!--
You can also use the CLI to check for mistakes:
```
thingpedia lint-device --manifest restaurant/schema.tt --dataset restaurant/schema.tt
```
-->

After tweaking the annotations, you can run the following command to see what sentences will be generated with your canonical annotations.
Iterate your annotations until you are happy with you synthetic data. Note that synthetic data won't be 
perfect, so try to have as many variety as possible.
```bash
make restaurants/synthetic-d5.tsv
```

You can change `d5` to higher numbers (e.g. `d7`) to see sentences of different complexity (grammar derivation depth), at the cost of waiting longer. After you submit, your skill will generate the dataset at depth 7.

## Create Your Own Skill
As we said, in this homework, you will work on a domain of your choice. 
You can find all schema.org domains at [here](https://schema.org/docs/full.html). Do not choose `Restaurant` or `FoodEstablishment`.
Note that some schemas are more widely used than others. It might be hard to find webpages for some of the domains. 
Two tricks to find websites for a certain domain: 
- [Google Custom Search](https://cse.google.com/) allows you create a customized search engine which only search 
for pages using a given schema.org types.
- [Google Structured Data Testing Tool](https://search.google.com/structured-data/testing-tool/) 
can show you the schema.org types used in a given webpage.

If you have trouble finding a suitable webpage, you may select one from this list of example domains:
- Hotel [hotels.com](https://hotels.com)
- Housing (SingleFamilyResidence) [zillow.com](https://zillow.com)
- Product [ebay.com](https://ebay.com)
- Recipes [allrecipes.com](https://allrecipes.com)

We also provide you a [crawler](scripts/data-crawler.py) to help you get data from websites.
This example shows how you can crawl data from Yelp. Install the dependencies and run it. 
```bash
pip3 install extruct requests bs4
python3 scripts/data-crawler.py
```
It will generate you `yelp.json`, which should look similar to what we provided under `source-data/restaurants/sample.json`.

In the python script, set the `init_url` and `base_url` to the websites you want to crawl accordingly.
Set `target_size` to be at least 100.  
Note that different websites may have slightly different structures, so you might need to tweak the script to make it work. 
Follow the comments in the code to modify it. 

Once you have decided on your domain and collected data for it, create a new directory under `source-data/`, and 
put the data under that folder. Use only alphanumeric characters for this directory, without any special character (including `_` or `-`).
Create a directory with the same name under `hw1`.

To allow the `Makefile` working on your own skill. You will need to update it by changing the following fields:

- `experiment`: change it to the directory name you created for your data file;
- `white_list`: change it the function you want to expose to the user. 

Then you can run the same command as shown in the restaurant example (replace "restaurants" with your directory name) 
to create your own QA skill.
Make sure you check the synthetic datasets, and iterate the annotations before you move to the next step.


## Submit your skill to Thingpedia
Once you finished your `schema.tt` you can prepare your skill to upload to Thingpedia.

NOTE: In Thingpedia parlance, a skill is called a "device", and this is reflected in CLI and in URLs.

First, you will need to upload a "dummy" empty skill. Doing so will let you "take ownership" of the skill ID, and will let you upload the string and entity datasets.

Go to [Thingpedia skill creation page](https://almond.stanford.edu/thingpedia/upload/create), which you can find from your [Developer Console](https://almond.stanford.edu/developers).
Put in the metadata: 
- ID: the same as the one in `schema.tt` (should be in the form of `edu.stanford.cs294s.$(student-name-or-group-name)`)
- Name: a short name for your skill, which is also optionally used to call your skill from Almond (to resolve ambiguity)
- Description: describe your skill in a couple of sentences
- Category: choose "Service" (or an appropriate category for your domain)
- License: MIT
- Check the box for "This license is GPL compatible"
- Leave website, source code repository, issue tracker empty
- Icon: choose a png file as the icon of your skill
- Zipfile: leave empty for now.
- On the `manifest.tt` tab, enter:
  ```
  class @edu.stanford.cs294s.<student-name-or-group-name> {
     import loader from @org.thingpedia.generic_rest();
     import config from @org.thingpedia.config.none();
  }
  ```
- On the `dataset.tt` tab, enter:
  ```
  dataset @edu.stanford.cs294s.<student-name-or-group-name> {}
  ```

Click "Create" at the top and go back to your developer console.

Then you will need to upload all the string and entity datasets under `$(your-folder-name)/parameter-datasets/` to Thingpedia.
Normally you will need to upload it through a web interface ([https://almond.stanford.edu/thingpedia/strings]() and [https://almond.stanford.edu/thingpedia/entities]()). 
But we have a script for you to automatically upload all of them. 
Run
```bash
make upload-datasets
```
Check the Thingpedia [string dataset page](https://almond.stanford.edu/thingpedia/strings) 
and [entity dataset page](https://almond.stanford.edu/thingpedia/entities)
to make sure the datasets are successfully uploaded.

After uploading all the datasets, you can now upload the real version of your skill. 
Run the following command to pack your skill in a zip file.  
```bash
make skill-library.zip
```

Then go to your developer console, and click "Update" next to the previously uploaded skill.
Upload the just generate zip file in the "Zipfile" field, and copy the real `schema.tt` to `manifest.tt`.
Then click "Save" at top.

Once you skill is submitted, we will train the natural language overnight, but you can test it with ThingTalk directly. 
For example, type the following command in web almond to return all data you collected
(replace `xxx` with `owner`, `Restaurant` with your function name):
```
\t now => @edu.stanford.cs294.xxx.Restaurant() => notify;
```
Here `\t` indicates the system that this is a raw ThingTalk command, not natural language.

(Optional) You might notice the output looks terrible with one property at a time. 
You can actually define how the result should be formatted with an appropriate function annotation. 
For example, restaurant function can have the following annotation to display one sentence
to describe each restaurant.
```
#_[formatted=["${id}: ${aggregateRating.ratingValue} star ${servesCuisine} restaurant"]]
```
See this [guide](https://almond.stanford.edu/doc/thingpedia-nl-support.md#output-format) for more details.


## Homework submission
All members of a group should submit the same text file on Canvas, and include the following information:
- Name of the students in your group
- A link to the private copy of this repository containing the data you collected and `schema.tt` you generated and tuned
- The domain you chose
- The website you used to collect your data
- A list of the changes you made to the automatically generated `schema.tt`
- A list of example questions that can be answered by your QA skill
