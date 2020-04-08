# Natural Language Annotations for Properties

In ThingTalk, each parameter can have multiple natural language annotations
to describe how it will be referred in natural language. 
It is described under the canonical annotation with the following syntax:

```
#_[canonical = { 
    $type_1: [$value_1_1, $value_1_2, ... ], 
    $type_2: [$value_2_1, $value_2_2, ... ], 
    ...
}]
``` 

Values are simply a string where we use `#` to indicate where the actual value should be placed.
And types indicate how the values will be used in a sentence.

In total, we identified 7 different types of NL annotations, 
and we split them into 4 different categories based on the NL grammar.
Note that since we have one type with name "property", we use "parameter" to refer to the properties of a subject/table.  

## Noun phrase 
**Base form** (`base`)

The base form of a parameter is a noun phrase used for describing the parameter without context. In particular, it is supposed to be used without a value round it. This includes projection questions. A projection question asks about one parameter of the subject, such as "what is the address of a restaurant?". The base form is also used for questions related to the count of a parameter. For example, we can ask "how many college degrees does Bob have?", "show me a person with 3 awards."

```js
out alumniOf: Entity(org.schema:Organization)
#_[canonical = {
    base = ["college degree"]
}],

// projection
"what college degree does Bob have?"
// count
"how many college degrees does Bob have?" 
"show me a person with 3 or more college degrees."
```

**Property** (`property`)

This describes what the subject has, i.e., a property that the subject owns. If `property` annotation is missing, we will use `base form` instead.

```js
out alumniOf: Entity(org.schema:Organization)
#_[canonical = {
    property = ["college degree from #", "# degree"]
}],

"Show me persons with college degree from Stanford."
"Show me persons with a Stanford degree"
```


**Reverse property** (`reverse_property`)

This describes what the subject is, i.e., the identity of the subject. It can also be considered as a reversed property where the subject is a *property* of the value. For example, `worksFor` has reverse property annotation "employee" - Bob works for Stanford, and Stanford has "employee" Bob.

```js
out alumniOf: Entity(org.schema:Organization)
#_[canonical = {
    reverse_property = ["# grads", "# alumni"]
}]

"show me Stanford grads."
"who are Stanford Alumni?"
```

## Verb phrase
**Active** (`verb`)

This describes the property in the form of an active verb phrase

```js
out alumniOf: Entity(org.schema:Organization)
#_[canonical = {
    verb = ["went to #", "graduated from #"]
}]

"Who went to Stanford University?"
"Show me a person that graduated from Stanford."
```

**Passive** (`passive_verb`)

This describes the property in the form of a passive verb phrase.


```js
out worksFor: Entity(org.schema:Organization)
#_[canonical = {
    passive_verb = ["employed by #"]
}]

"Who is employed by Stanford University?"
"Show me a person employed from Stanford."
```


## Adjective 
**Adjective** (`adjective`)

The adjective form of a parameter is used in front of the subject as an adjective. In the paper, this is only a boolean flag. Now we extend it to also take values. 

```js
out rating: Number
#_[canonical = {
    adjective = ["#-star"]
}]
out servesCuisien: String
#_[canonical = {
    adjective = ["#"]
}]

"Show me a 5-star restaurant"
"Show me a Chinese restaurant"
```

## Implicit identity 
**Identity** (`implicit_identity`)

This is a boolean flag which is set to true when the value of the parameter alone is unambiguous enough to be used as an identity of the subject.  

```js
out category: String
#_[canonical = {
    implicit_identity = true
}]

"Search for a smartphone" // use the value directly without mentioning the subject "Product" or the property "category"
```