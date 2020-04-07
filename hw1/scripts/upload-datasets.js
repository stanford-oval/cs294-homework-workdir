// -*- mode: js; indent-tabs-mode: nil; js-basic-offset: 4 -*-
//
// This file is part of Genie
//
// Copyright 2020 The Board of Trustees of the Leland Stanford Junior University
//
// Author: Silei Xu <silei@cs.stanford.edu>
//
// See COPYING for details
"use strict";

const fs = require('fs');
const child_process = require('child_process');
const meta = require(`../skill-package/meta.json`);

const [experiment, className, developerKey, accessToken] = process.argv.slice(2);

function uploadString(stringId, path) {
    console.log(`upload string: ${stringId}`)
    const args = [
        '--url',
        'https://almond.stanford.edu/thingpedia',
        '--developer-key',
        developerKey,
        '--access-token',
        accessToken,
        'upload-string-values',
        '--preprocessed', 
        '--type-name',
        stringId,
        '--name',
        stringId,
        path
    ];
    const process = child_process.spawn(`thingpedia`, args);
}

function uploadEntity(entityId, path) {
    console.log(`upload entity: ${entityId}`);
    const args = [
        '--url',
        'https://almond.stanford.edu/thingpedia',
        '--developer-key',
        developerKey,
        '--access-token',
        accessToken,
        'upload-entity-values',
        '--entity-id',
        entityId,
        '--entity-name',
        entityId,
    ];
    if (path) {
        args.push('--json');
        args.push(path);
    } else {
        args.push('--no-ner-support')
    }
    const process = child_process.spawn(`thingpedia`, args);
}


function main() {
    const uploadedEntities = new Set();
    for (let file of fs.readdirSync(`${experiment}/parameter-datasets/`)) {
        if (file.endsWith('.json')) {
            let entityId = file.slice(0, - '.json'.length);
            let query = file.slice(className.length + 1, - '.json'.length);
            uploadEntity(entityId, `${experiment}/parameter-datasets/${file}`);
            uploadedEntities.add(query);
        } else if (file.endsWith('.tsv')) {
            let stringId = file.slice(0, - '.tsv'.length);
            uploadString(stringId, `${experiment}/parameter-datasets/${file}`);
        }
    }

    for (let query in meta) {
        if (!uploadedEntities.has(query)) {
            uploadEntity(`${className}:${query}`);
        }
    }
}

main();


