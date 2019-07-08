=======
Pygists
=======

Just a tool to manage GitHub gists

---

Usage
-----

To get all your gists with embed links:

::

  $ pygists -u your_username -t path/to/token.txt --get

  tomasfarias's GitHub Gist: 6d83bf247790b4116f0575ee230cc4d0
  'Just a second test'
  Created: 2019-06-27 05:22:08
  Updated: 2019-07-08 19:57:12
  Embed: https://gist.github.com/tomasfarias/6d83bf247790b4116f0575ee230cc4d0.js
  File | Size (chars)
  test_2.py | 15


  tomasfarias's GitHub Gist: 2be660066572b42a898c87f48b756b89
  'Just a test'
  Created: 2019-06-27 05:20:24
  Updated: 2019-07-08 19:56:51
  Embed: https://gist.github.com/tomasfarias/2be660066572b42a898c87f48b756b89.js
  File | Size (chars)
  test_1.py | 15


To create a new gist from a file:

::

  $ pygists -n test_3.py -u tomasfarias -t auth/token.txt -d 'Just another test'

  tomasfarias's GitHub Gist: c4eb4855f02e77d162a78520da50a0b9
  'Just another test'
  Created: 2019-07-08 20:03:56
  Updated: 2019-07-08 20:03:56
  Embed: https://gist.github.com/tomasfarias/c4eb4855f02e77d162a78520da50a0b9.js
  File | Size (chars)
  test_3.py | 16


To edit an existing gist get the ID and pass it. Only defined arguments will be edited, previous values will be kept for the rest:

::

  $ pygists -i c4eb4855f02e77d162a78520da50a0b9 -u tomasfarias -t auth/token.txt -d "New description" -n test_new_3.py

  tomasfarias's GitHub Gist: c4eb4855f02e77d162a78520da50a0b9
  'New description'
  Created: 2019-07-08 20:03:56
  Updated: 2019-07-08 21:26:47
  Embed: https://gist.github.com/tomasfarias/c4eb4855f02e77d162a78520da50a0b9.js
  File | Size (chars)
  test_new_3.py | 16
