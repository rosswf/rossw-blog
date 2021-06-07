Title: PyCon US 2021 - My Thoughts
Date: 2021-05-16 14:48
Tags: python, pycon, conference
Summary: My thoughts on PyCon US 2021 as somebody that has never attended a conference before either in person or virtual.
Slug: pycon-us-2021
Description: My thoughts on PyCon US 2021 as somebody that has never attended a conference before either in person or virtual.

PyCon US 2021 was online this year due to the current global situation so I thought I'd take advantage of this opportunity to virtually attend as it's unlikely I'll be able to attend future US conferences in person.

I've never attended a conference before either in person or online so I want to give my thoughts on conferences as a newbie.

All of the talks I was able to watch live were fantastic but some definitely stood out to me so I'm going to give my thoughts on these. There were multiple tracks so unfortunately I didn't get to watch all the talks I wanted to see live as there were some scheduling clashes, sometimes 3 at a time! This should give you an idea of how interesting the talks were.


### Overview

Obviously with this being online I wasn't able to get the full conference experience but it was a great opportunity to dip my toe in the water and see if it was something that I would like to experience in person in the future. 

I primarily just watched the talks however the online platform they used was great, after each talk there was an opportunity to join a virtual room with the person that gave the talk for a live Q&A session and there was a live chat during the talk to ask questions and engage with other members of the community.

There were also lounges for networking and sponsor booths where you could drop in to ask questions through out the entirety of the event.

The online experience has definitely wet my appetite for attending something like this in person in future to get the full in person experience - I'm looking at you [PyCon UK](https://twitter.com/pyconuk?lang=en)!

### Highlights

As I mentioned earlier all of the talks were great but these are some of the ones that stood out to me in particular. 

---

**[Day 1 Keynote - Robert Erdmann](https://www.youtube.com/watch?v=z_hm5oX7ZlE)**

Robert Erdmann has been using python to create an extremely high resolution image of Rembrandt's Night Watch painting. The final image will be 925,000px x 775,000px, that translates to each pixel representing 5 µm of the painting.

This image has not been released to the public yet but there is a [20 µm version](http://hyper-resolution.org/Nightwatch) available which in itself is incredible so I cannot wait to see the new higher resolution version!

The number of moving parts involved in producing these images was mind blowing. Here are just a few:

- Due to the operating range of the camera to retrieve a sharp image was so small that he first had to produce a 3D scan of the painting to take into account it's topology. This allowed them to adjust the position and angle of the camera to get a sharp image.
- The use of machine learning to assess the quality of each image.
- ML to stitch the final image together, skewing each individual photograph as required and decided which image to use where pixel values were contested due to overlaps.

The talk needs to be seen purely to see how python as a programming language can be utilised for so many different aspects of a project from controlling the position of the camera to performing analysis on each image.

---

**[From 3 to 300 fps: NES Emulation in Python and Cython - James Murphy](https://www.youtube.com/watch?v=3of9pY2vovA)**

I didn't expect to enjoy this talk quite as much as I did but it was a great insight into just how flexible python is (I'd never expected it to be able to be used for an emulator) and how it can be optimised using the likes of Cython to see huge performance gains.

The finished emulator using CPython at first only ran at 2-3 fps but after a few days of optimisation utilising Cython it was running at over 300 fps. These performance gains are astonishing, it shows just how versatile python can be and that "python is slow" might not always be true with a little extra work.

---

**[Intro to Pydantic, run-time type checking for your dataclasses - Alexander Hultnér](https://www.youtube.com/watch?v=W7f52FhfYqQ)**

I'd heard of pydantic but it's not something I've got round to exploring yet. Alexander's talk was a fantastic introduction and really engaging. He used a very basic example of a Waffle House to clearly portray the benefits and uses of pydantic.

JSON is a first class citizen in pydantic and Alexander demonstrated how it can be utilised for creating APIs. It's definitely a tool that I'm going to utilise in the near future, most likely with Fast API which I will come onto next!

If like me you have heard of pydantic and aren't sure what it's about, why you might need it and how it can be used I'd definitely recommend checking out this talk. Alexander does a great job of explaining it in a beginner friendly manner which makes it feel much less daunting for getting started with.

---

**[An Introduction to FastAPI - Thomas Jewitt](https://www.youtube.com/watch?v=_jh4Wc3CE38)**

FastAPI is something that I've been aware of for a while and the general consensus was that is is the next big thing but I wasn't entirely sure *why* it was so amazing. Thomas did a great job of explaining the features & benefits of FastAPI and how quick it is to get up and running.

Some of the stand out features to me were:

- It's use of pydantic for validation.
- Automatic generation of documentation based on the OpenAPI specification.
- It's pythonic as it utilises pythons type hinting.

This talk has definitely given me the push to bump FastAPI further up my ever growing list of things to learn and try. 

I don't think this will completely replace Flask in the web framework world as they seem to fill different niches. 
If you are going to use a front-end framework such as React or Vue it definitely makes sense to go with FastAPI but if you just want to build a web app with python, HTML, CSS and JS then I'd say Flask still has it's place. This opinion might change once I start using FastAPI but only time will tell. Let me know what your thoughts are.

---

### Final Thoughts

I thoroughly enjoyed PyCon US 2021 even if I didn't take advantage of everything that was available. There was a large variety of talks and some that I didn't get to watch live due to scheduling clashes but I definitely intend to watch these at a later date.

It's made me excited for next year and being able to attend conferences in person when things return to normal.

Did you attend PyCon US 2021? If so, let me know which your favourite talks were and why! Contact details be found [here]({filename}/pages/about.md).