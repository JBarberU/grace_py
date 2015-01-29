#!/usr/bin/env python

import os
import re
import sys
import subprocess
import threading

class Track:

  def __init__(self, dirname, filename):
    self.dirname = dirname
    self.filename = filename

class AudioPlayer:

  def __init__(self, exit_listener):
    self.process = None
    self.exit_listener = exit_listener
    self.terminate = False

    if sys.platform == "linux" or sys.platform == "linux2":
      raise RuntimeError("AudioPlayer hasn't been implemented on linux yet")
      self.player_cmd = ""
      self.audio_extensions = []
    elif sys.platform == "darwin":
      self.player_cmd = "afplay"
      self.audio_extensions = [re.compile(".*\.mp3"), re.compile(".*\.wav")]

  def play(self, track):
    self.stop()

    def create_subprocess(self, exit_listener):
      self.process = subprocess.Popen([self.player_cmd, "{}/{}".format(track.dirname, track.filename)])
      self.process.wait()
      self.process = None
      if not self.terminate:
        exit_listener.on_exit()

    self.thread = threading.Thread(target=create_subprocess, args=(self, self.exit_listener))
    self.thread.start()

  def stop(self):
    if self.process:
      self.terminate = True
      self.process.terminate()
      self.process = None

class Player():

  def __init__(self, working_directory):
    self.audio_player = AudioPlayer(self)
    self.working_directory = working_directory
    self.tracks = []
    self.__add_dir(working_directory)
    self.current_track = None

  def play(self):
    if not self.tracks:
      print("There are no tracks to play")
      return

    if self.current_track == None:
      self.current_track = 0

    track = self.tracks[self.current_track]
    print("Playing: {}".format(track.filename))
    self.audio_player.play(track)

  def pause(self):
    pass

  def stop(self):
    self.audio_player.stop()

  def next(self):
    if not self.tracks:
      return

    self.stop()

    if self.current_track == len(self.tracks) -1:
      self.current_track = 0
    else:
      self.current_track = self.current_track + 1

    self.play()

  def prev(self):
    if not self.tracks:
      return

    self.stop()

    if self.current_track == 0:
      self.current_track = len(self.tracks) -1
    else:
      self.current_track = self.current_track - 1

    self.play()

  def on_exit(self):
    self.next()

  def list(self):
    for t in self.tracks:
      print("{}".format(t.filename))

  def __add_dir(self, dirname):
    for dirname, dirnames, filenames in os.walk(self.working_directory):
      for f in filenames:
        for ext in self.audio_player.audio_extensions:
          if ext.match(f):
            self.tracks.append(Track(dirname, f))
            break

def main():
  if len(sys.argv) > 1:
    path = sys.argv[1]
  else:
    path = "."
  p = Player(path)
  p.play()
  running = True
  while running:
    cmd = raw_input()
    if cmd == "stop":
      p.stop()
    elif cmd == "play":
      p.play()
    elif cmd == "next":
      p.next()
    elif cmd == "prev":
      p.prev()
    elif cmd == "list":
      p.list()
    elif cmd == "quit":
      p.stop()
      running = False
    else:
      print("Available commands: stop|play|next|prev|list|quit")

if __name__ == "__main__": main()

