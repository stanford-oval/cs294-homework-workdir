// -*- mode: js; indent-tabs-mode: nil; js-basic-offset: 4 -*-
//
// Copyright 2020 The Board of Trustees of the Leland Stanford Junior University
//
// Permission is hereby granted, free of charge, to any person obtaining a
// copy of this software and associated documentation files (the
// "Software"), to deal in the Software without restriction, including
// without limitation the rights to use, copy, modify, merge, publish,
// distribute, sublicense, and/or sell copies of the Software, and to
// permit persons to whom the Software is furnished to do so, subject to
// the following conditions:
//
// The above copyright notice and this permission notice shall be included
// in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
// OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
// IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
// CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
// TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
// SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.//
"use strict";

const Tp = require('thingpedia');

const data = require('./restaurant_db.json');

module.exports = class MultiwozDevice extends Tp.BaseDevice {
    get_Restaurant() {
        // return everything, let ThingTalk deal with it
        return data.map((restaurant) => {
            // fix the type of restaurant.id
            const obj = {};
            Object.assign(obj, restaurant);
            obj.id = new Tp.Value.Entity(restaurant.id.value, restaurant.id.display);
            return obj;
        });
    }

    async do_make_reservation({ restaurant, book_time, book_day, book_people }, env) {
        // make the reservation ...
        let successful = true;
        if (successful) {
            return {
                reference_number: 'XXXXX'
            };
        } else {
            throw new Error(`no tables available`);
        }
    }
}
