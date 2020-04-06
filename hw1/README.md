# Homework 1
In this homework, you will build a toy question answering (QA) skill for the Almond virtual assistant on 
a domain of your choice using schema.org data from websites.
This workdir provides you a `Makefile` to help you run the scripts needed, as 
well as an example QA skill for the restaurant domain.

## Install dependencies
This homework requires `java`, `nodejs` (>=10.0), and `yarn` as a package manager. 
Follow the guide from their websites to install them on your local machine. See [nodejs](https://nodejs.org/en/download/) and [yarn](https://classic.yarnpkg.com/en/docs/install/) for installation details. You can check your installation by running `node --version` and `yarn --version`.

In addition, you will need 3 libraries from OVAL: 
[genie-toolkit](https://github.com/stanford-oval/genie-toolkit), 
[almond-tokenizer](https://github.com/stanford-oval/almond-tokenizer),
and [thingpedia-cli](https://github.com/stanford-oval/thingpedia-cli). 

Follow their own instructions to install `almond-tokenizer` and `thingpedia-cli`, 
and for `genie-toolkit`, we would like you to clone the Github directly. 
Make sure you run `yarn` after cloning. 


## Configuration 
Follow this simple [instruction](instructions/almond-registration.md) to register as a Thingpedia developer, and get your developer key. 
We also suggests you to follow at least one of the tutorials to learn the basics of Thingpedia development.

This workdir comes with a `Makefile` to help you run the scripts needed to build 
the QA skill. You will need to configure the following field in the `Makefile`:

- `geniedir`: set this to the path to where you installed `genie-toolkie`.
- `developer_key`: set this to your own developer key in Thingpedia. 


Before you move on, make sure you keep your tokenizer running in the background: go to `almond-tokenizer` directory and run
```bash
LANGUAGES=en ./run.sh
```


## An Example QA Skill: Restaurant
This workdir comes with a sample data for restaurants: `./source-data/restaurants/sample.json`. 
It is similar to what you can get from Yelp pages, where it contains schema.org markups in the form of `json-ld`.

With this sample data you can simply run the following two commands under `hw1` directory to 
get a manifest, and a set of value datasets for your skill.

```bash
make restaurants/schema.tt
make restaurants/parameter-datasets.tsv
```

The `schema.tt` contains the function signature of your skill. Each function has a list of parameters. 
And each parameters has one or more canonical annotations. 
Note that we only offer very basic heuristic to generate these annotations.
So to improve the natural language for your skill, you need to tweak these annotations manually. 
A full documentation of different annotation types can be found [here](instructions/nl-annotations.md).

You can run the following command to see what sentences will be generated with your canonical annotations.
Iterate your annotations until you are happy with you synthetic data. (Note that synthetic data won't be 
perfect, try to have as many variety as possible.)
```bash
make restaurants/synthetic-d5.tsv
```


## Create Your Own Skill
As we said, in this homework, you will work on a domain of your choice. 
You can find all schema.org domains at [here](https://schema.org/docs/full.html). Do not choose `Restaurant`.
Note that some schemas are more widely used than others. It might be hard to find some of the domains. 
To identify schema.org data in web pages. You can use this [tool from Google](https://search.google.com/structured-data/testing-tool/).

We also provide you an example [crawler](data-crawler/crawler.py) to help you get data from websites.
The example shows how you can crawl the data from Yelp. Set the `init_url` and `base_url` to the websites you want to crawl accordingly. 
Note that difference website may have slight different structure, you might need to tweak the scripts a little bit to make it work. 
Hopefully the comments in the code makes it simple to understand and easy to modify. 

Once you decide your domain and collected the data for it, You can update the 
`Makefile`: change `experiment` to the folder name you created for your data file;
change `class_name` to the domain name in [schema.org](https://schema.org);
and set `white_list` to the table names in `schema.tt` you would like query about.

Then you can run the same command as shown in the restaurant example to create your own QA skill.


## Submit your device to Thingpedia
Once you finished your `schema.tt` you can prepare your skill to upload to Thingpedia. 

First you will need to upload all the string set and entities under `$(your-folder-name)/parameter-datasets/` to Thingpedia.
You can find the portal to upload them at [https://almond.stanford.edu/thingpedia/strings]() and [https://almond.stanford.edu/thingpedia/entities](). 
(we probably should recommend using command line tool for uploading?)

Then, you can upload your skill. To do so, simply run 
```bash
make skill-library.zip
```
Then fill in the metadata of your skill, upload the zip file, upload an icon you like,
copy your `schema.tt`, and `emptydataset.tt` to the online editor, then click "create".

Once you skill is submitted, we will train the natural language overnight, but you can test it with ThingTalk directly. 
For example, type the following command in web almond to return all data you collected (replace `Restaurant` with you class name):
```
\t now => @org.schema.Restaurant.Restaurant() => notify;
```


## Homework submission
Submit a simple text file to include the following information:

- A link to a private fork of the this repository containing the data you collected and `schema.tt` you generated and tuned.
- The domain you choose
- The website you use to collect your data
- All the changes you made to the automatically generated `schema.tt`
- A list of example questions that can be answered by your QA skill
