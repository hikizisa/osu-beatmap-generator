# osu-auto-mapper

ReadSongs.py : get beatmap file lists from song folder

for studying, I'm really bad at making something

requirements:
 numpy, configparser

 

separate mapping for easy, normal, hard, insane+
use distance snap for easy, normal so it's easier

distinguish anti jump or stack and usual jump pattern
distance should be flexible so difficulty can be adjusted

distinguish clickable sounds from others.
then analyze intensity whether it should be expressed as objects.

including auto hitsounder also working as standalone would be good.
it'd be easier than auto mapper imo. if it just implements basic drum hitsounding.

Place objects considering the preceding objects at first.
After that adjust objects' positions considering the preceding and succeeding objects several times.

Treat stack as unique case. it may cause distance to converge to wrong value overall