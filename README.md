This code was designed to take the bible as a text file and make it compatable with a sql-lite database so that each verse would be a record.
There was an attempt to use NLTK features on each verse of the bible so that a users prompt could generate bible verses that did not directly match the text of the user.
glove-wiki-gigaword-100.gz  was dropped from the program but may need to be pip installed in order to use some of the functions.

Bible.txt is modified version of the King James Bible by [Gutenberg](https://gutenberg.org/)  ##### has been added to separate each chapter so that the DB loader can identify chapter breaks when creating table entries for bible verses.
