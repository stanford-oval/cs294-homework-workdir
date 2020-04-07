# Homework 1
In this homework, you will build a toy question answering (QA) skill for the Almond virtual assistant on 
a domain of your choice using schema.org data from websites.
This workdir provides you a `Makefile` to help you run the scripts needed, as 
well as an example QA skill for the restaurant domain.

## Install dependencies
This homework requires `java`, `nodejs` (>=10.0), and `yarn` as a package manager. 
Follow the guide from their websites to install them on your local machine. 
See [nodejs](https://nodejs.org/en/download/) and [yarn](https://classic.yarnpkg.com/en/docs/install/) for installation details. 
You can check your installation by running `node --version` and `yarn --version`.

In addition, you will need 3 libraries from OVAL: 
[genie-toolkit](https://github.com/stanford-oval/genie-toolkit), 
[almond-tokenizer](https://github.com/stanford-oval/almond-tokenizer),
and [thingpedia-cli](https://github.com/stanford-oval/thingpedia-cli). 

Run the following command to install them: 
```bash
# install genie-toolkit
git clone git@github.com:stanford-oval/genie-toolkit.git
cd genie-toolkit
yarn
cd ..

# install almond-tokenizer
git clone git@github.com:stanford-oval/almond-tokenizer.git
cd almond-tokenizer
./pull-dependencies.sh
JAVAHOME=$(path-to-java) ant
# e.g., JAVAHOME=/usr/lib/jvm/openjdk-1.8.0 ant

# install thingpedia-cli 
yarn global add thingpedia-cli
```

After installation, you should get a command called `thingpedia`.
If encounter `command not found`, make sure the Yarn global bin directory
(usually `~/.yarn/bin`) is in your PATH. You can find the path with the command
`yarn global bin`.


## Configuration 

This workdir comes with a `Makefile` to help you run the scripts needed to build 
the QA skill. You will need to configure the following field in the `Makefile`:

- `geniedir`: set this to the path to where your `genie-toolkie` is installed.
- `developer_key`: set this to your own developer key in Thingpedia. 
Follow this simple [instruction](instructions/almond-registration.md) to register as a Thingpedia developer, 
and get your developer key. 
- `access_token`: set this to your access token in Thingpedia. 
Again, see this [instruction](instructions/almond-registration.md) for where to find it.
- `owner`: set this either your sid, or your group name (no space, letter, numbers, and `.` only)

We also suggests you to follow at least one of the [tutorials](https://almond.stanford.edu/doc/thingpedia-tutorial-hello-world.md) 
to learn the basics of Thingpedia skill development.


Before you move forward, make sure you keep your tokenizer running in the background: 
go to `almond-tokenizer` directory and run
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

You can also update the `canonical` annotation of a function. By default, it's the same as the function name.
However, this is not always suitable. For example, if you are building a 
QA skill for dentists and scraping your data from Yelp. Yelp is not using `Dentist` class, instead, 
they use `LocalBusiness`. In this case, you can replace the `canonical` annotation for function `LocalBusiness`
to `dentist` in your `schema.tt`.

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
Two tricks to find websites of a certain domain: 
- [Google Custom Search](https://cse.google.com/) allows you create a customized search engine which only search 
for pages using a given schema.org types. 
- [Google Structural Data Testing Tool](https://search.google.com/structured-data/testing-tool/) 
can show you the schema.org types in given web page. 

We also provide you an example [crawler](scripts/data-crawler.py) to help you get data from websites.
The example shows how you can crawl the data from Yelp. Install the following dependencies and run it. 
```bash
pip3 install extruct requests bs4 --user
python3 scripts/data-crawler.py
```
It will generate you `yelp.json`, which should look similar to what we provided under `source-data/restaurants/sample.json`.

Set the `init_url`, `base_url` to the websites you want to crawl accordingly.
Set `target_size` to be at least 100.  
Note that difference website may have slight different structure, you might need to tweak the scripts a little bit to make it work. 
Hopefully the comments in the code makes it simple to understand and easy to modify. 


Once you decide your domain and collected the data for it, create a new directory under `source-data/`, and 
put the collected data under that folder. 
Create a directory with the same name under `hw1`.

To allow the `Makefile` working on your own skill. You will update it by changing the following fields:

- `experiment`: change it to the directory name you created for your data file;
- `white_list`: change it the function you want to expose to the user. 

Then you can run the same command as shown in the restaurant example (replace "restaurants" with your directory name) 
to create your own QA skill.


## Submit your device to Thingpedia
Once you finished your `schema.tt` you can prepare your skill to upload to Thingpedia. 

First you will need to upload all the string set and entities under `$(your-folder-name)/parameter-datasets/` to Thingpedia.
Normally you will need to upload it through a web interface ([https://almond.stanford.edu/thingpedia/strings]() and [https://almond.stanford.edu/thingpedia/entities]()). 
But we have create a simple scripts for you to automatically upload all of them. 
Simply run
```bash
make upload-datasets
```
Check the Thingpedia [string dataset page](https://almond.stanford.edu/thingpedia/strings) 
and [entity dataset page](https://almond.stanford.edu/thingpedia/entities).
Make sure the datasets are successfully uploaded.

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
- Category: choose "Media"
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


## Homework submission
Submit a simple text file to TA, and include the following information:
- A link to a private fork of the this repository containing the data you collected and `schema.tt` you generated and tuned.
- The domain you choose
- The website you use to collect your data
- All the changes you made to the automatically generated `schema.tt`
- A list of example questions that can be answered by your QA skill
