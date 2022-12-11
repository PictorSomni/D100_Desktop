# D100_Desktop
An interface to manage my own Table RPGs - Using PySide6

For the record, i made this years ago and just adapted it to work using PySide6.4.
There are places to generate NPCs (for the story or ennemies to battle) with unique names, vocation and stats
(The stats of the NPCs are identical but useful for battle since you can roll a dice and having their health change accordingly).
You can select any player or NPC in the dropdown then perform some dice rolls.
The damages section is separated so you can first see if a character succeed an attack
and then choose the correct opponent (or choose it randomly using the global dice roll at the top) to calculate the damages taken.

You even have a timer that you can set precisely or randomly and a popup will appears at the end of it (useful for random events).
There's even a soundbox !
Either you put individual files in the audio folder and they will appears in blue
or you can put folders containing variant of the same sound and they will be played randomly when you click on the orange button !

The UI was made to use one half of the screen and having your text application with you scenario on the other half.
There is a CONSTANT.py where you can set some options.
The player table is generated from a .CSV file so it's easily customizable. ;)

Everything is in french but you should be able to change it in the code.
Refer to the CSV file to change the players'table headers.

I'm planning to make a modified version of this for iOS.
![Screenshot01](https://user-images.githubusercontent.com/16622605/206892479-e9264dd7-7d83-4397-b941-655b7347180e.jpg)
![Screenshot02](https://user-images.githubusercontent.com/16622605/206892482-1a5a6ba5-1eb4-4e30-86a1-4d6e42f04406.jpg)
![Screenshot03](https://user-images.githubusercontent.com/16622605/206892486-58cf2876-b3f4-4016-81eb-aa002360cc05.jpg)
![Screenshot04](https://user-images.githubusercontent.com/16622605/206892695-27534f4c-acf6-40d3-b17d-53e94f22d3ae.jpg)
