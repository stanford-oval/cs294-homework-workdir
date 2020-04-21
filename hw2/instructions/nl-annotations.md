# Dialogue Specific Natural Language Annotations

In Homework 1, you learned how to use annotations to describe database fields in Question Answering.
In this homework, you will learn new annotations that can be used to make your dialogues more natural in Genie.

Some annotations are _optional_. If you do not provide them, Genie will generate a templatized sentence
based on the parameter-level annotations, but the sentence might be more clunky. Try generating the dataset without
any of the optional annotations first, to see the default templates. Maybe you won't need the annotations in your domain!

NOTE: **all annotations must be lower case**.

## string values

This annotation is **required** for String-type parameters. 

Use the `#_[string_values]` annotation to indicate a string dataset containing example values for the parameter. 

```
in req name: String #_[string_values="tt:person_full_name"] 
```

## prompt

This annotation is applied to _input parameters_ and _output parameters_. This annotation is **optional**.

Use the `#_[prompt]` annotation to contain a question that the agent will use to ask the user to fill a
parameter. For example:

```
out food : String #_[prompt=["what are you in the mood for", "what food do you fancy"]]
```

Do not include the "?" mark in the question. This way, questions can be combined to ask for two parameters
at once: "what food do you fancy and what area of the city would you like".

## result

This annotation is applied to _queries_ and _actions_. This annotation is **optional**.

Use the `#_[result]` annotation to describe a single result from your search, or to describe the result of
your action. The result annotation can use placeholders, using the syntax "$" followed by the name of an **output**
parameter (similar to bash variables).

Example for a query:
```
query restaurant(...)
#_[result=["${id} is a ${price_range} restaurant that serves ${food} cuisine",
   "i found ${id} , a ${price_range} restaurant"]]
```

Example for an action:
```
action make_reservation(...)
#_[result=["your reservation is confirmed , and your code is ${reservation_code}"]]
```

The `result` should be a full phrase uttered by the agent. For queries, the templates will optionally add
an action offer (such as "would you like to reserve it?"). You should not include it in the annotation.

## on_error

This annotation is applied to _action_. This annotation is **required**.

The `#_[on_error]` annotation should be an object literal mapping an error code (an arbitrary identifier) to one or
more phrases describing the error. The annotation can use placeholders, using the syntax "$" followed by the name of
an **input** parameter (similar to bash variables).

Example:

```
action make_reservation(...)
#_[on_error={
  no_slot_available=["there are no tables available on ${book_day} at ${book_time}",
                     "the restaurant is already full on ${book_day} at ${book_time}"],
  closed=["the restaurant is closed on ${book_day}"]
}]
```

Your error message should not include any preamble such as "sorry", and should not include any offer to change
parameters. Both of those elements will be added automatically by the templates.

At runtime, your action code should throw an exception with the `code` parameter containing the error code.
Example:

```javascript
do_make_reservation({ book_day, book_time }) {
  if (isAHoliday(book_day)) {
    const err = new Error(`${book_day} is a holiday.`);
    err.code = 'closed';
    throw err;
  }
  if (!findSlot(book_day, book_time)) {
    const err = new Error(`no reservation available.`);
    err.code = 'no_slot_available';
    throw err;
  }
  ...
}
```

If the error code is recognized, the error message is logged but not displayed to the user. Otherwise, it's
assumed that the error is some unexpected condition (such as a programmer error or a network error) and the message
is displayed to the user.
