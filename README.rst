Pygists
=======

Just a tool to manage GitHub gists

Usage
-----

To list all your gists with embed links use :code:`ls`:

::

  $ pygists ls -u your_username -t $GITHUB_TOKEN

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


To :code:`create` a new gist from a file call:

::

  $ pygists create path/to/gist/file.py -u tomasfarias -t $GITHUB_TOKEN -d 'Just another test'

  tomasfarias's GitHub Gist: c4eb4855f02e77d162a78520da50a0b9
  'Just another test'
  Created: 2019-07-08 20:03:56
  Updated: 2019-07-08 20:03:56
  Embed: https://gist.github.com/tomasfarias/c4eb4855f02e77d162a78520da50a0b9.js
  File | Size (chars)
  test_3.py | 16


To :code:`update` an existing gist get the ID and pass it. Use :code:`add`, :code:`delete`, :code:`modify` to add new files to the gist, delete an existing file and modifiy the contents and name of an existing file:

::

  $ pygists update c4eb4855f02e77d162a78520da50a0b9 -u tomasfarias -t $GITHUB_TOKEN -d "New description" --add test_new_3.py --modify old_file_name.py=path/to/new_file.py

  tomasfarias's GitHub Gist: c4eb4855f02e77d162a78520da50a0b9
  'New description'
  Created: 2019-07-08 20:03:56
  Updated: 2019-07-08 21:26:47
  Embed: https://gist.github.com/tomasfarias/c4eb4855f02e77d162a78520da50a0b9.js
  File | Size (chars)
  test_new_3.py | 16
  new_file.py | 25
