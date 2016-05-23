# Autovivification in python

## Autovivification

[Wikipedia](https://en.wikipedia.org/wiki/Autovivification)

The gist - "it is the automatic creation of new arrays and hashes as required every time an undefined value is dereferenced"

## Origins

Perl. 

```
$ perl cat_wallking_on_keyboard.pl

$VAR1 = {
          'Will' => [
                      undef,
                      undef,
                      undef,
                      {
                        'this' => [
                                    undef,
                                    [
                                      undef,
                                      undef,
                                      {
                                        'work' => [
                                                    undef,
                                                    {
                                                      'Why' => {
                                                                 'Abuse' => {
                                                                              'Power' => 1
                                                                            }
                                                               }
                                                    }
                                                  ]
                                      }
                                    ]
                                  ]
                      }
                    ]
        };
```

Autovivification supplied by default in Perl, but not so much in python

## Autovivification failure in python

```
$ python autovivification_fail.py

Traceback (most recent call last):
    File "autovivification_fail.py", line 5, in <module>
        print x['a']
    KeyError: 'a'
```

## Basic defaultdict of integers

```

$ python int_dict.py
defaultdict(<type 'int'>, {})
0
```

## Pass in a callable function to generate default values

```
$ python icecream_dict.py
defaultdict(<function <lambda> at 0x7fbd26bf79b0>, {})
  chocolate
```

## Basic first level dictionary

```
$ python firstlevel_dict.py
{}
firstlevel_dict - Keyerror: 'b'
```

## Basic second level dictionary

```
$ python secondlevel_dict.py
{}
secondlevel_dict - Keyerror: 'c'
```

## Basic third level dictionary - see the pattern

```
$ python thirdlevel_dict.py
{}
thirdlevel_dict - Keyerror: 'd'
```

## Use recursion to always generate default values

```
$ python nlevel_dict.py
defaultdict(<function makehash at 0x7f36d3443758>, {})
{
  "a": {
    "b": {
      "c": {
        "d": {
          "e": {
            "f": {
              "g": [
                1, 
                2, 
                3
              ]
            }
          }
        }
      }
    }
  }
}
```

## Read more at

[Stackoverflow - how does defaultdict work](http://stackoverflow.com/questions/5900578/how-does-collections-defaultdict-work)
