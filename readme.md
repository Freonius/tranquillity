# Tranquillity

![Workflow](https://github.com/Freonius/tranquillity/actions/workflows/gh-action-python.yml/badge.svg)
[![codecov](https://codecov.io/gh/Freonius/tranquillity/branch/master/graph/badge.svg?token=F6HK01BK76)](https://codecov.io/gh/Freonius/tranquillity)
![Lines of code](https://tokei.rs/b1/github/Freonius/tranquillity)

Tranquillity is a set of utilities that I got tired of copying and pasting everywhere,
and that helps me doing the things that need to be done, without worrying too much
about connections, logging, requests, or endpoints.

It is a work in progress, so, if you use it, keep that in mind. (As soon as I am done working on it, I'll remove this line)

**Seriously**, don't use it now, it doesn't even work (except for a couple of modules).

If you want to help me out, or make any changes, write me at freonius@gmail.com.

I think it's nice, but I am biased, but if nobody else uses it, I will.

Anyway, enough about this -- I haven't talked about me, so I could not say "enough about me" --, here's the documentation
so far.

## Python

The Python section is divided into modules. Some modules build on top of others, but some are self sustained.

Here are the modules.

### Exceptions

The exception part is pretty easy to understand. Some are really simple exceptions, others are Http Exceptions, that have a reason and a status code. So, if you didn't find a resource, you could raise a ResourceNotFound, and you would automatically get a 404 status code.

### Enums

TODO

### Shell

TODO

### Utils

TODO
