geniedir ?= ./genie-toolkit
thingpedia_cli ?= thingpedia

memsize := $(shell echo $$(($$(grep MemTotal /proc/meminfo | sed 's/[^0-9]//g')/3000-2500)))
parallel := $(shell echo $$(($$(grep processor /proc/cpuinfo | wc -l)-1)))
genie = node --experimental_worker --max_old_space_size=$(memsize) $(geniedir)/tool/genie.js

##### BEGIN EDIT HERE to set your developer key #####
thingpedia_developer_key =
##### END EDIT HERE #####

##### BEGIN EDIT HERE to configure your experiments #####
# for HW2, you should have one experiment called "restaurant", and one experiment with the domain
# you choose
# (the experiment name must be alphanumeric only, no special characters allowed, including _, + or -)
# you can also reuse this Makefile for your class project

# set this when you run "make" to change which experiment your running
# e.g. "make experiment=foo datadir"
experiment ?= restaurant
all_experiments = restaurant

# edit here if you have paraphrase data
# (you don't for the homework, but you might in the project)
restaurant_paraphrase_user ?=
restaurant_paraphrase_agent ?=
# edit here if you make another evaluation set
restaurant_test_sets = eval
# which models to evaluate on the dev set (called "eval")?
restaurant_eval_nlu_models = pretrained

# if you add another evaluation set, e.g. "test",
# make a folder called "restaurant/test" containing "annotated.txt" with the annotated dialogues
# then add a line "restaurant_test_nlu_models = " with the models you want to evaluate on that set

# when you add the new experiment, replicate all lines above with the new experiment name

##### END EDIT HERE #####

# the following variables are for command-line use:

# which model to train:
# (set as: `make train model=2`)
model ?= 1
# which dataset to evaluate on: eval (dev) or test
# (set as: `make evaluate eval_set=test`)
eval_set ?= eval

# you should edit below only if you wish to change the generation or training parameters

template_file ?= thingtalk/en/dialogue.genie
dataset_file ?= $(experiment)/dataset.tt
synthetic_flags ?= \
	dialogues \
	multifilters \
	nostream \
	notablejoin \
	projection \
	projection_with_filter \
	schema_org \
	undefined_filter

target_pruning_size ?= 50
minibatch_size ?= 5000
target_size ?= 15000
subdatasets ?= 1 2 3 4 5
max_turns ?= 6

generate_flags = $(foreach v,$(synthetic_flags),--set-flag $(v)) --target-pruning-size $(target_pruning_size) --max-turns $(max_turns) --maxdepth 9
custom_gen_flags ?=

schema_deps = $(experiment)/schema.tt $(experiment)/entities.json
template_deps = \
	$(geniedir)/languages/thingtalk/*.js \
	$(geniedir)/languages/thingtalk/*.genie \
	$(geniedir)/languages/thingtalk/en/*.genie \
	$(geniedir)/languages/thingtalk/en/dlg/*.genie

evalflags ?=

train_nlu_flags ?= \
	--train_iterations=40000 \
	--dimension=150 \
	--transformer_hidden=150 \
	--seq2seq_encoder=Coattention \
	--context_embeddings= \
	--question_embeddings=bert-base-uncased \
	--trainable_encoder_embeddings=50 \
	--train_context_embeddings \
	--trainable_decoder_embeddings=50 \
	--decoder_embeddings= \
	--transformer_layers=4 \
	--rnn_layers=1 \
	--train_batch_tokens=9000 \
	--transformer_lr_multiply=0.5
custom_train_nlu_flags ?=


#######################################################
########## Do not change anything below here ##########
#######################################################

GENIE_TOKENIZER_ADDRESS = cs294s-tokenizer.almond.stanford.edu:8888

all: datadir

.PHONY: all evaluate train-user train-agent clean mostlyclean
.SECONDARY:

emptydataset.tt:
	echo 'dataset @empty {}' > $@

$(experiment)/synthetic-%.txt : $(schema_deps) $(dataset_file) $(template_deps)
	$(genie) generate-dialogs \
	  --locale en-US --target-language dlgthingtalk \
	  --template $(geniedir)/languages/$(template_file) \
	  --thingpedia $(experiment)/schema.tt --entities $(experiment)/entities.json --dataset $(dataset_file) \
	  -o $@.tmp -f txt $(generate_flags) --debug $(custom_gen_flags) --random-seed $@ \
	  -n $(target_size) -B $(minibatch_size)
	mv $@.tmp $@

$(experiment)/synthetic.txt: $(foreach v,$(subdatasets),$(experiment)/synthetic-$(v).txt)
	cat $^ > $@

$(experiment)/synthetic.user.tsv : $(experiment)/synthetic.txt $(schema_deps)
	GENIE_TOKENIZER_ADDRESS=$(GENIE_TOKENIZER_ADDRESS) \
	$(genie) dialog-to-contextual \
	  --locale en-US --target-language dlgthingtalk \
	  --thingpedia $(experiment)/schema.tt --side user --flags S \
	  -o $@.tmp $<
	mv $@.tmp $@

$(experiment)/synthetic.agent.tsv : $(experiment)/synthetic.txt $(schema_deps)
	GENIE_TOKENIZER_ADDRESS=$(GENIE_TOKENIZER_ADDRESS) \
	$(genie) dialog-to-contextual \
	  --locale en-US --target-language dlgthingtalk \
	  --thingpedia $(experiment)/schema.tt --side agent --flags S \
	  -o $@.tmp $<
	mv $@.tmp $@

#paraphrase-%.tsv : mturk-batches/Batch_%_batch_results.csv $(experiment)/schema.tt
#	GENIE_USE_TOKENIZER=local $(genie) mturk-validate -o $@ --thingpedia $(experiment)/schema.tt --paraphrasing-input $< --validation-threshold 0 --paraphrasing-rejects mturk-batches/reject-$*.csv --debug

shared-parameter-datasets.tsv:
	$(thingpedia_cli) --url https://almond.stanford.edu/thingpedia --developer-key $(thingpedia_developer_key) --access-token invalid \
	  download-entity-values --manifest $@ --append-manifest -d shared-parameter-datasets
	$(thingpedia_cli) --url https://almond.stanford.edu/thingpedia --developer-key $(thingpedia_developer_key) --access-token invalid \
	  download-string-values --manifest $@ --append-manifest -d shared-parameter-datasets

$(experiment)/augmented.user.tsv : $(experiment)/synthetic.user.tsv $($(experiment)_paraphrase_user) shared-parameter-datasets.tsv
	$(genie) augment -o $@.tmp \
	  --locale en-US --target-language dlgthingtalk --contextual \
	  --thingpedia $(experiment)/schema.tt --parameter-datasets shared-parameter-datasets.tsv \
	  --synthetic-expand-factor 5 --quoted-paraphrasing-expand-factor 60 --no-quote-paraphrasing-expand-factor 20 --quoted-fraction 0.0 \
	  --no-debug $($(experiment)_paraphrase_user) $(experiment)/synthetic.user.tsv --parallelize $(parallel)
	mv $@.tmp $@

# NOTE: there is no augmentation of agent sentences! The agent network (NLG) operates with QUOTED tokens exclusively

datadir/agent: $(experiment)/synthetic.agent.tsv
	mkdir -p $@
	cp $(experiment)/synthetic.agent.tsv $@/
	$(genie) split-train-eval \
	  --locale en-US --contextual \
	  --train $@/train.tsv \
	  --eval $@/eval.tsv \
	  --split-strategy context-and-program \
	  --eval-on-synthetic \
	  --eval-probability 0.1 \
	  --random-seed $@ $<
	touch $@

datadir/user: $(experiment)/augmented.user.tsv
	mkdir -p $@
	cp $(experiment)/synthetic.user.tsv $@/
	$(genie) split-train-eval \
	  --locale en-US --contextual \
	  --train $@/train.tsv \
	  --eval $@/eval.tsv \
	  --split-strategy raw-sentence \
	  --eval-on-synthetic \
	  --eval-probability 0.1 \
	  --random-seed $@ $<
	touch $@

datadir: datadir/agent datadir/user
	cp $(experiment)/synthetic.txt $@/
	touch $@

clean:
	for exp in $(all_experiments) ; do \
		rm -rf $$exp/synthetic* $$exp/data.json $$exp/parameter-datasets* $$exp/everything* $$exp/constants.tsv ; \
	done

mostlyclean:
	for exp in $(all_experiments) ; do \
		rm -rf $$exp/synthetic* $$exp/data.json $$exp/parameter-datasets* $$exp/everything* $$exp/constants.tsv ; \
	done

$(experiment)/$(eval_set)/agent.tsv : $(experiment)/$(eval_set)/annotated.txt $(schema_deps)
	GENIE_TOKENIZER_ADDRESS=$(GENIE_TOKENIZER_ADDRESS) \
	$(genie) dialog-to-contextual \
	  --locale en-US --target-language dlgthingtalk --no-tokenized \
	  --thingpedia $(experiment)/schema.tt --side agent --flags E \
	  -o $@.tmp $<
	mv $@.tmp $@

$(experiment)/$(eval_set)/user.tsv : $(experiment)/$(eval_set)/annotated.txt $(schema_deps)
	GENIE_TOKENIZER_ADDRESS=$(GENIE_TOKENIZER_ADDRESS) \
	$(genie) dialog-to-contextual \
	  --locale en-US --target-language dlgthingtalk --no-tokenized \
	  --thingpedia $(experiment)/schema.tt --side user --flags E \
	  -o $@.tmp $<
	mv $@.tmp $@

train-user: datadir
	mkdir -p $(experiment)/models/$(model)
	ln -sf . datadir/almond
	genienlp train \
	  --data datadir \
	  --embeddings .embeddings \
	  --save $(experiment)/models/$(model) \
	  --tensorboard_dir $(experiment)/models/$(model) \
	  --cache datadir/.cache \
	  --train_tasks almond_dialogue_nlu \
	  --preserve_case \
	  --save_every 1000 \
	  --log_every 100 \
	  --val_every 1000 \
	  --exist_ok \
	  --skip_cache \
	  $(train_nlu_flags) \
	  $(custom_train_nlu_flags)

train-agent: datadir
	mkdir -p $(experiment)/models/$(model)
	ln -sf . datadir/almond
	genienlp train \
	  --data datadir \
	  --embeddings .embeddings \
	  --save $(experiment)/models/$(model) \
	  --tensorboard_dir $(experiment)/models/$(model) \
	  --cache datadir/.cache \
	  --train_tasks almond_dialogue_nlg \
	  --preserve_case \
	  --save_every 1000 \
	  --log_every 100 \
	  --val_every 1000 \
	  --exist_ok \
	  --skip_cache \
	  $(train_nlg_flags) \
	  $(custom_train_nlg_flags)

evaluate: $(foreach v,$($(experiment)_$(eval_set)_nlu_models),$(experiment)/$(eval_set)/$(v).nlu.results)
	for f in $^ ; do echo $$f ; cat $$f ; done

$(experiment)/$(eval_set)/%.nlu.results: $(experiment)/models/%/best.pth $(experiment)/$(eval_set)/user.tsv $(experiment)/schema.tt
	GENIE_TOKENIZER_ADDRESS=$(GENIE_TOKENIZER_ADDRESS) \
	$(genie) evaluate-server --contextual \
	  --url "file://$(abspath $(dir $<))" \
	  --thingpedia $(experiment)/schema.tt \
	  $(experiment)/$(eval_set)/user.tsv \
	  --debug --csv-prefix $(eval_set) --csv $(evalflags) \
	  -o $@.tmp | tee $(experiment)/$(eval_set)/$*.nlu.debug
	mv $@.tmp $@
