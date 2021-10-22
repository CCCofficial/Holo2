import time

def playChord(notes,vel,duration):
    # notes is a list of normalized notes in good midi range (30 to 100)
    # vel is volume of chord from 0 to 127, bigger is louder
    # duration is how long chord is held, in seconds, can be less than one like 0.1 for a tenth of a second between notes
    
    # start notes
    for note in notes:
        player.note_on(note,vel)    # start note

    # hold chord
    time.sleep(duration)

    # stop notes
    for note in notes:
        player.note_off(note,vel)    # stop note

def arpeggiateChord(notes,vel,timeBetweenNotes):
    # timeBetween notes in seconds, can be less than one like 0.1 for a tenth of a second between notes

    # start notes
    for note in notes:
        player.note_on(note,vel)    # start note

    # hold chord
    time.sleep(timeBetweenNotes)

    # stop notes
    for note in notes:
        player.note_off(note,vel)    # stop note


        
