Title:  MAESTRO Real - Multiple Annotator Estimated STROng labels

# MAESTRO Real

Machine Listening Group, Tampere University <https://research.tuni.fi/machinelistening/>

Authors

- Irene Martin Morato (<irene.martinmorato@tuni.fi>)
- Manu Harju (<manu.harju@tuni.fi>)
- Annamaria Mesaros (<annamaria.mesaros@tuni.fi>, <http://homepages.tuni.fi/annamaria.mesaros/>)

## 1. Dataset

MAESTRO real development contains 49 real-life audio files from 5 different acoustic scenes, each of them from 3 to 5 minutes long. 
The other 26 files are kept for evaluation purposes on the DCASE task 4 B. The distribution of files per scene is the following: 
cafe restaurant 10 files, city center 10 files, residential_area 11 files, metro station 9 files and grocery store 9 files. 
The total duration of the development dataset is 97 minutes and 4 seconds.

The audio files contain sounds from the following classes:

- announcement
- birds singing
- breakes squeaking
- car
- cash register
- children voices
- coffee machine
- cutlery/dishes
- door opens/closes
- footsteps
- furniture dragging


The real life-recordings used in this study include a subset of the TUT Sound Events 2016 and a subset of TUT Sound Events 2017.

### Annotation procedure

For annotation, each file was split into 10-second segments, with a hop of one second. Each segment was annotated using crowdsourcing, in a tagging scenario. 

For each segment, the annotators were required to select from the given list of classes the sounds active (audible).  Each 10-s segment was annotated by five persons. 

Full details on the annotation procedure and the processing of the tags can be found in: 

Irene Martin Morato, Manu Harju, and Annamaria Mesaros. Crowdsourcing strong labels for sound event detection, in IEEE Workshop on Applications of Signal Processing to Audio and Acoustics (WASPAA 2021). New Paltz, NY, Oct 2021. 

More details regarding the dataset and the soft-labels can be found in:

Irene Martin Morato, Manu Harju, Paul Ahokas and Annamaria Mesaros. Training sound event detection wiht soft labels from crowdsourced annotations, in IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP 2023). Rhodes Island, Greece, June 2023. 

### Dataset content

The dataset contains: 

- audio: the 49 real-life soundscapes, each 3 to 5 min long
- soft labels: estimated strong labels from the crowdsourced data, values between 0 and 1 indicates the uncertainty of the annotators.


### File structure

```
dataset root
│   README.md	                this file
│
└───development_audio
│    └───cafe_restaurant
│           │   cafe_restaurant_00.wav		
│           │   cafe_restaurant_04.wav
│           │   ...
│
└───development_annotation         soft-label annotations 
│    └───soft_labels_cafe_restaurant
│       │   cafe_restaurant_00.txt           format: start_time [tab] end_time [tab] label [tab] soft_label_value
│       │   cafe_restaurant_04.txt
│       │   ...	
    
```


## 2. License

License permits free academic usage. Any commercial use is strictly prohibited. For commercial use, contact dataset authors.


    Copyright (c) 2020 Tampere University and its licensors
    All rights reserved.
    Permission is hereby granted, without written agreement and without license or royalty
    fees, to use and copy the MAESTRO Real - Multi Annotator Estimated Strong Labels (“Work”) described in this document
    and composed of audio and metadata. This grant is only for experimental and non-commercial
    purposes, provided that the copyright notice in its entirety appear in all copies of this Work,
    and the original source of this Work, (MAchine Listening Group at Tampere University),
    is acknowledged in any publication that reports research using this Work.
    Any commercial use of the Work or any part thereof is strictly prohibited.
    Commercial use include, but is not limited to:
    - selling or reproducing the Work
    - selling or distributing the results or content achieved by use of the Work
    - providing services by using the Work.
    
    IN NO EVENT SHALL TAMPERE UNIVERSITY OR ITS LICENSORS BE LIABLE TO ANY PARTY
    FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE
    OF THIS WORK AND ITS DOCUMENTATION, EVEN IF TAMPERE UNIVERSITY OR ITS
    LICENSORS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    
    TAMPERE UNIVERSITY AND ALL ITS LICENSORS SPECIFICALLY DISCLAIMS ANY
    WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
    FITNESS FOR A PARTICULAR PURPOSE. THE WORK PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND
    THE TAMPERE UNIVERSITY HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT,
    UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
