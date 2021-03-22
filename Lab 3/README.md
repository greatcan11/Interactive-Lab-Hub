# You're a wizard, Grace

<img src="https://pbs.twimg.com/media/Cen7qkHWIAAdKsB.jpg" height="400">

In this lab, we want you to practice wizarding an interactive device as discussed in class. We will focus on audio as the main modality for interaction but there is no reason these general techniques can't extend to video, haptics or other interactive mechanisms. In fact, you are welcome to add those to your project if they enhance your design.


## Text to Speech and Speech to Text

In the home directory of your Pi there is a folder called `text2speech` containing some shell scripts.

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav

```

you can run these examples by typing 
`./espeakdeom.sh`. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts

```

You can also play audio files directly with `aplay filename`.

After looking through this folder do the same for the `speech2text` folder. In particular, look at `test_words.py` and make sure you understand how the vocab is defined. Then try `./vosk_demo_mic.sh`

## Serving Pages

In Lab 1 we served a webpage with flask. In this lab you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/$ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to [http://ixe00.local:5000]()


## Demo

In the [demo directory](./demo), you will find an example wizard of oz project you may use as a template. **You do not have to** feel free to get creative. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser. You can control what system says from the controller as well.

## Optional

There is an included [dspeech](.dspeech) demo that uses [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech) for speech to text. If you're interested in trying it out we suggest you create a seperarate virutalenv. 



# Lab 3 Part 2

Create a system that runs on the Raspberry Pi that takes in one or more sensors and requires participants to speak to it. Document how the system works and include videos of both the system and the controller.

## Prep for Part 2

1. Sketch ideas for what you'll work on in lab on Wednesday.

## Share your idea sketches with Zoom Room mates and get feedback

*what was the feedback? Who did it come from?*

## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works*

*Include videos or screencaptures of both the system and the controller.*

### System Overview

>Our system is inspired by our own lives, as when we try to do work, we often find ourselves procrastinating.  What if there was a system that would remind us to not procrastinate so that we could work when we are supposed to?
>
>We have come up with “Bill,” an accountable friend who helps the user not procrastinate.  >Whenever the user is not doing work, Bill will remind the user to do it.  This system will have a Picamera so that the Wizard can see whether the user is doing work or not via a livestream and talk to prompt the user to do work.  Below is the storyboard, which we will explain each picture in detail below.
>
> ![](storyboard.png)
>
>The first picture shows how Bill will initialize.  Dspeech will always be running to listen to the user.  When the user says “Bill,” the Picamera will turn on and the camera live stream will start.  This is similar to when people are used to interacting with their Google Home and say “Hey Google” or their AmazonAlexa and say “Alexa.”  We chose “Bill” for the name instead of a device name such as “Anti-Procrastinator” because users will feel more comfortable talking to a person as they are doing their work (or procrastinating).  Additionally, after the user says “I will start work,” espeak will turn on so the Wizard can start to tell the user to go back to work if the user procrastinates.
>
>The second picture shows the user procrastinating by seeing a meme on facebook and as Bill sees and hears this, Bill will say, “STOP.”
>
> The third picture shows how the user is reminded of going back to work, and so his laptop screen goes back to all the documents that need to be worked on.

### Implementing Bill

>Overall, we tried to integrate incrementally in order to create this wizard.  All our code is in WizardingDemo.py.  
>
>We decided to integrate the Pi camera with our system so that we can have a livestream of the user.  We first tried using [web streaming](https://picamera.readthedocs.io/en/release-1.13/recipes2.html#web-streaming) to start a livestream.  However, after we rebooted the Pi and played around with dspeech, the web streaming module was not working for some reason.  After some research, we decided to try [pistreaming](https://github.com/waveform80/pistreaming/) and it worked.  Additionally, it worked even better than web streaming since it has lower latency. Here is a picture of how we tested the live stream:
> ![](testing_livestream_caitlin.png)
>
>After trying to integrate the code related to the server and dspeech, we were getting an error at this line:
>
```
>#self.send_header('Last-Modified', self.date_time_string(time()))
```
>
>However, when we commented the following line of code, it worked and we were able to start the livestream after “Bill” is recognized.
>
>After trying to integrate espeak, we were getting errors.  We needed to figure out how to use websocket in JavaScript and connect the button to the websocket, and have the python file call the espeak command. Below is some brainstorming with diagrams we drew out to make sure we understood the problem:
>
>![](debug_espeek.jpeg)
>
>After realizing that there was some other program running on that particular port, we were able to kill that program, and we were able to integrate espeek.  Afterwards, we encountered the following error:
>
```
>WARNING:root:Removed streaming client ('192.168.1.6', 49544): name 'output' is not defined
```
>
>This is because the output had to be global, as described in this [link](https://raspberrypi.stackexchange.com/questions/99756/cannot-turn-web-streaming-into-a-function).




## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?
*your answer here*

### What worked well about the controller and what didn't?

*your answer here*

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

*your answer here*


### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

*your answer here*

