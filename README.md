MusicBirds
==========
Current version: 0.1

Python script that visualizes music as birds on a telephone wire.

This script requires image assets, so make sure those are included in the same folder as the .py file.
In addition, MusicBirds creates video via stdin jpeg pipe into FFMPEG.exe, so make sure that is also in
the directory.

Currently, you are required to input your song data as a Python dict with the following format:

note_data = { FRAME_NUMBER:[NOTE 1, NOTE 2, ...], ...}

Where the FRAME_NUMBER is the frame number your note(s) occur at. The time-to-frame conversion in 
the current setup is 24 fps; programs like Audacity will display timing in music files as frames, too.

The NOTE list is a list of integers 0-11 (inclusive) which correspond to sheet music notes.
11 corresponds to E4, and increases diatonically to A5. I'll probably add a note-converter function
later on to make transcribing easier.

===

Currently the script works like this:

-Crop the next frame of the background image from the loopable .png in the folder

-Check to see if an object is created at this frame number

  -If yes, then create the corresponding object
  
  -If the object being created is a bird, refer to wire_data array to also get the vertical coordinate to draw the bird on
-Find and draw all instances of existing objects

  -Draw in this order: tree, pole, wires, birds
  
  -Call the object.nextframe() method to move each object to the left for the animation effect
  
-Repeat this loop until FRAME == TOTAL FRAMES
