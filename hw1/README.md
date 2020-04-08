# Homework 1
In this homework, you will build a toy question answering (QA) skill for the Almond virtual assistant on 
a domain of your choice using schema.org data from websites.
This workdir provides you a `Makefile` to help you run the scripts needed, as 
well as an example QA skill for the restaurant domain.

## Install dependencies
This homework requires `nodejs` (>=10.0), and `yarn` as a package manager. 
See [nodejs](https://nodejs.org/en/download/) and [yarn](https://classic.yarnpkg.com/en/docs/install/) for installation details. 
You can check your installation by running `node --version` and `yarn --version`.

In addition, you will need 2 libraries from OVAL: 
[genie-toolkit](https://github.com/stanford-oval/genie-toolkit), 
[almond-tokenizer](https://github.com/stanford-oval/almond-tokenizer).
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
docker run --name tokenizer -p 8888:8888 -e LANGUAGES=en stanfordoval/almont-tokenizer:latest
# the next time 
docker start tokenizer
```


## Configuration 

This workdir comes with a `Makefile` to help you run the scripts needed to build 
the QA skill. You will need to configure the following fields in the [`Makefile`](Makefile):

- `geniedir`: set this to the absolute path of where `genie-toolkie` is installed.
- `developer_key`: set this to your own developer key in Thingpedia. 
Follow this simple [instruction](instructions/almond-registration.md) to register as a Thingpedia developer, 
and get your developer key. 
- `access_token`: set this to your access token in Thingpedia. 
Again, see this [instruction](instructions/almond-registration.md) for where to find it.
- `owner`: set this either your sid, or your group name (letter, numbers, and `.` only; no space). 
This is used to name your device automatically, so we won't have conflicts among homeworks.

We also suggest that you to follow at least one of the [tutorials](https://almond.stanford.edu/doc/thingpedia-tutorial-hello-world.md) 
to learn the basics of Thingpedia skill development.



## An Example QA Skill: Restaurant
This work directory comes with a sample data for restaurants: [`./source-data/restaurants/sample.json`](source-data/restaurants/sample.json). 
It is similar to what you can crawl from yelp.com pages, which contain schema.org markups in the form of [`json-ld`](https://en.wikipedia.org/wiki/JSON-LD).

### Generate Manifest and Value Datasets
With this sample data you can simply run the following two commands under `hw1` directory to 
get a base manifest and a set of value datasets for your skill.

```bash
make restaurants/schema.tt
make restaurants/parameter-datasets.tsv
```

The first command, will call 3 commands `process-schemaorg`, `normalize-data`, `trim-class` in Genie. 
It takes the source data and check with the schema.org ontology (in `schema.jsonld`), and produce a Thingpedia manifest
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
A full documentation of different annotation types can be found [here](instructions/nl-annotations.md).

You can also update the `canonical` annotation of a function. By default, it's the same as the function name.
However, this is not always suitable. For example, if you are building a 
QA skill for dentists and scraping your data from Yelp. Yelp is not using `Dentist` class, instead, 
they use `LocalBusiness`. In this case, you can replace the `canonical` annotation for function `LocalBusiness`
to `dentist` in your `schema.tt`.

You can use Thingpedia website to edit the `schema.tt`. In the [device creation page](https://almond.stanford.edu/thingpedia/upload/create),
`manifest.tt` tab provides an online editor - including syntax highlighting, syntax error warning, which 
you might find helpful. 

After tweaking the annotations, you can run the following command to see what sentences will be generated with your canonical annotations.
Iterate your annotations until you are happy with you synthetic data. (Note that synthetic data won't be 
perfect, try to have as many variety as possible.)
```bash
make restaurants/synthetic-d5.tsv
```


## Create Your Own Skill
As we said, in this homework, you will work on a domain of your choice. 
You can find all schema.org domains at [here](https://schema.org/docs/full.html). Do not choose `Restaurant`.
Note that some schemas are more widely used than others. It might be hard to find web pages for some of the domains. 
Two tricks to find websites for a certain domain: 
- [Google Custom Search](https://cse.google.com/) allows you create a customized search engine which only search 
for pages using a given schema.org types.
- [Google Structural Data Testing Tool](https://search.google.com/structured-data/testing-tool/) 
can show you the schema.org types used in a given web page. 

We also provide you an example [crawler](scripts/data-crawler.py) to help you get data from websites.
The example shows how you can crawl data from Yelp. Install the dependencies and run it. 
```bash
pip3 install extruct requests bs4
python3 scripts/data-crawler.py
```
It will generate you a `yelp.json`, which should look similar to what we provided under `source-data/restaurants/sample.json`.

In the python script, set the `init_url`, `base_url` to the websites you want to crawl accordingly.
Set `target_size` to be at least 100.  
Note that different websites may have slight different structures, you might need to tweak the script to make it work. 
Follow the comments in the code to modify it. 

Once you decide your domain and collected data for it, create a new directory under `source-data/`, and 
put the data under that folder. 
Create a directory with the same name under `hw1`.

To allow the `Makefile` working on your own skill. You will need to update it by changing the following fields:

- `experiment`: change it to the directory name you created for your data file;
- `white_list`: change it the function you want to expose to the user. 

Then you can run the same command as shown in the restaurant example (replace "restaurants" with your directory name) 
to create your own QA skill.
Make sure you check the synthetic datasets, and iterate the annotations before you move to the next step.


## Submit your device to Thingpedia
Once you finished your `schema.tt` you can prepare your skill to upload to Thingpedia. 

First you will need to upload all the string and entity datasets under `$(your-folder-name)/parameter-datasets/` to Thingpedia.
Normally you will need to upload it through a web interface ([https://almond.stanford.edu/thingpedia/strings]() and [https://almond.stanford.edu/thingpedia/entities]()). 
But we have create a simple script for you to automatically upload all of them. 
Simply run
```bash
make upload-datasets
```
Check the Thingpedia [string dataset page](https://almond.stanford.edu/thingpedia/strings) 
and [entity dataset page](https://almond.stanford.edu/thingpedia/entities)
to make sure the datasets are successfully uploaded.

After uploading all the datasets, you can now upload your skill. 
Run the following command to pack your skill in a zip file.  
```bash
make skill-library.zip
```

Go to [Thingpedia skill creation page](https://almond.stanford.edu/thingpedia/upload/create).
Put in the metadata: 
- ID: the same as the one in `schema.tt` (should be in the form of `edu.stanford.cs294s.$(student-name-or-group-name)`)
- Name: a short name for your skill
- Description: describe your skill in a couple of sentences
- Category: choose "Service"
- License: MIT
- Check the box for "This license is GPL compatible"
- Leave website, source code repository, issue tracker empty
- Icon: choose a png file as the icon of your skill
- Zipfile: the `skill-library.zip` generated.

Copy your `schema.tt` to `manifest.tt`;
copy `emptydataset.tt` to `dataset.tt`;
Then click "create".

Once you skill is submitted, we will train the natural language overnight, but you can test it with ThingTalk directly. 
For example, type the following command in web almond to return all data you collected
(replace `xxx` with `owner`, `Restaurant` with your function name):
```
\t now => @edu.stanford.cs294.xxx.Restaurant() => notify;
```
Here `\t` indicates the system that this is a raw ThingTalk command, not natural language.

(Optional) You might notice the output looks terrible with one property at a time. 
You can actually define how the result should be formatted with annotation. 
For example, restaurant function can have the following annotation to display one sentence
to describe each restaurant.
```
#_[formatted=["${id}: ${aggregateRating.ratingValue} star ${servesCuisine} restaurant"]]
```
See this [instruction](https://almond.stanford.edu/doc/thingpedia-nl-support.md#output-format) for more details.


## Homework submission
Submit a simple text file to TA, and include the following information:
- A link to a private fork of the this repository containing the data you collected and `schema.tt` you generated and tuned.
- The domain you choose
- The website you use to collect your data
- All the changes you made to the automatically generated `schema.tt`
- A list of example questions that can be answered by your QA skill
