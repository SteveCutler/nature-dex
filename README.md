#####

Nature-DEX

Offline CNN model to run locally on iphone for nature classification.

All images pulled from iNaturalist REST api

###

1st training attempt:

###

I used mobilenetv3 for pretraining, about 70 training images, 15 val and 15 test for each of the 219 plant species. Image resolution was about 160x160 and I ran it for 25 epochs with an extra 10 for fine tuning.

moderate to bad results, about 35% val accuracy by the end.

Going to switch to an efficientnet model, higher resolution images at 360 x 360 and about an extra 150 training images per each plant class for the next round.
