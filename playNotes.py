'''
Demonstrates playing notes on different midi instruments in the computer using pygame
Instructions on installing pygame  https://www.pygame.org/wiki/GettingStarted

V1 09.22.21
Tom Zimmerman, IBM Research-Almaden, Center for Cellular Construction
This material is based upon work supported by the NSF under Grant No. DBI-1548297.  
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation
'''

#!/usr/bin/env python

import pygame.midi
import time

pygame.midi.init()

print (pygame.midi.get_default_output_id())
print (pygame.midi.get_device_info(0))

player = pygame.midi.Output(0)


print ('Playing...')
vel=64
startNote=40
endNote=100
for note in range (startNote,endNote):
    inst=note-startNote         # make instrument start with 0
    player.set_instrument(inst) # determines the instrument (timbre)
    player.note_on(note,vel)    # start note
    print('note',note,'instrument',inst)
    time.sleep(0.5)             # duration of note (seconds)
    player.note_off(note,vel)   # stop note

print ('Done')

pygame.midi.quit()
