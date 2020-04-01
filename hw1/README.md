# Homework 1
In this homework, you will build a toy QA skill for Almond virtual assistant on 
a domain of your choice using schema.org data from websites.
This workdir provides you a `Makefile` to help you run the scripts needed, as 
well as an example QA skill for restaurant domain.

## Acquiring dependencies
This homework requires `nodejs` (>=8.0), and `yarn` as a package manager. 
Follow the guide from their own websites to install them on your local machine.

In addition to that, you will need 3 libraries: 
[genie-toolkit](https://github.com/stanford-oval/genie-toolkit), 
[almond-tokenizer](https://github.com/stanford-oval/almond-tokenizer),
and [thingpedia-cli](https://github.com/stanford-oval/thingpedia-cli). 

Follow their own instructions to install `almond-tokenizer` and `thingpedia-cli`, 
and for `genie-toolkit`, we would like you to clone the Github directly. 
Make sure you run `yarn` after cloning. 


## Configuration 
This workdir comes with a `Makefile` to help you run the scripts needed to build 
the QA skill. You will need to configure the following field in the `Makefile`:

- `geniedir`: set this to the path to where you installed `genie-toolkie`.
- `developer_key`: set this to your own developer key in Thingpedia. 


## An Example Domain: Restaurant
This workdir comes with a sample data for restaurants: `./source-data/restaurants/sample.json`

```bash
make restaurants/schema.tt
make restaurants/parameter-datasets.tsv
```

You can tweak the property types and canonical annotations manually. 

Run the following command to what sentences will be generated with your canonical annotations.
```bash
make restaurants/synthetic-d5.tsv
```

## Collect your own data
TODO

Once you decide your domain and collected the data for it, You can update the 
`Makefile`: change `experiment` to the folder name you created for your data file;
change `class_name` to the domain name in [schema.org](https://schema.org);
and set `white_list` to the table names in `schema.tt` you would like to include 
when generating synthetic sentences.


## Submit your device to Thingpedia
Once you are finished, you can submit your QA skill to Thingpedia and test it with our
web interface. 
We will train the natural language overnight, but you can test it with ThingTalk directly. 

## Homework submission
Submit a simple text file to include the following information:

- The domain you choose
- The website you use to collect your data
- A link to a private fork of the this repository containing the data you collected and `schema.tt` you generated and tuned.
- All the changes you made to the automatically generated `schema.tt`
- A list of example questions can be answered by your QA skill
