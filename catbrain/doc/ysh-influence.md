Catbrain influences YSH?
----------

Ideas

- I kind of like the explicit stack rather than "registers"?
  - for status
  - for pipeline status
  - for eggex match

- I wonder about this syntax:
  - filter [age > 1]

- instead, it could be
  - filter ^[age > 1]
  - synonym for filter (^[age > 1])

---

In catbrain, we have % and ^

- % is OK I guess
- Does ^ mean two things?  It means "pop", and it means Unevaluated
  - maybe it could be * or !

```
ls !
ls !!  # splice it

```

That char also has the "history" connotation

But it's the last VALUE, not the last command

Pipeline status
-----------

ls | grep | wc -l

[status: [0 1 0]]

[%error [pipeline [0 1 0]]]



