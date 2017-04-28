# forterChallenge
hello :)

This is my solution to both of the challenges given.

In the first challenge (the lz-string challenge), I've started by searching how to run IE6 on my windows 10 computer.
I found out that I can run my IE11 with emulator settings so its like IE6. Meanwhile, I searched for more information
about the lz-string library. I got into their git-hub repository, and found out that they uploaded a library called lz-string.min,
and it's description is: "small fix for IE <= 7" :)
So before I had the chance to explore the problem myself, I found the solution - the code was accessing characters from a string like an
array, (using []) - an option that isn't available in older versions of js. The solution was to change it into .charAt().

For the bonus challenge I noticed that the call 
```
LZString._compress(input);
```
passes only one argument to _compress, which takes 3 arguments.
Then i studied the _compress function and saw that in order to exit the while(true) loop these arguments must be defined.
In orderd to prevent any false calls like this one from freezing the browser, I added the following code in the beggining 
of the compress function:
```
if(bitsPerChar == null || getCharFromInt == null){
		var args = 1;
		args += (bitsPerChar != null) + (getCharFromInt != null);
		html_log("_compress expects 3 arguments, only " + args + " were given, stoping compression");
		return "";
	}
```

I started the second challenge by searching for an online nickname database.
I found one, and it containing thousands of different names.
Im using a Fuzzy Logic based library -  fuzzywuzzy  to determent if a name has a typo in it.
The fuzzzywuzzy function I use is fuzz.ration(str1, str2) - it returns a number between 0-100 that represents the similarity of the strings.
after many testing, I've decided to accept strings with a similarity level of over 67 - 67 allows typo's in strings the length of 3,
but doesn't allow to many typo's in other strings.
For the middle names, I decided that if both people specify their middle name and they both have different middle names - they are not the same person.
I used fuzz.partial_ratio(str1, str2) function for middle names. it's like the ratio() function, but if one string is a substring of the other string
it accepts it. For example, fuzz.ratio("brown", "brown charlie") = 56; fuzz.partial_ratio("brown", "brown charlie") = 100
I chose to accept values over 75 - to catch typo's.

A link to the lz-string git-hub repository i got the solution from:
https://github.com/pieroxy/lz-string/tree/master/libs

A link to the fuzzywuzzy git-hub repository:
https://github.com/seatgeek/fuzzywuzzy



