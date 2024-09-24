"python har_device.py" in the terminal to start program

\n\nSetup:
\nInput your session User - Your name
\nInput your session ID - Number of times you have performed a movement actvity (to differentiate between entries easily if there is an issue)
\nInput the performed movement type - The movement type you are going to perform; running, walking, situps or rest

\n\nDuring device validation:
\nSkip - Input "y" to skip or "n" to start validation
\nLED TEST - LED Should start blinking
\nSENSOR TEST - The current time as well as x, y and z values from the sesnor should printed
\nNOTE - If any of the following are not functioning as stated above then the device is NOT working

\n\nOnce in use:
\nPress button to start the session, after which movement data will begin being recorded
\nPress button again to end session

\n\nSession Instructions:
\nThe following items below MUST be recorded for time you use the device
\nThe session ID - Number of times you have performed any movement activity
\nThe movement performed for that session - This is a backup incase the MongoDB has the incorrect movement type
\nTime of each session - Each activty should add up to 10 minutes in total (More may be need, this will be discussed depending on how the next 2 weeks go)

\n\nErrors:
\nOnce a session starts the LED should be always be ON unless the session has ended (button has been pressed again)
\nOFF LED - There is something wrong with the device or the sesnor
\nBLINKING LED - The device has lost connection to the MongoDB (check internet connection or there is an error with the database itself)

\n\nCRTL+C to kill the program after use (should exit without an error)
