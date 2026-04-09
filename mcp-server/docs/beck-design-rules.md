Beck Design Rules

* [Refactoring](https://refactoring.com)
* [Agile](/agile.html)
* [Architecture](/architecture)
* [About](/aboutMe.html)
* [Thoughtworks](https://www.thoughtworks.com/engineering)

## Topics

[Architecture](/architecture)

[Refactoring](https://refactoring.com)

[Agile](/agile.html)

[Delivery](/delivery.html)

[Microservices](/microservices)

[Data](/data)

[Testing](/testing)

[DSL](/dsl.html)

## about me

[About](/aboutMe.html)

[Books](/books)

[FAQ](/faq.html)

## content

[Videos](/videos.html)

[Content Index](/tags)

[Board Games](/boardgames)

[Photography](/photos)

## Thoughtworks

[Home](https://thoughtworks.com)

[Insights](https://thoughtworks.com/insights)

[Careers](https://thoughtworks.com/careers)

[Radar](https://thoughtworks.com/radar)

[Engineering](https://www.thoughtworks.com/engineering)

## follow

[RSS](/feed.atom)

[Mastodon](https://toot.thoughtworks.com/@mfowler)

[LinkedIn](https://www.linkedin.com/in/martin-fowler-com/)

[Bluesky](https://bsky.app/profile/martinfowler.com)

[X](https://www.twitter.com/martinfowler)

[BGG](https://boardgamegeek.com/blog/13064/martins-7th-decade)

# [Beck Design Rules](BeckDesignRules.html)

2 March 2015

[Martin Fowler](/)

[extreme programming](/tags/extreme%20programming.html)

[programming style](/tags/programming%20style.html)

[refactoring](/tags/refactoring.html)

Kent Beck came up with his four rules of simple design while he
was developing [ExtremeProgramming](/bliki/ExtremeProgramming.html) in the late 1990's. I express
them like this. 1

1:

There are many expressions of the four rules out there,
Kent stated them in lots of media, and plenty of other people
have liked them and phrased them their own way. So you'll see
plenty of descriptions of the rules, but each author has their
own twist - as do I.

If you want an authoritative formulation from the man
himself, probably your best bet is from the first edition of
[The
White Book](https://www.amazon.com/gp/product/0201616416/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0201616416&linkCode=as2&tag=martinfowlerc-20) (p 57) in the section that outlines the XP practice
of Simple Design.

* Runs all the tests
* Has no duplicated logic. Be wary of hidden duplication like
  parallel class hierarchies
* States every intention important to the programmer
* Has the fewest possible classes and methods

(Just to be confusing, there's another formulation on page
109 that omits “runs all the tests” and splits “fewest classes”
and “fewest methods” over the last two rules. I recall this was
an earlier formulation that Kent improved on while writing the
White Book.)

* Passes the tests
* Reveals intention
* No duplication
* Fewest elements

The rules are in priority order, so “passes the tests” takes
priority over “reveals intention”

Kent Beck developed Extreme Programming, Test Driven Development,
and can always be relied on for good Victorian facial hair for his
local ballet.

The most important of the rules is “passes the tests”. XP was
revolutionary in how it raised testing to a first-class activity in
software development, so it's natural that testing should play a
prominent role in these rules. The point is that whatever else you
do with the software, the primary aim is that it works as
intended and tests are there to ensure that happens.

“Reveals intention” is Kent's way of saying the code
should be easy to understand. Communication is a core value of
Extreme Programing, and many programmers like to stress that
programs are there to be read by people. Kent's form of expressing
this rule implies that the key to enabling understanding is to express your
intention in the code, so that your readers can understand what your
purpose was when writing it.

The “no duplication” is perhaps the most powerfully subtle of
these rules. It's a notion expressed elsewhere as DRY or SPOT 2, Kent
expressed it as saying everything should be said “Once and only Once.”
Many programmers have observed that the exercise of eliminating
duplication is a powerful way to drive out good designs. 3

2: 
DRY stands for Don't Repeat Yourself, and comes from [The Pragmatic Programmer](https://www.amazon.com/gp/product/020161622X/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=020161622X&linkCode=as2&tag=martinfowlerc-20). SPOT stands
for [Single
Point Of Truth](http://www.catb.org/~esr/writings/taoup/html/ch04s02.html#spot_rule).

3: 
This principle was the basis of my [first design column for IEEE Software](/ieeeSoftware/repetition.pdf).

The last rule tells us that anything that doesn't serve the three
prior rules should be removed. At the time these rules were
formulated there was a lot of design advice around adding elements to
an architecture in order to increase flexibility for future requirements.
Ironically the extra complexity of all of these elements usually
made the system harder to modify and thus less flexible in practice.

People often find there is some tension between “no duplication”
and “reveals intention”, leading to arguments about which order
those rules should appear. I've always seen their order as
unimportant, since they feed off each other in refining the code. Such things
as adding duplication to increase clarity is often papering over a problem,
when it would be better to solve it. 4

4: 
When reviewing this post, Kent said “In the rare case they are
in conflict (in tests are the only examples I can recall),
empathy wins over some strictly technical metric.” I like his
point about empathy - it reminds us that when writing code we
should always be thinking of the reader.

What I like about these rules is that they are very simple to
remember, yet following them improves code in any language or
programming paradigm that I've worked with. They are an example of
Kent's skill in finding principles that are generally applicable and
yet concrete enough to shape my actions.

> At the time there was a lot of “design is subjective”, “design is
> a matter of taste” bullshit going around. I disagreed. There are
> better and worse designs. These criteria aren’t perfect, but they
> serve to sort out some of the obvious crap and (importantly) you can
> evaluate them right now. The real criteria for quality of design,
> “minimizes cost (including the cost of delay) and maximizes benefit
> over the lifetime of the software,” can only be evaluated post hoc,
> and even then any evaluation will be subject to a large bag full of
> cognitive biases. The four rules are generally predictive.
>
> -- Kent Beck

## Further Reading

There are many expressions of these rules out there, here are a
few that I think are worth exploring:

* [J.B.
  Rainsberger's summary](http://www.jbrains.ca/permalink/the-four-elements-of-simple-design). He also has a good discussion of [the
  interplay between the rules 2&3.](http://blog.thecodewhisperer.com/2013/12/07/putting-an-age-old-battle-to-rest/)
* [Ron Jeffries](http://xprogramming.com/classics/expemergentdesign/)
* These rules, like much else of Extreme Programming, were
  originally discussed and refined [on Ward's Wiki](http://c2.com/cgi/wiki?XpSimplicityRules).

## Acknowledgements

Kent reviewed this post and sent me some very helpful feedback,
much of which I appropriated into the text.

## Notes

### 1: Authoritative Formulation

There are many expressions of the four rules out there,
Kent stated them in lots of media, and plenty of other people
have liked them and phrased them their own way. So you'll see
plenty of descriptions of the rules, but each author has their
own twist - as do I.

If you want an authoritative formulation from the man
himself, probably your best bet is from the first edition of
[The
White Book](https://www.amazon.com/gp/product/0201616416/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0201616416&linkCode=as2&tag=martinfowlerc-20) (p 57) in the section that outlines the XP practice
of Simple Design.

* Runs all the tests
* Has no duplicated logic. Be wary of hidden duplication like
  parallel class hierarchies
* States every intention important to the programmer
* Has the fewest possible classes and methods

(Just to be confusing, there's another formulation on page
109 that omits “runs all the tests” and splits “fewest classes”
and “fewest methods” over the last two rules. I recall this was
an earlier formulation that Kent improved on while writing the
White Book.)

2: 
DRY stands for Don't Repeat Yourself, and comes from [The Pragmatic Programmer](https://www.amazon.com/gp/product/020161622X/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=020161622X&linkCode=as2&tag=martinfowlerc-20). SPOT stands
for [Single
Point Of Truth](http://www.catb.org/~esr/writings/taoup/html/ch04s02.html#spot_rule).

3: 
This principle was the basis of my [first design column for IEEE Software](/ieeeSoftware/repetition.pdf).

4: 
When reviewing this post, Kent said “In the rare case they are
in conflict (in tests are the only examples I can recall),
empathy wins over some strictly technical metric.” I like his
point about empathy - it reminds us that when writing code we
should always be thinking of the reader.

## Topics

[Architecture](/architecture)

[Refactoring](https://refactoring.com)

[Agile](/agile.html)

[Delivery](/delivery.html)

[Microservices](/microservices)

[Data](/data)

[Testing](/testing)

[DSL](/dsl.html)

## about me

[About](/aboutMe.html)

[Books](/books)

[FAQ](/faq.html)

## content

[Videos](/videos.html)

[Content Index](/tags)

[Board Games](/boardgames)

[Photography](/photos)

## Thoughtworks

[Home](https://thoughtworks.com)

[Insights](https://thoughtworks.com/insights)

[Careers](https://thoughtworks.com/careers)

[Radar](https://thoughtworks.com/radar)

[Engineering](https://www.thoughtworks.com/engineering)

## follow

[RSS](/feed.atom)

[Mastodon](https://toot.thoughtworks.com/@mfowler)

[LinkedIn](https://www.linkedin.com/in/martin-fowler-com/)

[Bluesky](https://bsky.app/profile/martinfowler.com)

[X](https://www.twitter.com/martinfowler)

[BGG](https://boardgamegeek.com/blog/13064/martins-7th-decade)

© Martin Fowler | [Disclosures](/aboutMe.html#disclosures)