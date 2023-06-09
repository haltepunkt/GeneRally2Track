from dataclasses import dataclass
from enum import IntEnum
from struct import *
import argparse, json, os

class TrackType(IntEnum):
  OTHER = 0,
  CIRCUIT = 1,
  STREETCIRCUIT = 2,
  ROADCOURSE = 3,
  OVAL = 4,
  STUNT = 5,
  OFFROAD = 6

  def __str__(self):
    if self == self.STREETCIRCUIT:
      return 'Street Circuit'
    elif self == self.ROADCOURSE:
      return 'Road Course'
    elif self == self.OFFROAD:
      return 'Off-Road'
    else:
      return self.name.capitalize()

@dataclass
class Track:
  name: str
  author: str
  comments: str
  water_level: int
  view_angle: int
  rotation: int
  zoom: int
  world_size: int
  real_world: bool
  type: TrackType

argument_parser = argparse.ArgumentParser(description='Print details of GeneRally 2 tracks')

argument_parser.add_argument('track')
argument_parser.add_argument('--json', action='store_true', default=False)

arguments = argument_parser.parse_args()

with open(arguments.track, 'rb') as track_file:
  buffer = track_file.read()

  signature_format = '6s'
  signature_size = calcsize(signature_format)

  signature = unpack(signature_format, buffer[0:signature_size])[0].decode('utf-8')

  if signature == 'GR2TRK':
    properties_offset = 0x5F
    properties_format = 'BBHBB'
    properties_size = calcsize(properties_format)

    water_level, view_angle, rotation, zoom, world_size = unpack(properties_format, buffer[properties_offset:properties_offset + properties_size])

    strings_offset = 0x65

    name_offset = strings_offset
    name_length_format = 'B'
    name_length = unpack(name_length_format, buffer[name_offset:name_offset + calcsize(name_length_format)])[0]
    name_format = f'{name_length}s'

    name = unpack(name_format, buffer[name_offset + calcsize(name_length_format):name_offset + calcsize(name_length_format) + name_length])[0].decode('utf-8')

    author_offset = name_offset + calcsize(name_length_format) + name_length
    author_length_format = 'B'
    author_length = unpack(author_length_format, buffer[author_offset:author_offset + calcsize(author_length_format)])[0]
    author_format = f'{author_length}s'

    author = unpack(author_format, buffer[author_offset + calcsize(author_length_format):author_offset + calcsize(author_length_format) + author_length])[0].decode('utf-8')

    comments_offset = author_offset + calcsize(author_length_format) + author_length
    comments_length_format = 'B'
    comments_length = unpack(comments_length_format, buffer[comments_offset:comments_offset + calcsize(comments_length_format)])[0]
    comments_format = f'{comments_length}s'

    comments = unpack(comments_format, buffer[comments_offset + calcsize(comments_length_format):comments_offset + calcsize(comments_length_format) + comments_length])[0].decode('utf-8')

    real_world_offset = comments_offset + calcsize(comments_length_format) + comments_length
    real_world_format = '?'
    real_world_size = calcsize(real_world_format)
    real_world = unpack(real_world_format, buffer[real_world_offset:real_world_offset + real_world_size])[0]

    track_type_offset = real_world_offset + real_world_size
    track_type_format = 'B'
    track_type_size = calcsize(track_type_format)
    track_type = TrackType(unpack(track_type_format, buffer[track_type_offset: track_type_offset + track_type_size])[0])

    track = Track(
      name, author, comments,
      water_level, view_angle, rotation, zoom, world_size,
      real_world, track_type
    )

    if arguments.json:
      print(json.dumps(track.__dict__))
    else:
      print(f'File name:\t{os.path.basename(arguments.track)}')
      print(f'File signature:\t{signature}')
      print('')
      print(f'Name:\t\t{track.name}')
      print(f'Author:\t\t{track.author}')
      print(f'Comments:\t{track.comments}')
      print('')
      print(f'Water level:\t{track.water_level}')
      print(f'View angle:\t{track.view_angle}')
      print(f'Rotation:\t{track.rotation}')
      print(f'Zoom:\t\t{track.zoom}')
      print(f'World size:\t{track.world_size}')
      print(f'Real world:\t{track.real_world}')
      print(f'Type:\t\t{track.type}')
