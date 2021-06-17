mode: sleep
-

^talon wake$: 
    speech.enable()
    user.mouse_wake()
    app.notify("Awake")

#this exists solely to prevent talon from waking up super easily in sleep mode at the moment with wav2letter
<phrase>: skip()