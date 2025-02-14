#!/usr/bin/env python3
# For python 3 interpretation / Shebang line for (Unix/Linux)

# Taghi Mammadov

import signal # This package allows registering signal handlers for UNIX signals
import os # For the process management
import time # This package is used for delays that will be inside the code
from queue import Queue # For communication
from threading import Thread, Event # For running operations subsequently

# Global variables
sigusr1_queue = Queue() # SIGUSR1 signals handling
run = True # This is flag to control the main loop's execution time and the process
processing_event = Event() # for managing the evenets that are coming to the main loop

def process_sigusr1_queue(): # Processes queued SIGUSR1 signals one by one
    global run
    while True: # This is needed to ensure that the interation goes infinetely
        sigusr1_queue.get() # Get a SIGUSR1 signal from the queue
        processing_event.clear()  # Ensure main loop is paused
        print("Event processing started for signal 10 (SIGUSR1)")
        for i in range(1, 6): # For simulation from 1 to 5
            print(f"Processing signal 10: {i}/5")
            time.sleep(1) # Delay that allows to have signals step by step
        print("Event processing completed for signal 10 (SIGUSR1)")
        sigusr1_queue.task_done() # if the signal is executed make it done
        if sigusr1_queue.empty() and run: # Check if there are other sequences in the queue
            processing_event.set()
        if not run and sigusr1_queue.empty():
            break  # Exit thread if no longer sihnals left running and queue is empty

def handle_sigusr1(signum, frame): # processes incoming SIGUSR1 signals and pauses the main loop if needed.
    sigusr1_queue.put(signum) # Add the signal to the queue
    if processing_event.is_set():
        processing_event.clear()  # Pauses the main loop if it's running

def custom_sigterm_handler(signum, frame): # Programm stops running and prints a termination message.
    global run
    run = False # Signal the main loop to stop because we had infine as True and now it set to False
    processing_event.set()  # Ensure the main loop can exit
    print("Received SIGTERM, saving data before exit")

def custom_sigint_handler(signum, frame): # For the SIGINT
    print("Received SIGINT, canceling process")
    os._exit(1)

# Signal handlers
signal.signal(signal.SIGUSR1, handle_sigusr1)
signal.signal(signal.SIGTERM, custom_sigterm_handler)
signal.signal(signal.SIGINT, custom_sigint_handler)

# For SIGUSR1 signals
Thread(target=process_sigusr1_queue, daemon=True).start()

print(f"Process with PID={os.getpid()} started")
processing_event.set()  # Allows the main loop to run

try:
    iteration = 1 # Inetarion counter for the main loop
    while run: # It will be running until the run is set to False
        processing_event.wait()  # If there are any SIGUSR1 signals it starts to wait
        print(f"Process: iteration {iteration}")
        iteration += 1
        time.sleep(1) # There has to be a wait for the next iteration of 1 second
finally:
    print(f"Process with PID={os.getpid()} finished") # Finish message when the process is ended
